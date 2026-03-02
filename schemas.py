"""Pydantic v2 schemas for validating AI API responses.

Ensures that JSON received from Gemini/Qwen/DeepSeek/Groq
is structurally valid before entering the pipeline.
Invalid fields are silently defaulted rather than crashing.
"""

from __future__ import annotations
from core.logger import get_logger
logger = get_logger(__name__)


from pydantic import BaseModel, Field, field_validator


# ──────────────────────────────────────────────
# ANALYZER — Viral Moments
# ──────────────────────────────────────────────

class ClipAnalysis(BaseModel):
    """A single clip identified by the AI analyzer."""
    title: str = ""
    start: float = Field(default=0, ge=0)
    end: float = Field(default=0, ge=0)
    viral_score: int = Field(default=5, ge=1, le=10)
    suggested_caption: str = ""
    hook_type: str = ""
    hook_timestamp: float = 0
    climax_timestamp: float = 0
    energy_map: list[int] = Field(default_factory=list)

    @field_validator("energy_map", mode="before")
    @classmethod
    def coerce_energy_map(cls, v: object) -> list[int]:
        """Accept list of int/float and clamp each value to 1-10."""
        if not isinstance(v, list):
            return []
        return [max(1, min(10, int(x))) for x in v if isinstance(x, (int, float))]


class AnalyzerResponse(BaseModel):
    """Root response from the viral moments analyzer."""
    clips: list[ClipAnalysis] = Field(default_factory=list)


# ──────────────────────────────────────────────
# EFFECTS DIRECTOR — Per-platform effects plan
# ──────────────────────────────────────────────

class PlatformEffects(BaseModel):
    """Effects plan for a single platform."""
    effects: list[str] = Field(default_factory=list)
    color_filter: str = ""
    transition: str = "none"
    subtitle_style: str = "bold"


class ClipEffects(BaseModel):
    """Effects for one clip across all platforms."""
    clip_index: int = 1
    energy: str = "medium"
    platforms: dict[str, PlatformEffects] = Field(default_factory=dict)


class EffectsResponse(BaseModel):
    """Root response from the effects director."""
    clips: list[ClipEffects] = Field(default_factory=list)


# ──────────────────────────────────────────────
# SEO GENERATOR — Descriptions & Hashtags
# ──────────────────────────────────────────────

class PlatformSEO(BaseModel):
    """SEO data for one platform."""
    title: str = ""
    description: str = ""
    hashtags: str = ""


class ClipSEO(BaseModel):
    """SEO data for one clip across all platforms."""
    clip_index: int = 1
    original_title: str = ""
    platforms: dict[str, PlatformSEO] = Field(default_factory=dict)


class SEOResponse(BaseModel):
    """Root response from the SEO generator."""
    clips: list[ClipSEO] = Field(default_factory=list)


# ──────────────────────────────────────────────
# Parsing helpers
# ──────────────────────────────────────────────

def parse_analyzer_response(raw: dict | None) -> AnalyzerResponse | None:
    """Validate and parse an analyzer response dict.

    Returns:
        Validated AnalyzerResponse or None if input is invalid.
    """
    if not raw:
        return None
    try:
        return AnalyzerResponse.model_validate(raw)
    except Exception as e:
        logger.error(f"⚠️  Validation AnalyzerResponse échouée : {e}")
        return None


def parse_effects_response(raw: dict | None) -> EffectsResponse | None:
    """Validate and parse an effects director response dict."""
    if not raw:
        return None
    try:
        return EffectsResponse.model_validate(raw)
    except Exception as e:
        logger.error(f"⚠️  Validation EffectsResponse échouée : {e}")
        return None


def parse_seo_response(raw: dict | None) -> SEOResponse | None:
    """Validate and parse an SEO generator response dict."""
    if not raw:
        return None
    try:
        return SEOResponse.model_validate(raw)
    except Exception as e:
        logger.error(f"⚠️  Validation SEOResponse échouée : {e}")
        return None
