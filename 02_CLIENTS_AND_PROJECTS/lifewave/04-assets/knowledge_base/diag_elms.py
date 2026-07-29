"""
================================================================================
  ELMS / WEB2LEARN DIAGNOSTIC SCRIPT (diag_elms.py) - FIX v2.0
================================================================================
  Poprawka: Usunięcie wywołania response.text() z event listenera oraz 
  zamiana wait_until="networkidle" na "domcontentloaded" (zapobiega timeoutom wideo).
================================================================================
"""

import os
import re
import json
import time
from playwright.sync_api import sync_playwright

LOGIN_URL  = "https://piotrlotniczy.elms.pl/next/public/login"
USER_EMAIL = "monika.spoton@gmail.com"
USER_PASS  = "Filipiny26"
COURSE_URL = "https://piotrlotniczy.elms.pl/next/public/training/2"

OUTPUT_DIR = r"C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\lifewave\04-assets\knowledge_base\piotrlotniczy\diagnostics"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def run_diagnostics():
    print("=" * 80)
    print(" 🔍 URUCHAMIANIE DIAGNOSTYKI SIECIOWEJ I HTML DLA PLATFORMY ELMS (v2.0)")
    print("=" * 80)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        network_logs = []

        def on_request(request):
            try:
                network_logs.append({
                    "time": time.strftime("%H:%M:%S"),
                    "type": "REQUEST",
                    "method": request.method,
                    "url": request.url,
                    "resource_type": request.resource_type
                })
            except Exception:
                pass

        def on_response(response):
            try:
                network_logs.append({
                    "time": time.strftime("%H:%M:%S"),
                    "type": "RESPONSE",
                    "url": response.url,
                    "status": response.status,
                    "content_type": response.headers.get("content-type", "")
                })
            except Exception:
                pass

        page.on("request", on_request)
        page.on("response", on_response)

        # 1. Logowanie
        print(f"[1] Logowanie do {LOGIN_URL}...")
        page.goto(LOGIN_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)

        email_in = page.query_selector("input[type='email']") or page.query_selector("input[name='email']")
        pass_in = page.query_selector("input[type='password']") or page.query_selector("input[name='password']")

        if email_in: email_in.fill(USER_EMAIL)
        if pass_in: pass_in.fill(USER_PASS)

        submit_btn = page.query_selector("button[type='submit']") or page.query_selector("input[type='submit']")
        if submit_btn:
            submit_btn.click()
            page.wait_for_timeout(3000)

        # 2. Kurs
        print(f"[2] Otwieranie kursu: {COURSE_URL}...")
        page.goto(COURSE_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        anchors = page.query_selector_all("a[href*='/lesson/'], a[href*='/lekcja/']")
        lesson_urls = []
        for a in anchors:
            href = a.get_attribute("href")
            if href and href not in lesson_urls and "logout" not in href:
                if not href.startswith("http"):
                    base_domain = f"{page.url.split('/')[0]}//{page.url.split('/')[2]}"
                    href = f"{base_domain}{href}" if href.startswith('/') else f"{base_domain}/{href}"
                lesson_urls.append(href)

        # Wybieramy 3 RÓŻNE lekcje
        target_lessons = []
        for u in lesson_urls:
            if u not in target_lessons:
                target_lessons.append(u)
            if len(target_lessons) == 3:
                break

        print(f"  🎯 Wyselekcjonowano {len(target_lessons)} unikalne lekcje do diagnostyki: {target_lessons}")

        for idx, lurl in enumerate(target_lessons, 1):
            print(f"\n[3.{idx}] Diagnostyka lekcji: {lurl}")
            network_logs.clear()
            
            page.goto(lurl, wait_until="domcontentloaded")
            page.wait_for_timeout(4000)

            # Zapis HTML
            html_content = page.content()
            html_file = os.path.join(OUTPUT_DIR, f"debug_elms_html_{idx}.html")
            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"  📄 Zapisano HTML do: {html_file} ({len(html_content)} znaków)")

            # Zapis informacji o iframe
            frames_info = [{"frame_index": i, "name": fr.name, "url": fr.url} for i, fr in enumerate(page.frames)]

            net_file = os.path.join(OUTPUT_DIR, f"debug_elms_network_{idx}.txt")
            with open(net_file, "w", encoding="utf-8") as f:
                f.write(f"=== LESSON URL: {lurl} ===\n")
                f.write(f"=== FRAMES DETECTED: {json.dumps(frames_info, indent=2)} ===\n\n")
                f.write("=== NETWORK LOGS ===\n")
                for item in network_logs:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")

            print(f"  🌐 Zapisano logi sieciowe do: {net_file} ({len(network_logs)} zdarzeń)")

        browser.close()

    print("\n" + "=" * 80)
    print(" ✅ DIAGNOSTYKA ZAKOŃCZONA SUKCESEM!")
    print(f" 📂 Zrzuty sieciowe i HTML zapisane w: {OUTPUT_DIR}")
    print("=" * 80)


if __name__ == "__main__":
    run_diagnostics()
