from __future__ import annotations
from core.logger import get_logger
logger = get_logger(__name__)


import mediapipe as mp
import numpy as np
import os
import subprocess
import json

class FaceTracker:
    def __init__(self, min_detection_confidence: float = 0.5) -> None:
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(
            model_selection=1, # 1 pour les visages à plus de 2 mètres, 0 pour les proches
            min_detection_confidence=min_detection_confidence
        )

    def __enter__(self) -> FaceTracker:
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()

    def close(self) -> None:
        """Libère les ressources MediaPipe pour éviter les fuites mémoire."""
        if hasattr(self, 'face_detection') and self.face_detection:
            self.face_detection.close()
            self.face_detection = None

    def get_tracking_data(self, video_path: str, start_time: float, end_time: float, sample_rate: int = 5) -> list[tuple[float, float]]:
        """Analyse la vidéo entre start_time et end_time pour tracker le visage.
        
        Args:
            video_path: Chemin vers la vidéo source.
            start_time: Temps de début en secondes.
            end_time: Temps de fin en secondes.
            sample_rate: Nombre de frames analysées par seconde.
            
        Returns:
            Une liste de tuples (timestamp, position_x_lissée).
        """
        if not os.path.exists(video_path):
            logger.info(f"Erreur : Vidéo non trouvée {video_path}")
            return []

        try:
            probe_cmd = [
                'ffprobe', '-v', 'quiet', '-print_format', 'json', 
                '-show_streams', '-show_format', video_path
            ]
            probe = json.loads(subprocess.check_output(probe_cmd))
            video_stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            fps_str = video_stream['r_frame_rate']
            if '/' in fps_str:
                num, den = fps_str.split('/')
                fps = int(num) / int(den)
            else:
                fps = float(fps_str)
        except (subprocess.CalledProcessError, StopIteration, KeyError, ValueError) as e:
            logger.warning(f"   ⚠️ Impossible de lire les métadonnées vidéo : {e}")
            return []
        
        # On calcule la commande FFmpeg pour extraire les frames brutes (rawvideo)
        # On réduit la résolution pour accélérer la détection MediaPipe
        target_width = 640
        target_height = int(height * (target_width / width))
        
        ffmpeg_cmd = [
            'ffmpeg',
            '-ss', str(start_time),
            '-t', str(end_time - start_time),
            '-i', video_path,
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            '-vcodec', 'rawvideo',
            '-vf', f'scale={target_width}:{target_height}',
            '-loglevel', 'quiet',
            '-'
        ]
        
        process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**8)
        
        raw_x_coords = []
        timestamps = []
        
        frame_size = target_width * target_height * 3
        frame_count = 0
        
        while True:
            if process.stdout is None:
                break
            in_bytes = process.stdout.read(frame_size)
            if not in_bytes or len(in_bytes) != frame_size:
                break
            
            if frame_count % sample_rate == 0:
                frame = np.frombuffer(in_bytes, np.uint8).reshape((target_height, target_width, 3))
                results = self.face_detection.process(frame)
                
                if results.detections:
                    detection = results.detections[0]
                    bbox = detection.location_data.relative_bounding_box
                    center_x = bbox.xmin + (bbox.width / 2)
                    raw_x_coords.append(center_x)
                else:
                    last_val = raw_x_coords[-1] if raw_x_coords else 0.5
                    raw_x_coords.append(last_val)
                
                timestamps.append(start_time + (frame_count / fps))
                
            frame_count += 1
            
        if process.stdout is not None:
            process.stdout.close()
        process.wait()
        
        if not raw_x_coords:
            return []
            
        # Lissage par moyenne mobile
        window_size = 15 # Taille de la fenêtre de lissage
        smoothed_x = self._smooth_coordinates(raw_x_coords, window_size)
        
        # Décimation : On ne garde qu'un point par seconde environ pour FFmpeg
        # (Sinon l'expression devient trop longue pour le shell/FFmpeg)
        final_data = [] # type: list[tuple[float, float]]
        last_added_ts: float = -1.0
        for ts, x in zip(timestamps, smoothed_x):
            if ts >= last_added_ts + 0.8: # On prend un point toutes les 0.8s
                final_data.append((ts, x))
                last_added_ts = ts
                
        return final_data

    def _smooth_coordinates(self, coords: list[float], window_size: int) -> list[float]:
        """Applique une moyenne mobile pour éviter les saccades.
        
        Args:
            coords: Liste de coordonnées X (0.0 - 1.0).
            window_size: Taille de la fenêtre mobile.
            
        Returns:
            Liste des coordonnées lissées.
        """
        if len(coords) < window_size:
            return coords
            
        smoothed = np.convolve(coords, np.ones(window_size)/window_size, mode='same')
        # Gérer les bords du convolve qui peuvent être imprécis
        for i in range(window_size // 2):
            smoothed[i] = coords[i]
            smoothed[-(i+1)] = coords[-(i+1)]
            
        return smoothed.tolist()

if __name__ == "__main__":
    # Script de test rapide
    tracker = FaceTracker()
    test_video = "downloads/_dUxqxVoqM4.mp4" 
    if os.path.exists(test_video):
        logger.info(f"Test de tracking sur {test_video}...")
        try:
            data = tracker.get_tracking_data(test_video, 10, 15)
            if data:
                logger.info(f"✅ Succès ! {len(data)} points de tracking générés.")
                for ts, x in data[:10]:
                    logger.info(f"  [{ts:.2f}s] X = {x:.4f}")
            else:
                logger.error("❌ Aucun visage détecté ou erreur de lecture.")
        except Exception as e:
            logger.error(f"❌ Erreur pendant le tracking : {e}")
    else:
        logger.info("Vidéo de test non trouvée.")
