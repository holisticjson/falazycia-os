import os
import sys
import time
import json
from playwright.sync_api import sync_playwright

OUTPUT_FILE = r"C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\lifewave\04-assets\knowledge_base\FLIGHT_HACKING_MASTER.md"

def extract_course():
    print("=" * 60)
    print("🚀 AUTOMATYCZNY POBIERACZ KURSU PIOTRA LOTNICZEGO")
    print("=" * 60)
    print("Za chwilę otworzy się okno przeglądarki Chrome...")
    print("Zaloguj się w oknie, które się pojawi, przejdź do kursu, a następnie wróć tutaj i naciśnij ENTER.")
    print("-" * 60)

    with sync_playwright() as p:
        # Launch browser in visible (non-headless) mode
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to training main page
        target_url = "https://piotrlotniczy.elms.pl/next/public/training/2"
        page.goto(target_url)

        print("\n👉 OKNO PRZEGLĄDARKI JEST OTWARTE.")
        print("👉 Jeśli nie jesteś zalogowany - zaloguj się teraz w przeglądarce.")
        print("👉 Po zalogowaniu i wejściu do kursu, naciśnij ENTER poniżej:\n")
        
        input(">>> PACNIJ ENTER TUTAJ PO ZALOGOWANIU W PRZEGLĄDARCE <<< ")

        print("\n⏳ Pobieram zawartość kursu i strukturę lekcji...")
        
        # Wait for any active navigation/loading to finish cleanly
        try:
            page.wait_for_load_state("domcontentloaded", timeout=10000)
        except Exception:
            pass
        
        time.sleep(2)

        # Robust link extraction with retry and page load wait
        links = []
        for attempt in range(5):
            try:
                # Always grab the active top-level page
                active_page = context.pages[-1] if context.pages else page
                active_page.wait_for_load_state("networkidle", timeout=5000)
                eval_links = active_page.evaluate("""() => {
                    return Array.from(document.querySelectorAll('a[href]')).map(e => ({
                        href: e.href,
                        text: (e.innerText || e.textContent || '').trim()
                    }));
                }""")
                links = eval_links
                page = active_page
                break
            except Exception as e:
                print(f"Oczekiwanie na ustabilizowanie się strony (próba {attempt+1}/5)...")
                time.sleep(2)

        lesson_urls = []
        for l in links:
            href = l.get('href', '')
            text = l.get('text', '')
            if href and ('/lesson/' in href or '/training/' in href or '/module/' in href or '/course/' in href):
                if href not in [item['href'] for item in lesson_urls]:
                    lesson_urls.append({'href': href, 'text': text})

        # Grab page title, current URL and text content
        title = page.title()
        current_url = page.url
        
        try:
            body_text = page.inner_text("body")
        except Exception:
            body_text = "Nie udało się odczytać tekstu body."

        # Compile Markdown document
        markdown_lines = []
        markdown_lines.append("# ✈️ Baza Wiedzy Piotra Lotniczego – Akademia Punktów & Flight Hacking\n")
        markdown_lines.append("> Wyselekcjonowane materiały z platformy eLMS Piotra Lotniczego.\n\n")
        markdown_lines.append(f"## 📌 Tytuł Kursu / Strony: {title}\n")
        markdown_lines.append(f"**URL:** {current_url}\n\n")
        markdown_lines.append("---\n\n")
        markdown_lines.append("### 📚 Wykryte Moduły, Lekcje i Odnośniki:\n\n")

        if lesson_urls:
            for idx, item in enumerate(lesson_urls, 1):
                label = item['text'] if item['text'] else item['href']
                markdown_lines.append(f"{idx}. [{label}]({item['href']})\n")
        else:
            # Fallback to all hrefs if specific patterns weren't matched
            markdown_lines.append("Zeskanowano wszystkie aktywne odnośniki na stronie:\n\n")
            for idx, item in enumerate(links[:50], 1):
                if item.get('href'):
                    label = item['text'] if item['text'] else item['href']
                    markdown_lines.append(f"{idx}. [{label}]({item['href']})\n")

        markdown_lines.append("\n---\n\n### 📝 Pobrana Treść Główna:\n\n")
        markdown_lines.append("```text\n")
        markdown_lines.append(body_text[:20000]) # First 20k chars
        markdown_lines.append("\n```\n")

        # Write to FLIGHT_HACKING_MASTER.md
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(markdown_lines))

        print(f"\n✅ SUKCES! Pobrano zawartość i zapisano do pliku:\n{OUTPUT_FILE}")
        print("Skanowanie zakończone pomyślnie.")
        
        time.sleep(3)
        browser.close()

if __name__ == "__main__":
    extract_course()
