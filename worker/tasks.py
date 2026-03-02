import os
import sys

# Ajouter le répertoire parent pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.celery_app import celery_app
from core.logger import get_logger
from main import run_pipeline

logger = get_logger(__name__)

@celery_app.task(bind=True, name="video.process")
def process_video_task(self, url: str, preferred_engine: str = "auto", num_clips: int | None = None):
    """
    Task Celery qui emballe le pipeline complet d'AutoClip-AI.
    """
    logger.info(f"Démarrage de la tâche de clipping pour URL: {url} (Engine: {preferred_engine})")
    
    try:
        result = run_pipeline(url=url, preferred_engine=preferred_engine, num_clips=num_clips)
        logger.info(f"Tâche de clipping terminée avec succès pour URL: {url}")
        return {
            "status": "success",
            "message": "Pipeline exécuté avec succès.",
            "clips_dir": result.get("clips_dir"),
            "seo_generated": result.get("seo_generated")
        }
    except Exception as e:
        logger.error(f"Erreur lors du traitement de la vidéo {url}: {e}", exc_info=True)
        # On relance l'exception pour que Celery la marque en FAILED
        raise
