"""
Module d'effets sonores FFmpeg natifs (ear candy).
Tous les sons sont GÉNÉRÉS par FFmpeg via synthèse — aucun fichier .wav nécessaire.
Synchronisés avec l'energy_map du clip.
"""
import math


def build_audio_effects(duration, energy_map=None, hook_timestamp=0, climax_timestamp=None, clip_start=0):
    """
    Construit les filtres audio FFmpeg basés sur l'energy_map.
    Retourne un tuple (input_args, filter_parts) :
      - input_args : arguments -f lavfi pour les sources audio synthétiques
      - filter_parts : filtres audio à appliquer au mix final
    """
    if not energy_map:
        return [], []

    sfx_inputs = []  # Sources audio synthétiques additionnelles
    filter_parts = []  # Filtres pour le mix
    input_index = 1  # [0] est la vidéo/audio source

    # 1. WHOOSH au début (transition d'entrée)
    whoosh = _generate_whoosh(0.4)
    sfx_inputs.append(whoosh)
    filter_parts.append(f"[{input_index}:a]adelay=0|0,volume=0.3[whoosh];")
    input_index += 1

    # 2. BASS DROP au climax
    if climax_timestamp is not None:
        local_climax = max(0, climax_timestamp - clip_start)
        if local_climax > 0 and local_climax < duration - 1:
            bass = _generate_bass_drop(0.5)
            sfx_inputs.append(bass)
            delay_ms = int(local_climax * 1000)
            filter_parts.append(f"[{input_index}:a]adelay={delay_ms}|{delay_ms},volume=0.25[bass];")
            input_index += 1

    # 3. RISER avant le hook (si le hook n'est pas au tout début)
    if hook_timestamp is not None:
        local_hook = max(0, hook_timestamp - clip_start)
        if local_hook > 1.5:
            riser = _generate_riser(1.2)
            sfx_inputs.append(riser)
            riser_start_ms = int(max(0, (local_hook - 1.2)) * 1000)
            filter_parts.append(f"[{input_index}:a]adelay={riser_start_ms}|{riser_start_ms},volume=0.2[riser];")
            input_index += 1

    # 4. NOTIFICATION "ting" aux moments d'énergie 9-10
    ting_count = 0
    for i, energy in enumerate(energy_map):
        if energy >= 9 and ting_count < 3:  # Max 3 tings par clip
            t = i * 2  # 2s par chunk
            if t > 0 and t < duration - 1:
                ting = _generate_ting(0.2)
                sfx_inputs.append(ting)
                delay_ms = int(t * 1000)
                filter_parts.append(f"[{input_index}:a]adelay={delay_ms}|{delay_ms},volume=0.15[ting{ting_count}];")
                input_index += 1
                ting_count += 1

    return sfx_inputs, filter_parts


def build_mix_filter(num_sfx, duration):
    """
    Construit le filtre amix final pour mixer l'audio source avec les SFX.
    """
    if num_sfx == 0:
        return ""

    # Lister toutes les entrées audio
    labels = ["[0:a]"]
    sfx_labels = []
    
    # On nomme les SFX d'après leur ordre
    sfx_names = ["whoosh", "bass", "riser"] + [f"ting{i}" for i in range(10)]
    for i in range(num_sfx):
        label = sfx_names[i] if i < len(sfx_names) else f"sfx{i}"
        sfx_labels.append(f"[{label}]")

    all_labels = "".join(["[0:a]"] + sfx_labels)
    return f"{all_labels}amix=inputs={num_sfx + 1}:duration=first:dropout_transition=2[aout]"


def _generate_whoosh(duration=0.4):
    """
    Génère un son de whoosh (bruit filtré avec sweep fréquentiel).
    """
    return (
        f"-f lavfi -t {duration} "
        f"-i \"anoisesrc=d={duration}:c=pink:a=0.3,"
        f"bandpass=f=800:width_type=o:w=2,"
        f"afade=t=in:st=0:d=0.05,"
        f"afade=t=out:st={duration - 0.1}:d=0.1\""
    )


def _generate_bass_drop(duration=0.5):
    """
    Génère un impact basse (sine wave descendante 80Hz → 30Hz).
    """
    return (
        f"-f lavfi -t {duration} "
        f"-i \"sine=f=80:d={duration},"
        f"tremolo=f=10:d=0.5,"
        f"afade=t=in:st=0:d=0.02,"
        f"afade=t=out:st={duration - 0.15}:d=0.15,"
        f"lowpass=f=120\""
    )


def _generate_riser(duration=1.2):
    """
    Génère un son montant (bruit blanc avec sweep high-pass ascendant).
    """
    return (
        f"-f lavfi -t {duration} "
        f"-i \"anoisesrc=d={duration}:c=white:a=0.2,"
        f"highpass=f=200,"
        f"afade=t=in:st=0:d={duration * 0.8},"
        f"afade=t=out:st={duration - 0.1}:d=0.1\""
    )


def _generate_ting(duration=0.2):
    """
    Génère un son de notification court et brillant (sine haute fréquence).
    """
    return (
        f"-f lavfi -t {duration} "
        f"-i \"sine=f=2400:d={duration},"
        f"afade=t=in:st=0:d=0.01,"
        f"afade=t=out:st=0.05:d={duration - 0.05}\""
    )


def get_sfx_for_clip(clip_data, clip_start):
    """
    Interface principale : génère les inputs et filtres audio SFX
    pour un clip donné à partir de ses métadonnées.
    
    Retourne (sfx_input_args, filter_complex_parts, num_sfx).
    """
    duration = float(clip_data.get("end", 0)) - float(clip_data.get("start", 0))
    energy_map = clip_data.get("energy_map", [])
    hook_ts = clip_data.get("hook_timestamp")
    climax_ts = clip_data.get("climax_timestamp")

    sfx_inputs, filter_parts = build_audio_effects(
        duration, energy_map, hook_ts, climax_ts, clip_start
    )

    return sfx_inputs, filter_parts, len(sfx_inputs)
