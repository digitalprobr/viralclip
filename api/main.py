from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import sys

# Ajouter le répertoire parent pour les imports (si on lance direct via uvicorn)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from worker.tasks import process_video_task
from celery.result import AsyncResult
from core.celery_app import celery_app

app = FastAPI(
    title="AutoClip-AI SaaS API",
    description="API permettant d'ingérer des requêtes de clipping vidéo et de les traiter asynchrone.",
    version="1.0.0"
)

# ─── CORS - Allow Frontend (Next.js) ───
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClipRequest(BaseModel):
    url: str
    preferred_engine: Optional[str] = "auto"
    num_clips: Optional[int] = None

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "autoclip-api"}

@app.post("/api/v1/clip")
def start_clipping_task(request: ClipRequest):
    """
    Démarre une tâche asynchrone de clipping pour une vidéo.
    Retourne l'ID de la tâche Celery pour faire du polling ensuite.
    """
    task = process_video_task.delay(
        request.url,
        request.preferred_engine,
        request.num_clips
    )
    return {
        "task_id": task.id,
        "message": "Vidéo ajoutée à la file d'attente avec succès",
        "status": "processing"
    }

@app.get("/api/v1/tasks/{task_id}")
def get_task_status(task_id: str):
    """
    Récupère le statut d'une tâche de clipping, ansi que son résultat final (si terminée).
    """
    task_result = AsyncResult(task_id, app=celery_app)
    response = {
        "task_id": task_id,
        "task_status": task_result.status,
    }
    
    if task_result.ready():
        if task_result.successful():
            response["result"] = task_result.result
        else:
            # Gestion basique des erreurs exposées à l'utilisateur
            response["error"] = str(task_result.result)
            
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
