"""
================================================================================
  UNIVERSAL ELMS.PL / WEB2LEARN INTELLIGENCE SCRAPER (v6.0)
================================================================================
  Dla platform: Piotr Łotowski / EasyLMS (elms.pl) / Web2Learn / BunnyCDN / Vimeo
  Stack: Playwright (Chromium) + Netscape Cookies + faster-whisper (medium/int8/VAD)
================================================================================
"""

import sys
import os
import re
import time
import json
import shutil
import urllib.request
import zipfile
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Wymagane pakiety: pip install playwright yt-dlp faster-whisper python-dotenv imageio-ffmpeg")
    print("Wykonaj też: python -m playwright install chromium")
    sys.exit(1)

# ==============================================================================
# ⚙️ USTAWIENIA DLA KURSÓW PIOTRA ŁOTOWSKIEGO (ELMS.PL)
# ==============================================================================
LOGIN_URL    = "https://piotrlotniczy.elms.pl/next/public/login"
USER_EMAIL   = "monika.spoton@gmail.com"
USER_PASS    = "Filipiny26"
COURSE_URL   = "https://piotrlotniczy.elms.pl/next/public/training/2"

OUTPUT_DIR   = r"C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\lifewave\04-assets\knowledge_base\piotrlotniczy"
JSON_OUT     = os.path.join(OUTPUT_DIR, "piotr_lotowski_rag.json")
OBSIDIAN_DIR = os.path.join(OUTPUT_DIR, "obsidian_notes")


def ensure_ffmpeg():
    """Gwarantuje obecność pliku 'ffmpeg.exe' w PATH na potrzeby faster-whisper."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bin_dir = os.path.join(script_dir, "bin")
    os.makedirs(bin_dir, exist_ok=True)

    ffmpeg_exe = os.path.join(bin_dir, "ffmpeg.exe")
    ffprobe_exe = os.path.join(bin_dir, "ffprobe.exe")

    os.environ["PATH"] = bin_dir + os.path.pathsep + os.environ["PATH"]

    if os.path.exists(ffmpeg_exe):
        return True, bin_dir

    try:
        import imageio_ffmpeg
        img_ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        if os.path.exists(img_ffmpeg_path):
            shutil.copy(img_ffmpeg_path, ffmpeg_exe)
            return True, bin_dir
    except Exception:
        pass

    system_ffmpeg = shutil.which("ffmpeg")
    if system_ffmpeg:
        return True, None

    return False, None


def export_cookies_netscape(context, cookies_filepath):
    """Eskportuje ciasteczka z kontekstu Playwright do formatu Netscape wymaganego przez yt-dlp."""
    try:
        cookies = context.cookies()
        with open(cookies_filepath, "w", encoding="utf-8") as f:
            f.write("# Netscape HTTP Cookie File\n")
            for c in cookies:
                domain = c.get("domain", "")
                include_subdomains = "TRUE" if domain.startswith(".") else "FALSE"
                path = c.get("path", "/")
                secure = "TRUE" if c.get("secure", False) else "FALSE"
                expires = int(c.get("expires", time.time() + 86400))
                if expires < 0:
                    expires = int(time.time() + 86400)
                name = c.get("name", "")
                value = c.get("value", "")
                f.write(f"{domain}\t{include_subdomains}\t{path}\t{secure}\t{expires}\t{name}\t{value}\n")
        return True
    except Exception as e:
        print(f"  ⚠️ Błąd eksportu ciasteczek: {e}")
        return False


def load_db():
    if os.path.exists(JSON_OUT):
        try:
            with open(JSON_OUT, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"_meta": {"author": "Piotr Łotowski", "platform": "elms.pl"}, "lessons": {}}

def save_db(db):
    os.makedirs(os.path.dirname(JSON_OUT), exist_ok=True)
    db["_meta"]["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)

def clean_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name).strip()

def save_obsidian(module_name, lesson_title, content_md):
    os.makedirs(OBSIDIAN_DIR, exist_ok=True)
    safe_title = clean_filename(lesson_title) or "Lekcja_Bez_Tytulu"
    filepath = Path(OBSIDIAN_DIR) / f"{safe_title}.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content_md)
    print(f"  📝 Zapisano prawdziwą notatkę Obsidian: {filepath.name}")

def download_audio_ytdlp(video_url, referer_url, cookies_file=None, ffmpeg_dir=None):
    tmpdir = tempfile.mkdtemp(prefix="elms_audio_")
    out_template = os.path.join(tmpdir, "audio.%(ext)s")
    
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--referer", referer_url,
        "--add-header", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "--socket-timeout", "30",
        "--concurrent-fragments", "4",
        "--retries", "5",
        "--no-playlist",
        "-o", out_template
    ]

    if cookies_file and os.path.exists(cookies_file):
        cmd.extend(["--cookies", cookies_file])

    if ffmpeg_dir:
        cmd.extend(["--ffmpeg-location", ffmpeg_dir])

    cmd_audio = cmd + ["--extract-audio", "--audio-format", "mp3", video_url]

    try:
        print(f"  📥 Pobieranie strumienia yt-dlp z: {video_url[:70]}...")
        res = subprocess.run(cmd_audio, capture_output=True, text=True, timeout=300)
        
        for f in os.listdir(tmpdir):
            full_p = os.path.join(tmpdir, f)
            if os.path.isfile(full_p) and os.path.getsize(full_p) > 150000:
                print(f"  ✅ Pobrano plik audio ({round(os.path.getsize(full_p)/1024, 1)} KB)")
                return full_p, tmpdir

        print("  ⚠️ Błąd rozmiaru audio. Próba pobrania strumienia surowego...")
        cmd_raw = cmd + [video_url]
        res_raw = subprocess.run(cmd_raw, capture_output=True, text=True, timeout=300)
        
        for f in os.listdir(tmpdir):
            full_p = os.path.join(tmpdir, f)
            if os.path.isfile(full_p) and os.path.getsize(full_p) > 150000:
                print(f"  ✅ Pobrano surowy plik multimedialny ({round(os.path.getsize(full_p)/1024, 1)} KB)")
                return full_p, tmpdir

    except Exception as e:
        print(f"  ⚠️ Błąd podczas pobierania audio yt-dlp: {e}")
        
    return None, tmpdir

def transcribe_faster_whisper(audio_path):
    """Silnik STT wykorzystujący faster-whisper (model medium, int8, VAD filter)."""
    try:
        from faster_whisper import WhisperModel
        print("  🎙️ Wykonywanie transkrypcji mowy przez faster-whisper (model: medium, CPU int8, VAD=True)...")
        model = WhisperModel("medium", device="cpu", compute_type="int8")
        segments, info = model.transcribe(audio_path, language="pl", vad_filter=True)
        
        text_segments = []
        for segment in segments:
            text_segments.append(segment.text)
            
        full_text = " ".join(text_segments).strip()
        return full_text
    except ImportError:
        print("  ❌ Brak pakietu faster-whisper! Uruchom: pip install faster-whisper")
        # Fallback do zwykłego whisper jeśli brak faster-whisper
        try:
            import whisper
            print("  ⚠️ Fallback do standardowego whisper (base)...")
            w_model = whisper.load_model("base")
            res = w_model.transcribe(audio_path, language="pl")
            return res.get("text", "").strip()
        except Exception as ex:
            print(f"  ⚠️ Błąd transkrypcji: {ex}")
            return ""
    except Exception as e:
        print(f"  ⚠️ Błąd faster-whisper: {e}")
        return ""

def extract_js_context_video(page):
    """Wyciąga obiekty konfiguracyjne z kontekstu JS strony."""
    try:
        js_code = """
        () => {
            if (window.videoData && window.videoData.url) return window.videoData.url;
            if (window.elmsPlayer && window.elmsPlayer.videoUrl) return window.elmsPlayer.videoUrl;
            if (window.__NEXT_DATA__) {
                const str = JSON.stringify(window.__NEXT_DATA__);
                const match = str.match(/https?:\\\\/\\\\/[^"']+\\\\.(m3u8|mp4)/);
                if (match) return match[0].replace(/\\\\/g, '');
            }
            return null;
        }
        """
        res = page.evaluate(js_code)
        if res:
            return res
    except Exception:
        pass
    return None

def find_direct_video_stream(page):
    """Wielowarstwowe przeszukiwanie DOM, Shadow DOM oraz ramek iframe pod kątem wideo."""
    # 1. Odczyt z obiektów JS strony
    js_url = extract_js_context_video(page)
    if js_url:
        return js_url

    # 2. Przeszukiwanie ramek iframe i shadow root
    for frame in page.frames:
        try:
            url = frame.url
            if any(k in url for k in [".m3u8", ".mp4", "vimeo.com/video", "b-cdn.net", "mediadelivery.net", "iframe.mediadelivery"]):
                return url
            video_el = frame.query_selector("video, video source")
            if video_el:
                src = video_el.get_attribute("src") or video_el.get_attribute("data-src")
                if src:
                    return src
        except Exception:
            pass

    # 3. Szukanie w głównym elemencie <video>
    video_el = page.query_selector("video source, video")
    if video_el:
        src = video_el.get_attribute("src") or video_el.get_attribute("data-src")
        if src:
            return src

    return None


def main():
    print("=" * 80)
    print(" 🚀 ROZPOCZYNANIE POBIERANIA LEKCJI PIOTRA ŁOTOWSKIEGO (ELMS.PL) - VER 6.0")
    print("=" * 80)

    has_ffmpeg, ffmpeg_dir = ensure_ffmpeg()
    db = load_db()
    
    with sync_playwright() as p:
        print("[1] Uruchamianie Playwright (Chromium)...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        stream_urls = {}
        def on_request(req):
            u = req.url
            if any(ext in u for ext in [".m3u8", ".mp4", ".ts", "vimeo.com/video/", "playlist.m3u8"]):
                stream_urls[page.url] = u
            elif "video.webtolearn.pl" in u and page.url not in stream_urls:
                stream_urls[page.url] = u
                
        page.on("request", on_request)

        # Logowanie
        print(f"[2] Logowanie do {LOGIN_URL}...")
        page.goto(LOGIN_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        email_input = page.query_selector("input[type='email']") or page.query_selector("input[name='email']")
        pass_input = page.query_selector("input[type='password']") or page.query_selector("input[name='password']")

        if email_input: email_input.fill(USER_EMAIL)
        if pass_input: pass_input.fill(USER_PASS)

        submit_btn = page.query_selector("button[type='submit']") or page.query_selector("input[type='submit']")
        if submit_btn:
            submit_btn.click()
            page.wait_for_timeout(4000)

        cookies_file = os.path.join(OUTPUT_DIR, "elms_cookies.txt")
        export_cookies_netscape(context, cookies_file)
        print("  🔑 Wyeksportowano autoryzowane ciasteczka elms_cookies.txt")

        # Kurs
        print(f"[3] Otwieranie kursu: {COURSE_URL}...")
        page.goto(COURSE_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        for btn in page.query_selector_all(".accordion-button, .card-header, [data-toggle='collapse']"):
            try: btn.click(); page.wait_for_timeout(200)
            except Exception: pass

        lesson_anchors = page.query_selector_all("a[href*='/lesson/'], a[href*='/lekcja/'], .lesson-link, .list-group-item a")
        lessons = []
        seen = set()
        
        for a in lesson_anchors:
            href = a.get_attribute("href")
            title = re.sub(r'\s+', ' ', a.inner_text().strip())
            
            if href and href not in seen and len(title) > 2 and "logout" not in href and "login" not in href:
                if not href.startswith("http"):
                    base_domain = f"{page.url.split('/')[0]}//{page.url.split('/')[2]}"
                    href = f"{base_domain}{href}" if href.startswith('/') else f"{base_domain}/{href}"
                seen.add(href)
                lessons.append({"url": href, "title": title})

        print(f"  ✅ Znaleziono lekcji w kursie: {len(lessons)}")

        # Pętla po lekcjach
        for idx, linfo in enumerate(lessons, 1):
            ltitle, lurl = linfo["title"], linfo["url"]

            existing_transcript = db.get("lessons", {}).get(ltitle, {}).get("transcript", "")
            if existing_transcript and len(existing_transcript) > 1000:
                print(f"  [{idx}/{len(lessons)}] ⏭️ {ltitle} (Posiada już pełną transkrypcję STT - pomijam)")
                continue

            print(f"\n  [{idx}/{len(lessons)}] 📖 Przetwarzanie lekcji: {ltitle}")
            print(f"     URL: {lurl}")
            try:
                page.goto(lurl, wait_until="domcontentloaded")
                page.wait_for_timeout(4000)
            except Exception as e:
                print(f"  ⚠️ Błąd ładowania lekcji {lurl}: {e}")
                continue

            # Symulacja kliknięcia w odtwarzacz wideo
            try:
                play_btn = page.query_selector("button.play, .vjs-big-play-button, .play-button, .video-player")
                if play_btn:
                    play_btn.click()
                    page.wait_for_timeout(2000)
            except Exception:
                pass

            video_url = find_direct_video_stream(page)

            if not video_url and lurl in stream_urls:
                video_url = stream_urls[lurl]

            raw_transcript = ""

            if video_url:
                print(f"  🎬 Wykryto odtwarzacz / strumień wideo: {video_url[:75]}...")
                audio_file, tmpdir = download_audio_ytdlp(video_url, referer_url=lurl, cookies_file=cookies_file, ffmpeg_dir=ffmpeg_dir)
                
                if audio_file:
                    raw_transcript = transcribe_faster_whisper(audio_file)
                    print(f"  ✅ Wygenerowano transkrypcję faster-whisper ({len(raw_transcript)} znaków)")
                    try:
                        os.remove(audio_file)
                        shutil.rmtree(tmpdir, ignore_errors=True)
                    except Exception: pass
                else:
                    print("  ⚠️ Nie udało się pobrać prawdziwego strumienia wideo. POMIJAMY LEKCJĘ!")
                    continue
            else:
                # Wypisanie treści z lekcji pisemnej
                main_el = page.query_selector(".lesson-content, .training-content, #app main, .main-content, article")
                page_text = main_el.inner_text().strip() if main_el else page.inner_text("body")
                if len(page_text) > 500:
                    raw_transcript = page_text
                    print(f"  ✅ Wykryto treść tekstową lekcji ({len(raw_transcript)} znaków)")
                else:
                    print("  ⚠️ Brak wideo oraz brak treści tekstowej (>500 znaków). POMIJAMY LEKCJĘ!")
                    continue

            # PROTOKÓŁ 4: GUARD ANTI-HALLUCINATION (< 500 ZNAKÓW)
            if not raw_transcript or len(raw_transcript) < 500:
                print("  ⚠️ Brak wystarczającej transkrypcji (< 500 znaków). POMIJAMY LEKCJĘ — ZERO HALUCYNACJI!")
                continue

            note_md = f"""---
title: "{ltitle}"
source: "Piotr Łotowski - Akademia Punktów"
platform: "elms.pl"
url: "{lurl}"
date: "{datetime.now().strftime('%Y-%m-%d')}"
tags:
  - piotr-lotniczy
  - akademia-punktow
  - flight-hacking
  - faster-whisper
---

# ✈️ {ltitle}

## 🎙️ Prawdziwa Transkrypcja Mowy (faster-whisper medium - Piotr Łotowski)

{raw_transcript}
"""

            db.setdefault("lessons", {})[ltitle] = {
                "title": ltitle,
                "url": lurl,
                "transcript": raw_transcript,
                "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            save_db(db)
            save_obsidian("Piotr_Lotowski_Kurs", ltitle, note_md)

        browser.close()
        
    print("\n" + "=" * 80)
    print(" ✅ PROCES ZAKOŃCZONY SUKCESEM!")
    print(f" 📄 Przetworzono lekcji: {len(db.get('lessons', {}))}")
    print(f" 📂 Notatki Obsidian w: {OBSIDIAN_DIR}")
    print("=" * 80)

if __name__ == "__main__":
    main()
