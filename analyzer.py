from __future__ import annotations
from core.logger import get_logger
logger = get_logger(__name__)


import os
import json
import requests


def analyze_transcription(
    transcription_json_path: str,
    output_json_path: str = "downloads/viral_moments.json",
    preferred_engine: str = "auto",
    num_clips: int | None = None
) -> dict | None:
    """Analyse la transcription pour extraire les moments viraux.
    
    Args:
        transcription_json_path: Chemin vers le fichier JSON de transcription.
        output_json_path: Chemin du fichier JSON de sortie.
        preferred_engine: Moteur IA ('auto', 'gemini', 'deepseek', 'qwen', 'groq').
        num_clips: Nombre exact de clips à extraire (surcharge settings).
        
    Returns:
        Dictionnaire des moments viraux ou None en cas d'échec.
    """
    if not os.path.exists(transcription_json_path):
        logger.error(f"❌ ERREUR : Fichier de transcription '{transcription_json_path}' introuvable.")
        return None

    prompt = _build_prompt(transcription_json_path, num_clips)
    if not prompt:
        return None

    from engines.engine_manager import manager
    system_prompt = "Tu es un expert en contenu viral. Réponds UNIQUEMENT en JSON valide."
    result = manager.execute_json(prompt, system_prompt, preferred_engine)
    
    if result:
        from schemas import parse_analyzer_response
        validated = parse_analyzer_response(result)
        if validated:
            return _save_result(validated.model_dump(), output_json_path, "EngineManager")
            
    logger.error("❌ Tous les moteurs ont échoué ou le JSON est invalide.")
    return None

def _build_prompt(transcription_json_path, num_clips=None):
    """Construit le prompt d'analyse avec structure Hook/Contenu/CTA + energy map."""
    from core.config import settings

    with open(transcription_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    full_text = data.get("text", "")
    segments = data.get("segments", [])
    
    simplified_segments = [
        {"id": s.get("id"), "start": s.get("start"), "end": s.get("end"), "text": s.get("text")}
        for s in segments
    ]

    min_c = settings.pipeline.min_clips
    max_c = settings.pipeline.max_clips
    min_d = settings.pipeline.clip_duration.min
    max_d = settings.pipeline.clip_duration.max
    
    if num_clips:
        format_instruction = f"2. FORMAT SÉRIE : Tu DOIS ABSOLUMENT générer EXACTEMENT {num_clips} clips complets, nomenclature \"Part X - [Titre]\", en suivant l'ordre chronologique."
    else:
        format_instruction = f"2. FORMAT SÉRIE : Entre {min_c} et {max_c} clips, nomenclature \"Part X - [Titre]\", ordre chronologique."

    prompt = f"""
Tu es un MONTEUR PROFESSIONNEL spécialisé en contenu short-form viral (TikTok, Reels, Shorts).
Tu maîtrises les PATTERNS qui font scroller puis rester : hook puissant, rythme, tension, punchline.

TEXTE COMPLET :
{full_text}

---
SEGMENTS AVEC TIMESTAMPS :
{json.dumps(simplified_segments, indent=2)}

---
RÈGLES DE MONTAGE OBLIGATOIRES :

1. STRUCTURE DE CHAQUE CLIP (OBLIGATOIRE) :
   - HOOK (0-3 secondes) : Le clip DOIT commencer par un moment qui accroche IMMÉDIATEMENT.
     Types de hooks : phrase choc, question provocante, action visuelle forte, révélation, moment WTF.
     ⚠️ NE JAMAIS commencer par "bonjour", "salut", ou une intro molle.
   - CONTENU (milieu) : Développement, valeur, tension narrative.
   - CTA / CLIFFHANGER (dernières 3-5s) : Finir par un teaser, une question ouverte,
     ou une transition vers la Part suivante. Le spectateur DOIT vouloir la suite.

{format_instruction}

3. DURÉE : {min_d}-{max_d} secondes par clip. Pas de phrases coupées.

4. ENERGY MAP : Pour chaque clip, fournis une carte d'énergie (intensité 1-10)
   par tranches de 2 secondes. Ceci sera utilisé pour synchroniser les effets visuels
   et sonores automatiquement.
   - 1-3 = calme (pas d'effets)
   - 4-6 = montée (zoom léger, riser audio)
   - 7-8 = intense (zoom, bass boost)
   - 9-10 = IMPACT (zoom pulse, shake, bass drop, flash)

5. TIMESTAMPS CLÉS : Indique le moment exact du hook et du climax pour chaque clip.

---
RENVOIE UNIQUEMENT ce JSON (pas de markdown, pas de texte autour) :

{{
  "clips": [
    {{
      "clip_index": 1,
      "title": "Part 1 - [Titre accrocheur avec hook]",
      "start": 12.5,
      "end": 45.2,
      "viral_score": 9,
      "hook_type": "question",
      "hook_timestamp": 12.5,
      "climax_timestamp": 35.0,
      "energy_map": [3, 5, 6, 7, 8, 9, 10, 8, 7, 5, 4, 6, 8, 7, 5, 3],
      "suggested_caption": "Le début de l'histoire..."
    }},
    {{
      "clip_index": 2,
      "title": "Part 2 - [Le rebondissement]",
      "start": 60.0,
      "end": 95.5,
      "viral_score": 8,
      "hook_type": "revelation",
      "hook_timestamp": 60.0,
      "climax_timestamp": 82.0,
      "energy_map": [5, 7, 8, 9, 6, 5, 7, 8, 9, 10, 8, 6, 5, 4, 7, 8, 6],
      "suggested_caption": "Vous ne devinerez jamais..."
    }}
  ]
}}

TYPES DE HOOK VALIDES : "question", "revelation", "action", "emotion", "wtf", "statement"
"""
    return prompt


def _parse_ai_response(result_text):
    """Nettoie et parse la réponse JSON de l'IA."""
    # Nettoyage des balises markdown
    if result_text.startswith("```json"):
        result_text = result_text.replace("```json", "", 1)
    if result_text.startswith("```"):
        result_text = result_text.replace("```", "", 1)
    if result_text.endswith("```"):
        result_text = result_text.rsplit("```", 1)[0]
    
    try:
        return json.loads(result_text.strip())
    except json.JSONDecodeError as e:
        logger.error(f"❌ Impossible de parser la réponse JSON de l'IA : {e}")
        logger.info(f"   Réponse brute : {result_text[:200]}...")
        return None


def _save_result(viral_data, output_json_path, engine_name):
    """Sauvegarde le résultat et retourne les données."""
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(viral_data, f, indent=4, ensure_ascii=False)
    logger.info(f"✅ Analyse réussie avec {engine_name} ! Moments sauvegardés dans : {output_json_path}")
    return viral_data


def _analyze_gemini(prompt, api_key):
    """Analyse via l'API REST Gemini 2.0 Flash."""
    logger.info("Envoi de la transcription à Google Gemini pour analyse des moments viraux...")
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.2
            }
        }
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
        
        if response.status_code == 200:
            result_json = response.json()
            candidates = result_json.get("candidates", [])
            if not candidates:
                logger.error("❌ Gemini : réponse vide ou filtrée.")
                return None
            
            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                logger.error("❌ Gemini : aucun contenu dans la réponse.")
                return None
            
            return _parse_ai_response(parts[0].get("text", ""))
        else:
            logger.error(f"❌ Erreur Gemini ({response.status_code}): {response.text[:200]}")
            return None
    except Exception as e:
        logger.error(f"❌ Erreur Gemini : {e}")
        return None


def _analyze_groq(prompt, api_key):
    """Analyse via l'API Groq (Llama 3.3 70B). Prompt tronqué pour respecter les limites TPM."""
    logger.info("Envoi de la transcription à Groq (Llama 3.3 70B) pour analyse des moments viraux...")
    
    # Groq a une limite TPM stricte (12K tokens free tier)
    # On tronque intelligemment par segments entiers
    truncated_prompt = prompt
    if len(prompt) > 8000:
        # Garder le début (texte complet tronqué) + les instructions de mission
        mission_idx = prompt.rfind("TA MISSION")
        mission_part = prompt[mission_idx:] if mission_idx != -1 else ""
        truncated_prompt = prompt[:8000] + "\n\n[... TRANSCRIPTION TRONQUÉE ...]\n\n" + mission_part
    
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "Tu es un expert en montage vidéo viral. Réponds UNIQUEMENT en JSON valide."},
                {"role": "user", "content": truncated_prompt}
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"}
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result_json = response.json()
            choices = result_json.get("choices", [])
            if not choices:
                logger.error("❌ Groq : aucune réponse.")
                return None
            
            result_text = choices[0].get("message", {}).get("content", "")
            return _parse_ai_response(result_text)
        else:
            logger.error(f"❌ Erreur Groq ({response.status_code}): {response.text[:200]}")
            return None
    except Exception as e:
        logger.error(f"❌ Erreur Groq : {e}")
        return None


if __name__ == "__main__":
    transcription_file = "downloads/transcription.json"
    logger.info("--- Démarrage du module Analyzer ---")
    
    result = analyze_transcription(transcription_file)
    if result:
        logger.info("\n🏆 Clips potentiels trouvés :")
        for i, clip in enumerate(result.get("clips", [])):
            logger.info(f"[{i+1}] {clip['title']} (Score: {clip['viral_score']}) -> De {clip['start']}s à {clip['end']}s")
