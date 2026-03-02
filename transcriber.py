from core.logger import get_logger
logger = get_logger(__name__)

import os
import json
import requests

def transcribe_audio(audio_path, api_key=None, output_json_path="downloads/transcription.json"):
    """
    Transcrit un fichier audio avec un système de fallback :
    1. Groq API (Whisper cloud) — rapide (~10s)
    2. Whisper local — lent mais sans limite
    """
    if not os.path.exists(audio_path):
        logger.error(f"❌ ERREUR : Le fichier audio '{audio_path}' est introuvable.")
        return None

    # --- Tentative 1 : Groq API (rapide) ---
    if api_key:
        result = _transcribe_groq(audio_path, api_key, output_json_path)
        if result:
            return result
        logger.error("⚠️  Groq a échoué. Basculement vers Whisper local...")
    else:
        logger.warning("⚠️  Pas de clé Groq. Utilisation directe de Whisper local.")

    # --- Tentative 2 : Whisper local (fallback) ---
    result = _transcribe_local(audio_path, output_json_path)
    return result


def _transcribe_groq(audio_path, api_key, output_json_path):
    """Transcription via l'API Groq (Whisper cloud)."""
    logger.info(f"Envoi de l'audio '{audio_path}' à Groq (Whisper)...")
    
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "whisper-large-v3",
        "temperature": "0",
        "response_format": "verbose_json"
    }

    try:
        with open(audio_path, "rb") as audio_file:
            files = {
                "file": (os.path.basename(audio_path), audio_file, "audio/mpeg")
            }
            response = requests.post(url, headers=headers, data=data, files=files, timeout=30)

        if response.status_code == 200:
            result = response.json()
            with open(output_json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            logger.info(f"✅ Transcription Groq réussie ! → {output_json_path}")
            return result
        else:
            logger.error(f"❌ Erreur Groq ({response.status_code}): {response.text[:200]}")
            return None

    except Exception as e:
        logger.error(f"❌ Erreur réseau Groq : {e}")
        return None


def _transcribe_local(audio_path, output_json_path, model_size="base"):
    """
    Transcription locale avec OpenAI Whisper.
    Modèle 'base' = bon compromis vitesse/qualité (~1 Go RAM).
    Modèle 'small' ou 'medium' pour plus de précision si besoin.
    """
    try:
        import whisper
    except ImportError:
        logger.error("❌ ERREUR : Le module 'whisper' n'est pas installé.")
        logger.info("   Installe-le avec : pip install openai-whisper")
        return None

    logger.info(f"🔄 Transcription locale en cours (modèle: {model_size})...")
    logger.info("   ⏳ Cela peut prendre quelques minutes...")
    
    model = whisper.load_model(model_size)
    raw_result = model.transcribe(audio_path, verbose=False)
    
    # Formatage du résultat au même format que Groq (verbose_json)
    # pour que le reste du pipeline fonctionne sans modification
    result = {
        "task": "transcribe",
        "language": raw_result.get("language", "unknown"),
        "duration": 0,
        "text": raw_result.get("text", ""),
        "segments": []
    }
    
    for seg in raw_result.get("segments", []):
        result["segments"].append({
            "id": seg.get("id", 0),
            "seek": seg.get("seek", 0),
            "start": seg.get("start", 0),
            "end": seg.get("end", 0),
            "text": seg.get("text", ""),
            "tokens": seg.get("tokens", []),
            "temperature": seg.get("temperature", 0),
            "avg_logprob": seg.get("avg_logprob", 0),
            "compression_ratio": seg.get("compression_ratio", 0),
            "no_speech_prob": seg.get("no_speech_prob", 0),
        })
    
    # Calculer la durée totale
    if result["segments"]:
        result["duration"] = result["segments"][-1]["end"]
    
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    
    logger.info(f"✅ Transcription locale réussie ! → {output_json_path}")
    return result


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(dotenv_path="/app/.env", override=True)
    
    API_KEY = os.getenv("GROQ_API_KEY")
    audio_test_file = "downloads/dQw4w9WgXcQ.mp3"
    
    logger.info("--- Démarrage du module Transcriber ---")
    transcription = transcribe_audio(audio_test_file, API_KEY)
    if transcription:
        logger.info(f"Aperçu du texte : {transcription.get('text', '')[:100]}...")
