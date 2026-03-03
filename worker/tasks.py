import os
import sys
import json
import time

# Ajouter le répertoire parent pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.celery_app import celery_app
from core.logger import get_logger
from main import run_pipeline

# Sync DB imports for worker — use raw SQL to avoid importing async models
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from datetime import datetime, timezone

logger = get_logger(__name__)

# ── Sync DB connection for worker updates ─────────────────

def _get_sync_db_url():
    """Convert async DB URL to sync for the worker."""
    url = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@postgres:5432/autoclip")
    return url.replace("+asyncpg", "")

def _update_job_status(celery_task_id: str, **kwargs):
    """Update a Job row in the database (sync, from worker) using raw SQL."""
    try:
        engine = create_engine(_get_sync_db_url())
        with engine.connect() as conn:
            if kwargs:
                from sqlalchemy import update
                from core.models import Job
                stmt = update(Job).where(Job.celery_task_id == celery_task_id).values(**kwargs)
                conn.execute(stmt)
                conn.commit()
        engine.dispose()
    except Exception as e:
        logger.warning(f"Could not update job in DB: {e}")


# ── Pipeline progress callback ────────────────────────────

class ProgressTracker:
    """Publishes pipeline progress to Celery state (→ Redis → SSE)."""
    
    def __init__(self, task):
        self.task = task
        self.logs = []
        self.start_time = time.time()

    
    def log(self, message: str):
        """Add a log line."""
        self.logs.append(message)
    
    def set_progress(self, progress: float, step: str):
        """Set exact progress value and push to Celery state."""
        elapsed = time.time() - self.start_time
        eta_seconds = 0
        if 0 < progress < 100:
            eta_seconds = max(0, int((elapsed / (progress / 100.0)) - elapsed))

        self.task.update_state(
            state='STARTED',
            meta={
                'progress': progress,
                'step': step,
                'logs': self.logs[-20:],  # Last 20 lines
                'eta_seconds': eta_seconds,
            }
        )


# ── Main Celery Task ──────────────────────────────────────

@celery_app.task(bind=True, name="video.process")
def process_video_task(self, url: str, preferred_engine: str = "auto", num_clips: int | None = None, platforms: dict | None = None):
    """
    Task Celery qui emballe le pipeline complet d'AutoClip-AI.
    Publie le progrès via Celery state (incluant ETA) → Redis → SSE.
    Met à jour le Job dans la base de données.
    """
    task_id = self.request.id
    tracker = ProgressTracker(self)
    
    logger.info(f"Démarrage de la tâche de clipping pour URL: {url} (Engine: {preferred_engine})")
    
    # Mark job as STARTED in DB
    _update_job_status(task_id, status="STARTED", progress=0.0, current_step="Starting pipeline...")
    
    try:
        # Push initial progress
        tracker.set_progress(5, "📥 Downloading video...")
        tracker.log(f"🔗 Starting pipeline for: {url}")
        tracker.log(f"🤖 Engine: {preferred_engine}")
        if platforms:
            tracker.log(f"🎯 Target platforms: {platforms}")
        if num_clips:
            tracker.log(f"✂️ Requested clips: {num_clips}")
        
        result = run_pipeline(url=url, preferred_engine=preferred_engine, num_clips=num_clips, platforms=platforms)
        
        # Mark as complete
        tracker.set_progress(100, "✅ Completed!")
        tracker.log("✅ Pipeline finished successfully!")
        
        clips_dir = result.get("clips_dir")
        
        # Update job in DB as SUCCESS
        _update_job_status(
            task_id,
            status="SUCCESS",
            progress=100.0,
            current_step="Completed",
            result_path=clips_dir,
            completed_at=datetime.now(timezone.utc),
        )
        
        logger.info(f"Tâche de clipping terminée avec succès pour URL: {url}")
        return {
            "status": "success",
            "message": "Pipeline exécuté avec succès.",
            "clips_dir": clips_dir,
            "seo_generated": result.get("seo_generated")
        }
    except Exception as e:
        logger.error(f"Erreur lors du traitement de la vidéo {url}: {e}", exc_info=True)
        
        # Update job in DB as FAILURE
        error_msg = str(e)
        if len(error_msg) > 500:
            error_msg = error_msg[:500]
        _update_job_status(task_id, status="FAILURE", error_message=error_msg)
        
        tracker.log(f"❌ Error: {error_msg[:200]}")
        raise
