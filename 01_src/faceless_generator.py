"""
faceless_generator.py — Autonomiczny Generator Wideo Faceless Channels
=======================================================================
Pipeline: Skrypt (GHOST v2) → Lektor (edge-tts) → B-Roll (Pexels API) → Montaż (MoviePy)

Wymagania (instalacja w venv na VM GCP):
    pip install edge-tts moviepy requests

Zmienne środowiskowe:
    PEXELS_API_KEY  — klucz API Pexels (darmowy)

Uruchomienie:
    python 01_src/faceless_generator.py
    lub jako webhook via FastAPI:
        import asyncio
        from 01_src.faceless_generator import run_faceless_pipeline
        asyncio.run(run_faceless_pipeline(script_text, keyword, output_path))
"""

import os
import asyncio
import requests
import logging
import tempfile
import urllib.parse
from pathlib import Path
from datetime import datetime

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    logging.warning("edge-tts nie jest zainstalowany. Uruchom: pip install edge-tts")

try:
    from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    logging.warning("MoviePy nie jest zainstalowany. Uruchom: pip install moviepy")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")
DEFAULT_VOICE = "pl-PL-MarekNeural"
OUTPUT_DIR = Path("generated_media")
OUTPUT_DIR.mkdir(exist_ok=True)



# ──────────────────────────────────────────────────────────────
# KROK 1: Generowanie Lektora (edge-tts) — DARMOWE
# ──────────────────────────────────────────────────────────────

async def generate_tts(text: str, output_path: str, voice: str = DEFAULT_VOICE, rate: str = "+10%") -> bool:
    """
    Generuje plik audio .mp3 z tekstu przy użyciu darmowego Microsoft Edge TTS.
    
    Args:
        text: Tekst do przeczytania (przetworzony przez GHOST v2).
        output_path: Ścieżka zapisu pliku .mp3.
        voice: Głos TTS (domyślnie: pl-PL-MarekNeural — dynamiczny, głęboki).
        rate: Tempo mowy, np. "+10%" przyspiesza.
    Returns:
        True jeśli sukces, False jeśli błąd.
    """
    if not EDGE_TTS_AVAILABLE:
        logger.error("edge-tts niedostępny. Zainstaluj: pip install edge-tts")
        return False
    
    try:
        logger.info(f"🎙️ Generowanie lektora TTS: {len(text)} znaków | Głos: {voice}")
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(output_path)
        logger.info(f"✅ Audio zapisane: {output_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Błąd TTS: {e}")
        return False


# ──────────────────────────────────────────────────────────────
# KROK 2: Pobieranie B-Roll (Pexels API) — DARMOWE
# ──────────────────────────────────────────────────────────────

def fetch_pexels_broll(query: str, output_path: str, orientation: str = "portrait") -> bool:
    """
    Pobiera pionowy klip B-Roll z darmowego API Pexels na podstawie słowa kluczowego.
    
    Args:
        query: Słowo kluczowe (np. "focused developer laptop").
        output_path: Ścieżka zapisu pliku .mp4.
        orientation: Orientacja wideo ('portrait' dla TikTok/Shorts, 'landscape' dla YouTube).
    Returns:
        True jeśli sukces, False jeśli błąd.
    """
    if not PEXELS_API_KEY:
        logger.error("❌ Brak PEXELS_API_KEY w zmiennych środowiskowych. Ustaw: export PEXELS_API_KEY=twoj_klucz")
        return False
    
    try:
        logger.info(f"🎬 Pobieranie B-Roll z Pexels: '{query}' ({orientation})")
        headers = {"Authorization": PEXELS_API_KEY}
        url = f"https://api.pexels.com/videos/search?query={query}&orientation={orientation}&size=medium&per_page=5"
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        videos = data.get("videos", [])
        if not videos:
            logger.warning(f"Brak wyników Pexels dla: '{query}'. Spróbuj ogólniejszego słowa kluczowego.")
            return False
        
        # Wybieramy pierwszy klip z rozdzielczością HD
        best_file = None
        for video_file in videos[0].get("video_files", []):
            if video_file.get("quality") in ["hd", "sd"]:
                best_file = video_file
                break
        
        if not best_file:
            best_file = videos[0]["video_files"][0]
        
        video_url = best_file["link"]
        logger.info(f"📥 Pobieranie: {video_url[:60]}...")
        
        video_response = requests.get(video_url, timeout=60, stream=True)
        video_response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in video_response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        logger.info(f"✅ B-Roll zapisany: {output_path}")
        return True
    
    except requests.exceptions.Timeout:
        logger.error("❌ Timeout pobierania wideo. Sprawdź połączenie sieciowe.")
        return False
    except Exception as e:
        logger.error(f"❌ Błąd Pexels API: {e}")
        return False


def fetch_pixabay_broll(query: str, output_path: str, orientation: str = "vertical") -> bool:
    """
    Pobiera pionowy klip B-Roll z darmowego API Pixabay na podstawie słowa kluczowego (fallback).
    
    Args:
        query: Słowo kluczowe (np. "focused developer").
        output_path: Ścieżka zapisu pliku .mp4.
        orientation: Orientacja wideo ('vertical' dla pionowych, 'horizontal' dla poziomych).
    Returns:
        True jeśli sukces, False jeśli błąd.
    """
    if not PIXABAY_API_KEY:
        logger.warning("⚠️ Brak PIXABAY_API_KEY w .env. Pomijam Pixabay fallback.")
        return False
        
    try:
        logger.info(f"🎬 Pobieranie B-Roll z Pixabay: '{query}' ({orientation})")
        # Pixabay przyjmuje 'vertical' zamiast 'portrait'
        pixabay_orientation = "vertical" if orientation in ["portrait", "vertical"] else "horizontal"
        
        url = f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&q={urllib.parse.quote(query)}&orientation={pixabay_orientation}&per_page=5"
        
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        hits = data.get("hits", [])
        if not hits:
            logger.warning(f"Brak wyników Pixabay dla: '{query}'")
            return False
            
        video_hit = hits[0]
        video_data = video_hit.get("videos", {})
        
        # Wybieramy medium, potem large, potem small
        selected_video = video_data.get("medium") or video_data.get("large") or video_data.get("small")
        if not selected_video:
            logger.warning("Brak odpowiedniego pliku wideo w hitach Pixabay.")
            return False
            
        video_url = selected_video["url"]
        logger.info(f"📥 Pobieranie z Pixabay: {video_url[:60]}...")
        
        video_response = requests.get(video_url, timeout=60, stream=True)
        video_response.raise_for_status()
        
        with open(output_path, "wb") as f:
            for chunk in video_response.iter_content(chunk_size=8192):
                f.write(chunk)
                
        logger.info(f"✅ B-Roll z Pixabay zapisany: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Błąd Pixabay API: {e}")
        return False


# ──────────────────────────────────────────────────────────────
# KROK 3: Montaż Wideo (MoviePy) — z nakładką napisu Hook
# ──────────────────────────────────────────────────────────────

def build_faceless_video(
    audio_path: str,
    video_path: str,
    output_path: str,
    hook_text: str,
    hook_duration: float = 3.0
) -> bool:
    """
    Montuje wideo Faceless: B-Roll + Audio (TTS) + napisy w pierwszych sekundach.
    
    Args:
        audio_path: Ścieżka do pliku .mp3 z lektorem.
        video_path: Ścieżka do pliku .mp4 z B-Roll.
        output_path: Ścieżka zapisu gotowego wideo.
        hook_text: Tekst napisu (Hook) wyświetlany w pierwszych sekundach.
        hook_duration: Czas wyświetlania napisu Hook (s).
    Returns:
        True jeśli sukces, False jeśli błąd.
    """
    if not MOVIEPY_AVAILABLE:
        logger.error("MoviePy niedostępny. Zainstaluj: pip install moviepy")
        return False
    
    try:
        logger.info("🎞️ Montaż wideo...")
        
        audio = AudioFileClip(audio_path)
        video = VideoFileClip(video_path)
        
        # Zapętl jeśli B-Roll jest krótszy niż lektor
        if video.duration < audio.duration:
            logger.info(f"Zapętlanie wideo (długość B-Roll: {video.duration:.1f}s < audio: {audio.duration:.1f}s)")
            video = video.loop(duration=audio.duration)
        
        video = video.subclip(0, audio.duration)
        video_with_audio = video.set_audio(audio)
        
        # Nakładka z Hookiem (pierwsze X sekund)
        txt_clip = (
            TextClip(
                hook_text,
                fontsize=60,
                color="white",
                bg_color="rgba(0,0,0,0.6)",
                font="Arial-Bold",
                size=(int(video.size[0] * 0.85), None),
                method="caption"
            )
            .set_position("center")
            .set_duration(hook_duration)
        )
        
        final = CompositeVideoClip([video_with_audio, txt_clip])
        
        logger.info(f"💾 Zapis wideo: {output_path}")
        final.write_videofile(
            output_path,
            fps=30,
            codec="libx264",
            audio_codec="aac",
            threads=4,
            logger=None  # wyłącz verbose MoviePy progress
        )
        
        audio.close()
        video.close()
        final.close()
        
        logger.info(f"✅ Wideo gotowe: {output_path}")
        return True
    
    except Exception as e:
        logger.error(f"❌ Błąd montażu wideo: {e}")
        return False


# ──────────────────────────────────────────────────────────────
# PIPELINE — Wywołanie liniowe (Linear Swarm)
# ──────────────────────────────────────────────────────────────

async def run_faceless_pipeline(
    script_text: str,
    hook_text: str,
    search_keyword: str,
    output_filename: str = None
) -> dict:
    """
    Pełny pipeline Faceless od skryptu do gotowego wideo .mp4.
    Zwraca słownik ze statusem i ścieżką wyjściową.
    
    Args:
        script_text: Gotowy tekst lektora (przetworzony przez GHOST v2).
        hook_text: Tekst napisu-haka (Hook) w pierwszych ~3 sekundach.
        search_keyword: Słowo kluczowe do wyszukania B-Roll w Pexels.
        output_filename: Nazwa pliku wyjściowego (opcjonalnie, auto-generowana z timestamp).
    Returns:
        {"status": "success"|"error", "output_path": str, "message": str}
    """
    if output_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"reel_{timestamp}.mp4"
    
    output_path = str(OUTPUT_DIR / output_filename)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "voice.mp3")
        video_path = os.path.join(tmpdir, "broll.mp4")
        
        # Krok 1: TTS
        tts_ok = await generate_tts(script_text, audio_path)
        if not tts_ok:
            return {"status": "error", "output_path": None, "message": "TTS generation failed"}
        
        # Krok 2: B-Roll (Pexels z fallbackiem do Pixabay)
        broll_ok = False
        if PEXELS_API_KEY:
            broll_ok = fetch_pexels_broll(search_keyword, video_path)
            
        if not broll_ok and PIXABAY_API_KEY:
            logger.info("⚠️ Pexels B-Roll nieudany lub brak klucza. Próba Pixabay fallback...")
            broll_ok = fetch_pixabay_broll(search_keyword, video_path)
            
        if not broll_ok:
            return {"status": "error", "output_path": None, "message": f"B-Roll not found in Pexels or Pixabay for: '{search_keyword}'"}
        
        # Krok 3: Montaż
        build_ok = build_faceless_video(audio_path, video_path, output_path, hook_text)
        if not build_ok:
            return {"status": "error", "output_path": None, "message": "Video assembly failed"}
    
    file_size_mb = round(os.path.getsize(output_path) / (1024 * 1024), 2)
    return {
        "status": "success",
        "output_path": output_path,
        "message": f"Wideo Faceless wygenerowane pomyślnie ({file_size_mb} MB)"
    }


# ──────────────────────────────────────────────────────────────
# PRZYKŁAD URUCHOMIENIA (test na lokalnym środowisku / VM GCP)
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Przykładowy skrypt (w produkcji: generowany przez CCO AI → filtr GHOST v2)
    SCRIPT = (
        "Znowu masz chaos w firmie? "
        "Weź się w garść. "
        "Zamiast testować setki aplikacji, wdróż jednego agenta AI. "
        "On ogarnie Twój CRM, maile i treści. "
        "Bez stresu. Bez przepłacania. "
        "Link w bio, jeśli chcesz wiedzieć jak."
    )
    HOOK = "Chaos w firmie? ➜ 1 agent = spokój"
    KEYWORD = "focused person working laptop coffee"
    OUTPUT = "test_reel.mp4"
    
    result = asyncio.run(run_faceless_pipeline(SCRIPT, HOOK, KEYWORD, OUTPUT))
    print(f"\n{'='*50}")
    print(f"STATUS:  {result['status'].upper()}")
    print(f"ŚCIEŻKA: {result['output_path']}")
    print(f"INFO:    {result['message']}")
    print(f"{'='*50}\n")
