"""
🕵️ J(AI)SON Reverse-Engineer Bot — Content Box Scraper & Asset Extractor
========================================================================
Skrypt automatycznie uruchamia przeglądarkę, pozwala Ci się zalogować, a następnie 
pobiera całą strukturę strony (HTML, CSS, JSON API, układy kart, menu i style) 
narzędzia Content Box AI do folderu archiwum. 

Dzięki temu poznamy dokładny kod, wygląd i architekturę tych pięknych paneli, 
abyśmy mogli je odwzorować w 100% we własnym systemie operacyjnym!

Wymagania: pip install playwright
Uruchomienie instalacji i skryptu jednym poleceniem:
  .venv\\Scripts\\python 02-os-jaison\\integrations\\reverse_engineer_contentbox.py
"""

import os
import sys
import time
import json
from pathlib import Path

# Ścieżka docelowa na pobrane materiały
BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "09-archive" / "contentbox_reconstructed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("⚡ Instalowanie biblioteki Playwright (silnik automatyzacji przeglądarek)...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    from playwright.sync_api import sync_playwright


def log_step(text: str):
    print(f"\n[🕵️ BOT]: {text}")


def save_page_assets(page, page_name: str):
    """Zgrywa HTML, CSS, screenshot oraz strukturę DOM danej strony."""
    page_folder = OUTPUT_DIR / page_name
    page_folder.mkdir(parents=True, exist_ok=True)
    
    log_step(f"Skanowanie strony i pobieranie zasobów dla: '{page_name}'...")
    
    # 1. Zapis surowego kodu HTML
    html_content = page.content()
    with open(page_folder / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"  💾 Zapisano HTML -> {page_folder / 'index.html'}")
    
    # 2. Zrzut ekranu (Referencja wizualna)
    screenshot_path = page_folder / "screenshot.png"
    page.screenshot(path=str(screenshot_path), full_page=True)
    print(f"  📸 Zapisano Screenshot -> {screenshot_path}")
    
    # 3. Ekstrakcja wszystkich stylów CSS
    css_assets = page.evaluate("""() => {
        const styles = [];
        // Pobierz style z tagów <style>
        document.querySelectorAll('style').forEach((el, i) => {
            styles.push({ type: 'inline', index: i, content: el.innerHTML });
        });
        // Pobierz linki do zewnętrznych arkuszy CSS (np. Tailwind, Google Fonts)
        document.querySelectorAll('link[rel="stylesheet"]').forEach((el, i) => {
            styles.push({ type: 'external', index: i, href: el.href });
        });
        return styles;
    }""")
    
    with open(page_folder / "styles_info.json", "w", encoding="utf-8") as f:
        json.dump(css_assets, f, indent=2, ensure_ascii=False)
    print(f"  🎨 Zmapowano {len(css_assets)} arkuszy/tagów stylów CSS -> styles_info.json")
    
    # 4. Wyodrębnienie danych dynamicznych (np. kart pomysłów)
    if "pomysly" in page_name:
        ideas_data = page.evaluate("""() => {
            const cards = [];
            // Szukamy kontenerów kart (na podstawie struktury ze zrzutu ekranu)
            document.querySelectorAll('div').forEach(el => {
                // Jeśli element wygląda jak karta z pomysłem (posiada ikonkę, tytuł i platformę)
                if (el.textContent.includes('Pomysł') && (el.textContent.includes('Post') || el.textContent.includes('Wideo'))) {
                    const text = el.innerText.split('\\n').filter(t => t.trim() !== '');
                    if (text.length >= 3) {
                        cards.push({ raw_text: text });
                    }
                }
            });
            return cards;
        }""")
        if ideas_data:
            with open(page_folder / "scraped_ideas.json", "w", encoding="utf-8") as f:
                json.dump(ideas_data, f, indent=2, ensure_ascii=False)
            print(f"  💡 Wykryto i zgrano {len(ideas_data)} kart pomysłów na treści!")


def run_scraper():
    log_step("Inicjalizacja silnika Playwright...")
    
    with sync_playwright() as p:
        # Uruchom przeglądarkę Chromium w trybie graficznym (nie-headless)
        # Używamy profilu użytkownika, aby zapisać stan logowania
        user_data_dir = OUTPUT_DIR / "browser_session"
        browser_context = p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,
            viewport={"width": 1280, "height": 720},
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = browser_context.pages[0]
        
        # Przejdź na stronę logowania / główną
        target_url = "https://app.contentbox.ai"  # standardowa domena panelu SaaS
        log_step(f"Otwieranie strony panelu: {target_url}")
        
        try:
            page.goto(target_url, wait_until="networkidle", timeout=15000)
        except Exception:
            # Jeśli app.contentbox.ai nie działa, spróbujmy alternatywnej domeny
            fallback_url = "https://contentbox.ai"
            log_step(f"Przekierowanie awaryjne na: {fallback_url}")
            try:
                page.goto(fallback_url, wait_until="networkidle", timeout=15000)
            except Exception as e:
                log_step("⚠️ Nie można automatycznie otworzyć domeny. Wpisz ręcznie adres w otwartym oknie przeglądarki.")
        
        print("\n" + "="*70)
        print("🕵️ INSTALACJA BOTA - KROK PO KROKU:")
        print("1. W otwartym oknie przeglądarki zaloguj się na swoje konto Content Box AI.")
        print("2. Przejdź do głównego Pulpitu (Dashboard).")
        print("3. Po zalogowaniu, WRÓĆ DO TEGO TERMINALA i naciśnij ENTER, aby rozpocząć zgrywanie.")
        print("="*70 + "\n")
        
        input("👉 Naciśnij [ENTER] gdy będziesz gotowy na Pulpicie (Dashboard)...")
        
        # 1. Zgrywanie Pulpitu
        save_page_assets(page, "01_pulpit")
        
        # Instrukcje nawigacji
        print("\n" + "="*70)
        print("👉 KROK DLA CIEBIE: Przejdź teraz w przeglądarce do zakładki 'Pomysły na treści'.")
        print("Po załadowaniu strony, wróć tutaj i naciśnij ENTER.")
        print("="*70 + "\n")
        input("👉 Naciśnij [ENTER] po wejściu w 'Pomysły na treści'...")
        save_page_assets(page, "02_pomysly_na_tresci")
        
        # Kalendarz
        print("\n" + "="*70)
        print("👉 KROK DLA CIEBIE: Przejdź teraz w przeglądarce do zakładki 'Kalendarz'.")
        print("Po załadowaniu strony, wróć tutaj i naciśnij ENTER.")
        print("="*70 + "\n")
        input("👉 Naciśnij [ENTER] po wejściu w 'Kalendarz'...")
        save_page_assets(page, "03_kalendarz")
        
        # Kreator postów
        print("\n" + "="*70)
        print("👉 KROK DLA CIEBIE: Przejdź teraz w przeglądarce do zakładki 'Generuj post' / 'Dodaj nową treść'.")
        print("Po załadowaniu strony, wróć tutaj i naciśnij ENTER.")
        print("="*70 + "\n")
        input("👉 Naciśnij [ENTER] po wejściu w 'Generuj post'...")
        save_page_assets(page, "04_generuj_post")
        
        log_step("ZAKOŃCZONO SKANOWANIE!")
        print(f"\n🎉 Wszystkie zasoby, kod HTML, style i układ zostały pomyślnie zgrane!")
        print(f"📁 Lokalizacja plików: {OUTPUT_DIR}")
        print("Teraz przeanalizuję ten kod, abyśmy mogli odtworzyć te luksusowe panele bezpośrednio w Twoim systemie operacyjnym!")
        
        browser_context.close()


if __name__ == "__main__":
    try:
        run_scraper()
    except KeyboardInterrupt:
        print("\n❌ Przerwano działanie bota.")
        sys.exit(0)
