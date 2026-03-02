from __future__ import annotations
from core.logger import get_logger
logger = get_logger(__name__)

from typing import Type
from engines.base import AIEngine
from engines.gemini import GeminiEngine
from engines.deepseek import DeepSeekEngine
from engines.alibaba import AlibabaEngine
from engines.groq import GroqEngine
from engines.huggingface import HuggingFaceEngine
from core.config import settings

class EngineManager:
    """Gestionnaire centralisé pour la sélection et l'exécution asynchrone des moteurs IA.
    Implémente une logique de fallback robuste.
    """
    
    def __init__(self):
        # Ordre de base: on priorise les modèles les plus performants / adaptés au format JSON complexe
        self._engines: dict[str, AIEngine] = {
            "gemini": GeminiEngine(),
            "deepseek": DeepSeekEngine(),
            "qwen": AlibabaEngine(),
            "groq": GroqEngine(),
            "huggingface": HuggingFaceEngine(model_id="Qwen/Qwen2.5-72B-Instruct")
        }

    def _get_engine_order(self, preferred: str = "auto") -> list[str]:
        """Retourne l'ordre dans lequel les moteurs doivent être essayés."""
        default_order = ["gemini", "deepseek", "qwen", "groq", "huggingface"]
        
        # Le réglage global dans settings.yaml prévaut si present (hors fallback CLI args)
        if preferred == "auto":
            preferred = settings.pipeline.engine
            
        if preferred != "auto" and preferred in default_order:
            # Mettre le moteur choisi en premier, garder le reste dans l'ordre par défaut
            return [preferred] + [e for e in default_order if e != preferred]
            
        return default_order

    def execute_json(self, prompt: str, system_prompt: str, preferred_engine: str = "auto", temperature: float = 0.3) -> dict | None:
        """Exécute la requête JSON sur les moteurs disponibles jusqu'à réussite.
        
        Returns:
            Le premier Dictionnaire JSON valide retourné, ou None si tout échoue.
        """
        engine_order = self._get_engine_order(preferred_engine)
        
        for eng_key in engine_order:
            engine = self._engines.get(eng_key)
            if not engine or not engine.is_available():
                continue
                
            marker = "🎯" if eng_key == preferred_engine else "🧠"
            logger.info(f"{marker} Requête via {engine.name}{' (moteur forcé)' if eng_key == preferred_engine else ''}...")
            
            result = engine.call_json(prompt, system_prompt, temperature=temperature)
            
            if result is not None:
                return result
                
            logger.warning(f"⚠️  {engine.name} n'a pas retourné de résultat valide. Basculement...")
            
        logger.error("❌ Tous les moteurs IA ont échoué. Impossible de récupérer un résultat JSON valide.")
        return None

# Instance singleton pour tout le projet
manager = EngineManager()
