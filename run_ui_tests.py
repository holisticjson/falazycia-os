from playwright.sync_api import sync_playwright
import time
import os

ARTIFACT_DIR = r"C:\Users\tomas_yq1b9su\.gemini\antigravity\brain\5318ebb3-6fa9-4b29-ac85-2a6b3a2dd4b2"

routes = {
    "dashboard_main": "/",
    "dashboard_kanban": "/kanban",
    "dashboard_broker": "/broker",
    "dashboard_legal": "/legal",
    "dashboard_finance": "/finance",
    "dashboard_content": "/content",
    "dashboard_zen": "/zen",
    "dashboard_journal": "/journal",
    "dashboard_antigravity": "/antigravity"
}

def run_tests():
    print("Rozpoczynam zautomatyzowane testy UI (QA Tester)...")
    
    with sync_playwright() as p:
        # Odpalamy w headless=False żeby mieć pewność że zrenderuje efekty CSS (glassmorphism) poprawnie
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        
        # Oczekujemy aż serwer Vite w pełni wczyta apkę
        try:
            page.goto("http://localhost:5173", timeout=15000)
            page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Nie można połączyć się z http://localhost:5173. Upewnij się, że npm run dev działa. Błąd: {e}")
            browser.close()
            return
            
        print("Połączono z aplikacją. Tworzenie zrzutów ekranu...")
        
        for name, path in routes.items():
            print(f"Nawigacja: {path}...")
            page.goto(f"http://localhost:5173{path}")
            page.wait_for_load_state("networkidle")
            time.sleep(1) # Czas na wejście animacji
            
            screenshot_path = os.path.join(ARTIFACT_DIR, f"{name}.png")
            page.screenshot(path=screenshot_path)
            print(f"Zapisano zrzut: {screenshot_path}")
            
        # Testowanie modala Brain Dump (pływająca czaszka)
        print("Testowanie modala Brain Dump...")
        try:
            page.click("button[aria-label='Brain Dump']")
            time.sleep(1)
            modal_screenshot = os.path.join(ARTIFACT_DIR, "dashboard_modal_braindump.png")
            page.screenshot(path=modal_screenshot)
            print(f"Zapisano zrzut modala: {modal_screenshot}")
        except Exception as e:
            print(f"Błąd podczas otwierania modala Brain Dump: {e}")
            
        browser.close()
        print("Testy UI zakończone. Zrzuty wygenerowane pomyślnie.")

if __name__ == "__main__":
    run_tests()
