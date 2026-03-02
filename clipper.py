from __future__ import annotations
from core.logger import get_logger
logger = get_logger(__name__)


import os
import json
import re
import subprocess
from typing import Any
import subtitle_generator
from core.config import settings


def _safe_filename(title: str) -> str:
    """Nettoie un titre pour en faire un nom de fichier safe.
    
    Args:
        title: Le titre brut.
        
    Returns:
        Le titre assaini, avec max 80 caractères.
    """
    title = title.replace(" ", "_")
    title = re.sub(r'[^\w\-]', '', title, flags=re.UNICODE)
    return title[:80] if title else "clip"


def _get_video_info(video_path: str) -> dict[str, int]:
    """Récupère les dimensions de la vidéo source.
    
    Args:
        video_path: Le chemin vers la vidéo.
        
    Returns:
        Un dictionnaire contenant les clés 'width' et 'height'.
    """
    try:
        cmd = [
            'ffprobe', '-v', 'quiet', '-print_format', 'json',
            '-show_streams', video_path
        ]
        probe = json.loads(subprocess.check_output(cmd))
        video_stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        return {
            'width': int(video_stream['width']),
            'height': int(video_stream['height']),
        }
    except Exception as e:
        logger.warning(f"   ⚠️ Impossible de lire les infos vidéo : {e}")
        return {'width': 1920, 'height': 1080}


def process_clips(
    video_path: str,
    json_path: str,
    transcription_path: str,
    output_dir: str = "downloads/clips",
    effects_plan: dict | None = None
) -> None:
    """Découpe la vidéo et génère les clips.
    
    Si `effects_plan` est fourni, génère 3 versions par clip (tiktok, reels, facebook).
    Sinon, génère un seul clip vertical classique.
    
    Args:
        video_path: Chemin vers la vidéo source.
        json_path: Chemin vers le JSON des moments viraux.
        transcription_path: Chemin vers le JSON de transcription complet.
        output_dir: Dossier de sortie des clips.
        effects_plan: Optionnel. Plan d'effets IA généré par Director.
    """
    if not os.path.exists(video_path):
        logger.error(f"❌ ERREUR : La vidéo source '{video_path}' est introuvable.")
        return

    if not os.path.exists(json_path):
        logger.error(f"❌ ERREUR : Le fichier descriptif '{json_path}' est introuvable.")
        return

    os.makedirs(output_dir, exist_ok=True)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    clips = data.get("clips", [])
    if not clips:
        logger.warning("⚠️ Aucun clip n'a été trouvé dans le fichier JSON.")
        return

    # Récupérer les dimensions de la vidéo source
    video_info = _get_video_info(video_path)
    src_w = video_info['width']
    src_h = video_info['height']

    # Déterminer les plateformes à générer depuis settings
    active_platforms = [p for p, conf in settings.platforms.items() if conf.enabled]
    platforms = active_platforms if effects_plan else ["default"]
    
    total = len(clips) * len(platforms)
    logger.info(f"🎬 Début du montage : {len(clips)} clips × {len(platforms)} plateforme(s) = {total} vidéos")

    tracker = _init_tracker()

    try:
        for i, clip in enumerate(clips):
            raw_title = clip.get("title", f"Clip_{i+1}")
            title = _safe_filename(raw_title)
            start_time = float(clip.get("start", 0))
            end_time = float(clip.get("end", 0))
            duration = end_time - start_time

            if duration <= 0:
                logger.warning(f"   ⚠️ Clip {i+1} ignoré (durée invalide)")
                continue

            logger.info(f"\n✂️  Clip {i+1}: {raw_title} ({duration:.1f}s)")

            # Face tracking — position moyenne du visage (UNE SEULE FOIS par clip)
            face_x_center = _get_face_center(tracker, video_path, start_time, end_time)

            # Récupérer le plan d'effets pour ce clip
            clip_effects = _get_clip_effects(effects_plan, i + 1)

            for platform in platforms:
                _render_clip(
                    video_path, start_time, duration, raw_title, title, i,
                    face_x_center, transcription_path, output_dir,
                    platform, clip_effects, src_w, src_h, clip
                )
    finally:
        # Libérer les ressources MediaPipe après le rendu de tous les clips
        if tracker:
            tracker.close()
            logger.info("🧹 Face tracker libéré.")


def _render_clip(
    video_path: str,
    start_time: float,
    duration: float,
    raw_title: str,
    title: str,
    clip_index: int,
    face_x_center: float,
    transcription_path: str,
    output_dir: str,
    platform: str,
    clip_effects: dict | None,
    src_w: int,
    src_h: int,
    clip_data: dict | None = None
) -> None:
    """Rend un clip pour une plateforme donnée avec les effets visuels et ear candy."""

    # === Dimensions de sortie ===
    out_w, out_h, output_file = _prepare_output_path(output_dir, platform, clip_index, title)

    # === Construction des filtres ===
    vf_parts, af_parts = _build_video_filters(
        platform, duration, start_time, face_x_center, src_w, src_h, out_w, out_h, clip_effects, clip_data
    )

    # 5. SOUS-TITRES (+ Titre Part X)
    ass_filename = os.path.join(output_dir, f"temp_{clip_index}_{platform}.ass")
    end_time = start_time + duration
    has_subtitles = subtitle_generator.generate_ass_for_clip(
        transcription_path, start_time, end_time, ass_filename, title=raw_title
    )

    # === Commande FFmpeg ===
    vf_string = ",".join(vf_parts)

    # Si on a des sous-titres, on utilise filter_complex pour plus de fiabilité
    if has_subtitles:
        # Échapper les chemins dans les filtres ASS
        ass_escaped = ass_filename.replace("\\", "/").replace(":", "\\:")
        vf_string += f",ass='{ass_escaped}'"

    command = [
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-i", video_path,
        "-t", str(duration),
        "-vf", vf_string,
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-pix_fmt", "yuv420p",
    ]

    if af_parts:
        command.extend(["-af", ",".join(af_parts)])

    command.extend([
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        output_file
    ])

    platform_label = f" [{platform}]" if platform != "default" else ""
    try:
        result = subprocess.run(
            command, check=True,
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
        )
        # Validation : vérifier que le fichier existe et fait > 10 Ko
        if os.path.exists(output_file) and os.path.getsize(output_file) > 10240:
            logger.info(f"   ✅ Clip {clip_index+1}{platform_label} → {output_file}")
        else:
            logger.error(f"   ❌ Clip {clip_index+1}{platform_label} — fichier corrompu (trop petit)")
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode('utf-8', errors='replace') if e.stderr else ''
        # Afficher les 3 dernières lignes d'erreur pour le debug
        error_lines = [l for l in stderr.strip().split('\n') if l.strip()]
        error_summary = '\n'.join(error_lines[-3:]) if error_lines else 'Erreur inconnue'
        logger.error(f"   ❌ Erreur FFmpeg{platform_label}:")
        logger.info(f"      {error_summary}")

        # Fallback : essayer sans les effets
        if clip_effects:
            logger.info(f"   🔄 Retry sans effets...")
            _render_fallback(video_path, start_time, duration, output_file,
                             face_x_center, src_w, src_h, out_w, out_h)
    finally:
        # Nettoyage fichiers temporaires
        if has_subtitles and os.path.exists(ass_filename):
            os.remove(ass_filename)


def _get_face_center(tracker: Any, video_path: str, start_time: float, end_time: float) -> float:
    """Récupère la position moyenne (x) du visage."""
    if not tracker:
        return 0.5
    logger.info("   🔍 Face tracking...")
    tracking_data = tracker.get_tracking_data(video_path, start_time, end_time)
    if tracking_data:
        face_x_center = sum(x for _, x in tracking_data) / len(tracking_data)
        face_x_center = max(0.2, min(0.8, face_x_center))
        logger.info(f"   ✅ Visage détecté à X={face_x_center:.2f}")
        return face_x_center
    return 0.5


def _prepare_output_path(output_dir: str, platform: str, clip_index: int, title: str) -> tuple[int, int, str]:
    if platform == "default":
        return 1080, 1920, os.path.join(output_dir, f"{clip_index+1}_{title}.mp4")
        
    platform_dir = os.path.join(output_dir, platform)
    os.makedirs(platform_dir, exist_ok=True)
    output_file = os.path.join(platform_dir, f"{clip_index+1}_{title}.mp4")
    
    platform_config = settings.platforms.get(platform)
    if platform_config and hasattr(platform_config, "resolution"):
        w_str, h_str = platform_config.resolution.split("x")
        return int(w_str), int(h_str), output_file
        
    if platform == "facebook":
        return 1080, 1350, output_file
    return 1080, 1920, output_file


def _build_video_filters(platform: str, duration: float, start_time: float, face_x_center: float, src_w: int, src_h: int, out_w: int, out_h: int, clip_effects: dict | None, clip_data: dict | None) -> tuple[list[str], list[str]]:
    vf_parts, af_parts = [], ["loudnorm=I=-14:TP=-1:LRA=11"]

    aspect = out_w / out_h
    crop_w = int(src_h * aspect)
    if crop_w > src_w:
        crop_w = src_w
    crop_x = max(0, min(int(face_x_center * src_w - crop_w / 2), src_w - crop_w))
    vf_parts.extend([f"crop={crop_w}:{src_h}:{crop_x}:0", f"scale={out_w}:{out_h}"])

    if clip_effects and platform != "default":
        from effects_director import get_color_filter_vf, get_ffmpeg_filters
        color_vf = get_color_filter_vf(clip_effects, platform, 0)
        if color_vf:
            vf_parts.append(_tone_down_color(color_vf))
            
        _, extra_af = get_ffmpeg_filters(clip_effects, platform)
        af_parts.extend(extra_af)

        platform_plan = clip_effects.get("platforms", {}).get(platform, {})
        if platform_plan.get("transition") == "fade":
            fade_dur = min(0.3, duration / 6)
            vf_parts.extend([f"fade=in:0:d={fade_dur}", f"fade=out:st={duration - fade_dur}:d={fade_dur}"])
            af_parts.extend([f"afade=t=in:st=0:d={fade_dur}", f"afade=t=out:st={duration - fade_dur}:d={fade_dur}"])

    if clip_data and clip_data.get("energy_map"):
        try:
            from effects_visual import get_effects_for_clip
            visual_fx = get_effects_for_clip(clip_data, start_time)
            vf_parts.extend(visual_fx)
            if visual_fx:
                logger.info(f"   🎬 {len(visual_fx)} effets visuels appliqués")
        except Exception as e:
            logger.warning(f"   ⚠️ Effets visuels ignorés : {e}")

    vf_parts.append("eq=brightness=0.08:enable='between(t,0,0.1)'")
    return vf_parts, af_parts


def _render_fallback(
    video_path: str, start_time: float, duration: float, output_file: str,
    face_x_center: float, src_w: int, src_h: int, out_w: int, out_h: int
) -> None:
    """Rendu de secours sans effets — vidéo simple mais lisible."""
    aspect = out_w / out_h
    crop_w = int(src_h * aspect)
    if crop_w > src_w: crop_w = src_w
    crop_x = max(0, min(int(face_x_center * src_w - crop_w / 2), src_w - crop_w))

    vf = f"crop={crop_w}:{src_h}:{crop_x}:0,scale={out_w}:{out_h}"
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(start_time),
        "-i", video_path,
        "-t", str(duration),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        output_file
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        if os.path.exists(output_file) and os.path.getsize(output_file) > 10240:
            logger.info(f"   ✅ Fallback réussi → {output_file}")
        else:
            logger.error(f"   ❌ Fallback échoué — fichier corrompu")
    except subprocess.CalledProcessError:
        logger.error(f"   ❌ Fallback FFmpeg échoué également")


def _tone_down_color(color_vf: str) -> str:
    """Réduit l'agressivité du color grading pour éviter les vidéos surexposées.
    Utilise les limites définies dans settings.yaml.
    """
    import re
    max_sat = settings.video.max_saturation
    max_cont = settings.video.max_contrast

    # Limiter saturation
    color_vf = re.sub(r'saturation=([0-9.]+)', 
                     lambda m: f"saturation={min(float(m.group(1)), max_sat)}", color_vf)
    # Limiter contrast
    color_vf = re.sub(r'contrast=([0-9.]+)', 
                     lambda m: f"contrast={min(float(m.group(1)), max_cont)}", color_vf)
    # Limiter brightness
    color_vf = re.sub(r'brightness=(-?\d+\.?\d*)', lambda m: f"brightness={max(-0.03, min(float(m.group(1)), 0.03))}", color_vf)
    return color_vf


def _init_tracker() -> Any:
    if not settings.video.face_tracking: return None
    try:
        from face_tracker import FaceTracker
        return FaceTracker()
    except ImportError:
        logger.warning("⚠️  MediaPipe non disponible — face tracking désactivé.")
        return None

def _get_clip_effects(effects_plan: dict | None, clip_index: int) -> dict | None:
    if not effects_plan: return None
    for ec in effects_plan.get("clips", []):
        if ec.get("clip_index") == clip_index:
            return ec
    return None

if __name__ == "__main__":
    SOURCE_VIDEO = "downloads/dQw4w9WgXcQ.mp4"
    MOMENTS_JSON = "downloads/viral_moments.json"
    TRANSCRIPTION_JSON = "downloads/transcription.json"

    logger.info("--- Démarrage du module Clipper (FFmpeg) ---")
    process_clips(SOURCE_VIDEO, MOMENTS_JSON, TRANSCRIPTION_JSON)
