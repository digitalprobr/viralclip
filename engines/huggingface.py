from core.logger import get_logger
logger = get_logger(__name__)

import os
import requests
import json
from .base import AIEngine

class HuggingFaceEngine(AIEngine):
    """
    Moteur IA utilisant l'API Serverless d'Hugging Face.
    Par défaut, on pointe vers un modèle Llama 3 autorisé pour l'API gratuite,
    ou Mixtral/Qwen.
    """
    def __init__(self, model_id: str = "meta-llama/Meta-Llama-3-8B-Instruct"):
        self.model_id = model_id

    @property
    def name(self) -> str:
        return f"HuggingFace ({self.model_id})"

    @property
    def env_key(self) -> str:
        return "HF_TOKEN"

    def is_available(self) -> bool:
        return bool(os.getenv(self.env_key))

    def call_json(self, prompt: str, system_prompt: str = "Tu es un assistant JSON.", temperature: float = 0.3) -> dict | None:
        token = os.getenv(self.env_key)
        if not token:
            logger.error("❌ HF_TOKEN manquant pour HuggingFaceEngine.")
            return None

        url = "https://router.huggingface.co/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Format OpenAI compatible API sur Hugging Face
        data = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "max_tokens": 2048,
            "stream": False
        }

        try:
            response = requests.post(url, headers=headers, json=data, timeout=60)
            
            # Gestion des modèles en chargement sur l'API Serverless HF
            if response.status_code == 503:
                err_data = response.json()
                if "estimated_time" in err_data:
                    logger.warning(f"⚠️  Le modèle {self.model_id} est en cours de chargement sur Hugging Face. (Attente estimée : {err_data['estimated_time']:.1f}s)")
                else:
                    logger.error(f"❌ API Hugging Face indisponible : {response.text}")
                return None
                
            response.raise_for_status()
            
            result_json = response.json()
            if "choices" in result_json and len(result_json["choices"]) > 0:
                text_response = result_json["choices"][0]["message"]["content"]
                
                # Nettoyage et Parsing
                clean_text = self._clean_json_response(text_response)
                try:
                    return json.loads(clean_text)
                except json.JSONDecodeError:
                    logger.error(f"❌ HuggingFaceEngine a retourné un JSON invalide:\n{clean_text}")
                    return None
            else:
                logger.error(f"❌ Réponse inattendue de Hugging Face : {result_json}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur réseau / API avec Hugging Face : {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.info(f"Details: {e.response.text}")
            return None
