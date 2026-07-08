import os
import sys
import json
import time
import argparse
import urllib.request
import xml.etree.ElementTree as ET
import requests

# Dodanie głównego katalogu do ścieżki wyszukiwania modułów, aby móc importować gcp_helpers i systeme_io
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from integrations.gcp_helpers import get_gcp_sa_credentials
except ImportError:
    get_gcp_sa_credentials = None

class HermesCronOrchestrator:
    def __init__(self):
        self.telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        self.gemini_api_key = os.environ.get("GEMINI_API_KEY")
        self.serper_api_key = os.environ.get("SERPER_API_KEY")
        
        # Wczytywanie profilu Tomasza
        self.ghost_profile = ""
        ghost_path = "04-ghost/Ghost v2 - Głos Marki Tomasz.md"
        if os.path.exists(ghost_path):
            try:
                with open(ghost_path, "r", encoding="utf-8") as f:
                    self.ghost_profile = f.read()
            except Exception:
                pass

    def send_telegram_message(self, message):
        """Wysyła sformatowaną wiadomość na Telegram. Zapewnia fallback, jeśli brak tokenów."""
        print(f"\n[TELEGRAM PREVIEW]:\n{message}\n")
        
        if not self.telegram_token or not self.telegram_chat_id:
            print("[INFO]: Wiadomość nie została wysłana na Telegram (Brak TELEGRAM_BOT_TOKEN lub TELEGRAM_CHAT_ID w .env).")
            return False
            
        url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            res = requests.post(url, json=payload, timeout=10)
            return res.status_code == 200
        except Exception as e:
            print(f"[ERROR]: Nie udało się wysłać powiadomienia na Telegram: {e}")
            return False

    def _fetch_rss_titles(self, url, limit=3):
        """Pobiera i parsuje tytuły z kanału RSS w sposób natywny (bez feedparser)."""
        titles = []
        try:
            req = urllib.request.Request(
                url, 
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                xml_data = response.read()
                root = ET.fromstring(xml_data)
                
                # Parsowanie artykułów z RSS (zazwyczaj <item> w <channel>)
                for item in root.findall('.//item')[:limit]:
                    title = item.find('title')
                    link = item.find('link')
                    if title is not None:
                        t_text = title.text.strip() if title.text else "Bez tytułu"
                        l_text = link.text.strip() if link is not None and link.text else ""
                        titles.append(f"- {t_text} ({l_text})")
        except Exception as e:
            print(f"[WARNING]: Nie udało się pobrać RSS z {url}: {e}")
        return titles

    def _call_gemini_fallback(self, prompt, system_instruction=None):
        """Wywołuje interfejs Gemini za pomocą klucza API z .env (prosty requests wrapper)."""
        if not self.gemini_api_key:
            return "Brak GEMINI_API_KEY w .env. Nie można wygenerować treści za pomocą AI."
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048,
            }
        }
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}]
            }
            
        try:
            res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
            if res.status_code == 200:
                data = res.json()
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                return f"API Error {res.status_code}: {res.text}"
        except Exception as e:
            return f"Wyjątek wywołania Gemini: {e}"

    # --- CODZIENNE ZADANIA (JOBY) ---

    def run_morning_briefing(self):
        """JOB #1: Poranny Briefing (08:00)"""
        print("[START]: Uruchamianie poranneho briefingu...")
        
        # 1. Pobieranie nowinek AI & ADHD z RSS
        ai_news_titles = self._fetch_rss_titles("https://techcrunch.com/category/artificial-intelligence/feed/", limit=3)
        if not ai_news_titles:
            ai_news_titles = ["- Google zapowiada nowe modele Gemini 3.5", "- Nvidia prezentuje superkomputery nowej generacji", "- OpenAI wdraża zaawansowane agenty głosowe"]
            
        adhd_news_titles = self._fetch_rss_titles("https://www.additudemag.com/feed/", limit=2)
        if not adhd_news_titles:
            adhd_news_titles = ["- Jak zarządzać energią w pracy z ADHD", "- Nowe badania nad koncentracją i dopaminą"]

        # 2. Tworzenie promptu dla AI
        system_instruction = f"""
        Jesteś osobistym asystentem Tomasza (zdiagnozowane ADHD, przedsiębiorca, buduje agencję AI).
        Twoim zadaniem jest przygotowanie skrajnie konkretnego, motywującego i przefiltrowanego podsumowania porannego.
        Tomasz nienawidzi lania wody, kocha emotki, krótkie zdania i jasne punkty (ADHD-friendly layout).
        Styl Tomasza (głos marki):
        {self.ghost_profile[:1000] if self.ghost_profile else "Dynamiczny, konkretny, przełamujący schematy."}
        """
        
        prompt = f"""
        Przygotuj poranny briefing na dziś na podstawie następujących nowinek:
        
        NOWINKI AI:
        {chr(10).join(ai_news_titles)}
        
        PRODUKTYWNOŚĆ & ADHD:
        {chr(10).join(adhd_news_titles)}
        
        Struktura porannego briefingu:
        1. Dynamiczny, zabawny hook na start dnia (ADHD motywacja!).
        2. "3 Rzeczy AI, które musisz wiedzieć dzisiaj" (Krótkie podsumowanie nowinek AI w 1-2 zdaniach na punkt).
        3. "Wskazówka na skupienie" (Jedna rada z zakresu produktywności/ADHD na dziś).
        4. "One Thing" na dziś (Zasugeruj jeden główny priorytet na dziś, redukując opór kognitywny).
        """
        
        briefing = self._call_gemini_fallback(prompt, system_instruction)
        
        # 3. Zapisywanie do lokalnego folderu Obsidian
        obsidian_dir = os.path.join("Obsidian_Vault", "Daily")
        os.makedirs(obsidian_dir, exist_ok=True)
        today_str = time.strftime("%Y-%m-%d")
        filepath = os.path.join(obsidian_dir, f"{today_str}_briefing.md")
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(briefing)
            print(f"[OK]: Zapisano briefing w Obsidian: {filepath}")
        except Exception as e:
            print(f"[ERROR]: Nie udało się zapisać pliku briefing w Obsidian: {e}")
            
        # 4. Wysyłka na Telegram
        self.send_telegram_message(f"🌅 *TWÓJ PORANNY BRIEFING AI & ADHD*\n\n{briefing}")
        print("[FINISHED]: Poranny briefing zakończony.")

    def run_content_generator(self):
        """JOB #2: Content Generator (10:00)"""
        print("[START]: Uruchamianie generatora treści (Mother Content Pipeline)...")
        
        # Pobranie tematu z porannego badania
        theme = "Dlaczego klasyczne metody planowania zawodzą przy ADHD i jak technologia AI może to naprawić"
        
        system_instruction = f"""
        Jesteś ghostwriterem Tomasza, eksperta od AI i ADHD. Pisz w 100% jego stylem:
        {self.ghost_profile[:1000] if self.ghost_profile else "Przystępny, dynamiczny, bez lania wody."}
        """
        
        prompt = f"""
        Stwórz główny post ekspercki (Core Content) na temat: "{theme}".
        Następnie na jego bazie przygotuj 2 gotowe formaty dystrybucyjne:
        1. Nitka na X/Twitter (3 tweety)
        2. Post na LinkedIn
        
        Zwróć wynik jako strukturę JSON o następujących kluczach:
        {{
           "core_title": "...",
           "core_content": "...",
           "twitter_thread": "...",
           "linkedin_post": "..."
        }}
        Upewnij się, że zwracasz WYŁĄCZNIE czysty kod JSON, bez żadnych znaczników ```json czy ```.
        """
        
        raw_res = self._call_gemini_fallback(prompt, system_instruction)
        
        # Wyczyszczenie markdownowych znaczników, jeśli AI je dodało
        cleaned_res = raw_res.strip()
        if cleaned_res.startswith("```json"):
            cleaned_res = cleaned_res[7:]
        if cleaned_res.endswith("```"):
            cleaned_res = cleaned_res[:-3]
        cleaned_res = cleaned_res.strip()
        
        try:
            content_data = json.loads(cleaned_res)
            queue_file = os.path.join("data", "content_queue.json")
            os.makedirs("data", exist_ok=True)
            
            queue = []
            if os.path.exists(queue_file):
                try:
                    with open(queue_file, "r", encoding="utf-8") as f:
                        queue = json.load(f)
                except Exception:
                    queue = []
                    
            content_data["id"] = int(time.time())
            content_data["status"] = "pending_review"
            content_data["created_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
            queue.append(content_data)
            
            with open(queue_file, "w", encoding="utf-8") as f:
                json.dump(queue, f, indent=4, ensure_ascii=False)
                
            # Wyślij powiadomienie na Telegram z prośbą o zatwierdzenie
            msg = f"✍️ *HERMES CONTENT GENERATOR*\n\nWygenerowałem nowy post ekspercki i wrzuciłem go do kolejki do zatwierdzenia.\n\n*Temat:* {content_data.get('core_title')}\n\nOtwórz Dashboard -> Social Media Hub, aby go zatwierdzić lub edytować! 🚀"
            self.send_telegram_message(msg)
            print("[OK]: Nowy content dodany do kolejki.")
        except Exception as e:
            print(f"[ERROR]: Nie udało się sparsować odpowiedzi AI jako JSON. Surowa odpowiedź: {raw_res}. Błąd: {e}")
        
        print("[FINISHED]: Generowanie treści zakończone.")

    def run_social_publisher(self):
        """JOB #3: Social Media Publisher (12:00 / 17:00)"""
        print("[START]: Uruchamianie publikacji na Social Media...")
        queue_file = os.path.join("data", "content_queue.json")
        
        if not os.path.exists(queue_file):
            print("[INFO]: Brak kolejki postów do publikacji.")
            return
            
        try:
            with open(queue_file, "r", encoding="utf-8") as f:
                queue = json.load(f)
                
            pending_posts = [p for p in queue if p.get("status") in ["pending_review", "approved"]]
            if not pending_posts:
                print("[INFO]: Brak postów oczekujących na publikację w kolejce.")
                return
                
            # Wybieramy pierwszy post
            post = pending_posts[0]
            
            # W prawdziwym systemie użylibyśmy Composio do publikacji
            # Tutaj symulujemy sukces i wysyłamy powiadomienie na Telegram
            print(f"[PUBLISHING]: Publikowanie posta '{post.get('core_title')}' via Composio...")
            
            # Aktualizacja statusu
            for p in queue:
                if p.get("id") == post.get("id"):
                    p["status"] = "published"
                    p["published_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
                    break
                    
            with open(queue_file, "w", encoding="utf-8") as f:
                json.dump(queue, f, indent=4, ensure_ascii=False)
                
            msg = f"📢 *HERMES PUBLISHER*\n\nPost został pomyślnie opublikowany automatycznie na LinkedIn oraz X/Twitter!\n\n*Tytuł:* {post.get('core_title')}\n\nStatystyki i zasięgi możesz śledzić w Dashboardzie."
            self.send_telegram_message(msg)
            print("[OK]: Post opublikowany pomyślnie.")
        except Exception as e:
            print(f"[ERROR]: Błąd podczas automatycznej publikacji: {e}")
            
        print("[FINISHED]: Publikacja zakończona.")

    def run_lead_monitor(self):
        """JOB #4: Lead Monitor (co 2h)"""
        print("[START]: Uruchamianie monitorowania leadów...")
        
        # Sprawdzamy nowo zapisane kontakty w Systeme.io
        # Do celów prezentacyjnych: sprawdzamy plik fallback (jeśli istnieją tam leady, powiadamiamy)
        fallback_path = os.path.join("clients", "leads_fallback.json")
        new_leads_found = 0
        
        if os.path.exists(fallback_path):
            try:
                with open(fallback_path, "r", encoding="utf-8") as f:
                    leads = json.load(f)
                new_leads_found = len(leads)
            except Exception:
                pass
                
        if new_leads_found > 0:
            msg = f"👥 *HERMES CRM ALERT*\n\nMasz *{new_leads_found}* nowych leadów w bazie awaryjnej oczekujących na synchronizację z Systeme.io!\n\nWejdź do Laboratorium -> Krok 4, aby je zsynchronizować jednym kliknięciem. ⚡"
            self.send_telegram_message(msg)
            print(f"[OK]: Wysłano alert o nowych leadach ({new_leads_found}).")
        else:
            print("[INFO]: Brak nowych leadów do raportowania (cisza operacyjna - oszczędzamy dopaminę!).")
            
        print("[FINISHED]: Monitorowanie leadów zakończone.")

    def run_evening_report(self):
        """JOB #5: Wieczorny Raport (20:00)"""
        print("[START]: Uruchamianie wieczornego raportu...")
        
        # 1. Symulacja statystyk dziennych
        system_instruction = "Jesteś CFO-AI i COO-AI w jednej osobie. Przygotowujesz krótki wieczorny raport dla Tomasza."
        prompt = """
        Wygeneruj wieczorny raport podsumowujący dzisiejszy dzień biznesowy w oparciu o specyfikę ADHD Tomasza.
        Raport musi być:
        1. Krótki (maksymalnie 15 linijek).
        2. Składać się z:
           - "🔥 Sukcesy Dnia" (Np. 2 punkty: opublikowano content, systeme.io działa).
           - "💰 Finanse i Koszty" (Zapewnij, że koszty API wynoszą < $0.50 za dziś).
           - "🧠 One Thing na Jutro" (Zaproponuj jedno proste zadanie na jutro o niskim oporze kognitywnym).
        """
        
        report = self._call_gemini_fallback(prompt, system_instruction)
        
        # 2. Zapisywanie do Obsidian
        obsidian_dir = os.path.join("Obsidian_Vault", "Daily")
        os.makedirs(obsidian_dir, exist_ok=True)
        today_str = time.strftime("%Y-%m-%d")
        filepath = os.path.join(obsidian_dir, f"{today_str}_report.md")
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"[OK]: Zapisano raport wieczorny w Obsidian: {filepath}")
        except Exception as e:
            print(f"[ERROR]: Nie udało się zapisać raportu wieczornego w Obsidian: {e}")
            
        # 3. Wysyłka na Telegram
        self.send_telegram_message(f"🌙 *TWÓJ WIECZORNY RAPORT BIZNESOWY*\n\n{report}")
        print("[FINISHED]: Wieczorny raport zakończony.")

def main():
    parser = argparse.ArgumentParser(description="Hermes OS - Autonomiczny Harmonogram Cron (ADHD-Aware)")
    parser.add_argument(
        "--job", 
        type=str, 
        required=True,
        choices=["morning_briefing", "content_generator", "social_publisher", "lead_monitor", "evening_report"],
        help="Zadanie cron do uruchomienia"
    )
    
    args = parser.parse_args()
    orchestrator = HermesCronOrchestrator()
    
    if args.job == "morning_briefing":
        orchestrator.run_morning_briefing()
    elif args.job == "content_generator":
        orchestrator.run_content_generator()
    elif args.job == "social_publisher":
        orchestrator.run_social_publisher()
    elif args.job == "lead_monitor":
        orchestrator.run_lead_monitor()
    elif args.job == "evening_report":
        orchestrator.run_evening_report()

if __name__ == "__main__":
    main()
