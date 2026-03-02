from __future__ import annotations
from core.logger import get_logger
logger = get_logger(__name__)


import os
import json
import requests
import re

def _safe_filename(title: str) -> str:
    """Nettoie un titre pour en faire un nom de fichier safe."""
    title = title.replace(" ", "_")
    title = re.sub(r'[^\w\-]', '', title, flags=re.UNICODE)
    return title[:80] if title else "clip"

def generate_seo(
    url: str,
    video_metadata: dict,
    viral_moments_path: str,
    transcription_path: str,
    output_path: str,
    clips_dir: str,
    preferred_engine: str = "auto"
) -> dict | None:
    """Génère des descriptions et hashtags optimisés par plateforme pour chaque clip.
    
    Args:
        url: URL de la vidéo source.
        video_metadata: Dictionnaire des métadonnées vidéo.
        viral_moments_path: Chemin vers le JSON des moments viraux.
        transcription_path: Chemin vers le JSON de transcription.
        output_path: Chemin du fichier JSON de sortie.
        clips_dir: Dossier où sauvegarder les fichiers textes individuels.
        preferred_engine: Moteur IA à privilégier.
        
    Returns:
        Dictionnaire du SEO généré ou None en cas d'échec.
    """
    if not os.path.exists(viral_moments_path):
        logger.error(f"❌ Fichier viral moments introuvable : {viral_moments_path}")
        return None
    
    with open(viral_moments_path, "r", encoding="utf-8") as f:
        viral_data = json.load(f)
    
    # Charger un extrait de la transcription pour contexte
    transcript_text = ""
    if os.path.exists(transcription_path):
        with open(transcription_path, "r", encoding="utf-8") as f:
            t_data = json.load(f)
            transcript_text = t_data.get("text", "")[:2000]

    clips = viral_data.get("clips", [])
    if not clips:
        logger.warning("⚠️  Aucun clip à traiter pour le SEO.")
        return None
    
    prompt = _build_seo_prompt(url, video_metadata, clips, transcript_text)
    
    from engines.engine_manager import manager
    system_prompt = "Tu es un expert en SEO pour les réseaux sociaux verticaux. Réponds UNIQUEMENT en JSON valide."
    result = manager.execute_json(prompt, system_prompt, preferred_engine)
    
    if result:
        from schemas import parse_seo_response
        validated = parse_seo_response(result)
        if validated:
            result = validated.model_dump()
            logger.info("✅ SEO généré via EngineManager.")
    
    if not result:
        logger.error("❌ Impossible de générer les descriptions SEO ou JSON invalide.")
        return None
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    
    # Génération des fichiers textes individuels par plateforme
    for clip in result.get("clips", []):
        clip_index = clip.get("clip_index")
        raw_title = clip.get("original_title", f"Clip_{clip_index}")
        safe_title = _safe_filename(raw_title)
        
        for platform, p_data in clip.get("platforms", {}).items():
            platform_dir = os.path.join(clips_dir, platform)
            os.makedirs(platform_dir, exist_ok=True)
            
            txt_filename = os.path.join(platform_dir, f"{clip_index}_{safe_title}.txt")
            
            desc = p_data.get("description", "")
            hashtags = p_data.get("hashtags", "")
            content = f"{desc}\n\n{hashtags}\n"
            
            with open(txt_filename, "w", encoding="utf-8") as tf:
                tf.write(content)
    
    logger.info(f"✅ Descriptions SEO générées → {output_path}")
    logger.info(f"✅ Fichiers textes SEO générés dans {clips_dir}/[Plateforme]/")
    return result


def _call_deepseek_seo(prompt: str) -> dict | None:
    """Wrapper pour l'appel DeepSeek SEO."""
    from deepseek_client import call_deepseek_json
    return call_deepseek_json(prompt, "Tu es un expert SEO social media. Réponds UNIQUEMENT en JSON valide.")


def _call_alibaba_seo(prompt: str) -> dict | None:
    """Wrapper pour l'appel Alibaba Qwen SEO."""
    from alibaba_client import call_alibaba_json
    return call_alibaba_json(prompt, "Tu es un expert SEO social media. Réponds UNIQUEMENT en JSON valide.")


def _build_seo_prompt(url: str, metadata: dict, clips: list[dict], transcript_text: str) -> str:
    """Construit le prompt pour la génération SEO."""
    meta_info = ""
    if metadata:
        meta_info = f"""
MÉTADONNÉES YOUTUBE :
- Titre : {metadata.get('title', 'N/A')}
- Chaîne : {metadata.get('channel', 'N/A')}
- Tags : {', '.join(metadata.get('tags', [])[:15])}
- Catégories : {', '.join(metadata.get('categories', []))}
- Vues : {metadata.get('view_count', 'N/A')}
- Description (extrait) : {metadata.get('description', '')[:500]}
"""
    
    clips_info = json.dumps([{
        "index": i+1,
        "title": c.get("title", ""),
        "start": c.get("start"),
        "end": c.get("end"),
        "caption": c.get("suggested_caption", "")
    } for i, c in enumerate(clips)], indent=2)

    return f"""
Tu es un expert en Social Media Marketing et SEO vidéo pour TikTok, Instagram Reels et Facebook.

URL DE LA VIDÉO ORIGINALE : {url}

{meta_info}

EXTRAIT DE LA TRANSCRIPTION :
{transcript_text[:1500]}

CLIPS EXTRAITS :
{clips_info}

TA MISSION :
Pour CHAQUE clip, génère des descriptions et hashtags optimisés pour 3 plateformes.

Règles SEO par plateforme :
- TikTok : Description courte et punchy (max 150 chars). Hashtags tendance (#fyp #pourtoi). Ton fun et direct.
- Instagram Reels : Description moyenne (max 200 chars). Mix hashtags niche + populaires. Ton inspirant.
- Facebook : Description plus longue et informative (max 300 chars). Peu de hashtags (3-5 max). Ton conversationnel.

Renvoie UNIQUEMENT un JSON valide (pas de markdown) :

{{
  "clips": [
    {{
      "clip_index": 1,
      "original_title": "titre du clip",
      "platforms": {{
        "tiktok": {{
          "title": "Titre court accrocheur",
          "description": "Description courte et punchy...",
          "hashtags": "#fyp #pourtoi #tag1 #tag2"
        }},
        "reels": {{
          "title": "Titre pour Reels",
          "description": "Description moyenne inspirante...",
          "hashtags": "#reels #viral #tag1 #tag2"
        }},
        "facebook": {{
          "title": "Titre pour Facebook",
          "description": "Description plus longue et informative...",
          "hashtags": "#tag1 #tag2 #tag3"
        }}
      }}
    }}
  ]
}}
"""


def _parse_response(text: str) -> dict | None:
    """Parse et nettoie la réponse JSON de l'IA."""
    if text.startswith("```json"):
        text = text.replace("```json", "", 1)
    if text.startswith("```"):
        text = text.replace("```", "", 1)
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError as e:
        logger.error(f"❌ Impossible de parser le SEO JSON : {e}")
        return None


def _call_gemini(prompt: str, api_key: str) -> dict | None:
    """Appel Gemini pour le SEO."""
    logger.info("🔍 Génération SEO via Gemini...")
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.3}
        }
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
        if response.status_code == 200:
            parts = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [])
            if parts:
                return _parse_response(parts[0].get("text", ""))
        logger.error(f"❌ Gemini SEO ({response.status_code}): {response.text[:150]}")
    except Exception as e:
        logger.error(f"❌ Erreur Gemini SEO : {e}")
    return None


def _call_groq(prompt: str, api_key: str) -> dict | None:
    """Appel Groq Llama pour le SEO."""
    logger.info("🔍 Génération SEO via Groq Llama...")
    
    truncated = prompt
    if len(prompt) > 8000:
        mission_idx = prompt.rfind("TA MISSION")
        mission_part = prompt[mission_idx:] if mission_idx != -1 else ""
        truncated = prompt[:8000] + "\n\n[... TRONQUÉ ...]\n\n" + mission_part
    
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "Tu es un expert SEO social media. Réponds UNIQUEMENT en JSON valide."},
                {"role": "user", "content": truncated}
            ],
            "temperature": 0.3,
            "response_format": {"type": "json_object"}
        }
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            text = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            return _parse_response(text)
        logger.error(f"❌ Groq SEO ({response.status_code}): {response.text[:150]}")
    except Exception as e:
        logger.error(f"❌ Erreur Groq SEO : {e}")
    return None
