"""Configuration centrale de l'application.

Charge les paramètres depuis config/settings.yaml et valide la structure
avec Pydantic pour s'assurer que l'application démarre avec des paramètres valides.
"""
from __future__ import annotations

import os
import yaml
from pydantic import BaseModel, Field

class ClipDurationConfig(BaseModel):
    min: int = 15
    max: int = 60

class PipelineConfig(BaseModel):
    engine: str = "auto"
    min_clips: int = 3
    max_clips: int = 7
    clip_duration: ClipDurationConfig = Field(default_factory=ClipDurationConfig)
    structure: str = "episodic"

class VideoConfig(BaseModel):
    output_quality: str = "high"
    max_saturation: float = 1.2
    max_contrast: float = 1.1
    face_tracking: bool = True
    subtitles: bool = True

class PlatformConfig(BaseModel):
    enabled: bool = True
    resolution: str = "1080x1920"
    color_style: str = "vibrant"

class VisualEffectsConfig(BaseModel):
    zoom_on_hook: bool = True
    zoom_on_climax: bool = True
    shake_on_impact: bool = True
    vignette: bool = True

class AudioEffectsConfig(BaseModel):
    sfx_enabled: bool = True
    bass_drop_on_punchline: bool = True
    whoosh_on_transition: bool = True
    riser_before_hook: bool = True

class TransitionsConfig(BaseModel):
    style: str = "crossfade"
    duration: float = 0.3

class EffectsConfig(BaseModel):
    visual: VisualEffectsConfig = Field(default_factory=VisualEffectsConfig)
    audio: AudioEffectsConfig = Field(default_factory=AudioEffectsConfig)
    transitions: TransitionsConfig = Field(default_factory=TransitionsConfig)

class AppConfig(BaseModel):
    pipeline: PipelineConfig = Field(default_factory=PipelineConfig)
    video: VideoConfig = Field(default_factory=VideoConfig)
    platforms: dict[str, PlatformConfig] = Field(default_factory=dict)
    effects: EffectsConfig = Field(default_factory=EffectsConfig)

def load_config(config_path: str = "config/settings.yaml") -> AppConfig:
    """Charge et valide la configuration YAML."""
    if not os.path.exists(config_path):
        print(f"⚠️  Fichier de config '{config_path}' introuvable. Utilisation des valeurs par défaut.")
        return AppConfig()
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            raw_data = yaml.safe_load(f) or {}
        return AppConfig.model_validate(raw_data)
    except Exception as e:
        print(f"❌ ERREUR: Impossible de lire '{config_path}' : {e}")
        print("💡 Utilisation des valeurs par défaut en mode dégradé.")
        return AppConfig()

# Instance globale (Singleton) pour un accès facile
settings = load_config()
