from __future__ import annotations
from core.logger import get_logger
logger = get_logger(__name__)


import os
import json
import requests


# === CATALOGUE D'EFFETS FFMPEG ===

# Filtres de couleur vibrante (appliqués en rotation)
COLOR_FILTERS = {
    "vibrant_warm": {
        "name": "Chaud Vibrant",
        "vf": "eq=saturation=1.15:contrast=1.05:brightness=0.02,colorbalance=rs=0.08:gs=-0.03:bs=-0.06"
    },
    "vibrant_cool": {
        "name": "Froid Vibrant",
        "vf": "eq=saturation=1.15:contrast=1.05,colorbalance=rs=-0.06:gs=0.03:bs=0.08"
    },
    "vibrant_golden": {
        "name": "Golden Hour",
        "vf": "eq=saturation=1.2:contrast=1.05:brightness=0.02,colorbalance=rs=0.1:gs=0.05:bs=-0.08"
    },
    "vibrant_teal_orange": {
        "name": "Teal & Orange",
        "vf": "eq=saturation=1.2:contrast=1.08,colorbalance=rs=0.08:gs=-0.03:bs=0.06:rh=-0.05:gh=0.01:bh=0.06"
    },
    "vibrant_neon": {
        "name": "Néon",
        "vf": "eq=saturation=1.2:contrast=1.1:brightness=0.01,hue=s=1.1"
    },
    "vibrant_cinematic": {
        "name": "Cinématique",
        "vf": "eq=saturation=1.1:contrast=1.1:brightness=-0.01,colorbalance=rs=0.03:gs=-0.02:bs=0.05"
    }
}

# Liste ordonnée pour la rotation entre plateformes
COLOR_ROTATION = list(COLOR_FILTERS.keys())

# Catalogue d'effets visuels et audio
EFFECTS_CATALOG = {
    # NOTE: zoompan entries removed (freeze videos). Zoom is handled by effects_visual.py.
    "zoom_pulse": {
        "description": "Zoom lent pulsé",
        "vf": "zoompan=z='if(lte(mod(on\\,90)\\,45)\\,min(zoom+0.002\\,1.15)\\,max(zoom-0.002\\,1))':d=1:s={w}x{h}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    },
    "smooth_zoom": {
        "description": "Zoom in progressif",
        "vf": "zoompan=z='min(zoom+0.0008\\,1.12)':d=1:s={w}x{h}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    },
    "subtle_zoom": {
        "description": "Zoom très subtil",
        "vf": "zoompan=z='min(zoom+0.0004\\,1.05)':d=1:s={w}x{h}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    },
    "bass_boost": {
        "description": "Boost basses fréquences",
        "af": "equalizer=f=80:t=q:w=1:g=5"
    },
    "audio_normalize": {
        "description": "Normalisation volume",
        "af": "loudnorm=I=-14:TP=-1:LRA=11"
    },
    "sharp": {
        "description": "Netteté accrue",
        "vf": "unsharp=5:5:1.0:5:5:0.0"
    }
}

# Presets par plateforme
DEFAULT_PRESETS = {
    "tiktok": {
        "format": {"width": 1080, "height": 1920},
        "effects": ["bass_boost", "sharp"],
        "color_filter": "vibrant_neon",
        "subtitle_style": "bold",
        "transition": "none",
    },
    "reels": {
        "format": {"width": 1080, "height": 1920},
        "effects": ["audio_normalize", "sharp"],
        "color_filter": "vibrant_teal_orange",
        "subtitle_style": "clean",
        "transition": "fade",
    },
    "facebook": {
        "format": {"width": 1080, "height": 1350},
        "effects": ["audio_normalize"],
        "color_filter": "vibrant_cinematic",
        "subtitle_style": "readable",
        "transition": "fade",
    }
}


def generate_effects_plan(
    viral_moments_path: str,
    output_path: str = "downloads/effects_plan.json",
    preferred_engine: str = "auto"
) -> dict | None:
    """Génère un plan d'effets visuels et sonores pour chaque clip.
    
    Args:
        viral_moments_path: Chemin vers le JSON des moments viraux.
        output_path: Chemin du fichier JSON de sortie.
        preferred_engine: Moteur IA à privilégier.
        
    Returns:
        Dictionnaire du plan d'effets généré ou None en cas d'échec.
    """
    if not os.path.exists(viral_moments_path):
        logger.error(f"❌ Fichier viral moments introuvable : {viral_moments_path}")
        return None
    
    with open(viral_moments_path, "r", encoding="utf-8") as f:
        viral_data = json.load(f)
    
    clips = viral_data.get("clips", [])
    if not clips:
        logger.warning("⚠️  Aucun clip pour le plan d'effets.")
        return None
    
    prompt = _build_effects_prompt(clips)
    
    from engines.engine_manager import manager
    system_prompt = "Tu es un directeur artistique vidéo. Réponds UNIQUEMENT en JSON valide."
    result = manager.execute_json(prompt, system_prompt, preferred_engine)
    
    if result:
        from schemas import parse_effects_response
        validated = parse_effects_response(result)
        if validated:
            result = validated.model_dump()
            logger.info("✅ Effets sélectionnés via EngineManager.")
    
    if not result:
        logger.warning("⚠️  IA indisponible ou JSON invalide. Utilisation des presets par défaut.")
        result = _generate_default_plan(clips)
    
    result = _validate_and_enrich(result)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)
    
    logger.info(f"✅ Plan d'effets généré → {output_path}")
    return result


def get_color_filter_vf(clip_effects: dict, platform: str, clip_index: int) -> str:
    """Retourne le filtre couleur FFmpeg pour ce clip/plateforme.
    
    Chaque plateforme a un filtre couleur différent, et ça tourne entre clips.
    """
    # D'abord chercher dans le plan IA
    if clip_effects:
        pf = clip_effects.get("platforms", {}).get(platform, {})
        color_key = pf.get("color_filter", "")
        if color_key in COLOR_FILTERS:
            return COLOR_FILTERS[color_key]["vf"]
    
    # Sinon rotation automatique
    # Chaque plateforme a un offset différent dans la rotation
    platform_offset = {"tiktok": 0, "reels": 2, "facebook": 4}.get(platform, 0)
    idx = (clip_index + platform_offset) % len(COLOR_ROTATION)
    color_key = COLOR_ROTATION[idx]
    return COLOR_FILTERS[color_key]["vf"]


def get_ffmpeg_filters(clip_effects: dict, platform: str) -> tuple[list[str], list[str]]:
    """Traduit le plan d'effets en filtres FFmpeg."""
    platform_plan = clip_effects.get("platforms", {}).get(platform, DEFAULT_PRESETS.get(platform, {}))
    effects = platform_plan.get("effects", [])
    
    video_filters = []
    audio_filters = []
    
    for effect_name in effects:
        if effect_name in EFFECTS_CATALOG:
            effect = EFFECTS_CATALOG[effect_name]
            if "vf" in effect:
                video_filters.append(effect["vf"])
            if "af" in effect:
                audio_filters.append(effect["af"])
    
    # Transition
    transition = platform_plan.get("transition", "none")
    if transition == "fade":
        audio_filters.append("afade=t=in:st=0:d=0.5")
    
    return video_filters, audio_filters


def get_output_dimensions(platform: str) -> tuple[int, int]:
    """Retourne les dimensions pour la plateforme."""
    from core.config import settings
    platform_config = settings.platforms.get(platform)
    if platform_config and hasattr(platform_config, "resolution"):
        w, h = platform_config.resolution.split("x")
        return int(w), int(h)
        
    preset = DEFAULT_PRESETS.get(platform, DEFAULT_PRESETS["tiktok"])
    return preset["format"]["width"], preset["format"]["height"]  # type: ignore


def _build_effects_prompt(clips: list[dict]) -> str:
    clips_info = json.dumps([{
        "index": i+1,
        "title": c.get("title", ""),
        "viral_score": c.get("viral_score", 5),
        "duration": round(c.get("end", 0) - c.get("start", 0), 1),
    } for i, c in enumerate(clips)], indent=2)
    
    color_names = list(COLOR_FILTERS.keys())
    effect_names = list(EFFECTS_CATALOG.keys())

    return f"""
Tu es un directeur artistique vidéo spécialisé en contenu viral court.

CLIPS :
{clips_info}

EFFETS DISPONIBLES : {json.dumps(effect_names)}
FILTRES COULEUR DISPONIBLES : {json.dumps(color_names)}

RÈGLES :
- CHAQUE plateforme doit avoir un filtre couleur DIFFÉRENT
- TikTok = vibrant_neon ou vibrant_warm + bass_boost + sharp. Dynamique.
- Reels = vibrant_teal_orange ou vibrant_golden + audio_normalize. Esthétique.
- Facebook = vibrant_cinematic ou vibrant_cool + audio_normalize. Posé.
- Plus le viral_score est élevé, plus d'effets.

JSON UNIQUEMENT :
{{
  "clips": [
    {{
      "clip_index": 1,
      "energy": "high",
      "platforms": {{
        "tiktok": {{
          "effects": ["bass_boost", "sharp"],
          "color_filter": "vibrant_neon",
          "transition": "none",
          "subtitle_style": "bold"
        }},
        "reels": {{
          "effects": ["audio_normalize", "sharp"],
          "color_filter": "vibrant_teal_orange",
          "transition": "fade",
          "subtitle_style": "clean"
        }},
        "facebook": {{
          "effects": ["audio_normalize"],
          "color_filter": "vibrant_cinematic",
          "transition": "fade",
          "subtitle_style": "readable"
        }}
      }}
    }}
  ]
}}
"""


def _generate_default_plan(clips):
    result: dict[str, list[dict]] = {"clips": []}
    for i, clip in enumerate(clips):
        score = clip.get("viral_score", 5)
        energy = "high" if score >= 8 else "medium" if score >= 6 else "low"
        
        # Rotation des couleurs entre clips
        tk_color = COLOR_ROTATION[(i * 2) % len(COLOR_ROTATION)]
        rl_color = COLOR_ROTATION[(i * 2 + 2) % len(COLOR_ROTATION)]
        fb_color = COLOR_ROTATION[(i * 2 + 4) % len(COLOR_ROTATION)]
        
        result["clips"].append({
            "clip_index": i + 1,
            "energy": energy,
            "platforms": {
                "tiktok": {
                    "effects": ["bass_boost", "sharp"] if energy != "low" else ["sharp"],
                    "color_filter": tk_color,
                    "transition": "none",
                    "subtitle_style": "bold"
                },
                "reels": {
                    "effects": ["audio_normalize", "sharp"],
                    "color_filter": rl_color,
                    "transition": "fade",
                    "subtitle_style": "clean"
                },
                "facebook": {
                    "effects": ["audio_normalize"],
                    "color_filter": fb_color,
                    "transition": "fade",
                    "subtitle_style": "readable"
                }
            }
        })
    return result


def _validate_and_enrich(result):
    if not result or "clips" not in result:
        return {"clips": []}
    for clip in result["clips"]:
        for platform in ["tiktok", "reels", "facebook"]:
            if platform not in clip.get("platforms", {}):
                clip.setdefault("platforms", {})[platform] = DEFAULT_PRESETS[platform]
            else:
                plan = clip["platforms"][platform]
                plan["effects"] = [e for e in plan.get("effects", []) if e in EFFECTS_CATALOG]
                if plan.get("color_filter", "") not in COLOR_FILTERS:
                    plan["color_filter"] = DEFAULT_PRESETS[platform].get("color_filter", "vibrant_warm")
    return result


def _parse_response(text):
    if text.startswith("```json"):
        text = text.replace("```json", "", 1)
    if text.startswith("```"):
        text = text.replace("```", "", 1)
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON invalide : {e}")
        return None


def _call_gemini(prompt, api_key):
    logger.info("🎨 Sélection des effets via Gemini...")
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2}
        }
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
        if response.status_code == 200:
            parts = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [])
            if parts:
                return _parse_response(parts[0].get("text", ""))
        logger.error(f"❌ Gemini effects ({response.status_code}): {response.text[:150]}")
    except Exception as e:
        logger.error(f"❌ Erreur Gemini : {e}")
    return None


def _call_groq(prompt, api_key):
    logger.info("🎨 Sélection des effets via Groq Llama...")
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "Tu es un directeur artistique vidéo. JSON valide uniquement."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"}
        }
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            text = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
            return _parse_response(text)
        logger.error(f"❌ Groq effects ({response.status_code}): {response.text[:150]}")
    except Exception as e:
        logger.error(f"❌ Erreur Groq : {e}")
    return None
