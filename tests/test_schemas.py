import pytest
import json
from schemas import (
    AnalyzerResponse,
    EffectsResponse,
    SEOResponse,
    parse_analyzer_response,
    parse_effects_response,
    parse_seo_response
)

def test_parse_analyzer_response_valid():
    """Vérifie que la validation Pydantic fonctionne pour un JSON d'analyse valide."""
    valid_json = '''
    {
      "clips": [
        {
          "title": "Un titre de test",
          "start": 10.5,
          "end": 25.0,
          "viral_score": 8,
          "explanation": "Bon moment",
          "suggested_caption": "Regardez ça !",
          "hook_timestamp": 10.5,
          "climax_timestamp": 15.0,
          "energy_map": [{"start": 10.5, "end": 15.0, "energy": "medium"}]
        }
      ]
    }
    '''
    result = parse_analyzer_response(json.loads(valid_json))
    assert result is not None
    assert isinstance(result, AnalyzerResponse)
    assert len(result.clips) == 1
    assert result.clips[0].viral_score == 8
    assert result.clips[0].title == "Un titre de test"

def test_parse_analyzer_response_invalid():
    """Vérifie que le parser retourne None ou lève une exception (handle gracefully) pour du JSON corrompu."""
    invalid_json = '{ "clips": [ { "start": "pas_un_nombre" } ] }'
    result = parse_analyzer_response(json.loads(invalid_json))
    assert result is None  # Le parser catch l'erreur ValidationError et retourne None

def test_parse_effects_response_valid():
    valid_json = '''
    {
      "clips": [
        {
          "clip_index": 1,
          "platforms": {
            "tiktok": {
              "color_filter": "vibrant_warm",
              "effects": ["flash_white", "zoom_pulse"],
              "transition": "fade"
            }
          }
        }
      ]
    }
    '''
    result = parse_effects_response(json.loads(valid_json))
    assert result is not None
    assert isinstance(result, EffectsResponse)
    assert len(result.clips) == 1
    assert result.clips[0].platforms["tiktok"].color_filter == "vibrant_warm"

def test_parse_seo_response_valid():
    valid_json = '''
    {
      "clips": [
        {
          "clip_index": 1,
          "original_title": "Titre super cool",
          "platforms": {
            "tiktok": {
              "title": "Tiktok title",
              "description": "OMG",
              "hashtags": "#test"
            }
          }
        }
      ]
    }
    '''
    result = parse_seo_response(json.loads(valid_json))
    assert result is not None
    assert isinstance(result, SEOResponse)
    assert result.clips[0].platforms["tiktok"].title == "Tiktok title"
