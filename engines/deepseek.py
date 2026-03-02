from core.logger import get_logger
logger = get_logger(__name__)

import os
import json
import requests
from engines.base import AIEngine

class DeepSeekEngine(AIEngine):
    @property
    def name(self) -> str:
        return "DeepSeek"

    @property
    def env_key(self) -> str:
        return "DEEPSEEK_API_KEY"

    def is_available(self) -> bool:
        return bool(os.getenv(self.env_key))

    def call_json(self, prompt: str, system_prompt: str = "Tu es un expert.", temperature: float = 0.3) -> dict | None:
        api_key = os.getenv(self.env_key)
        if not api_key:
            return None

        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        full_system = f"{system_prompt}\nRÉPONDS UNIQUEMENT EN JSON VALIDE SANS BALISE MARKDOWN."
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": full_system},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=45)
            response.raise_for_status()
            result_json = response.json()
            raw_text = result_json["choices"][0]["message"]["content"]
            
            cleaned = self._clean_json_response(raw_text)
            return json.loads(cleaned)

        except requests.exceptions.HTTPError as e:
            logger.error(f"❌ Erreur HTTP avec Deepseek : {e}")
            if e.response is not None:
                logger.info(f"Details : {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"❌ Erreur avec DeepSeek : {e}")
            return None
