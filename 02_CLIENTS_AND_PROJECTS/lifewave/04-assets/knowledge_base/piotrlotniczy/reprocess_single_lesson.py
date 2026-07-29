import os
import re
import sys
import time
import json
import shutil
import tempfile
import subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

LOGIN_URL    = "https://piotrlotniczy.elms.pl/next/public/login"
USER_EMAIL   = "monika.spoton@gmail.com"
USER_PASS    = "Filipiny26"
LESSON_URL   = "https://piotrlotniczy.elms.pl/next/public/lesson/55" # Lekcja 6.1

OUTPUT_DIR   = r"C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\lifewave\04-assets\knowledge_base\piotrlotniczy"
AUDIO_DIR    = os.path.join(OUTPUT_DIR, "audio_downloads")
OBSIDIAN_DIR = os.path.join(OUTPUT_DIR, "obsidian_notes")

os.makedirs(AUDIO_DIR, exist_ok=True)

script_dir = os.path.dirname(os.path.abspath(__file__))
bin_dir = os.path.join(script_dir, "bin")
os.environ["PATH"] = bin_dir + os.path.pathsep + os.environ["PATH"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width": 1280, "height": 800})
    page = context.new_page()

    page.goto(LOGIN_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    email_in = page.query_selector("input[type='email']") or page.query_selector("input[name='email']")
    pass_in = page.query_selector("input[type='password']") or page.query_selector("input[name='password']")
    if email_in: email_in.fill(USER_EMAIL)
    if pass_in: pass_in.fill(USER_PASS)

    btn = page.query_selector("button[type='submit']") or page.query_selector("input[type='submit']")
    if btn: btn.click(); page.wait_for_timeout(3000)

    page.goto(LESSON_URL, wait_until="domcontentloaded")
    page.wait_for_timeout(4000)

    video_url = None
    for frame in page.frames:
        u = frame.url
        if any(k in u for k in ["iframe.mediadelivery.net", "embed", ".m3u8"]):
            video_url = u
            break

    print(f"🎬 Wykryto wideo dla Lekcji 6.1: {video_url}")

    if video_url:
        target_mp3 = os.path.join(AUDIO_DIR, "Lekcja_6.1_Najnizsza_cena_AVIOS.mp3")
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--referer", LESSON_URL,
            "--extract-audio", "--audio-format", "mp3",
            "-o", target_mp3,
            video_url
        ]
        subprocess.run(cmd)

        if os.path.exists(target_mp3):
            print(f"✅ Pobrano MP3: {target_mp3} ({round(os.path.getsize(target_mp3)/1024, 1)} KB)")

            # Transkrypcja przez faster-whisper lub Gemini
            from faster_whisper import WhisperModel
            print("🎙️ Transkrypcja przez faster-whisper small...")
            model = WhisperModel("small", device="cpu", compute_type="int8")
            segments, _ = model.transcribe(target_mp3, language="pl", vad_filter=True)
            txt = " ".join([s.text for s in segments]).strip()

            print(f"✅ Wygenerowano transkrypcję ({len(txt)} znaków)")

            note_md = f"""---
title: "Lekcja 6.1 Najniższa cena AVIOS. (Nowa Lekcja Bonusowa)"
source: "Piotr Łotowski - Akademia Punktów"
platform: "elms.pl"
url: "{LESSON_URL}"
date: "2026-07-29"
tags:
  - piotr-lotniczy
  - akademia-punktow
  - flight-hacking
  - faster-whisper
---

# ✈️ Lekcja 6.1 Najniższa cena AVIOS. (Nowa Lekcja Bonusowa)

## 🎙️ Prawdziwa Transkrypcja Mowy (Piotr Łotowski)

{txt}
"""
            filepath = Path(OBSIDIAN_DIR) / "Lekcja 6.1 Najniższa cena AVIOS. (Nowa Lekcja Bonusowa).md"
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(note_md)
            print(f"📝 Dociągnięto i zapisano notatkę: {filepath.name}")

    browser.close()
