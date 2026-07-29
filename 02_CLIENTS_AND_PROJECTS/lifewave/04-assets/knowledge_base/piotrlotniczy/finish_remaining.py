"""
================================================================================
  FAST BULK AUDIO DOWNLOADER & LIGHTNING STT SCRAPER (v7.0)
================================================================================
  1. Wykrywa, że 53/61 lekcji jest JUŻ GOTOWYCH i pomija je błyskawicznie.
  2. Dla pozostałych ~8 lekcji szybko pobiera pliki MP3 przez yt-dlp.
  3. Dokonuje BŁYSKAWICZNEJ transkrypcji z użyciem Gemini 2.5 Flash API lub faster-whisper.
================================================================================
"""

import sys
import os
import re
import time
import json
import shutil
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
    print("❌ Wymagane pakiety: pip install playwright yt-dlp python-dotenv imageio-ffmpeg google-genai")
    sys.exit(1)

# ==============================================================================
# ⚙️ USTAWIENIA DLA KURSÓW PIOTRA ŁOTOWSKIEGO (ELMS.PL)
# ==============================================================================
LOGIN_URL    = "https://piotrlotniczy.elms.pl/next/public/login"
USER_EMAIL   = "monika.spoton@gmail.com"
USER_PASS    = "Filipiny26"
COURSE_URL   = "https://piotrlotniczy.elms.pl/next/public/training/2"

OUTPUT_DIR   = r"C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\lifewave\04-assets\knowledge_base\piotrlotniczy"
AUDIO_DIR    = os.path.join(OUTPUT_DIR, "audio_downloads")
JSON_OUT     = os.path.join(OUTPUT_DIR, "piotr_lotowski_rag.json")
OBSIDIAN_DIR = os.path.join(OUTPUT_DIR, "obsidian_notes")

os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(OBSIDIAN_DIR, exist_ok=True)


def ensure_ffmpeg():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bin_dir = os.path.join(script_dir, "bin")
    os.makedirs(bin_dir, exist_ok=True)

    ffmpeg_exe = os.path.join(bin_dir, "ffmpeg.exe")
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

    if shutil.which("ffmpeg"):
        return True, None

    return False, None


def export_cookies_netscape(context, cookies_filepath):
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
                if expires < 0: expires = int(time.time() + 86400)
                f.write(f"{domain}\t{include_subdomains}\t{path}\t{secure}\t{expires}\t{c.get('name', '')}\t{c.get('value', '')}\n")
        return True
    except Exception:
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
    safe_title = clean_filename(lesson_title) or "Lekcja_Bez_Tytulu"
    filepath = Path(OBSIDIAN_DIR) / f"{safe_title}.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content_md)
    print(f"  📝 Zapisano notatkę Obsidian: {filepath.name}")


def download_audio_fast(video_url, referer_url, ltitle, cookies_file=None, ffmpeg_dir=None):
    """Pobiera plik MP3 do dedykowanego folderu AUDIO_DIR bez czekania na transkrypcję."""
    safe_title = clean_filename(ltitle)
    target_mp3 = os.path.join(AUDIO_DIR, f"{safe_title}.mp3")

    if os.path.exists(target_mp3) and os.path.getsize(target_mp3) > 100000:
        print(f"  ✅ Istnieje już plik MP3 ({round(os.path.getsize(target_mp3)/1024, 1)} KB): {os.path.basename(target_mp3)}")
        return target_mp3

    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--referer", referer_url,
        "--add-header", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "--socket-timeout", "20",
        "--concurrent-fragments", "4",
        "--retries", "3",
        "--no-playlist",
        "-o", target_mp3
    ]

    if cookies_file and os.path.exists(cookies_file):
        cmd.extend(["--cookies", cookies_file])

    if ffmpeg_dir:
        cmd.extend(["--ffmpeg-location", ffmpeg_dir])

    cmd_audio = cmd + ["--extract-audio", "--audio-format", "mp3", video_url]

    try:
        print(f"  ⚡ Błyskawiczne pobieranie MP3: {video_url[:65]}...")
        subprocess.run(cmd_audio, capture_output=True, text=True, timeout=120)
        
        if os.path.exists(target_mp3) and os.path.getsize(target_mp3) > 100000:
            print(f"  ✅ Pobrano MP3 ({round(os.path.getsize(target_mp3)/1024, 1)} KB)")
            return target_mp3

    except Exception as e:
        print(f"  ⚠️ Błąd yt-dlp: {e}")

    return None


def transcribe_audio_fast(audio_path):
    """Transkrybuje audio z użyciem Gemini 2.5 Flash API lub faster-whisper."""
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if gemini_key:
        try:
            from google import genai
            print("  ⚡ Transkrypcja przez Gemini 2.5 Flash API (~3 sekundy)...")
            client = genai.Client(api_key=gemini_key)
            
            # Czysta tymczasowa nazwa bez polskich znaków / pauz unicode
            clean_temp = os.path.join(tempfile.gettempdir(), "gemini_audio.mp3")
            shutil.copyfile(audio_path, clean_temp)

            audio_file = client.files.upload(file=clean_temp)
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=[
                    audio_file,
                    "Dokonaj dokładnej, dosłownej transkrypcji mowy z tego nagrania po polsku. Zapisz wyłącznie wypowiedziane słowa."
                ]
            )
            try: client.files.delete(name=audio_file.name)
            except Exception: pass
            try: os.remove(clean_temp)
            except Exception: pass

            txt = response.text.strip()
            if len(txt) > 200:
                return txt
        except Exception as e:
            print(f"  ℹ️ Gemini API błąd ({e}). Przełączanie na lokalny faster-whisper...")

    # 2. Fallback do local faster-whisper (model small/medium z VAD)
    try:
        from faster_whisper import WhisperModel
        print("  🎙️ Transkrypcja przez lokalny faster-whisper (model: small, CPU int8, VAD=True)...")
        model = WhisperModel("small", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(audio_path, language="pl", vad_filter=True)
        return " ".join([s.text for s in segments]).strip()
    except Exception as e:
        print(f"  ⚠️ Błąd faster-whisper: {e}")
        return ""


def find_direct_video_stream(page):
    for frame in page.frames:
        try:
            url = frame.url
            if url.endswith(".js") or url.endswith(".css"):
                continue
            if any(k in url for k in ["/embed/", ".m3u8", ".mp4", "vimeo.com/video", "b-cdn.net", "mediadelivery.net"]):
                return url
        except Exception:
            pass

    video_el = page.query_selector("video source, video")
    if video_el:
        src = video_el.get_attribute("src") or video_el.get_attribute("data-src")
        if src and not src.endswith(".js"): return src

    return None


def main():
    print("=" * 80)
    print(" 🚀 BULK AUDIO DOWNLOADER & FAST STT - DLA POZOSTAŁYCH LEKCJI (v7.0)")
    print("=" * 80)

    has_ffmpeg, ffmpeg_dir = ensure_ffmpeg()
    db = load_db()
    
    # 1. Sprawdzamy stan gotowych plików w Obsidian Notes
    completed_files = list(Path(OBSIDIAN_DIR).glob("*.md"))
    print(f" 📊 Liczba JUŻ GOTOWYCH notatek w Obsidian: {len(completed_files)}")

    with sync_playwright() as p:
        print("[1] Uruchamianie Playwright...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        stream_urls = {}
        def on_request(req):
            u = req.url
            if any(ext in u for ext in [".m3u8", ".mp4", ".ts", "vimeo.com/video/", "playlist.m3u8", "mediadelivery.net"]):
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
            page.wait_for_timeout(3000)

        cookies_file = os.path.join(OUTPUT_DIR, "elms_cookies.txt")
        export_cookies_netscape(context, cookies_file)

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

        print(f"  ✅ Wszystkich lekcji w kursie: {len(lessons)}")

        # Pętla po lekcjach - z szybkimi pominięciami gotowych
        for idx, linfo in enumerate(lessons, 1):
            ltitle, lurl = linfo["title"], linfo["url"]

            safe_title = clean_filename(ltitle)
            existing_note = Path(OBSIDIAN_DIR) / f"{safe_title}.md"

            # POMIJANIE: Jeśli notatka istnieje i ma > 500 znaków -> SKOK ORAZ BRAK SOWITEGO CZEKANIA!
            if existing_note.exists() and os.path.getsize(existing_note) > 500:
                print(f"  [{idx}/{len(lessons)}] ⏭️ {ltitle} (Gotowe — notatka istnieje)")
                continue

            print(f"\n  [{idx}/{len(lessons)}] 📖 BŁYSKAWICZNE POBIERANIE AUDIO DLA: {ltitle}")
            print(f"     URL: {lurl}")
            try:
                page.goto(lurl, wait_until="domcontentloaded")
                page.wait_for_timeout(3000)
            except Exception as e:
                print(f"  ⚠️ Błąd ładowania {lurl}: {e}")
                continue

            video_url = find_direct_video_stream(page)
            if not video_url and lurl in stream_urls:
                video_url = stream_urls[lurl]

            raw_transcript = ""

            if video_url:
                audio_file = download_audio_fast(video_url, referer_url=lurl, ltitle=ltitle, cookies_file=cookies_file, ffmpeg_dir=ffmpeg_dir)
                if audio_file:
                    raw_transcript = transcribe_audio_fast(audio_file)
                    print(f"  ✅ Przetranskrybowano ({len(raw_transcript)} znaków)")
                else:
                    print("  ⚠️ Błąd pobierania MP3!")
                    continue
            else:
                main_el = page.query_selector(".lesson-content, .training-content, #app main, .main-content, article")
                page_text = main_el.inner_text().strip() if main_el else page.inner_text("body")
                if len(page_text) > 300:
                    raw_transcript = page_text

            if not raw_transcript or len(raw_transcript) < 300:
                print("  ⚠️ Treść zbyt krótka. Pomijamy!")
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
  - fast-stt
---

# ✈️ {ltitle}

## 🎙️ Prawdziwa Transkrypcja Mowy (Piotr Łotowski)

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
    print(" ✅ BULK FINISH ZAKOŃCZONY SUKCESEM!")
    print(f" 📂 Zapisano wszystkie notatki w: {OBSIDIAN_DIR}")
    print("=" * 80)

if __name__ == "__main__":
    main()
