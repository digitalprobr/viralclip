"""
Module d'effets visuels FFmpeg natifs pour VIDÉO (pas de zoompan — c'est pour les photos).
Tous les effets sont des expressions FFmpeg compatibles avec la vidéo en mouvement.
Synchronisés avec l'energy_map du clip (intensité 1-10 par tranche de 2s).
"""


def build_visual_effects(duration, energy_map=None, hook_timestamp=0, climax_timestamp=None):
    """
    Construit les filtres FFmpeg visuels basés sur l'energy_map du clip.
    Retourne une liste de strings de filtres vidéo FFmpeg.
    
    IMPORTANT : Tous les filtres ici sont VIDEO-SAFE (pas de zoompan).
    """
    if not energy_map:
        return []

    vf_parts = []
    avg_energy = sum(energy_map) / len(energy_map)

    # 1. ZOOM vidéo-safe via scale+crop (léger, basé sur l'énergie moyenne)
    if avg_energy >= 6:
        zoom = 1.04 if avg_energy >= 8 else 1.02
        # Scale up slightly, then crop to center → subtle zoom effect
        # Force exact output resolution to avoid 1078 instead of 1080
        vf_parts.append(
            f"scale=iw*{zoom}:ih*{zoom},"
            f"crop=iw/{zoom}:ih/{zoom},"
            f"scale=1080:1920:force_original_aspect_ratio=disable"
        )

    # 2. VIGNETTE douce (focus sur le sujet)
    vf_parts.append("vignette=PI/5")

    return vf_parts


def get_effects_for_clip(clip_data, clip_start):
    """
    Interface principale : génère la liste complète des filtres visuels
    pour un clip donné à partir de ses métadonnées (energy_map, timestamps).
    """
    effects = []
    duration = float(clip_data.get("end", 0)) - float(clip_data.get("start", 0))
    energy_map = clip_data.get("energy_map", [])
    hook_ts = clip_data.get("hook_timestamp")
    climax_ts = clip_data.get("climax_timestamp")

    visual_parts = build_visual_effects(duration, energy_map, hook_ts, climax_ts)
    effects.extend(visual_parts)

    return effects
