import os
import json
import re


def format_time_ass(seconds: float) -> str:
    """Convertit des secondes en format ASS (H:MM:SS.CC).
    
    Args:
        seconds: Durée en secondes.
        
    Returns:
        Chaîne de caractères au format ASS.
    """
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds % 1) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def chunk_text(text: str, max_chars: int = 35) -> list[str]:
    """Découpe un texte en morceaux respectant une longueur maximale.
    
    Préserve les mots entiers si possible.
    
    Args:
        text: Texte à découper.
        max_chars: Longueur maximale d'un morceau.
        
    Returns:
        Liste des morceaux de texte.
    """
    words = text.split()
    chunks = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if len(test) <= max_chars:
            current = test
        else:
            if current:
                chunks.append(current)
            current = word
    if current:
        chunks.append(current)
    return chunks if chunks else [text[:max_chars]]


def generate_ass_for_clip(
    transcription_path: str,
    clip_start: float,
    clip_end: float,
    output_ass_path: str,
    title: str = ""
) -> bool:
    """Génère un fichier de sous-titres ASS pour un clip donné.
    
    Args:
        transcription_path: Chemin vers le JSON de transcription complet.
        clip_start: Temps de début du clip en secondes.
        clip_end: Temps de fin du clip en secondes.
        output_ass_path: Chemin du fichier ASS à générer.
        title: Titre "Part X" optionnel à afficher en permanence.
        
    Returns:
        True si des sous-titres ont été générés, False sinon.
    """
    if not os.path.exists(transcription_path):
        return False

    with open(transcription_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    segments = data.get("segments", [])

    # En-tête ASS pour une vidéo verticale 1080x1920
    # Default : sous-titres en bas, fond semi-transparent, bordure épaisse
    # Title : titre "PART X" en haut de l'écran
    ass_content = "[Script Info]\n"
    ass_content += "ScriptType: v4.00+\n"
    ass_content += "PlayResX: 1080\n"
    ass_content += "PlayResY: 1920\n"
    ass_content += "\n"
    ass_content += "[V4+ Styles]\n"
    ass_content += "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    # Default: Impact, blanc de base, box background noir semi-transparent
    # BorderStyle=3 (Opaque Box), Outline=12 (Padding de la box)
    ass_content += "Style: Default,Impact,100,&H00FFFFFF,&H000000FF,&H80000000,&H80000000,-1,0,0,0,100,100,0,0,3,12,0,2,40,40,520,1\n"
    # Title: blanc, bordure noire, box style, centré en haut
    # MarginV=300 → titre à Y≈300 (safe zone, au-dessous de la zone danger Y=0-250)
    ass_content += "Style: Title,Arial,90,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,3,8,0,8,40,40,300,1\n"
    ass_content += "\n"
    ass_content += "[Events]\n"
    ass_content += "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    has_text = False

    # Extraction de "Part X" du titre si présent
    part_match = re.search(r"^(Part \d+)", title, re.IGNORECASE)
    if part_match:
        part_text = part_match.group(1).upper()
        ass_start = "0:00:00.00"
        ass_end = format_time_ass(clip_end - clip_start)
        # Titre permanent en haut — texte simple sans tags de formatage
        ass_content += f"Dialogue: 0,{ass_start},{ass_end},Title,,0,0,0,,{part_text}\n"
        has_text = True

    # Sous-titres principaux
    for seg in segments:
        seg_start = float(seg.get("start", 0))
        seg_end = float(seg.get("end", 0))
        text = seg.get("text", "").strip()

        if not text or seg_end <= clip_start or seg_start >= clip_end:
            continue

        # Ajuster au clip
        local_start = max(0, seg_start - clip_start)
        local_end = min(clip_end - clip_start, seg_end - clip_start)

        if local_end <= local_start:
            continue

        # Découper les textes longs — Hormozi-style (2-3 mots max par écran)
        chunks = chunk_text(text.upper(), max_chars=15)
        chunk_duration = (local_end - local_start) / len(chunks)

        for j, chunk in enumerate(chunks):
            chunk_start = local_start + j * chunk_duration
            chunk_end = chunk_start + chunk_duration
            clean_chunk = chunk.replace("\\", "").replace("{", "").replace("}", "")
            words = clean_chunk.split()
            
            if not words:
                continue
                
            word_duration = (chunk_end - chunk_start) / len(words)
            
            # Animation dynamique mot par mot (Hormozi style)
            for w_idx, word in enumerate(words):
                w_start = chunk_start + w_idx * word_duration
                w_end = chunk_start + (w_idx + 1) * word_duration
                ass_start = format_time_ass(w_start)
                ass_end = format_time_ass(w_end)
                
                styled_words = []
                for i, w in enumerate(words):
                    if i == w_idx:
                        # Le mot en cours de prononciation est surligné en JAUNE vif (\c&H00FFFF&) et légèrement plus gros
                        styled_words.append(f"{{\\c&H00FFFF&\\fs110}}{w}{{\\c&HFFFFFF&\\fs100}}")
                    else:
                        styled_words.append(w)
                
                line = " ".join(styled_words)
                ass_content += f"Dialogue: 0,{ass_start},{ass_end},Default,,0,0,0,,{line}\n"
                has_text = True

    if not has_text:
        return False

    with open(output_ass_path, "w", encoding="utf-8") as f:
        f.write(ass_content)

    return True
