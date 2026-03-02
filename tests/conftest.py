import pytest

@pytest.fixture
def mock_transcriber(mocker):
    """Bouche la transcription audio (ne coûte rien, ne nécessite pas d'API)."""
    return mocker.patch(
        "transcriber.transcribe_audio",
        return_value={
            "text": "Coucou, c'est le test ! On est là. Achetez mon produit. Abonnez-vous !",
            "words": [
                {"word": "Coucou,", "start": 0.0, "end": 0.5},
                {"word": "c'est", "start": 0.5, "end": 1.0},
                {"word": "le", "start": 1.0, "end": 1.2},
                {"word": "test", "start": 1.2, "end": 2.0},
                {"word": "!", "start": 2.0, "end": 2.2},
            ]
        }
    )

@pytest.fixture
def mock_analyzer(mocker):
    """Bouche l'analyse IA des moments viraux."""
    return mocker.patch(
        "analyzer.analyze_transcription",
        return_value={
            "clips": [
                {
                    "title": "Clip de Test",
                    "start": 0.0,
                    "end": 2.0,
                    "viral_score": 9,
                    "explanation": "Test explanation",
                    "suggested_caption": "Le meilleur clip de test",
                    "hook_timestamp": 0.0,
                    "climax_timestamp": 1.0,
                    "energy_map": [{"start": 0, "end": 2, "energy": "high"}]
                }
            ]
        }
    )

@pytest.fixture
def mock_effects_director(mocker):
    """Bouche la génération du plan d'effets visuels/audio."""
    return mocker.patch(
        "effects_director.generate_effects_plan",
        return_value={
            "clips": [
                {
                    "clip_index": 1,
                    "platforms": {
                        "tiktok": {"color_filter": "vibrant_warm", "effects": ["flash_white"], "transition": "fade"},
                        "reels": {"color_filter": "vibrant_cool", "effects": ["zoom_pulse"], "transition": "fade"},
                        "facebook": {"color_filter": "cinematic", "effects": [], "transition": "cut"}
                    }
                }
            ]
        }
    )

@pytest.fixture
def mock_seo_generator(mocker):
    """Bouche la génération SEO."""
    return mocker.patch(
        "seo_generator.generate_seo",
        return_value={
            "clips": [
                {
                    "clip_index": 1,
                    "original_title": "Clip de Test",
                    "platforms": {
                        "tiktok": {"description": "Le meilleur clip TikTok", "hashtags": "#test #tiktok"},
                        "reels": {"description": "Le meilleur clip Insta", "hashtags": "#test #reels"},
                        "facebook": {"description": "Le meilleur clip FB", "hashtags": "#test #facebook"}
                    }
                }
            ]
        }
    )

@pytest.fixture
def mock_downloader(mocker):
    """Bouche le téléchargement YouTube."""
    mocker.patch("downloader.get_video_metadata", return_value={"title": "Test Video"})
    mocker.patch("downloader.download_video", return_value="downloads/test_video.mp4")
    mocker.patch("downloader.extract_audio", return_value="downloads/test_audio.mp3")
    return mocker
