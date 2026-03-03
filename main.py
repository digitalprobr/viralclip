from core.logger import get_logger
logger = get_logger(__name__)

import os
import sys
import argparse
from dotenv import load_dotenv

import downloader
import transcriber
import analyzer
import effects_director
import clipper
import seo_generator

import re

def _sanitize_title(title, default="video_clips"):
    """Nettoie un titre pour en faire un nom de dossier safe."""
    if not title:
        return default
    title = title.replace(" ", "_").replace("/", "_").replace("\\", "_")
    title = re.sub(r'[^\w\-]', '', title, flags=re.UNICODE)
    return title[:100] if title else default

def _sanitize_video_id(video_path):
    """Extrait un identifiant unique depuis le chemin vidéo."""
    return os.path.splitext(os.path.basename(video_path))[0]

def _parse_args():
    """Parse les arguments de la ligne de commande."""
    parser = argparse.ArgumentParser(
        description="🚀 Pipeline de Clipping Multi-Plateforme",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
  python main.py "https://youtube.com/watch?v=xxx"                  # Priorité par défaut (Gemini)
  python main.py "https://youtube.com/watch?v=xxx" --engine qwen    # Forcer Alibaba Qwen
  python main.py "https://youtube.com/watch?v=xxx" --engine deepseek # Forcer DeepSeek
  python main.py "https://youtube.com/watch?v=xxx" --engine groq    # Forcer Groq Llama
  python main.py "https://youtube.com/watch?v=xxx" --engine gemini  # Forcer Gemini (défaut)
  python main.py "https://youtube.com/watch?v=xxx" --engine auto    # Auto-fallback intelligent
        """
    )
    parser.add_argument("url", help="URL de la vidéo YouTube à traiter")
    parser.add_argument(
        "--engine", "-e",
        choices=["auto", "gemini", "deepseek", "qwen", "groq"],
        default="auto",
        help="Moteur IA à utiliser en priorité (défaut: auto = Gemini → DeepSeek → Qwen → Groq)"
    )
    parser.add_argument(
        "--clips", "-c",
        type=int,
        default=None,
        help="Nombre exact de clips à extraire (surcharge la configuration settings.yaml)"
    )
    return parser.parse_args()

def main():
    logger.info("=====================================================")
    logger.info("🚀 Pipeline de Clipping Multi-Plateforme 🚀")
    logger.info("=====================================================")
    
    # 0. Charger l'environnement
    load_dotenv(dotenv_path="/app/.env", override=True)
    
    args = _parse_args()
    url = args.url
    
    from core.config import settings
    preferred_engine = args.engine if args.engine != "auto" else settings.pipeline.engine

    groq_api_key = os.getenv("GROQ_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    alibaba_api_key = os.getenv("ALIBABA_API_KEY")
    
    if not any([groq_api_key, gemini_api_key, deepseek_api_key, alibaba_api_key]):
        logger.error("❌ ERREUR: Aucune clé API configurée (GEMINI / DEEPSEEK / ALIBABA / GROQ)")
        logger.info("   Au moins une clé est nécessaire pour l'analyse et le SEO.")
        return
    
    # Affichage des APIs disponibles
    api_status = {
        "gemini": ("Gemini 2.0 Flash", gemini_api_key),
        "deepseek": ("DeepSeek V3", deepseek_api_key),
        "qwen": ("Alibaba Qwen Plus", alibaba_api_key),
        "groq": ("Groq Llama 3.3", groq_api_key),
    }
    
    for key, (name, api_key) in api_status.items():
        if api_key:
            marker = "🎯" if preferred_engine == key else "✅"
            logger.info(f"   {marker} {name} {'(MOTEUR FORCÉ)' if preferred_engine == key else ''}")
        else:
            logger.warning(f"   ⚠️  {name} — clé absente")
    
    if preferred_engine != "auto":
        logger.info(f"\n   🔧 Mode : --engine {preferred_engine} (moteur forcé)")
    else:
        logger.info(f"\n   🔧 Mode : auto (fallback intelligent)")
    
    if not groq_api_key:
        logger.warning("   ⚠️  GROQ_API_KEY absente — transcription via Whisper local (plus lent)")

    # ================================================
    # EXÉCUTION DU PIPELINE AVEC GESTION D'ERREUR
    # ================================================
    try:
        result = run_pipeline(url, preferred_engine, args.clips)
        
        # RÉSUMÉ FINAL
        logger.info("\n=====================================================")
        logger.info("🌈 PIPELINE TERMINÉ AVEC SUCCÈS !")
        logger.info(f"   📁 Clips      → {result['clips_dir']}/")
        if result['effects_plan_used']:
            logger.info(f"   🎬 TikTok     → {result['clips_dir']}/tiktok/")
            logger.info(f"   🎬 Reels      → {result['clips_dir']}/reels/")
            logger.info(f"   🎬 Facebook   → {result['clips_dir']}/facebook/")
        if result['seo_result']:
            logger.info(f"   📄 SEO Généré avec succès")
            _print_seo_summary(result['seo_result'])
        logger.info("=====================================================")
        
    except KeyboardInterrupt:
        logger.warning("\n\n⚠️ Interruption par l'utilisateur. Arrêt du pipeline.")
        sys.exit(1)
    except Exception as e:
        import traceback
        logger.info("\n=====================================================")
        logger.error("💥 ERREUR CRITIQUE")
        logger.info("=====================================================")
        logger.info(f"Une erreur inattendue a bloqué le pipeline : {e}")
        logger.info("\nDétails techniques pour debug :")
        traceback.print_exc(file=sys.stdout)
        logger.info("=====================================================")
        sys.exit(1)

def run_pipeline(url: str, preferred_engine: str = "auto", num_clips: int | None = None, platforms: dict | None = None) -> dict:
    """Exécute le pipeline complet de clipping (utilisable via CLI ou Celery)."""
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    logger.info(f"\n[ÉTAPE 1/6] 📥 Téléchargement de la vidéo : {url}")
    
    video_metadata = downloader.get_video_metadata(url)
    if video_metadata:
        logger.info(f"   📊 Métadonnées récupérées : \"{video_metadata.get('title', '')}\"")
    
    video_file = downloader.download_video(url)
    if not video_file:
        raise RuntimeError("Fin prématurée suite à une erreur de téléchargement.")
        
    audio_file = downloader.extract_audio(video_file)
    if not audio_file:
        raise RuntimeError("Fin prématurée suite à une erreur d'extraction audio.")

    video_title = video_metadata.get('title', 'video') if video_metadata else 'video'
    safe_folder_name = _sanitize_title(video_title)
    
    video_id = _sanitize_video_id(video_file)
    base_output_dir = f"downloads/{safe_folder_name}"
    os.makedirs(base_output_dir, exist_ok=True)
    
    transcription_json = f"{base_output_dir}/{video_id}_transcription.json"
    viral_json = f"{base_output_dir}/{video_id}_viral_moments.json"
    effects_json = f"{base_output_dir}/{video_id}_effects.json"
    seo_json = f"{base_output_dir}/{video_id}_seo.json"
    clips_dir = base_output_dir

    engine = "Groq Whisper" if groq_api_key else "Whisper Local"
    logger.info(f"\n[ÉTAPE 2/6] 📝 Transcription audio ({engine})")
    transcription = transcriber.transcribe_audio(audio_file, groq_api_key, transcription_json)
    if not transcription:
        raise RuntimeError("Fin prématurée suite à une erreur de transcription.")

    logger.info(f"\n[ÉTAPE 3/6] 🧠 Analyse des moments viraux (moteur: {preferred_engine})")
    analysis = analyzer.analyze_transcription(
        transcription_json, 
        viral_json, 
        preferred_engine=preferred_engine,
        num_clips=num_clips
    )
    if not analysis:
        raise RuntimeError("Fin prématurée suite à une erreur d'analyse IA.")

    logger.info(f"\n[ÉTAPE 4/6] 🎨 Sélection des effets par plateforme (moteur: {preferred_engine})")
    effects_plan = effects_director.generate_effects_plan(viral_json, effects_json, preferred_engine=preferred_engine)

    n_clips = len(analysis.get("clips", []))
    
    # --- DISTRIBUTION DES PLATEFORMES ---
    if platforms and effects_plan:
        distribution = []
        for p, count in platforms.items():
            if count and count > 0:
                if p == "shorts": p = "youtube" # Mapper noms frontend vers backend si nécessaire
                if p == "instagram": p = "reels" # Mapper noms frontend vers backend
                distribution.extend([p] * count)
        
        # Filtre le plan d'effets pour assigner une seule plateforme par clip
        for i, clip in enumerate(effects_plan.get("clips", [])):
            if i < len(distribution):
                target_p = distribution[i]
                orig_platforms = clip.get("platforms", {})
                clip["platforms"] = {target_p: orig_platforms.get(target_p, {})}
                logger.info(f"   🎯 Clip {i+1} assigné exclusivement à: {target_p}")
            else:
                 # S'il y a plus de clips que demandé, on vide les plateformes ou on garde le premier
                 if len(distribution) > 0:
                     target_p = distribution[-1]
                     clip["platforms"] = {target_p: clip.get("platforms", {}).get(target_p, {})}
                 else:
                     clip["platforms"] = {} # Exclure du rendu multiformat

    n_platforms = 3 if effects_plan and not platforms else (len(platforms) if platforms else 1)
    logger.info(f"\n[ÉTAPE 5/6] ✂️ Montage ({n_clips} clips)")
    clipper.process_clips(video_file, viral_json, transcription_json, clips_dir, effects_plan)

    logger.info(f"\n[ÉTAPE 6/6] 🔍 Génération des descriptions SEO (moteur: {preferred_engine})")
    seo_result = seo_generator.generate_seo(url, video_metadata, viral_json, transcription_json, seo_json, clips_dir, preferred_engine=preferred_engine)
    
    return {
        "status": "success",
        "clips_dir": clips_dir,
        "effects_plan_used": bool(effects_plan),
        "seo_generated": bool(seo_result),
        "analysis": analysis,
        "seo_result": seo_result
    }

def _print_seo_summary(seo_data):
    """Affiche un résumé des descriptions SEO générées."""
    for clip in seo_data.get("clips", []):
        idx = clip.get("clip_index", "?")
        title = clip.get("original_title", "")
        logger.info(f"\n   📋 Clip {idx}: {title}")
        for platform in ["tiktok", "reels", "facebook"]:
            p_data = clip.get("platforms", {}).get(platform, {})
            desc = p_data.get("description", "")[:60]
            tags = p_data.get("hashtags", "")
            logger.info(f"      {platform:8s} → {desc}... {tags}")

if __name__ == "__main__":
    main()
