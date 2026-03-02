from core.logger import get_logger
logger = get_logger(__name__)

import os
import json
import requests
from engines.base import AIEngine

class GeminiEngine(AIEngine):
    @property
    def name(self) -> str:
        return "Gemini"

    @property
    def env_key(self) -> str:
        return "GEMINI_API_KEY"

    def is_available(self) -> bool:
        return bool(os.getenv(self.env_key))

    def call_json(self, prompt: str, system_prompt: str = "Tu es un expert.", temperature: float = 0.3) -> dict | None:
        api_key = os.getenv(self.env_key)
        if not api_key:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        
        full_prompt = f"{system_prompt}\n\n{prompt}\n\nRÉPONDS UNIQUEMENT EN JSON VALIDE STRICTEMENT SANS AUCUN COMMENTAIRE NI BALISE MARKDOWN."
        
        payload = {
            "contents": [{"parts": [{"text": full_prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "response_mime_type": "application/json"
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=45)
            response.raise_for_status()
            data = response.json()
            
            try:
                # Structure typique de réponse Gemini avec JSON Mode
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                cleaned = self._clean_json_response(raw_text)
                return json.loads(cleaned)
            except (KeyError, IndexError):
                logger.error("❌ Gemini: Format de réponse inattendu.")
                return None
            except json.JSONDecodeError as e:
                logger.error(f"❌ Gemini: JSON invalide retourné : {e}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur réseau / API avec Gemini : {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.info(f"Details: {e.response.text}")
            return None
