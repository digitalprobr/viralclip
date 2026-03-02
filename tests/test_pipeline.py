import os
import pytest
from clipper import process_clips
import json

def test_pipeline_end_to_end(mock_transcriber, mock_analyzer, mock_effects_director, mock_seo_generator, tmp_path):
    """
    Test d'intégration end-to-end de la fonction process_clips en utilisant les mocks.
    On vérifie que les sous-titres, la découpe et le rendu génèrent bien des vidéos.
    """
    video_path = "downloads/test_dummy_video.mp4"
    if not os.path.exists(video_path):
        pytest.skip("La vidéo de test_dummy_video.mp4 n'existe pas. Veuillez l'exécuter avant.")

    # Créer les fichiers JSON factices pour le test
    viral_json = tmp_path / "viral.json"
    transcription_json = tmp_path / "transcription.json"
    
    with open(viral_json, "w") as f:
        json.dump(mock_analyzer.return_value, f)
        
    with open(transcription_json, "w") as f:
        json.dump(mock_transcriber.return_value, f)
        
    effects_plan = mock_effects_director.return_value
    
    # Exécuter le pipeline
    output_dir = tmp_path / "clips"
    process_clips(video_path, str(viral_json), str(transcription_json), str(output_dir), effects_plan)
    
    # Vérifier que les dossiers de plateforme sont créés
    assert (output_dir / "tiktok").exists()
    assert (output_dir / "reels").exists()
    assert (output_dir / "facebook").exists()
    
    # Vérifier que les fichiers MP4 existent
    assert (output_dir / "tiktok" / "1_Clip_de_Test.mp4").exists()
    assert (output_dir / "reels" / "1_Clip_de_Test.mp4").exists()
    assert (output_dir / "facebook" / "1_Clip_de_Test.mp4").exists()
    
    # Vérifier que leur taille est raisonnable (>10Ko)
    assert os.path.getsize(output_dir / "tiktok" / "1_Clip_de_Test.mp4") > 10240
