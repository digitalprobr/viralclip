"""
ViralClip SaaS API — Main FastAPI application.
Follows 'thin routes, fat services' pattern.
"""
import asyncio
import json
import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

# Path setup for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import get_db, init_db, engine
from core.models import User, Job
from core.celery_app import celery_app
from worker.tasks import process_video_task
from celery.result import AsyncResult
from api.auth.router import router as auth_router
from api.auth.dependencies import get_current_user, get_current_user_optional
from api.auth.service import AuthService
from api.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


# ── Lifespan ─────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables on startup."""
    await init_db()
    yield
    await engine.dispose()


# ── App ──────────────────────────────────────────────────

app = FastAPI(
    title="ViralClip SaaS API",
    description="AI-powered video clipping platform API.",
    version="2.0.0",
    lifespan=lifespan,
)

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SecurityHeadersMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

# Auth router
app.include_router(auth_router)

# Serve video files
downloads_path = Path("/app/downloads")
if downloads_path.exists():
    app.mount("/files", StaticFiles(directory=str(downloads_path)), name="files")


# ── Schemas ──────────────────────────────────────────────

class ClipRequest(BaseModel):
    url: str
    preferred_engine: Optional[str] = "auto"
    num_clips: Optional[int] = None


class JobResponse(BaseModel):
    id: int
    celery_task_id: str | None
    url: str
    engine: str
    status: str
    progress: float
    current_step: str | None
    result_path: str | None
    error_message: str | None
    credits_used: int
    created_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True


# ── Health ───────────────────────────────────────────────

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "viralclip-api", "version": "2.0.0"}


# ── Credits ──────────────────────────────────────────────

@app.get("/api/v1/credits")
async def get_credits(user: User = Depends(get_current_user)):
    return {"credits": user.credits, "email": user.email}


# ── Submit Job ───────────────────────────────────────────

@app.post("/api/v1/clip")
async def start_clipping_task(
    request: ClipRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit a new clipping job. Requires authentication and credits."""
    cost = 10

    # Check credits
    if user.credits < cost:
        raise HTTPException(
            status_code=402,
            detail=f"Insufficient credits. You have {user.credits}, need {cost}."
        )

    # Create job record
    job = Job(
        user_id=user.id,
        url=request.url,
        engine=request.preferred_engine or "auto",
        num_clips=request.num_clips,
        status="PENDING",
        credits_used=cost,
    )
    db.add(job)
    await db.flush()

    # Deduct credits
    user.credits -= cost
    await db.flush()

    # Enqueue Celery task
    task = process_video_task.delay(
        request.url,
        request.preferred_engine,
        request.num_clips,
    )

    # Store Celery task ID
    job.celery_task_id = task.id
    await db.flush()

    return {
        "job_id": job.id,
        "task_id": task.id,
        "message": "Video added to the clipping queue",
        "status": "PENDING",
        "credits_remaining": user.credits,
    }


# ── List Jobs ────────────────────────────────────────────

@app.get("/api/v1/jobs")
async def list_jobs(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all jobs for the current user, syncing Celery status for pending ones."""
    result = await db.execute(
        select(Job)
        .where(Job.user_id == user.id)
        .order_by(Job.created_at.desc())
        .limit(50)
    )
    jobs = result.scalars().all()

    # Sync Celery status for non-terminal jobs
    for job in jobs:
        if job.status in ("PENDING", "STARTED") and job.celery_task_id:
            try:
                task_result = AsyncResult(job.celery_task_id, app=celery_app)
                if task_result.successful():
                    job.status = "SUCCESS"
                    job.progress = 100.0
                    job.current_step = "Completed"
                    job.result_path = task_result.result.get("clips_dir") if task_result.result else None
                    job.completed_at = datetime.utcnow()
                elif task_result.failed():
                    job.status = "FAILURE"
                    job.error_message = str(task_result.result)[:500] if task_result.result else "Unknown error"
                elif task_result.status == "STARTED":
                    job.status = "STARTED"
                    meta = task_result.info or {}
                    job.progress = meta.get("progress", 0)
                    job.current_step = meta.get("step", "Processing...")
            except Exception:
                pass  # Skip sync errors
    await db.flush()

    return [JobResponse.model_validate(j) for j in jobs]


# ── Task Status ──────────────────────────────────────────

@app.get("/api/v1/tasks/{task_id}")
async def get_task_status(task_id: str, db: AsyncSession = Depends(get_db)):
    """Get Celery task status and sync with Job table."""
    task_result = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "task_status": task_result.status,
    }

    if task_result.ready():
        if task_result.successful():
            response["result"] = task_result.result
            # Update job in DB
            await db.execute(
                update(Job)
                .where(Job.celery_task_id == task_id)
                .values(
                    status="SUCCESS",
                    progress=100.0,
                    current_step="Completed",
                    result_path=task_result.result.get("clips_dir") if task_result.result else None,
                    completed_at=datetime.utcnow(),
                )
            )
        else:
            response["error"] = str(task_result.result)
            await db.execute(
                update(Job)
                .where(Job.celery_task_id == task_id)
                .values(
                    status="FAILURE",
                    error_message=str(task_result.result),
                    completed_at=datetime.utcnow(),
                )
            )

    return response


# ── SSE Progress Stream ──────────────────────────────────

@app.get("/api/v1/tasks/{task_id}/stream")
async def stream_task_progress(task_id: str):
    """Server-Sent Events endpoint for real-time task progress."""
    async def event_generator():
        progress_steps = [
            (0, 15, "📥 Downloading video..."),
            (15, 35, "📝 Transcribing audio..."),
            (35, 55, "🧠 Analyzing viral moments..."),
            (55, 70, "🎨 Planning effects..."),
            (70, 90, "✂️ Clipping & rendering..."),
            (90, 100, "🔍 Generating SEO descriptions..."),
        ]

        while True:
            task_result = AsyncResult(task_id, app=celery_app)

            if task_result.status == "SUCCESS":
                yield f"data: {json.dumps({'progress': 100, 'step': '✅ Completed!', 'status': 'SUCCESS', 'result': task_result.result})}\n\n"
                break
            elif task_result.status == "FAILURE":
                yield f"data: {json.dumps({'progress': 0, 'step': '❌ Failed', 'status': 'FAILURE', 'error': str(task_result.result)})}\n\n"
                break
            elif task_result.status == "STARTED":
                # Try to read progress from task meta
                meta = task_result.info or {}
                progress = meta.get("progress", 0)
                step = meta.get("step", "Processing...")
                logs = meta.get("logs", [])
                yield f"data: {json.dumps({'progress': progress, 'step': step, 'status': 'STARTED', 'logs': logs})}\n\n"
            else:
                yield f"data: {json.dumps({'progress': 0, 'step': '⏳ Waiting in queue...', 'status': 'PENDING'})}\n\n"

            await asyncio.sleep(2)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


# ── List clip files ──────────────────────────────────────

@app.get("/api/v1/clips/{job_id}/files")
async def list_clip_files(
    job_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all generated clip files for a job."""
    result = await db.execute(
        select(Job).where(Job.id == job_id, Job.user_id == user.id)
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if not job.result_path:
        return {"files": [], "message": "No clips generated yet"}

    clips_dir = Path(f"/app/{job.result_path}")
    # Strip 'downloads/' prefix for URL since StaticFiles mounts /app/downloads at /files
    relative_path = job.result_path
    if relative_path.startswith("downloads/"):
        relative_path = relative_path[len("downloads/"):]
    
    files = []

    for platform in ["tiktok", "reels", "facebook"]:
        platform_dir = clips_dir / platform
        if platform_dir.exists():
            for f in sorted(platform_dir.glob("*.mp4")):
                files.append({
                    "name": f.name,
                    "platform": platform,
                    "url": f"/files/{relative_path}/{platform}/{f.name}",
                    "size": f.stat().st_size,
                })

    # Also check root clips
    for f in sorted(clips_dir.glob("*.mp4")):
        files.append({
            "name": f.name,
            "platform": "default",
            "url": f"/files/{relative_path}/{f.name}",
            "size": f.stat().st_size,
        })

    return {"files": files, "clips_dir": job.result_path}


# ── Entry point ──────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
