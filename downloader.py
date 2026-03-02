from core.logger import get_logger
logger = get_logger(__name__)

import os
import subprocess
import json
import yt_dlp

def get_video_metadata(url):
    """
    Récupère les métadonnées YouTube (titre, description, tags, etc.)
    sans télécharger la vidéo. Utile pour l'analyse SEO.
    """
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get("title", ""),
                "description": info.get("description", ""),
                "tags": info.get("tags", []),
                "categories": info.get("categories", []),
                "channel": info.get("channel", ""),
                "duration": info.get("duration", 0),
                "view_count": info.get("view_count", 0),
                "like_count": info.get("like_count", 0),
                "language": info.get("language", ""),
            }
    except Exception as e:
        logger.warning(f"⚠️  Impossible de récupérer les métadonnées YouTube : {e}")
        return None

def download_video(url, output_folder="downloads"):
    """
    Télécharge une vidéo YouTube dans la meilleure qualité (mp4).
    Retourne le chemin du fichier vidéo téléchargé.
    """
    os.makedirs(output_folder, exist_ok=True)

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': f'{output_folder}/%(id)s.%(ext)s',
        'quiet': False,
        'merge_output_format': 'mp4',
        'extractor_args': {'youtube': {'player_client': ['web', 'default']}}, # Bypasse HTTP 400
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"Téléchargement de la vidéo : {url} ...")
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Puisque yt-dlp peut fusionner l'extension dynamiquement, on s'assure que c'est bien .mp4
            if not filename.endswith('.mp4'):
                filename = os.path.splitext(filename)[0] + '.mp4'
            logger.info(f"✅ Vidéo téléchargée avec succès : {filename}")
            return filename
    except Exception as e:
        logger.error(f"❌ Erreur lors du téléchargement: {e}")
        return None

def extract_audio(video_path):
    """
    Extrait l'audio d'une vidéo MP4 pour le sauvegarder en MP3 (nécessaire pour Whisper).
    Utilise ffmpeg en ligne de commande.
    """
    if not video_path or not os.path.exists(video_path):
        logger.error("❌ Fichier vidéo introuvable pour l'extraction audio.")
        return None

    audio_path = os.path.splitext(video_path)[0] + '.mp3'
    logger.info(f"Extraction de l'audio vers : {audio_path} ...")
    
    # On utilise des réglages optimisés pour la transcription IA (mono, 48k bitrate)
    # Cela permet de rester sous la limite de 25Mo tout en gardant une excellente qualité pour Whisper
    command = [
        'ffmpeg', '-i', video_path,
        '-ac', '1', '-b:a', '48k', '-map', 'a',
        audio_path, '-y', '-loglevel', 'error'
    ]
    try:
        subprocess.run(command, check=True, stderr=subprocess.PIPE)
        logger.info("✅ Extraction audio réussie.")
        return audio_path
    except subprocess.CalledProcessError as e:
        stderr_msg = e.stderr.decode('utf-8', errors='replace') if e.stderr else 'Aucun détail'
        logger.error(f"❌ Échec de l'extraction audio : {stderr_msg[:200]}")
        return None

if __name__ == "__main__":
    # Test avec une vidéo YouTube courte (libérée de droits ou bande annonce pour l'exemple)
    TEST_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Remplacer par n'importe quel lien pour tester
    logger.info("--- Démarrage du module Downloader ---")
    video_file = download_video(TEST_URL)
    audio_file = extract_audio(video_file)
