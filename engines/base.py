from __future__ import annotations
from abc import ABC, abstractmethod

class AIEngine(ABC):
    """Interface abstraite pour tous les moteurs d'Intelligence Artificielle."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Le nom d'affichage du moteur (ex: 'Gemini', 'DeepSeek')."""
        pass

    @property
    @abstractmethod
    def env_key(self) -> str:
        """Le nom de la variable d'environnement contenant la clé API."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Vérifie si la clé API requise est présente et valide."""
        pass

    @abstractmethod
    def call_json(self, prompt: str, system_prompt: str = "Tu es un expert.", temperature: float = 0.3) -> dict | None:
        """Effectue l'appel à l'API et garantit de renvoyer un JSON parsé valide ou None."""
        pass

    def _clean_json_response(self, text: str) -> str:
        """Nettoie une réponse texte pour s'assurer qu'elle n'est constituée que du JSON.
        Typiquement utile pour les LLMs qui renvoient du Markdown.
        """
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()
