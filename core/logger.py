import logging
import sys
from typing import Any

# Color constants for terminal development output
COLORS = {
    "INFO": "\033[92m",      # Green
    "WARNING": "\033[93m",   # Yellow
    "ERROR": "\033[91m",     # Red
    "CRITICAL": "\033[1;91m",# Bold Red
    "DEBUG": "\033[94m",     # Blue
    "RESET": "\033[0m"
}

class ColorFormatter(logging.Formatter):
    """Custom format pour avoir des logs propres et colorés pendant le dev."""
    def __init__(self, fmt: str) -> None:
        super().__init__(fmt)

    def format(self, record: logging.LogRecord) -> str:
        log_color = COLORS.get(record.levelname, COLORS["RESET"])
        reset_color = COLORS["RESET"]
        
        # Format the base message
        message = super().format(record)
        return f"{log_color}{message}{reset_color}"

def setup_logger(name: str | None = None) -> logging.Logger:
    """Initialize and return a configured logger."""
    logger = logging.getLogger(name or "AutoClip")
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # Un format propre incluant le niveau de log, le module et le message (plus facile que des prints sauvages)
        fmt = "%(asctime)s | %(levelname)-8s | %(module)-12s | %(message)s"
        formatter = ColorFormatter(fmt)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        
        # Pour le SaaS: ici on ajouterait plus tard un FileHandler en JSON pour Datadog/ELK
        
    return logger

# Default export instance pour simplifier l'utilisation : `from core.logger import get_logger; logger = get_logger(__name__)`
def get_logger(module_name: str) -> logging.Logger:
    """Donne un logger pour un module spécifique."""
    return setup_logger(module_name)
