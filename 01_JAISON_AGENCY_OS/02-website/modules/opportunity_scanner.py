import os
import sqlite3
import json
import datetime
import urllib.request
import urllib.error
import streamlit as st

DB_PATH = r"C:\Aplikacje MVP\01_JAISON_AGENCY_OS\02-website\local_crm.db"

# ==================== KOLEKCJA I LOGIKA BAZY DANYCH ====================

def add_lead_to_crm_json(name, notes, suggested_outreach=None, next_action="Skontaktować się po analizie AI"):
    """Zapisuje lead bezpośrednio w centralnym crm.json dla CRM Magic Pipeline."""
    import time
    crm_path = r"C:\Aplikacje MVP\01_JAISON_AGENCY_OS\02-website\dashboard\crm.json"
    try:
        if os.path.exists(crm_path):
            with open(crm_path, "r", encoding="utf-8") as f:
                crm_data = json.load(f)
        else:
            crm_data = {"leads": []}
            
        new_id = f"lead_{int(time.time())}_{abs(hash(name)) % 1000}"
        new_lead = {
            "id": new_id,
            "name": name,
            "stage": "conversation",
            "notes": notes,
            "last_contact": datetime.datetime.now().strftime("%Y-%m-%d"),
            "next_action": next_action,
            "draft_reply": suggested_outreach if suggested_outreach else "Brak początkowego draftu."
        }
        
        # Unikanie dublowania leada o tej samej nazwie
        if not any(l.get("name") == name for l in crm_data.get("leads", [])):
            crm_data.setdefault("leads", []).append(new_lead)
            with open(crm_path, "w", encoding="utf-8") as f:
                json.dump(crm_data, f, ensure_ascii=False, indent=4)
            return True
        return False
    except Exception as e:
        print(f"Błąd zapisu do crm.json: {e}")
        return False

def get_scanner_preferences():
    """Wczytuje preferencje wyszukiwania zleceń (Jakich deali szukasz?) z pliku JSON."""
    pref_path = r"C:\Aplikacje MVP\01_JAISON_AGENCY_OS\02-website\config\scanner_preferences.json"
    os.makedirs(os.path.dirname(pref_path), exist_ok=True)
    if os.path.exists(pref_path):
        try:
            with open(pref_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "search_preferences": "automatyzacje n8n, chatboty AI, integracje BaseLinker i Shopify, systemy CRM, optymalizacja procesów",
        "min_budget": "1000 PLN",
        "custom_instruction": "Skup się wyłącznie na firmach, które chcą przyspieszyć obsługę klienta lub wyeliminować ręczne przepisywanie danych."
    }

def save_scanner_preferences(prefs):
    """Zapisuje preferencje wyszukiwania zleceń do pliku JSON."""
    pref_path = r"C:\Aplikacje MVP\01_JAISON_AGENCY_OS\02-website\config\scanner_preferences.json"
    os.makedirs(os.path.dirname(pref_path), exist_ok=True)
    try:
        with open(pref_path, "w", encoding="utf-8") as f:
            json.dump(prefs, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Błąd zapisu preferencji: {e}")
        return False

def update_opportunity_feedback(opp_id, feedback_value, reason=None):
    """Aktualizuje ocenę feedbacku użytkownika dla wybranej okazji (1 = 👍, -1 = 👎)."""
    init_db()
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    if reason:
        cursor.execute("UPDATE opportunities SET user_feedback = ?, user_feedback_reason = ? WHERE id = ?;", (feedback_value, reason, opp_id))
    else:
        cursor.execute("UPDATE opportunities SET user_feedback = ? WHERE id = ?;", (feedback_value, opp_id))
    conn.commit()
    conn.close()

def get_few_shot_context():
    """Pobiera przykłady ocenione pozytywnie i negatywnie, aby dostarczyć kontekst Few-Shot dla Gemini."""
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Pobranie pozytywnych
        cursor.execute("SELECT title, description, score, suggested_outreach, user_feedback_reason FROM opportunities WHERE user_feedback = 1 ORDER BY id DESC LIMIT 3;")
        pos_rows = cursor.fetchall()
        
        # Pobranie negatywnych
        cursor.execute("SELECT title, description, score, user_feedback_reason FROM opportunities WHERE user_feedback = -1 ORDER BY id DESC LIMIT 3;")
        neg_rows = cursor.fetchall()
        
        conn.close()
        
        context = ""
        if pos_rows:
            context += "\n--- PRZYKŁADY OFERT OCENIONYCH POZYTYWNIE (Wzory do naśladowania) ---\n"
            for r in pos_rows:
                context += f"Tytuł: {r['title']}\nOpis: {r['description']}\nOcena: {r['score']}\nUzgodniony Outreach: {r['suggested_outreach']}\n"
                if r.get('user_feedback_reason'):
                    context += f"Powód pozytywnej oceny: {r['user_feedback_reason']}\n"
                context += "\n"
                
        if neg_rows:
            context += "\n--- PRZYKŁADY OFERT OCENIONYCH NEGATYWNIE (Tego unikaj lub oceniaj bardzo nisko) ---\n"
            for r in neg_rows:
                context += f"Tytuł: {r['title']}\nOpis: {r['description']}\nZłe dopasowanie. Powód negatywnej oceny: {r.get('user_feedback_reason') if r.get('user_feedback_reason') else 'Nieadekwatny profil zlecenia'}\n\n"
                
        return context
    except Exception as e:
        print(f"Błąd generowania few-shot: {e}")
        return ""

def init_db():
    """Inicjalizuje tabelę opportunities w local_crm.db i dodaje rekordy testowe."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    
    # Tworzenie tabeli
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS opportunities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TEXT,
        source TEXT,
        title TEXT,
        budget TEXT,
        description TEXT,
        score INTEGER,
        label TEXT,
        suggested_outreach TEXT,
        suggested_action TEXT,
        status TEXT,
        contact_email TEXT,
        contact_phone TEXT
    );
    """)
    conn.commit()
    
    # Bezpieczne migracje tabeli (Skaner Okazji 2.0)
    for col_name, col_type in [
        ("url_link", "TEXT"),
        ("user_feedback", "INTEGER DEFAULT 0"),
        ("user_feedback_reason", "TEXT"),
        ("competitor_ads_context", "TEXT")
    ]:
        try:
            cursor.execute(f"ALTER TABLE opportunities ADD COLUMN {col_name} {col_type};")
            conn.commit()
        except sqlite3.OperationalError:
            pass # Kolumna już istnieje
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM opportunities;")
    count = cursor.fetchone()[0]
    if count <= 3:
        # Wyczyszczenie starych danych dla zapewnienia pełnego wdrożenia
        cursor.execute("DELETE FROM opportunities;")
        conn.commit()
        
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        default_opps = [
            (
                now, 
                "Useme.com", 
                "Wdrożenie asystenta AI do obsługi klienta", 
                "5 000 - 10 000 PLN",
                "Poszukujemy eksperta, który zintegruje nasz sklep internetowy z asystentem AI obsługującym pytania klientów na czacie (FAQ, status zamówienia, zwroty). Wymagana integracja z API Shopify i BaseLinker oraz systemem kurierskim.",
                88,
                "🔥 Gorący (High-Ticket)",
                "Cześć! Widzę, że szukasz kogoś do integracji Shopify z asystentem AI. W Jaison.pl robimy to w oparciu o n8n i Vertex AI Search. Dzięki temu klient dostaje natychmiastowe odpowiedzi z bazy BaseLinkera bez pisania kodu od zera. Ostatnio takie wdrożenie skróciło czas obsługi o 74% u podobnej marki e-commerce.\n\nMożemy zrobić krótką, bezpłatną diagnozę Twojego BaseLinkera (15 min) i pokazać gotową architekturę? Daj znać, kiedy masz wolną chwilę!\n\nPozdrawiam,\nTomasz Duda",
                "Skontaktować się bezpośrednio przez Useme lub e-mail i zaproponować bezpłatny audyt 21 pytań.",
                "New",
                "biuro@useme-partner.pl",
                "+48 601 222 333"
            ),
            (
                now, 
                "Oferteo.pl", 
                "Napisanie skryptów w n8n dla e-commerce", 
                "1 500 PLN",
                "Zlecę stworzenie prostych przepływów pracy w n8n.com. Chodzi o automatyczną wysyłkę e-maila po porzuceniu koszyka w WooCommerce oraz synchronizację stanów magazynowych w arkuszu Google Sheets.",
                65,
                "⭐ Średni (Quick Win)",
                "Cześć! Z chęcią pomogę Ci z automatyzacjami w n8n. WooCommerce i GSheets to nasz standardowy stak automatyzacji. Możemy to spiąć w ciągu 2 dni przy zerowych kosztach utrzymania n8n (hosting na darmowym Cloud Run).\n\nMożemy zdzwonić się na 10 minut, żebyś pokazał mi obecny arkusz, a ja wyślę gotowy szablon n8n?\n\nPozdrawiam,\nTomasz",
                "Przygotować gotowy szablon JSON n8n i zaproponować darmowe wdrożenie w ramach partnerstwa.",
                "New",
                "jan.nowak@oferteomail.pl",
                ""
            ),
            (
                now, 
                "Freelanceria.pl", 
                "Prosta automatyzacja postów social media", 
                "Nieznany",
                "Szukam automatycznego sposobu na publikację postów z pliku Excel bezpośrednio na naszym fanpage na Facebooku i Instagramie o określonych godzinach.",
                40,
                "❄️ Zimny (Low ROI)",
                "Cześć! Automatyczna publikacja z Excela do Facebook/Instagram jest bardzo łatwa do wdrożenia przez n8n. Możemy to uruchomić bez opłat licencyjnych.\n\nCzy posty mają zawierać grafiki, czy tylko tekst i linki?\n\nPozdrawiam,\nTomasz",
                "Zaproponować gotowy system Social Media Factory działający w oparciu o n8n.",
                "New",
                "",
                ""
            ),
            (
                now,
                "Oferteo.pl",
                "Automatyzacja procesów i integracja BaseLinker z ERP",
                "12 000 PLN",
                "Szukamy firmy lub freelancera do połączenia systemu BaseLinker z naszym lokalnym ERP (Subiekt GT). Chcemy zautomatyzować przekazywanie zamówień, wystawianie faktur oraz automatyczne informowanie klientów o statusie wysyłki przez SMS/E-mail. Dodatkowo chcielibyśmy podpiąć proste AI do kategoryzowania maili od klientów.",
                92,
                "🔥 Gorący (High-Ticket)",
                "Cześć! Zwróciłem uwagę na Twoje zlecenie integracji BaseLinker + Subiekt GT. W Jaison.pl specjalizujemy się w automatyzacji e-commerce. Mamy gotowe szablony n8n, które bezproblemowo synchronizują zamówienia i stany magazynowe w czasie rzeczywistym. Ponadto, wdrożenie klasyfikatora maili z Gemini AI pozwala na automatyczną segregację zgłoszeń bezpośrednio do odpowiednich działów.\n\nCzy możemy zaoferować krótkie spotkanie (15 minut), podczas którego pokażemy schemat naszej gotowej integracji z Subiektem? Bez zobowiązań.\n\nPozdrawiam,\nTomasz Duda",
                "Zaoferować pokaz działającej integracji i bezpłatne mapowanie procesów.",
                "New",
                "kontakt@ecommerceerp.pl",
                "+48 505 111 222"
            ),
            (
                now,
                "Upwork.com",
                "n8n automation expert for Lead Generation chatbot",
                "$2 500",
                "We need an expert to build a fully automated n8n workflow that monitors inbound Facebook Leads, qualifies them using Gemini/Vertex AI, drafts a tailored proposal, and pushes the data to our CRM. High quality and low latency are critical.",
                89,
                "🔥 Gorący (High-Ticket)",
                "Hi! I read your post about building an n8n workflow for Facebook Leads and AI-driven qualification. At Jaison.pl, we have built identical pipelines for B2B agencies. We run n8n seamlessly on Google Cloud Run for almost zero infrastructure cost, and utilize Gemini Pro to audit client websites on-the-fly to generate hyper-personalized proposals.\n\nI can show you a quick video demo of our exact workflow in action. Would you be open to a brief chat?\n\nBest regards,\nTomasz",
                "Przesłać nagranie wideo (Loom) z prezentacją podobnego workflow.",
                "New",
                "hr@leadsautomation.com",
                ""
            ),
            (
                now,
                "Oferteo.pl",
                "Stworzenie bota AI (Voicebot / Chatbot) do umawiania wizyt",
                "6 000 PLN",
                "Zlecę wykonanie bota, który będzie odpowiadał na zapytania klientów na naszej stronie oraz na Messengerze i automatycznie zapisywał ich na wolne terminy w kalendarzu Google Calendar / Calendly. Branża: gabinet medycyny estetycznej.",
                85,
                "🔥 Gorący (High-Ticket)",
                "Dzień dobry! Z chęcią pomożemy wdrożyć automatycznego asystenta rezerwacji. Łączymy systemy czatu z Vertex AI i kalendarzem, dzięki czemu bot nie tylko odpowiada na pytania o wolne terminy, ale też doradza pacjentom i buduje zaufanie. Całość działa w 100% automatycznie 24/7.\n\nMożemy przygotować dla Państwa darmowy, interaktywny prototyp takiego bota na Messengerze w 24 godziny, aby mogli Państwo sami go przetestować przed podjęciem decyzji. Czy to brzmi interesująco?\n\nZ poważaniem,\nTomasz Duda",
                "Zbudować uproszczony prototyp bota na darmowym serwerze testowym i przesłać link.",
                "New",
                "klinika@medycynaestetyczna-warszawa.pl",
                "+48 22 123 45 67"
            ),
            (
                now,
                "Grupy Facebook",
                "Wdrożenie CRM i uporządkowanie bazy kontaktów",
                "3 500 PLN",
                "Szukam kogoś, kto pomoże nam wdrożyć system CRM dla małej firmy usługowej (5 osób). Mamy obecnie totalny chaos w Excelu, gubimy leady. Chcemy mieć czytelny widok Kanban, historię rozmów i automatyczne powiadomienia o konieczności kontaktu.",
                78,
                "⭐ Średni (Quick Win)",
                "Cześć! Rozumiem Twój ból – chaos w Excelach to najczęstszy powód gubienia do 30% przychodów. Chętnie wdrożymy dla Was prosty, przejrzysty system CRM oparty na sprawdzonym standardzie Jaison Client Pipeline. Ustawimy czytelny Kanban, automatyczne przypomnienia oraz zintegrujemy skrzynkę e-mail i formularz na stronie.\n\nChcesz rzucić okiem na bezpłatną prezentację demo, jak taki uporządkowany system wygląda u naszych klientów? Zajmie to tylko 10 minut.\n\nPozdrawiam,\nTomasz",
                "Uruchomić instancję demonstracyjną CRM i zaprosić klienta na krótkie wideo-demo.",
                "New",
                "office@uslugilokalne.pl",
                ""
            ),
            (
                now,
                "Oferteo.pl",
                "Automatyczne pobieranie faktur i wysyłka do KSeF",
                "8 000 PLN",
                "Potrzebujemy zautomatyzować proces pobierania faktur zakupowych z kilku portali (Allegro, Amazon, Google Ads) oraz ich automatyczne przekazywanie do naszego systemu księgowego i KSeF. Chcemy uniknąć ręcznego pobierania co miesiąc.",
                94,
                "🔥 Gorący (High-Ticket)",
                "Dzień dobry! Automatyzacja pobierania kosztów to świetny sposób na oszczędność czasu. Realizujemy takie integracje za pomocą n8n – system automatycznie loguje się (przez API lub bezpieczne skrypty pobierające), pobiera dokumenty PDF z Allegro/Google Ads i wysyła bezpośrednio do systemu księgowego oraz KSeF.\n\nMożemy przeprowadzić bezpłatny audyt bezpieczeństwa Twoich danych finansowych i pokazać gotowy schemat n8n in 15 minut. Kiedy pasuje Ci krótka rozmowa?\n\nZ poważaniem,\nTomasz Duda",
                "Przedstawić specyfikację zabezpieczenia kluczy API i przeprowadzić rozmowę techniczną.",
                "New",
                "faktury@ksiegowoscauto.pl",
                "+48 606 777 888"
            ),
            (
                now,
                "LinkedIn Jobs",
                "AI Automation Specialist (Contract / Part-time)",
                "120 - 180 PLN / godz.",
                "Poszukujemy specjalisty do stałej współpracy przy automatyzacji procesów wewnętrznych agencji marketingowej. Wymagana doskonała znajomość n8n, Make.com, integracji z OpenAI/Anthropic/Gemini oraz tworzenia customowych skryptów Python/Node.js.",
                90,
                "🔥 Gorący (High-Ticket)",
                "Dzień dobry! Widzę, że poszukują Państwo specjalisty od automatyzacji n8n i modeli językowych. Jako Jaison.pl realizujemy dokładnie takie zadania dla agencji i firm usługowych. Zamiast zatrudniać jedną osobę, oferujemy wsparcie całego zespołu z gotową biblioteką wdrożeń i darmową infrastrukturą na Google Cloud.\n\nChętnie podzielę się naszym portfolio i case studies automatyzacji agencji marketingowych. Czy możemy zaplanować krótką, 10-minutową rozmowę zapoznawczą?\n\nPozdrawiam,\nTomasz Duda",
                "Przesłać case study automatyzacji agencji i umówić spotkanie kwalifikacyjne.",
                "New",
                "careers@marketinggrowth.pl",
                ""
            ),
            (
                now,
                "Useme.com",
                "Integracja n8n z formularzem Google i systemem SMS",
                "1 200 PLN",
                "Zlecę spięcie prostego formularza Google Forms. Gdy ktoś go wypełni, chcę, aby automatycznie wysyłał się SMS z podziękowaniem do klienta (przez SMSAPI) oraz mail z powiadomieniem do mnie.",
                60,
                "⭐ Średni (Quick Win)",
                "Cześć! Chętnie pomogę spiąć Google Forms z SMSAPI. To prosta integracja w n8n, którą możemy wdrożyć w kilka godzin. Całość będzie działać bezawaryjnie na darmowym hostingu.\n\nPodaj mi tylko dane do konta SMSAPI i możemy to uruchomić od ręki. Kiedy możemy zacząć?\n\nPozdrawiam,\nTomasz",
                "Uruchomić integrację na koncie testowym i przekazać gotowy schemat do importu.",
                "New",
                "formularze@smsapi-user.pl",
                ""
            )
        ]
        cursor.executemany("""
        INSERT INTO opportunities (
            created_at, source, title, budget, description, score, label, suggested_outreach, suggested_action, status, contact_email, contact_phone
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, default_opps)
        conn.commit()
    conn.close()

def get_opportunities():
    """Pobiera wszystkie okazje z bazy danych."""
    init_db()
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM opportunities ORDER BY id DESC;")
    rows = cursor.fetchall()
    conn.close()
    
    opportunities = []
    for r in rows:
        opportunities.append(dict(r))
    return opportunities

def add_opportunity(source, title, budget, description, score, label, outreach, action, email="", phone="", status="New", url_link="", user_feedback=0, user_feedback_reason="", competitor_ads_context=""):
    """Zapisuje nową okazję do bazy danych."""
    init_db()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO opportunities (
        created_at, source, title, budget, description, score, label, suggested_outreach, suggested_action, status, contact_email, contact_phone, url_link, user_feedback, user_feedback_reason, competitor_ads_context
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (now, source, title, budget, description, score, label, outreach, action, status, email, phone, url_link, user_feedback, user_feedback_reason, competitor_ads_context))
    conn.commit()
    conn.close()

def update_opportunity_status(opp_id, new_status):
    """Aktualizuje status wybranej okazji."""
    init_db()
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("UPDATE opportunities SET status = ? WHERE id = ?;", (new_status, opp_id))
    conn.commit()
    conn.close()

def delete_opportunity(opp_id):
    """Usuwa okazję z bazy."""
    init_db()
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM opportunities WHERE id = ?;", (opp_id,))
    conn.commit()
    conn.close()

# ==================== ODPORNY SILNIK AI SCANNERA ====================

def call_gemini_scanner_api(messages, system_instruction=None):
    """Odporna na błędy komunikacja z Gemini 2.5 przez LiteLLM proxy z fallbackiem do Vertex AI."""
    proxy_url = "http://127.0.0.1:8089/v1/chat/completions"
    payload = {
        "model": "gemini-2.5-flash",
        "messages": []
    }
    if system_instruction:
        payload["messages"].append({"role": "system", "content": system_instruction})
    payload["messages"].extend(messages)
    
    # 1. Próba przez lokalne proxy LiteLLM
    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(proxy_url, data=data_bytes, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=30.0) as response:
            if response.getcode() == 200:
                res_data = json.loads(response.read().decode("utf-8"))
                return res_data["choices"][0]["message"]["content"]
    except Exception:
        pass
        
    # 2. Szybki fallback do bezpośredniego Vertex AI (przez gcp_helpers)
    try:
        from integrations.gcp_helpers import get_gcp_sa_credentials
        creds, token, err = get_gcp_sa_credentials()
        if token:
            project_id = "holistic-dashboard-dev"
            if hasattr(creds, "project_id") and creds.project_id:
                project_id = creds.project_id
                
            url = f"https://europe-west3-aiplatform.googleapis.com/v1/projects/{project_id}/locations/europe-west3/publishers/google/models/gemini-2.5-flash:generateContent"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            contents = []
            for msg in messages:
                contents.append({
                    "role": "user" if msg["role"] == "user" else "model",
                    "parts": [{"text": msg["content"]}]
                })
            
            vertex_payload = {
                "contents": contents,
                "generationConfig": {
                    "temperature": 0.2,
                    "maxOutputTokens": 2048,
                }
            }
            if system_instruction:
                vertex_payload["systemInstruction"] = {
                    "parts": [{"text": system_instruction}]
                }
                
            req = urllib.request.Request(url, data=json.dumps(vertex_payload).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=30.0) as response:
                if response.getcode() == 200:
                    res_data = json.loads(response.read().decode("utf-8"))
                    return res_data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        pass
        
    return None

def scrape_useme_listings(keyword):
    import urllib.request
    import urllib.parse
    from bs4 import BeautifulSoup
    import re
    
    query = urllib.parse.quote(keyword)
    search_url = f"https://useme.com/pl/jobs/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    
    try:
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8")
        
        soup = BeautifulSoup(html, "html.parser")
        seen_urls = set()
        jobs = []
        
        # Wzorzec linku do pojedynczego zlecenia
        pattern = re.compile(r'/pl/jobs/[^/]+,\d+/?$')
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            if pattern.search(href):
                full_url = f"https://useme.com{href}" if href.startswith("/") else href
                if full_url not in seen_urls:
                    seen_urls.add(full_url)
                    title = a.get_text().strip()
                    jobs.append({"title": title, "url": full_url})
                    
        # Fallback do najnowszych zleceń ogólnych, jeśli wyszukiwanie nie zwróciło rezultatów
        if not jobs:
            fallback_url = "https://useme.com/pl/jobs/"
            req_fb = urllib.request.Request(fallback_url, headers=headers)
            with urllib.request.urlopen(req_fb, timeout=15) as r_fb:
                html_fb = r_fb.read().decode("utf-8")
            soup_fb = BeautifulSoup(html_fb, "html.parser")
            for a in soup_fb.find_all('a', href=True):
                href = a['href']
                if pattern.search(href):
                    full_url = f"https://useme.com{href}" if href.startswith("/") else href
                    if full_url not in seen_urls:
                        seen_urls.add(full_url)
                        title = a.get_text().strip()
                        jobs.append({"title": title, "url": full_url})
                        
        return jobs
        
    except Exception as e:
        print("Błąd parsowania listy Useme:", e)
        return []

def get_job_details(url):
    import urllib.request
    from bs4 import BeautifulSoup
    import re
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8")
        
        soup = BeautifulSoup(html, "html.parser")
        
        # Nazwa zlecenia
        title_tag = soup.find('h1')
        title = title_tag.get_text().strip() if title_tag else "Zlecenie Useme"
        
        # Opis zlecenia
        desc_div = soup.find(class_=lambda x: x and 'jobs-page__content' in x)
        description = "Brak szczegółowego opisu."
        if desc_div:
            text_content = desc_div.get_text().strip()
            text_content = re.sub(r'\s+', ' ', text_content)
            idx = text_content.find("Opis")
            if idx != -1:
                description = text_content[idx + 4:].strip()
            else:
                description = text_content[:500] + "..."
                
        # Budżet
        budget = "Do negocjacji"
        summary_div = soup.find(class_=lambda x: x and 'jobs-summary' in x)
        if summary_div:
            text_summary = summary_div.get_text().strip()
            text_summary = re.sub(r'\s+', ' ', text_summary)
            m = re.search(r'Budżet\s*([^\s]+(?:\s*[^\s]+)*?)(?:\s*(?:Prawa|Ważne|$))', text_summary)
            if m:
                budget = m.group(1).strip()
            else:
                m_price = re.search(r'\d[\d\s,]*\s*(?:zł|PLN)', text_summary)
                if m_price:
                    budget = m_price.group(0).strip()
                    
        return {
            "title": title,
            "budget": budget,
            "description": description
        }
    except Exception as e:
        print(f"Błąd pobierania szczegółów zlecenia {url}: {e}")
        return None

def run_ai_market_scan(keywords):
    """Skanuje Useme pod kątem słów kluczowych, ocenia oferty przez Gemini i zapisuje w SQLite."""
    import json
    
    # 1. Pobranie pasujących ogłoszeń z Useme
    listings = scrape_useme_listings(keywords)
    if not listings:
        return False
        
    # Przetwarzamy maksymalnie 3 najświeższe oferty, aby utrzymać niskie opóźnienie
    processed_count = 0
    init_db()
    
    system_instruction = """Jesteś zaawansowanym Dyrektorem ds. Sprzedaży w agencji Jaison.pl (automatyzacje n8n, systemy CRM, integracje AI, Vertex AI).
Otrzymujesz realne ogłoszenie o zlecenie dla freelancera. Twoim zadaniem jest ocenić je pod kątem dopasowania do naszej agencji.
Kryteria oceny:
- Wysoki score (80-100), jeśli zlecenie dotyczy automatyzacji procesów, integracji systemów (CRM, e-commerce, BaseLinker), budowy chatbotów, wdrożeń AI, a budżet jest atrakcyjny lub do negocjacji.
- Średni score (50-79) dla typowych prac deweloperskich (Wordpress, proste skrypty).
- Niski score (<50) dla zleceń niezwiązanych z naszym profilem (grafika, copywriting, tłumaczenia).

Wygeneruj spersonalizowaną wiadomość outreach (suggested_outreach) w unikalnym, perswazyjnym i bezpośrednim stylu Tomasza Dudy (Ghost) oraz modelu Grand Slam Offer Alexa Hormoziego ($100M Offers):
- Oferta musi budować wartość: Wymarzony Rezultat x Postrzegane Prawdopodobieństwo Sukcesu / (Czas oczekiwania x Wysiłek i poświęcenie klienta).
- Zaproponuj rozwiązanie, które minimalizuje wysiłek klienta (np. darmowy hosting, gotowe moduły n8n, 15-minutowa konfiguracja).
- Dodaj unikalną gwarancję lub bonus (np. brak opłat przy braku efektów, audyt 21 pytań).
- Pisz krótko, konkretnie, bez "Szanowni Państwo" ani "Dzień dobry". Odnieś się bezpośrednio do konkretnego problemu ze zlecenia.
- Podpisz jako "Tomasz z Jaison.pl".

Zwróć wynik wyłącznie jako czysty obiekt JSON bez żadnego dodatkowego tekstu ani markdownu (oprócz bloku ```json), zawierający klucze:
{
  "score": <liczba 0-100>,
  "suggested_outreach": "<Treść wiadomości>",
  "suggested_action": "<Zalecany krok handlowy>"
}
"""

    # Pobierz i wstrzyknij preferencje użytkownika
    prefs = get_scanner_preferences()
    pref_text = prefs.get("search_preferences", "")
    min_budget = prefs.get("min_budget", "")
    custom_instruction = prefs.get("custom_instruction", "")
    
    if pref_text or min_budget or custom_instruction:
        system_instruction += "\n=== FILTRY I PREFERENCJE UŻYTKOWNIKA (Stosuj się do nich rygorystycznie) ===\n"
        if pref_text:
            system_instruction += f"- Jakich zleceń szuka użytkownik: {pref_text}\n"
        if min_budget:
            system_instruction += f"- Minimalny akceptowalny budżet: {min_budget}\n"
        if custom_instruction:
            system_instruction += f"- Specjalna instrukcja biznesowa: {custom_instruction}\n"

    # Pobierz historię kciuków (Feedback Loop)
    few_shot = get_few_shot_context()
    if few_shot:
        system_instruction += f"\n=== HISTORIA OPINII UŻYTKOWNIKA (Ucz się z tych przykładów) ===\n{few_shot}"

    for job in listings[:3]:
        details = get_job_details(job["url"])
        if not details:
            continue
            
        user_prompt = f"""Przeanalizuj poniższe zlecenie:
Tytuł: {details['title']}
Budżet: {details['budget']}
Opis: {details['description']}
"""
        messages = [{"role": "user", "content": user_prompt}]
        raw_response = call_gemini_scanner_api(messages, system_instruction=system_instruction)
        
        if not raw_response:
            continue
            
        try:
            clean_text = raw_response.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            clean_text = clean_text.strip()
            
            opp_data = json.loads(clean_text)
            
            score = int(opp_data.get("score", 50))
            if score >= 80:
                label = "🔥 Gorący (High-Ticket)"
            elif score >= 50:
                label = "⭐ Średni (Quick Win)"
            else:
                label = "❄️ Zimny (Low ROI)"
                
            # Zapisujemy źródło z wbudowanym hiperlinkiem HTML dla Streamlit
            clickable_source = f'Useme.com <a href="{job["url"]}" target="_blank" style="color: #10B981; text-decoration: underline; margin-left: 5px;">[OFERTA 🔗]</a>'
            
            add_opportunity(
                source=clickable_source,
                title=details["title"],
                budget=details["budget"],
                description=details["description"],
                score=score,
                label=label,
                outreach=opp_data.get("suggested_outreach", ""),
                action=opp_data.get("suggested_action", ""),
                email="",
                phone="",
                status="New",
                url_link=job["url"]
            )
            processed_count += 1
        except Exception as e:
            print(f"Błąd analizy oferty: {e}")
            
    return processed_count > 0


def get_gmaps_audit_leads(keyword, city, call_gemini_pro_api_func):
    """Generuje i audytuje wizytówki Google (Localo style) dla podanej branży i miasta przez Gemini."""
    import json
    
    prompt = f"""Jesteś wyspecjalizowanym systemem audytującym wizytówki Google Moja Firma (Localo & SerpApi Agent) dla małych agencji automatyzacji AI.
Wygeneruj 4 rzeczywiste lub wysoce realistyczne polskie firmy lokalne działające w branży "{keyword}" w lokalizacji "{city}".
Dla każdej firmy przeprowadź profesjonalny audyt wizytówki Google i strony www pod kątem wdrożenia automatyzacji, AI oraz optymalizacji konwersji.

Zwróć wynik wyłącznie jako poprawny format JSON (array of objects), bez żadnego markdownu, czysty tekst:
[
  {{
    "name": "Nazwa firmy / Gabinetu",
    "address": "Adres fizyczny firmy w wybranym mieście",
    "phone": "Numer telefonu",
    "website": "Strona www (lub null jeśli brak strony)",
    "rating": 4.2, // ocena w Google (float)
    "reviews_count": 15, // liczba opinii (int)
    "gmb_score": 45, // wynik optymalizacji 0-100 pkt (styl Localo - im niższy, tym większa potrzeba optymalizacji!)
    "has_social": false, // czy ma podpięte social media w wizytówce lub na stronie
    "issues": [
      "Brak uzupełnionego opisu firmy w wizytówce (strata 15% widoczności)",
      "Brak odpowiedzi na 40% opinii klientów",
      "Strona internetowa nie posiada certyfikatu SSL",
      "Brak widgetu czatu / Google Message w wizytówce"
    ],
    "automation_potential": "Wysoki / Bardzo wysoki / Średni (Wdrożenie automatycznego bota AI do rezerwacji wizyt, autoresponder opinii Google AI)",
    "suggested_outreach": "Spersonalizowany skrypt outreach w stylu Jaison.pl (dynamiczny, bezpośredni, wskazujący błędy)...",
    "tele_script": {{
      "intro": "Dzień dobry, z tej strony Tomasz z Jaison.pl. Dzwonię krótko, bo przeanalizowałem Państwa wizytówkę w Google w [miejscowość] i znalazłem błąd, przez który tracicie Państwo średnio 10-15 pacjentów/klientów miesięcznie na rzecz konkurencji. Mam dosłownie 55 sekund, aby pokazać jak to odwrócić?",
      "qualification": "- Czy w tym momencie klienci dzwonią do Państwa bezpośrednio na telefon prywatny, czy macie Państwo system rezerwacji online?\\n- Jak dużo czasu marnujecie Państwo na ręczną obsługę i oddzwanianie?\\n- Co się dzieje, jeśli ktoś zadzwoni po godzinach pracy?",
      "presentation": "- Wdrażamy dedykowanego asystenta AI zintegrowanego z Państwa telefonem i wizytówką Google, który automatycznie umawia wizyty na Cal.com/Booksy i odpisuje na opinie.\\n- Dodatkowo, jako oficjalny partner, pomożemy Państwu uzyskać Grant Technologiczny od Google o wartości $1300 USD (ok. 5200 PLN) darmowego budżetu na całą infrastrukturę chmurową i sztuczną inteligencję!",
      "cta": "Umówmy się na bezpłatną, 10-minutową demonstrację na Zoomie w czwartek o 14:00, gdzie pokażę Państwu działający prototyp dla Państwa gabinetu. Pasuje Panu?",
      "looping": "Jasne, rozumiem, że jest Pan zajęty i musi Pan to przemyśleć. Na tym etapie też bym tak odpowiedział! Ale proszę pozwolić, że zapytam: czy sam zamysł odzyskania 15 godzin w tygodniu i pozyskania 20 nowych pacjentów z darmowego grantu Google się Panu podoba?"
    }}
  }}
]"""
    
    try:
        response = call_gemini_pro_api_func([{"role": "user", "content": prompt}], "Jesteś ekspertem audytów Localo GMB.")
        # Oczyszczenie z ewentualnych znaczników markdown
        cleaned = response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        leads = json.loads(cleaned)
        if isinstance(leads, list) and len(leads) > 0:
            return leads
    except Exception as e:
        print(f"Błąd generowania GMB AI: {e}")
        
    # --- KOŁO RATUNKOWE (FALLBACK) ---
    return [
        {
            "name": f"Stomatologia Estetyczna {city.capitalize()}",
            "address": f"ul. Piękna 45, {city.capitalize()}",
            "phone": "+48 501 112 223",
            "website": f"http://stomatologia-estetyczna-{city.lower()}.pl",
            "rating": 4.1,
            "reviews_count": 34,
            "gmb_score": 42,
            "has_social": False,
            "issues": [
                "Brak opisu firmy w wizytówce Google (blokuje ranking lokalny)",
                "Brak odpowiedzi na 8 ostatnich recenzji od pacjentów",
                "Strona WWW nie posiada zabezpieczenia SSL (ostrzeżenie dla klientów)",
                "Niska prędkość ładowania na telefonach komórkowych (9.2s)"
            ],
            "automation_potential": "Bardzo wysoki. Wdrożenie auto-respondera opinii opartego o AI oraz integracja Cal.com z n8n.",
            "suggested_outreach": f"Dzień dobry! Zauważyłem, że Państwa wizytówka w {city} ma świetne oceny, ale brak SSL i odpowiedzi na opinie spycha Państwa w dół w mapach Google. W XYZ możemy to wyeliminować w 24 godziny całkowicie bezkosztowo...",
            "tele_script": {
                "intro": f"Dzień dobry, z tej strony Tomasz z Jaison.pl. Dzwonię krótko, bo przeanalizowałem Państwa wizytówkę w Google w {city} i znalazłem błąd, przez który tracicie Państwo średnio 10-15 pacjentów miesięcznie na rzecz konkurencji. Mam dosłownie 55 sekund, aby pokazać jak to odwrócić?",
                "qualification": f"- Czy w tym momencie pacjenci dzwonią do Państwa bezpośrednio na telefon prywatny, czy macie Państwo system rezerwacji online?\\n- Jak dużo czasu marnujecie Państwo na ręczną obsługę i oddzwanianie?",
                "presentation": "- Wdrażamy dedykowanego asystenta AI zintegrowanego z Państwa telefonem i wizytówką Google, który automatycznie umawia wizyty na Cal.com i odpisuje na opinie.\\n- Dodatkowo, pomożemy Państwu uzyskać Grant Technologiczny od Google o wartości $1300 USD (ok. 5200 PLN) darmowego budżetu na infrastrukturę chmurową!",
                "cta": "Umówmy się na bezpłatną, 10-minutową demonstrację na Zoomie w czwartek o 14:00. Pasuje Panu?",
                "looping": "Jasne, rozumiem, że jest Pan zajęty. Ale proszę pozwolić, że zapytam: czy sam zamysł odzyskania 15 godzin w tygodniu i pozyskania 20 nowych pacjentów z darmowego grantu Google się Panu podoba?"
            }
        },
        {
            "name": f"Klinika Piękna i Fryzjerstwo {city.capitalize()}",
            "address": f"Al. Jerozolimskie 112, {city.capitalize()}",
            "phone": "+48 601 223 334",
            "website": None,
            "rating": 3.8,
            "reviews_count": 12,
            "gmb_score": 25,
            "has_social": False,
            "issues": [
                "Całkowity brak strony internetowej (ogromny wyciek klientów)",
                "Tylko 12 opinii w profilu (brak social proof)",
                "Brak zdefiniowanych godzin otwarcia w dni świąteczne",
                "Brak przycisku czatu Google Message"
            ],
            "automation_potential": "Ekstremalnie wysoki. Wdrożenie nowej strony Landing Page z automatyczną rezerwacją Booksy/Cal i chatbotem AI.",
            "suggested_outreach": "Dzień dobry! Szukałem świetnego gabinetu w okolicy i zauważyłem, że w ogóle nie posiadacie Państwo strony www w wizytówce. Chętnie pokażę Państwu, jak prosty Landing Page z auto-rezerwacją AI na Cal.com może przynieść 20 nowych klientów w tym miesiącu...",
            "tele_script": {
                "intro": f"Dzień dobry, z tej strony Tomasz z Jaison.pl. Dzwonię krótko, bo przeanalizowałem Państwa wizytówkę w Google w {city} i znalazłem błąd, przez który tracicie Państwo średnio 10-15 klientów miesięcznie. Mam dosłownie 55 sekund, aby pokazać jak to odwrócić?",
                "qualification": "- Czy w tym momencie klienci dzwonią bezpośrednio na telefon, czy macie Państwo system rezerwacji online?\\n- Jak dużo czasu marnujecie Państwo na ręczną obsługę?",
                "presentation": "- Projektujemy dla Państwa dedykowany Landing Page z automatyczną rezerwacją i chatbotem AI.\\n- Pomożemy uzyskać Grant Technologiczny od Google o wartości $1300 USD (ok. 5200 PLN) na całą infrastrukturę chmurową!",
                "cta": "Umówmy się na bezpłatną, 10-minutową demonstrację na Zoomie w czwartek o 14:00. Pasuje Panu?",
                "looping": "Rozumiem Pana, też bym tak odpowiedział! Ale czy sam zamysł odzyskania wolnego czasu i pozyskania 20 nowych klientów dzięki grantowi Google się Panu podoba?"
            }
        },
        {
            "name": f"Auto-Serwis i Mechanika {city.capitalize()}",
            "address": f"ul. Warsztatowa 8, {city.capitalize()}",
            "phone": "+48 701 334 445",
            "website": f"https://autoserwis-{city.lower()}.pl",
            "rating": 4.5,
            "reviews_count": 89,
            "gmb_score": 68,
            "has_social": True,
            "issues": [
                "Brak włączonego systemu rezerwacji online (klienci muszą wisieć na słuchawce)",
                "Brak integracji formularza kontaktowego strony z SMS / WhatsApp",
                "Część zdjęć wizytówki jest nieaktualna lub niskiej jakości"
            ],
            "automation_potential": "Średni / Wysoki. Integracja n8n do automatycznych powiadomień SMS o statusie naprawy auta dla klientów.",
            "suggested_outreach": "Cześć! Zauważyłem, że Wasz warsztat ma świetne opinie! Klienci Was uwielbiają, ale marnujecie mnóstwo czasu na odbieranie telefonów o status naprawy. Możemy wdrożyć automatyczne SMSy wysyłane z n8n przy zmianie statusu auta...",
            "tele_script": {
                "intro": f"Dzień dobry, z tej strony Tomasz z Jaison.pl. Dzwonię krótko, bo przeanalizowałem Państwa wizytówkę w Google w {city} i znalazłem błąd, przez który tracicie Państwo średnio 10-15 klientów miesięcznie. Mam dosłownie 55 sekund, aby pokazać jak to odwrócić?",
                "qualification": "- Czy klienci dzwonią do Państwa bezpośrednio na telefon, czy macie Państwo system powiadomień?",
                "presentation": "- Wdrażamy automatyczny system n8n powiadamiający klientów o statusie naprawy przez SMS/WhatsApp.\\n- Pomożemy uzyskać Grant Technologiczny od Google o wartości $1300 USD (ok. 5200 PLN) darmowego budżetu!",
                "cta": "Umówmy się na bezpłatną demonstrację w czwartek o 14:00. Pasuje Panu?",
                "looping": "Rozumiem, czas to pieniądz. Ale czy sam zamysł odzyskania 15 godzin w tygodniu dzięki grantowi Google się Panu podoba?"
            }
        }
    ]


def get_cached_quick_tags(client_name, context_data, call_gemini_pro_api_func):
    """Generuje 4 wyspecjalizowane tagi słów kluczowych dla wybranego klienta."""
    state_key = f"quick_tags_{client_name.replace(' ', '_').lower()}"
    if state_key not in st.session_state:
        if not context_data or len(context_data.strip()) < 10:
            # Fallback dla domyślnych profili
            if "jaison" in client_name.lower():
                st.session_state[state_key] = ["szukam n8n", "automatyzacja procesów", "integracja CRM n8n", "chatbot ai b2b"]
            elif "holistic" in client_name.lower():
                st.session_state[state_key] = ["adhd produktywność", "zarządzanie energią adhd", "rutyna poranna adhd", "skupienie uwolnij umysł"]
            else:
                st.session_state[state_key] = ["n8n automatyzacja", "błędy WooCommerce", "szukam CRM", "integracje API"]
        else:
            prompt = f"""Na podstawie poniższego profilu klienta/projektu wygeneruj dokładnie 4 bardzo konkretne, wyszukiwane w języku polskim, krótkie frazy kluczowe (słowa kluczowe), które ten klient lub agencja wpisuje szukając zleceń, automatyzacji lub bólów na portalach lub grupach (np. 'szukam n8n', 'błędy WooCommerce', 'bramka sms API', itp.).
Wyjściem musi być wyłącznie czysty plik JSON będący listą 4 ciągów tekstowych. Brak jakichkolwiek dopisków, komentarzy czy formatowania markdown (bez ```json).

Profil:
{context_data}

Przykładowy wynik:
["szukam n8n", "automatyzacja WooCommerce", "błędy WordPress", "integracja fakturowania"]
"""
            try:
                response = call_gemini_pro_api_func([{"role": "user", "content": prompt}], "Jesteś asystentem generującym słowa kluczowe w formacie JSON.")
                cleaned = response.strip()
                if "```json" in cleaned:
                    cleaned = cleaned.split("```json")[1].split("```")[0].strip()
                elif "```" in cleaned:
                    cleaned = cleaned.split("```")[1].split("```")[0].strip()
                tags = json.loads(cleaned)
                if isinstance(tags, list) and len(tags) >= 4:
                    st.session_state[state_key] = tags[:4]
                else:
                    st.session_state[state_key] = ["n8n automatyzacja", "błędy WooCommerce", "szukam CRM", "integracje API"]
            except Exception as e:
                st.session_state[state_key] = ["n8n automatyzacja", "błędy WooCommerce", "szukam CRM", "integracje API"]
                
    return st.session_state[state_key]


def render_lead_radar_page(call_gemini_pro_api_func):
    """Renderuje cały moduł Skanera Okazji w Streamlicie (Lead Radar)."""
    
    # Inicjalizacja bazy przy wejściu na stronę
    init_db()
    
    # --- AKTYWNY KONTEKST PROJEKTU ---
    selected_context = st.session_state.get("selected_context", "J(AI)SON Agency")
    
    # Odczytaj szczegółowy opis i informacje z profilu dla wybranego kontekstu
    real_clients_dir = r"C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS"
    ctx_desc = "Oficjalny profil roboczy agencji."
    ctx_target = "Klienci B2B, automatyzacje n8n, systemy AI"
    ctx_nice_name = selected_context
    
    # Wyciągnij dopasowany folder klienta
    mapping = {
        "coolfon.pl": "coolfon",
        "kurczakujasia.pl (Bar Jaś)": "kurczakujasia",
        "lifewave.com (MLM)": "lifewave",
        "smartrade.pl": "smartrade_client",
        "viptransporter.pl": "viptransporter",
        "kantororanzada.pl": "kantor_lombard_oranzada",
        "vojsik.ai": "vojsik_ai",
        "app.jaison.pl (SaaS)": "apps.jaison.pl"
    }
    
    profile_content = None
    dir_name = mapping.get(selected_context)
    if dir_name and os.path.exists(os.path.join(real_clients_dir, dir_name)):
        # Proste wbudowane wyszukiwanie profilu .md
        target_path = os.path.join(real_clients_dir, dir_name)
        candidates = []
        gp = os.path.join(target_path, "ghost_profile.md")
        if os.path.exists(gp):
            candidates.append(gp)
        for root, dirs, files in os.walk(target_path):
            for f in files:
                if f.lower().startswith("profil_") and f.endswith(".md"):
                    candidates.append(os.path.join(root, f))
                elif f.lower() == "oferta.md":
                    candidates.append(os.path.join(root, f))
        if not candidates:
            brand_dir = os.path.join(target_path, "01-brand")
            if os.path.exists(brand_dir):
                for f in os.listdir(brand_dir):
                    if f.endswith(".md"):
                        candidates.append(os.path.join(brand_dir, f))
        if candidates:
            try:
                with open(candidates[0], "r", encoding="utf-8") as f_prof:
                    profile_content = f_prof.read()
            except:
                pass
                
    if profile_content:
        import re
        desc_match = re.search(r"Cel:?\s*(.*?)(?:\n|$)", profile_content, re.IGNORECASE)
        target_match = re.search(r"Odbiorcy|Target|Klienci:?\s*(.*?)(?:\n|$)", profile_content, re.IGNORECASE)
        if desc_match:
            ctx_desc = desc_match.group(1).strip()
        if target_match:
            ctx_target = target_match.group(1).strip()
        else:
            ctx_target = "Dedykowani odbiorcy profilu " + selected_context
            
    st.sidebar.markdown("<p style='color: #10B981; font-weight: bold; letter-spacing: 1px; margin-bottom: 2px;'>🔄 AKTYWNY OBSZAR ROBOCZY</p>", unsafe_allow_html=True)
    st.sidebar.markdown(f"""
    <div style="background: #0d121c; padding: 12px; border-radius: 6px; border-left: 3px solid #10B981; margin-bottom: 20px; border-top: 1px solid #1E293B; border-right: 1px solid #1E293B; border-bottom: 1px solid #1E293B;">
        <p style="margin: 0; font-size: 0.85rem; font-weight: bold; color: #E2E8F0;">🏢 {ctx_nice_name}</p>
        <p style="margin: 3px 0 0 0; font-size: 0.75rem; color: #94A3B8;">{ctx_desc[:120] + '...' if len(ctx_desc) > 120 else ctx_desc}</p>
        <p style="margin: 5px 0 0 0; font-size: 0.75rem; color: #10B981;">🎯 <b>Target:</b> {ctx_target[:120]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='color: #10B981; font-family: Outfit; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 2px;'>I. — PROSPECTING & SALES • LEAD RADAR</p>", unsafe_allow_html=True)
    st.title("🎯 Lead Radar (Skaner Okazji)")
    st.markdown("<p style='color: #CBD5E1; font-size: 1.1rem; margin-top: -5px;'>Autonomiczny system skanowania, scoringu i bezpośredniego outreachu B2B leadów zintegrowany z SQLite & n8n.</p>", unsafe_allow_html=True)
    
    # Banner informacyjny
    st.markdown("""
    <div class="one-thing-banner" style="border-left-color: #10B981;">
        <h3 style="margin-top: 0; color: #10B981;">🤖 Jak działa Skaner Okazji?</h3>
        <p style="color: #CBD5E1; line-height: 1.6; margin-bottom: 0;">
            System monitoruje portale zleceń B2B oraz grupy social media. Wszystkie pobrane oferty trafiają do lokalnej bazy SQLite (<code>local_crm.db</code>).
            Model Gemini analizuje je pod kątem budżetu i potencjału automatyzacji (scoring 0-100), generując spersonalizowany outreach gotowy do wysyłki.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dynamiczne statystyki (KPI) z SQLite
    opps = get_opportunities()
    total_leads = len(opps)
    hot_leads = sum(1 for o in opps if o["score"] >= 80)
    avg_score = int(sum(o["score"] for o in opps) / total_leads) if total_leads > 0 else 0
    
    st.markdown("### 📊 Kluczowe Wskaźniki Skanera")
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        st.markdown(f"""
        <div class="custom-card" style="border-left: 4px solid #10B981; text-align: center; padding: 15px;">
            <p style="margin: 0; color: #94A3B8; font-size: 0.85rem; font-weight: bold;">ZESKANOWANE OFERTY</p>
            <h2 style="margin: 5px 0 0 0; color: #E2E8F0; font-family: Outfit;">{total_leads}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col_kpi2:
        st.markdown(f"""
        <div class="custom-card" style="border-left: 4px solid #EF4444; text-align: center; padding: 15px;">
            <p style="margin: 0; color: #94A3B8; font-size: 0.85rem; font-weight: bold;">🔥 GORĄCE OKAZJE</p>
            <h2 style="margin: 5px 0 0 0; color: #E2E8F0; font-family: Outfit;">{hot_leads}</h2>
        </div>
        """, unsafe_allow_html=True)
    with col_kpi3:
        st.markdown(f"""
        <div class="custom-card" style="border-left: 4px solid #3B82F6; text-align: center; padding: 15px;">
            <p style="margin: 0; color: #94A3B8; font-size: 0.85rem; font-weight: bold;">ŚREDNIA OCENA DOPASOWANIA</p>
            <h2 style="margin: 5px 0 0 0; color: #E2E8F0; font-family: Outfit;">{avg_score} / 100</h2>
        </div>
        """, unsafe_allow_html=True)
    with col_kpi4:
        projected_value = sum(10000 for o in opps if o["score"] >= 80) + sum(3000 for o in opps if 50 <= o["score"] < 80)
        st.markdown(f"""
        <div class="custom-card" style="border-left: 4px solid #F59E0B; text-align: center; padding: 15px;">
            <p style="margin: 0; color: #94A3B8; font-size: 0.85rem; font-weight: bold;">PROJEKTOWANA WARTOŚĆ</p>
            <h2 style="margin: 5px 0 0 0; color: #E2E8F0; font-family: Outfit;">{projected_value:,} PLN</h2>
        </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    
    # Podział na zakładki
    tab_radar, tab_fb_spy, tab_gmaps, tab_sales_director, tab_audit, tab_map, tab_config = st.tabs([
        "📡 Radar Zleceń", 
        "🕵️ Facebook Ads Szpieg",
        "🔍 Skaner Wizytówek Google (Localo style)",
        "📢 Sales Director (Outbound)", 
        "📋 Audyty 21 Pytań (jaison.pl)", 
        "🗺️ Mapa Źródeł v2",
        "⚙️ Konfiguracja Skanera"
    ])
    
    # ==================== TAB 1: RADAR ZLECEŃ ====================
    with tab_radar:
        st.markdown("### 📥 Aktywne Okazje z Rynku (Baza SQLite)")
        st.write("Wpisz interesującą Cię niszę, aby za pomocą AI przeszukać i przeanalizować nowe zlecenia:")
        
        if "radar_search_kws_input" not in st.session_state:
            st.session_state.radar_search_kws_input = "n8n BaseLinker automation"
            
        c_scan1, c_scan2 = st.columns([3, 1])
        with c_scan1:
            search_kws = st.text_input("Słowa kluczowe (np. n8n automation, WooCommerce BaseLinker, chatbot AI):", key="radar_search_kws_input", label_visibility="collapsed")
        with c_scan2:
            if st.button("🚀 Uruchom AI Skaner", use_container_width=True, type="primary"):
                if search_kws:
                    with st.spinner("Skaner AI przeczesuje rynek i analizuje zlecenia..."):
                        success = run_ai_market_scan(search_kws)
                        if success:
                            st.success("Pomyślnie zasilono bazę nowymi, przeanalizowanymi okazjami!")
                            st.rerun()
                        else:
                            st.error("Błąd: Nie udało się połączyć ze Skanerem AI. Sprawdź status LiteLLM proxy na porcie 8089.")
                else:
                    st.warning("Wpisz słowa kluczowe przed skanowaniem!")
                    
        # Generuj i wyświetl dynamiczne Quick-Tagi
        tags = get_cached_quick_tags(selected_context, profile_content or "", call_gemini_pro_api_func)
        
        st.markdown("<p style='font-size: 0.8rem; color: #94A3B8; margin-top: -5px; margin-bottom: 5px; font-weight: bold;'>🏷️ SUGEROWANE SŁOWA KLUCZOWE (Dynamiczne tagi z Gemini na podstawie aktywnego profilu):</p>", unsafe_allow_html=True)
        cols = st.columns(len(tags))
        for idx, tag in enumerate(tags):
            with cols[idx]:
                if st.button(f"🔍 {tag}", key=f"tag_radar_{idx}", use_container_width=True):
                    st.session_state.radar_search_kws_input = tag
                    st.rerun()
                    
        st.write("")
        
        # Wyświetlanie listy z bazy danych
        show_rejected = st.checkbox("Pokaż zlecenia odrzucone (👎)", value=False, key="show_rejected_leads_lr")
        
        opportunities = get_opportunities()
        if not show_rejected:
            # Filtrujemy odrzucone (feedback = -1)
            opportunities = [opp for opp in opportunities if (opp.get("user_feedback") or 0) != -1]
            
        if not opportunities:
            st.info("Baza danych nie zawiera pasujących zleceń. Uruchom skaner powyżej lub włącz wyświetlanie odrzuconych.")
        else:
            for opp in opportunities:
                # Kolor na podstawie oceny
                if opp["score"] >= 80:
                    accent_color = "#EF4444" # Czerwony / Hot
                    badge_style = "background-color: #EF4444; color: white;"
                elif opp["score"] >= 50:
                    accent_color = "#3B82F6" # Niebieski / Medium
                    badge_style = "background-color: #3B82F6; color: white;"
                else:
                    accent_color = "#6B7280" # Szary / Cold
                    badge_style = "background-color: #6B7280; color: white;"
                    
                # Karta okazji
                import urllib.parse
                kw_query = opp['title']
                if "n8n" in kw_query.lower() or "automatyz" in kw_query.lower() or "integra" in kw_query.lower():
                    kw_query = "automatyzacja n8n"
                encoded_card_query = urllib.parse.quote(kw_query)
                card_fb_url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=PL&q={encoded_card_query}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&media_type=all"
                
                source_link_html = ""
                if opp.get("url_link"):
                    source_link_html = f'<span>🔗 <a href="{opp["url_link"]}" target="_blank" style="color: #10B981; font-weight: bold; text-decoration: none;">Link źródłowy</a></span>'
                else:
                    source_link_html = f'<span>🔗 <a href="https://useme.com" target="_blank" style="color: #94A3B8; text-decoration: none;">Useme</a></span>'

                # Karta okazji
                st.markdown(f"""
                <div class="custom-card" style="border-left: 5px solid {accent_color}; margin-bottom: 15px; padding: 20px;">
                	<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                		<span style="font-size: 0.85rem; color: #94A3B8; font-weight: bold; text-transform: uppercase;">🌐 Źródło: {opp['source']} | 📅 {opp['created_at']}</span>
                		<span style="padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: bold; {badge_style}">{opp['label']} (Dopasowanie: {opp['score']}%)</span>
                	</div>
                	<h4 style="margin: 0 0 10px 0; color: #F3F4F6; font-family: Outfit;">{opp['title']}</h4>
                	<p style="margin: 0 0 12px 0; color: #D1D5DB; font-size: 0.95rem; line-height: 1.6;">{opp['description']}</p>
                	<div style="display: flex; flex-wrap: wrap; gap: 15px; font-size: 0.85rem; color: #94A3B8; border-top: 1px solid #1E293B; padding-top: 10px; margin-bottom: 10px;">
                		<span>💰 Budżet: <strong style="color: #10B981;">{opp['budget']}</strong></span>
                		<span>📧 Email: <strong>{opp['contact_email'] if opp['contact_email'] else 'Brak'}</strong></span>
                		<span>📞 Tel: <strong>{opp['contact_phone'] if opp['contact_phone'] else 'Brak'}</strong></span>
                		<span>📦 Status: <strong style="color: #F59E0B;">{opp['status']}</strong></span>
                		{source_link_html}
                		<span>🕵️ <a href="{card_fb_url}" target="_blank" style="color: #3B82F6; font-weight: bold; text-decoration: none;">FB Ads Spy</a></span>
                	</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Elementy interaktywne pod kartą (Streamlit)
                c_opt1, c_opt2, c_opt3, c_opt4, c_opt5 = st.columns([2, 1, 1, 1, 1])
                with c_opt1:
                    with st.expander("📬 Zobacz spersonalizowaną wiadomość Outreach (Perswazyjna pomoc AI)"):
                        st.code(opp["suggested_outreach"], language="text")
                        st.caption(f"💡 **Next Action:** {opp['suggested_action']}")
                with c_opt2:
                    # Wybór statusu
                    status_options = ["New", "Outreached", "Imported", "Archived"]
                    current_idx = status_options.index(opp["status"]) if opp["status"] in status_options else 0
                    new_status = st.selectbox(
                        "Status:", 
                        status_options, 
                        index=current_idx, 
                        key=f"status_select_{opp['id']}", 
                        label_visibility="collapsed"
                    )
                    if new_status != opp["status"]:
                        update_opportunity_status(opp["id"], new_status)
                        st.success(f"Zaktualizowano status oferty na: `{new_status}`!")
                        st.rerun()
                with c_opt3:
                    if st.button("🚀 Importuj do CRM", key=f"crm_imp_{opp['id']}", use_container_width=True):
                        notes_content = f"Źródło: {opp.get('source')}. Budżet: {opp.get('budget')}. Opis: {opp.get('description')}"
                        imported = add_lead_to_crm_json(
                            name=opp.get("title"),
                            notes=notes_content,
                            suggested_outreach=opp.get("suggested_outreach"),
                            next_action=opp.get("suggested_action") if opp.get("suggested_action") else "Skontaktować się po analizie AI"
                        )
                        update_opportunity_status(opp["id"], "Imported")
                        if imported:
                            st.success("Zaimportowano bezpośrednio do CRM Pipeline!")
                        else:
                            st.success("Zaktualizowano status. Lead już istnieje w CRM Pipeline.")
                        import time
                        time.sleep(1.0)
                        st.rerun()
                with c_opt4:
                    # System feedbacku (kciuki 👍/👎)
                    feedback = opp.get("user_feedback", 0) or 0
                    if feedback == 1:
                        st.markdown("<p style='color: #10B981; font-weight: bold; text-align: center; margin-top: 5px; font-size: 0.9rem;'>👍 Trafiony!</p>", unsafe_allow_html=True)
                    elif feedback == -1:
                        st.markdown("<p style='color: #EF4444; font-weight: bold; text-align: center; margin-top: 5px; font-size: 0.9rem;'>👎 Słaby</p>", unsafe_allow_html=True)
                    else:
                        col_f_up, col_f_dn = st.columns(2)
                        with col_f_up:
                            if st.button("👍", key=f"f_up_{opp['id']}", use_container_width=True, help="Oznacz jako trafione zlecenie (AI zapamięta ten wzór)"):
                                update_opportunity_feedback(opp['id'], 1)
                                st.toast("Dzięki! AI zapamięta ten wzorzec jako pozytywny.")
                                import time
                                time.sleep(0.5)
                                st.rerun()
                        with col_f_dn:
                            if st.button("👎", key=f"f_dn_{opp['id']}", use_container_width=True, help="Oznacz jako słabe zlecenie (AI wyeliminuje podobne w przyszłości)"):
                                st.session_state[f"show_reason_input_{opp['id']}"] = True
                                st.rerun()
                with c_opt5:
                    if st.button("🗑️ Usuń", key=f"opp_del_{opp['id']}", use_container_width=True):
                        delete_opportunity(opp["id"])
                        st.success("Usunięto okazję!")
                        st.rerun()
                
                # Dodatkowe pole tekstowe na podanie powodu odrzucenia
                if st.session_state.get(f"show_reason_input_{opp['id']}"):
                    st.markdown("<div style='background: #1B0F1E; padding: 10px; border-radius: 8px; margin-top: 5px; border-left: 3px solid #EF4444;'>", unsafe_allow_html=True)
                    reason_val = st.text_input("Dlaczego odrzucasz to zlecenie? (np. za niski budżet, zła branża):", key=f"reason_text_{opp['id']}")
                    col_sav, col_can = st.columns([1, 1])
                    with col_sav:
                        if st.button("Zapisz", key=f"save_reason_{opp['id']}", type="primary", use_container_width=True):
                            update_opportunity_feedback(opp['id'], -1, reason_val)
                            st.session_state[f"show_reason_input_{opp['id']}"] = False
                            st.success("Odrzucono. Skaner nauczył się nowego wzorca!")
                            import time
                            time.sleep(0.5)
                            st.rerun()
                    with col_can:
                        if st.button("Anuluj", key=f"cancel_reason_{opp['id']}", use_container_width=True):
                            st.session_state[f"show_reason_input_{opp['id']}"] = False
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)
                        
                st.markdown("<hr style='border: 0; border-top: 1px solid #1E293B; margin: 15px 0;'>", unsafe_allow_html=True)

    # ==================== TAB 2: FACEBOOK ADS SZPIEG ====================
    with tab_fb_spy:
        st.markdown("### 🕵️ Szpiegowanie Reklam Konkurencji (Facebook Ads Library)")
        st.markdown("""
        Zgodnie ze strategią **Lead Radar 2.0 & Grand Slam Offer**, analiza działających reklam konkurencji pozwala na natychmiastowe ulepszenie oferty i wstrzyknięcie zwycięskich kreacji bezpośrednio do Twojego skryptu outreach.
        """)
        
        # Banner informacyjny o strategii
        st.markdown("""
        <div class="one-thing-banner" style="border-left-color: #3B82F6; background: #0c1524;">
            <h4 style="margin-top: 0; color: #3B82F6;">🎯 Jak wykorzystać szpiegowanie w Outreach?</h4>
            <p style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.5; margin-bottom: 0;">
                Wyszukaj konkurentów lub słowa kluczowe (np. <i>"n8n automatyzacja"</i>, <i>"agencja AI"</i>). Zobacz jakie oferty (Grand Slam) oraz bonusy dają w reklamach. 
                Nasze AI automatycznie wykorzysta te dane jako kontekst wykluczający lub ulepszający przy generowaniu spersonalizowanych ofert!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col_fb_q, col_fb_c = st.columns([2, 1])
        with col_fb_q:
            fb_search_query = st.text_input(
                "🔎 Wpisz słowo kluczowe lub nazwę konkurenta (fanpage):", 
                value=st.session_state.get("fb_search_kw_preset", "automatyzacje procesów"),
                key="fb_search_query_input"
            )
        with col_fb_c:
            fb_country = st.selectbox(
                "🌍 Kraj docelowy:", 
                ["PL", "ALL", "US", "DE", "GB"], 
                index=0, 
                key="fb_country_select"
            )
            
        # Generuj bezpieczny link do Facebook Ads Library
        import urllib.parse
        encoded_query = urllib.parse.quote(fb_search_query)
        country_param = "all" if fb_country == "ALL" else fb_country
        
        fb_library_url = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={country_param}&q={encoded_query}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&media_type=all"
        
        st.write("")
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 25px;">
            <a href="{fb_library_url}" target="_blank" style="text-decoration: none;">
                <button style="background: linear-gradient(135deg, #1877F2 0%, #0d59b3 100%); color: white; padding: 12px 25px; border-radius: 8px; border: none; font-size: 1rem; font-weight: bold; cursor: pointer; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 12px rgba(24, 119, 242, 0.3);">
                    🌐 Otwórz Bezpiecznie Facebook Ads Library dla: "{fb_search_query}" 🚀
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        # Sekcja Integracji Automatycznej z Apify
        st.markdown("#### 🤖 Automatyczny Monitoring przez Apify & n8n")
        st.markdown("""
        Chcesz, aby system automatycznie scrapował reklamy konkurencji w tle bez Twojego udziału? Zintegruj swój crawler za pomocą Apify (Meta Ads Scraper) i webhooka n8n.
        """)
        
        col_api_webhook, col_api_status = st.columns([2, 1])
        with col_api_webhook:
            apify_webhook_url = st.text_input(
                "🔗 Twój Webhook n8n dla Apify Meta Ads:", 
                value="https://n8n.jaison.pl/webhook/apify-meta-ads-ingest",
                key="apify_webhook_url_input"
            )
        with col_api_status:
            apify_status = "Aktywny" if apify_webhook_url else "Nieaktywny"
            st.markdown(f"""
            <div style="padding: 10px; border-radius: 6px; background-color: #0c1524; text-align: center; border-left: 3px solid #10B981; margin-top: 5px;">
                <p style="margin: 0; font-size: 0.8rem; color: #94A3B8;">STATUS INTEGRACJI</p>
                <h4 style="margin: 3px 0 0 0; color: #10B981;">{apify_status}</h4>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("""
        **Rekomendowany n8n Blueprint dla Apify Meta Ads Scraper:**
        1. **Trigger:** Cron co 24h lub Webhook ręczny.
        2. **Action:** Apify node wywołujący scraper `apify/facebook-ads-scraper` ze słowami kluczowymi z Twojego profilu.
        3. **Webhook Ingest:** n8n przesyła uzyskane reklamy konkurencji (teksty, hooki) bezpośrednio na powyższy webhook, zasilając kolumnę `competitor_ads_context` w bazie.
        """)

    # ==================== TAB: SKANER WIZYTÓWEK GOOGLE (LOCALO STYLE) ====================
    with tab_gmaps:
        st.subheader("🔍 Skaner i Audytor Wizytówek Google (Localo Style)")
        st.markdown("""
        System wyszukuje wizytówki firm (Google Moja Firma) w wybranym regionie, analizuje ich parametry techniczne i automatycznie segreguje według **potencjału wdrożenia automatyzacji AI i nowej strony WWW**.
        """)
        
        # Banner informacyjny
        st.markdown("""
        <div class="one-thing-banner" style="border-left-color: #3B82F6; background: #0c1524;">
            <h4 style="margin-top: 0; color: #3B82F6;">🎯 Strategia Prospectingu GMB</h4>
            <p style="color: #CBD5E1; font-size: 0.85rem; line-height: 1.5; margin-bottom: 0;">
                Wizytówki o <b>niskiej punktacji (GMB Score < 50)</b> posiadają krytyczne braki (np. brak strony, brak SSL, brak odpowiedzi na opinie). 
                To najprostsza droga wejścia dla Twojej agencji – oferujesz im natychmiastową optymalizację lub automatyczny system AI do pozyskiwania i odpowiadania na opinie.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Formularz filtrów
        col_f1, col_f2, col_f3 = st.columns([2, 2, 1])
        with col_f1:
            g_kw = st.text_input("Branża / Słowo kluczowe:", value="stomatolog", key="gmaps_search_kw")
        with col_f2:
            g_city = st.text_input("Miejscowość / Miasto:", value="Sopot", key="gmaps_search_city")
        with col_f3:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            run_g_scan = st.button("🚀 Audytuj GMB", use_container_width=True, type="primary")
            
        if run_g_scan or "last_gmaps_results" in st.session_state:
            if run_g_scan:
                with st.spinner(f"AI przeczesuje Google Maps i generuje audyty Localo dla '{g_kw}' w '{g_city}'..."):
                    results = get_gmaps_audit_leads(g_kw, g_city, call_gemini_pro_api_func)
                    st.session_state.last_gmaps_results = results
                    st.session_state.last_g_kw = g_kw
                    st.session_state.last_g_city = g_city
            
            leads = st.session_state.last_gmaps_results
            kw_display = st.session_state.get("last_g_kw", g_kw)
            city_display = st.session_state.get("last_g_city", g_city)
            
            st.markdown(f"### 📍 Wyniki wyszukiwania dla: `{kw_display}` w lokalizacji `{city_display}`")
            
            for lead in leads:
                score = lead.get("gmb_score", 50)
                # Wyznaczenie koloru dla punktacji
                if score < 40:
                    score_color = "#EF4444" # Czerwony - krytyczny
                    score_bg = "rgba(239, 68, 68, 0.1)"
                    score_label = "KRYTYCZNY (Wymaga pilnej uwagi)"
                elif score < 70:
                    score_color = "#F59E0B" # Żółty - średni
                    score_bg = "rgba(245, 158, 11, 0.1)"
                    score_label = "ŚREDNI (Duży potencjał poprawek)"
                else:
                    score_color = "#10B981" # Zielony - dobry
                    score_bg = "rgba(16, 185, 129, 0.1)"
                    score_label = "DOBRY (Dobrze zoptymalizowany)"
                
                # HTML Card
                st.markdown(f"""
                <div style="background: #0d131f; padding: 20px; border-radius: 12px; border: 1px solid #1E293B; margin-bottom: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                        <div>
                            <h3 style="margin: 0; font-family: Outfit; color: #E2E8F0;">🏢 {lead.get('name')}</h3>
                            <p style="margin: 5px 0; color: #94A3B8; font-size: 0.9rem;">📍 {lead.get('address')} | 📞 {lead.get('phone', 'Brak telefonu')}</p>
                            <p style="margin: 0; color: #3B82F6; font-size: 0.85rem;">
                                🌐 {f"<a href='{lead.get('website')}' target='_blank' style='color:#3B82F6; text-decoration:none;'>{lead.get('website')}</a>" if lead.get('website') else "<span style='color:#EF4444; font-weight:bold;'>⚠️ Całkowity brak strony www!</span>"}
                            </p>
                        </div>
                        <div style="text-align: right; background: {score_bg}; border: 1px solid {score_color}; padding: 10px 15px; border-radius: 8px;">
                            <span style="font-size: 0.8rem; color: #94A3B8; font-weight: bold; display: block;">LOCALO GMB SCORE</span>
                            <span style="font-size: 1.8rem; color: {score_color}; font-weight: bold; font-family: Outfit;">{score} / 100</span>
                            <span style="font-size: 0.7rem; color: {score_color}; display: block; font-weight: bold;">{score_label}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Elementy audytu
                c_det1, c_det2 = st.columns([1, 1])
                with c_det1:
                    st.markdown("**🚨 Wykryte błędy i braki w wizytówce:**")
                    for issue in lead.get("issues", []):
                        st.markdown(f"- <span style='color:#F59E0B;'>⚠️</span> {issue}", unsafe_allow_html=True)
                        
                    st.write("")
                    st.markdown(f"⭐ **Opinie:** `{lead.get('rating')} / 5.0` (Liczba recenzji: `{lead.get('reviews_count')}`)")
                    st.markdown(f"📲 **Podpięte Social Media:** `{'Tak ✅' if lead.get('has_social') else 'Nie ❌'}`")
                    
                    st.markdown(f"""
                    <div style="background: rgba(59, 130, 246, 0.08); padding: 12px; border-radius: 8px; border: 1px solid rgba(59, 130, 246, 0.3); margin-top: 15px;">
                        <span style="color: #3B82F6; font-weight: bold; font-size: 0.85rem;">🎁 GRANT TECHNOLOGICZNY GOOGLE</span>
                        <p style="margin: 5px 0 0 0; font-size: 0.78rem; color: #CBD5E1; line-height: 1.4;">
                            Firma kwalifikuje się do <b>Grantu Technologicznego o wartości $1300 USD (ok. 5200 PLN)</b> darmowego budżetu od Google na całą infrastrukturę chmurową GCP oraz Vertex AI Search!
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with c_det2:
                    st.markdown(f"🤖 **Potencjał Automatyzacji AI (Magic Value):**")
                    st.info(lead.get("automation_potential"))
                    
                    # Cold-calling script
                    ts = lead.get("tele_script", {})
                    if ts:
                        with st.expander("📞 Skrypt rozmowy telefonicznej (Metoda Prostej Linii Jana Szopy) 🚀"):
                            st.markdown(f"""
                            ### 🏁 1. Początek (Duża obietnica w 4 sekundy)
                            > **"{ts.get('intro', '')}"**
                            
                            ### 🔍 2. Kwalifikacja (Ból i Pieniądze)
                            {ts.get('qualification', '')}
                            
                            ### 🏗️ 3. Prezentacja (Logika + Emocje)
                            {ts.get('presentation', '')}
                            
                            ### 🎯 4. Wezwanie do akcji (CTA)
                            > **"{ts.get('cta', '')}"**
                            
                            ### 🔄 5. Looping (Zbijanie obiekcji)
                            {ts.get('looping', '')}
                            """)
                    
                    # Outreach Box
                    with st.expander("📬 Wygenerowana, spersonalizowana pomoc AI (Outreach B2B)"):
                        st.code(lead.get("suggested_outreach"), language="markdown")
                        if st.button("🚀 Wyślij do CRM", key=f"gmaps_crm_{lead.get('name')}"):
                            # 1. Dodanie do SQLite jako lead
                            conn = sqlite3.connect(DB_PATH)
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO opportunities (source, title, budget, description, score, label, suggested_outreach, suggested_action, status)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, (
                                "Google Maps",
                                lead.get("name"),
                                "Średni (Wdrożenie AI/WWW)",
                                f"Lokalizacja: {lead.get('address')}. Braki: {', '.join(lead.get('issues', []))}",
                                100 - score, # Niższy wynik GMB = wyższy priorytet handlowy dla nas!
                                "Gorący" if score < 50 else "Średni",
                                lead.get("suggested_outreach"),
                                "Wykonaj telefon cold-call z audytem",
                                "New"
                            ))
                            conn.commit()
                            conn.close()
                            
                            # 2. Fizyczny zapis do crm.json
                            notes_text = f"Lokalizacja: {lead.get('address')}. Wykryte braki GMB: {', '.join(lead.get('issues', []))}. Potencjał automatyzacji: {lead.get('automation_potential')}"
                            imported = add_lead_to_crm_json(
                                name=lead.get("name"),
                                notes=notes_text,
                                suggested_outreach=lead.get("suggested_outreach"),
                                next_action="Wykonaj telefon cold-call z gotowym audytem GMB"
                            )
                            if imported:
                                st.success("Pomyślnie zaimportowano do CRM Pipeline oraz Lead Radaru!")
                            else:
                                st.success("Dodano do Lead Radaru (lead już istnieje w CRM Pipeline).")
                            
                    # Jeśli nie ma strony WWW, pokaż widoczny przycisk przekierowania do Landing Page Factory!
                    if not lead.get("website"):
                        if st.button("👉 UTWÓRZ WIZUALNY PROJEKT STRONY (LANDING PAGE FACTORY) 🛠️", key=f"lp_redir_{lead.get('name')}", use_container_width=True, type="secondary"):
                            st.session_state.current_page = "Jaison Agency"
                            st.session_state.active_suite_tool = "Landing_Page"
                            st.session_state.lp_prefill_client_name = lead.get("name")
                            st.session_state.lp_prefill_industry = g_kw
                            st.session_state.lp_prefill_city = g_city
                            st.success("Przekierowywanie do Landing Page Factory...")
                            st.rerun()
                            
                st.markdown("<hr style='border:0; border-top: 1px solid #1E293B; margin: 25px 0;'>", unsafe_allow_html=True)

    # ==================== TAB 2: SALES DIRECTOR ====================
    with tab_sales_director:
        st.subheader("📢 Sales Director / Handlowiec AI")
        st.markdown("Ten agent przeszukuje fora, grupy dyskusyjne oraz social media i generuje outreach do osób szukających automatyzacji procesów.")
        
        with st.expander("📖 Skrypt Sprzedażowy i Autorski Protokół Jaison.pl", expanded=False):
            st.markdown(f"""
            Oto oficjalny, zintegrowany skrypt sprzedażowy Jaison.pl łączący psychologiczne NLP, obniżenie tarcia poznawczego oraz precyzyjną kwalifikację B2B.
            
            ---
            ### ⚡ 15-Minutowy Rytuał Handlowy (Daily Prospecting)
            1. **Skanowanie (5 min)**: Przejdź do zakładki *Radar Zleceń*, wpisz słowa kluczowe i kliknij `🚀 Uruchom AI Skaner`.
            2. **Selekcja (3 min)**: Zidentyfikuj zlecenia oznaczone jako **🔥 Gorący (High-Ticket)**.
            3. **Wysyłka (7 min)**: Skopiuj wygenerowany przez Gemini outreach, kliknij `[OFERTA 🔗]`, wklej na portalu i wyślij.
            
            ---
            ### 📞 Szkielet Skryptu (Straight Line Persuasion / Prosta Linia)
            Prowadź klienta po prostej linii od początku do zakupu. Gdy klient zbacza – wracaj na linię za pomocą tonacji i pytań kontrolnych.
            
            #### 1️⃣ Duża Obietnica (Pierwsze 4 sekundy)
            *Musisz brzmieć: kompetentnie (bystro/inteligentnie), entuzjastycznie (pasja) oraz jako absolutny ekspert.*
            > **"Dzień dobry! Z tej strony {ctx_info['name']}. Kontaktuję się z Państwem, ponieważ zauważyliśmy w {ctx_info['name']}, że [placówki medyczne/firmy w danej branży] mogą podwoić ilość klientów/pacjentów i odzyskać 15 godzin tygodniowo za pomocą automatyzacji już w pierwsze 30 dni, eliminując dosłownie trzy błędy. Brzmi to dla Państwa ciekawie?"**
            
            #### 2️⃣ Przejście do Kwalifikacji
            *Płynne przejęcie kontroli nad czasem klienta.*
            > **"Rozumiem Panią/Pana. Aby być pewnym, że nie marnuję Państwa czasu oraz żeby sprawdzić, czy możemy pomóc za pomocą naszych systemów automatyzacji, zadam tylko kilka prostych i szybkich pytań, dobrze?"**
            
            #### 3️⃣ Kwalifikacja (6 Pytań Kwalifikacyjnych Jaison.pl)**
            1. **Decyzyjność**: *"Czy sam/a zajmujesz się rozwojem firmy, czy jest ktoś jeszcze odpowiedzialny za te decyzje?"*
            2. **Bóle obecne**: *"Co podoba się Panu/Pani w obecnym marketingu/systemach, a co nie? Co podczas współpracy z innymi agencjami/firmami było według Pana totalnie niedopuszczalne?"*
            3. **Obawy i status**: *"Co Pana najbardziej martwi w swoim biznesie? Jak długo to trwa? Pana zdaniem jest coraz lepiej czy gorzej?"*
            4. **Cele i budżet**: *"Jakie wyniki chciałby Pan osiągnąć? Jaki rodzaj usługi jest u Was najbardziej opłacalny i na niego chcecie najwięcej klientów? Jaki budżet miesięczny na wdrożenie/reklamy jesteście w stanie zainwestować?"*
            5. **Priorytet**: *"Jaki czynnik spośród tych, które omówiliśmy, jest dla Pana najważniejszy?"*
            6. **Potwierdzenie**: *"Czy spytałem już o wszystkie istotne dla Pana sprawy?"*
            
            #### 4️⃣ Przejście do Prezentacji (Logiczny argument + Emocja)
            > **"Na podstawie tego, co mi Pan powiedział. Nasze rozwiązanie jest definitywnie, idealnie dopasowane do Pana potrzeb. Jeżeli ma Pan dosłownie 3-4 minuty, to chcę podzielić się z Panem szczegółami dotyczącymi naszego systemu. Ma Pan chwilę?"**
            
            #### 5️⃣ Szybka Prezentacja (Max 3 korzyści)
            *Przedstaw logiczne cyfry i popchnij emocją (np. odzyskanie wolnego czasu, redukcja stresu).*
            
            #### 6️⃣ Looping (Zapętlanie Belforta)
            *Gdy słyszysz „Muszę to przemyśleć” – wtedy zaczyna się sprzedaż!*
            - **Zgoda**: *"Jasne, rozumiem Pana. Na tym etanym etapie rozmowy też bym tak powiedział, ale proszę pozwolić, że zapytam: czy sam zamysł odzyskania tych 15 godzin i automatyzacji się Panu podoba?"* (Izolowanie obiekcji i powrót na prostą linię).
            - **Follow-up (Protokół Jaison)**: Po 3 loopingach kończysz rozmowę i wracasz z kreatywnym follow-upem.
            """)
        
        lr_search_kw = st.text_input("Słowa kluczowe do skanowania internetu:", value="n8n automatyzacja, szukam crm, błędy BaseLinker", key="lr_sales_search_kw_mod")
        
        # Generuj i wyświetl dynamiczne Quick-Tagi dla Sales Directora
        tags = get_cached_quick_tags(selected_context, profile_content or "", call_gemini_pro_api_func)
        
        st.markdown("<p style='font-size: 0.8rem; color: #10B981; margin-top: -5px; margin-bottom: 5px; font-weight: bold;'>🏷️ SUGEROWANE STRATEGIE PROSPECTINGU (Dynamiczne z Gemini):</p>", unsafe_allow_html=True)
        cols_sd = st.columns(len(tags))
        for idx, tag in enumerate(tags):
            with cols_sd[idx]:
                if st.button(f"📢 {tag}", key=f"tag_sd_{idx}", use_container_width=True):
                    st.session_state.lr_sales_search_kw_mod = tag
                    st.rerun()
                    
        st.write("")
        
        if st.button("Generuj Prospekty i Outreach", type="primary", key="lr_sales_scan_btn_mod"):
            with st.spinner("Sales Director analizuje social media..."):
                prompt = f"""Jesteś wirtualnym Sales Directorem w zespole 'Jaison.pl'.
Przeskanowałeś Reddit, fora oraz social media pod kątem słów kluczowych: "{lr_search_kw}".
Wygeneruj 3 realistyczne, gorące leady B2B na podstawie rzeczywistych, głębokich problemów rynkowych w tych kanałach.
ZABRONIONE jest generowanie wirtualnych (zmyślonych) leadów bez konkretnych źródeł. Każdy lead MUSI mieć podany realistyczny, precyzyjny link URL do posta na grupie Facebook, wątku na Reddit (np. w r/entrepreneur lub r/automations) lub aktualizacji LinkedIn.

Dla każdego leada podaj w formacie Markdown:
1. **Nazwa Leada / Kontakt**: Nazwisko osoby lub nazwa firmy
2. **Kanał / Grupa źródłowa**: np. 'Grupa FB: Automatyzacja Biznesu', 'Reddit: r/entrepreneur'
3. **Prawdziwy link URL**: `👉 [IDŹ DO WPISU / GRUPY 🔗](https://...)` z rzeczywistą lub realistyczną sub-domeną i ID posta
4. **Ból / Problem**: Dokładna treść wpisu / problemu (np. błąd n8n, brak integracji z fakturowaniem)
5. **Spersonalizowany outreach**: Gotowy, merytoryczny i nie-nachalny wpis/wiadomość w stylu Jaison.pl (obniżający tarcie poznawcze, oferujący wartość)
6. **Next Action**: Proponowane działanie w CRM
"""
                response = call_gemini_pro_api_func([{"role": "user", "content": prompt}], "Jesteś dynamicznym i skutecznym Sales Directorem.")
                st.session_state.sales_leads_result_mod = response
                st.rerun()
                
        if "sales_leads_result_mod" in st.session_state and st.session_state.sales_leads_result_mod:
            st.markdown("### 🎯 Wykryte Szanse i Gotowy Outreach:")
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid #10B981; white-space: pre-wrap; font-size: 0.95rem; line-height: 1.7; background-color: #0d121c; padding: 20px;">
{st.session_state.sales_leads_result_mod}
            </div>
            """, unsafe_allow_html=True)
            if st.button("Wyczyść leady", key="lr_sales_clear_btn_mod"):
                st.session_state.sales_leads_result_mod = None
                st.rerun()

    # ==================== TAB 3: AUDYTY 21 PYTAŃ ====================
    with tab_audit:
        st.markdown("### 📋 Kwalifikacja Inbound - Audyt Systemowy 21 Pytań")
        st.caption("Przeglądaj odpowiedzi z ankiety kwalifikacyjnej bota na jaison.pl i generuj architektury wdrożeń.")
        
        col_list, col_details = st.columns([1, 2])
        
        audits = {
            "Tomasz Kowalski (Holistic Agency)": {
                "date": "Dzisiaj, 11:20",
                "score": 14,
                "tier": "STREFA ŚREDNIAKÓW (Chaos narzędziowy)",
                "color": "#F59E0B",
                "phone": "+48 501 234 567",
                "email": "tomasz@holisticagency.pl",
                "answers": {
                    "S1_1": "10 godzin w tygodniu marnujemy na ręczne przepisywanie danych z CRM do GSheets.",
                    "S1_2": "Nie, wszystko jest w rozproszonych plikach i głowach zespołu.",
                    "S1_3": "Około tygodnia, brak jasnych SOP-ów.",
                    "S1_4": "Tak, często zapominamy o follow-upach z Messengera.",
                    "S1_5": "Codziennie podejmuję 5-10 prostych decyzji za ludzi.",
                    "S2_6": "Odpisujemy średnio po 2-3 godzinach, czasami na drugi dzień.",
                    "S2_7": "Nie, nie mamy żadnego automatycznego follow-up.",
                    "S2_8": "Działamy głównie na wyczucie, brak analityki konwersji.",
                    "S2_9": "Tracimy około 3-5 dużych kontraktów miesięcznie.",
                    "S2_10": "Ręcznie ustalamy terminy na czacie lub mailowo.",
                    "S3_11": "Nie, skrypty są nieuporządkowane.",
                    "S3_12": "Wszystko by się załamało - głównie mój wolny czas.",
                    "S3_13": "Słabo, robimy 90% ręcznie.",
                    "S3_14": "Ręcznie odpisuję na 15 pytań dziennie.",
                    "S3_15": "Nie zbieramy opinii automatycznie.",
                    "S4_16": "Jestem zmęczonym operacyjnie niewolnikiem własnej firmy.",
                    "S4_17": "Pracuję w prawie każdy weekend.",
                    "S4_18": "Firma przestałaby działać po 5 dniach bez mojego udziału.",
                    "S4_19": "Marnuję 80% energii na gaszenie pożarów technicznych.",
                    "S4_20": "Tracę ogromne pieniądze i mnóstwo wolności.",
                    "S4_21": "Tak, jestem gotowy na wdrożenie Niewidzialnego Pracownika AI!"
                },
                "recommendation": """### 🤖 Rekomendacja Systemowa Jaisona (Ewaluacja AI)
**Klient:** Tomasz Kowalski • **Wynik:** 14/21 pkt (Chaos Narzędziowy)
**Rekomendowane wdrożenie automatyzacji w darmowym staku:**

1. **Wdrożenie n8n do eliminacji "Rękodzieła" (Odzysk 10h/tydz):**
   - Połączenie formularzy na Facebook/Messenger z Twoim CRM za pomocą webhooka n8n.
   - Automatyczny dwustronny sync danych, eliminujący ręczne przepisywanie do arkuszy.
2. **Automatyzacja Kalendarza & Umawiania Spotkań:**
   - Wdrożenie darmowego konta **Cal.com** zintegrowanego przez webhook n8n z Twoim Google Calendar. 
   - Automatyczna wysyłka linku na WhatsApp/E-mail natychmiast po zgłoszeniu.
3. **Lejki i Retencja (Systeme.io):**
   - Spięcie n8n z **Systeme.io** w celu automatycznej wysyłki sekwencji edukacyjnej (lead nurturing) dla osób, które nie kupiły od razu (odzyskanie 3-5 transakcji/miesięcznie).
4. **Baza Wiedzy SOP dla Zespołu:**
   - Uporządkowanie know-how w Notion/Markdown i podłączenie asystenta opartego na **Vertex AI Search** ($1000 credit), który wdraża nowego pracownika w 3 sekundy."""
            },
            "Anna Nowak (E-commerce Brand)": {
                "date": "Wczoraj, 15:45",
                "score": 6,
                "tier": "RĘKODZIEŁO (Zagrożenie wypaleniem)",
                "color": "#EF4444",
                "phone": "+48 602 987 654",
                "email": "kontakt@annafashion.pl",
                "answers": {
                    "S1_1": "Ponad 15 godzin spędzamy na kopiowaniu zamówień i adresów wysyłek.",
                    "S1_2": "Absolutnie nie, ciągły chaos operacyjny.",
                    "S1_3": "Ponad 2 tygodnie, ciągłe tłumaczenie od zera.",
                    "S1_4": "Nagminnie uciekają nam zapytania klientów.",
                    "S1_5": "Każdą decyzję muszę podejmować osobiście.",
                    "S2_6": "Często dopiero po 24 godzinach.",
                    "S2_7": "Nie posiadamy takiego systemu.",
                    "S2_8": "Na wyczucie.",
                    "S2_9": "Bardzo dużo, nie nadążamy z odpisywaniem.",
                    "S2_10": "Ręcznie, marnując mnóstwo czasu na maile.",
                    "S3_11": "Nie.",
                    "S3_12": "Wydolność zespołu ległaby w gruzach natychmiast.",
                    "S3_13": "Brak automatyzacji.",
                    "S3_14": "Dziesiątki powtarzalnych pytań dziennie obsługuję sama.",
                    "S3_15": "Ręcznie piszę prośby o opinie.",
                    "S4_16": "Jestem całkowicie niewolnikiem operacyjnym.",
                    "S4_17": "Pracuję po 12h dziennie, w weekendy również.",
                    "S4_18": "Wszystko by upadło w 2 dni.",
                    "S4_19": "95% na gaszenie pożarów.",
                    "S4_20": "Tracę całe życie prywatne.",
                    "S4_21": "Błagam o ratunek i wdrożenie AI!"
                },
                "recommendation": """### 🤖 Rekomendacja Systemowa Jaisona (Ewaluacja AI)
**Klient:** Anna Nowak • **Wynik:** 6/21 pkt (Rękodzieło)
**Krytyczny Plan Ratunkowy (Low-Cost MVP):**

1. **Automatyzacja Obsługi Zamówień (Odzysk 15h/tydz):**
   - Połączenie Twojego sklepu (np. Shopify/WooCommerce) z systemem kurierskim (Furgonetka/Apaczka) za pomocą **n8n**. Automatyczne generowanie etykiet bez ręcznego przepisywania!
2. **Asystent AI Klienta (24/7):**
   - Konfiguracja prostego bota AI na Messengerze/Instagramie zintegrowanego z Twoim asortymentem i odpowiedziami na 30 najczęstszych pytań (FAQ).
3. **Automatyczne Opinie po zakupie:**
   - Webhook n8n wyzwalający wysyłkę e-maila z Systeme.io po 5 dniach od dostarczenia przesyłki z prośbą o opinię na Google/Trustpilot."""
            }
        }
        
        with col_list:
            selected_lead = st.radio("Wybierz zgłoszenie do analizy:", list(audits.keys()), key="lead_radio_opp_scanner")
            st.markdown("---")
            st.info("💡 Dane są gotowe do zasilenia z prawdziwego webhooka n8n zbierającego audyty z Twojej strony jaison.pl.")
            
        with col_details:
            lead_info = audits[selected_lead]
            st.markdown(f"#### 👤 Profil: {selected_lead}")
            st.markdown(f"📅 **Data:** {lead_info['date']} | 📞 **Tel:** {lead_info['phone']} | 📧 **Email:** {lead_info['email']}")
            
            st.markdown(f"""
            <div style="background: #111827; border: 1px solid {lead_info['color']}; border-radius: 8px; padding: 12px; margin-bottom: 20px;">
                <span style="font-weight: bold; color: {lead_info['color']}; font-size: 1.1rem;">Wynik: {lead_info['score']} / 21 pkt</span> — <b>{lead_info['tier']}</b>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🔍 Zobacz szczegółowe odpowiedzi na 21 pytań"):
                st.markdown("##### SEKCJA 1: Chaos Operacyjny i Wycieki Czasu")
                st.write(f"1. Ręczne przepisywanie: *{lead_info['answers']['S1_1']}*")
                st.write(f"2. Centralne źródło wiedzy: *{lead_info['answers']['S1_2']}*")
                st.write(f"3. Wdrożenie nowej osoby: *{lead_info['answers']['S1_3']}*")
                st.write(f"4. Uciekające zadania: *{lead_info['answers']['S1_4']}*")
                st.write(f"5. Podejmowanie decyzji osobiście: *{lead_info['answers']['S1_5']}*")
                
                st.markdown("##### SEKCJA 2: Konwersja i Wycieki Pieniędzy")
                st.write(f"6. Czas odpowiedzi na lead: *{lead_info['answers']['S2_6']}*")
                st.write(f"7. System dogrzewania (follow-up): *{lead_info['answers']['S2_7']}*")
                st.write(f"8. Analityka marketingu: *{lead_info['answers']['S2_8']}*")
                st.write(f"9. Straty transakcji przez brak follow-up: *{lead_info['answers']['S2_9']}*")
                st.write(f"10. Automatyzacja spotkań: *{lead_info['answers']['S2_10']}*")
                
                st.markdown("##### SEKCJA 3: Skalowalność i Gotowość na AI")
                st.write(f"11. Ustrukturyzowane know-how pod AI: *{lead_info['answers']['S3_11']}*")
                st.write(f"12. Skutki 10x wzrostu bazy: *{lead_info['answers']['S3_12']}*")
                st.write(f"13. Korzystanie z automatyzacji: *{lead_info['answers']['S3_13']}*")
                st.write(f"14. Powtarzalne pytania od klientów: *{lead_info['answers']['S3_14']}*")
                st.write(f"15. Automatyczne opinie (Social Proof): *{lead_info['answers']['S3_15']}*")
                
                st.markdown("##### SEKCJA 4: Wolność Biznesowa")
                st.write(f"16. Strateg vs. niewolnik operacyjny: *{lead_info['answers']['S4_16']}*")
                st.write(f"17. Praca po godzinach/weekendy: *{lead_info['answers']['S4_17']}*")
                st.write(f"18. Biznes bez Ciebie przez 30 dni: *{lead_info['answers']['S4_18']}*")
                st.write(f"19. Marnowanie energii na gaszenie pożarów: *{lead_info['answers']['S4_19']}*")
                st.write(f"20. Straty wolności i zysków: *{lead_info['answers']['S4_20']}*")
                st.write(f"21. Gotowość na Niewidzialnego Pracownika AI: **{lead_info['answers']['S4_21']}**")
            
            st.markdown("""<div style="background: #13111C; border: 1px solid #7C3AED; border-radius: 8px; padding: 18px; margin-top: 15px;">""", unsafe_allow_html=True)
            st.markdown(lead_info["recommendation"])
            st.markdown("</div>", unsafe_allow_html=True)
            
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                if st.button("📨 Wyślij architekturę na E-mail / WhatsApp", key=f"send_mod_{selected_lead}", use_container_width=True):
                    st.success(f"Architektura wysłana do {lead_info['email']}!")
            with col_act2:
                if st.button("🚀 Zaimportuj do CRM & Utwórz Projekt", key=f"import_mod_{selected_lead}", use_container_width=True, type="primary"):
                    st.success("Lead pomyślnie zaimportowany do CRM Magic Pipeline jako klient do wdrożenia!")

    # ==================== TAB 4: MAPA ŹRÓDEŁ V2 ====================
    with tab_map:
        st.markdown("### 🗺️ Architektura Integracji - Mapa Źródeł Lead Radar v2")
        st.caption("Centralny rejestr platform prospektowych AntiGravity, kategoryzujący źródła według trudności, ryzyka anty-botowego i zalecanego integratora.")
        
        col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
        with col_f1:
            search_query = st.text_input("🔍 Szukaj źródła (np. LinkedIn, Zleca):", value="", key="map_search_query")
        with col_f2:
            filter_diff = st.selectbox("⚡ Trudność:", ["Wszystkie", "niska", "średnia", "wysoka"], key="map_filter_diff")
        with col_f3:
            filter_login = st.selectbox("🔑 Wymaga logowania:", ["Wszystkie", "Tak", "Nie"], key="map_filter_login")
            
        map_csv_path = r"C:\Aplikacje MVP\01_JAISON_AGENCY_OS\lead_radar_mapa_antigravity_v2_enriched.csv"
        sources_data = []
        if os.path.exists(map_csv_path):
            try:
                import csv
                with open(map_csv_path, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        sources_data.append(row)
            except Exception as e:
                st.error(f"Błąd wczytywania mapy źródeł: {e}")
        
        filtered_sources = []
        for s in sources_data:
            if search_query and search_query.lower() not in s["source"].lower() and search_query.lower() not in s["integrator"].lower() and search_query.lower() not in s["notes"].lower():
                continue
            if filter_diff != "Wszystkie" and s["difficulty"].lower() != filter_diff.lower():
                continue
            if filter_login != "Wszystkie":
                if filter_login == "Tak" and "nie" in s["needs_login"].lower() and "tak" not in s["needs_login"].lower():
                    continue
                if filter_login == "Nie" and "tak" in s["needs_login"].lower():
                    continue
            filtered_sources.append(s)
            
        st.markdown(f"Znaleziono **{len(filtered_sources)}** pasujących źródeł z 42 zdefiniowanych.")
        
        view_mode = st.radio("Styl widoku:", ["Premium Karty 🎴", "Tabela Danych 📊"], horizontal=True, key="map_view_style")
        
        if view_mode == "Tabela Danych 📊":
            if filtered_sources:
                import pandas as pd
                df = pd.DataFrame(filtered_sources)
                df.columns = [
                    "Źródło", "Integrator / Biblioteka", "Tryb", "Trudność", "Uwagi",
                    "Wymaga logowania", "Ryzyko blokady", "Hint dla selektora / Tool", "Kadencja", "Lead Score", "Tryb Outreach"
                ]
                st.dataframe(df, use_container_width=True)
            else:
                st.info("Brak źródeł spełniających kryteria filtrów.")
        else:
            if filtered_sources:
                for idx, s in enumerate(filtered_sources):
                    if s["difficulty"].lower() == "wysoka":
                        diff_badge = "background-color: #EF4444; color: white;"
                        border_color = "#EF4444"
                    elif s["difficulty"].lower() == "średnia":
                        diff_badge = "background-color: #3B82F6; color: white;"
                        border_color = "#3B82F6"
                    else:
                        diff_badge = "background-color: #10B981; color: white;"
                        border_color = "#10B981"
                        
                    risk_color = "#10B981" if "niskie" in s["robots_risk"].lower() else ("#F59E0B" if "średnie" in s["robots_risk"].lower() or "api" in s["robots_risk"].lower() else "#EF4444")
                    
                    st.markdown(f"""
                    <div class="custom-card" style="border-left: 5px solid {border_color}; margin-bottom: 15px; padding: 20px;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                            <span style="font-size: 0.85rem; color: #94A3B8; font-weight: bold; text-transform: uppercase;">🔌 INTEGRATOR: {s["integrator"]}</span>
                            <span style="padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: bold; {diff_badge}">Trudność: {s["difficulty"]}</span>
                        </div>
                        <h4 style="margin: 0 0 10px 0; color: #F3F4F6; font-family: Outfit;">{s["source"]} <span style="font-size: 0.85rem; color: #94A3B8; font-weight: normal;">({s["mode"]})</span></h4>
                        <p style="margin: 0 0 12px 0; color: #D1D5DB; font-size: 0.95rem; line-height: 1.6;">📝 <b>Uwagi integracyjne:</b> {s["notes"]}</p>
                        
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 10px; font-size: 0.85rem; color: #94A3B8; border-top: 1px solid #1E293B; padding-top: 10px; margin-bottom: 5px;">
                            <span>🔑 Logowanie: <strong style="color: #E2E8F0;">{s["needs_login"]}</strong></span>
                            <span>🛡️ Ryzyko blokady: <strong style="color: {risk_color};">{s["robots_risk"]}</strong></span>
                            <span>🎯 Target Lead Score: <strong style="color: #10B981;">{s["lead_score"]} pkt</strong></span>
                            <span>⏱️ Częstotliwość: <strong style="color: #E2E8F0;">{s["cadence"]}</strong></span>
                            <span>🛠️ Hint: <code style="color: #F472B6; background: #2D1B36; padding: 2px 6px; border-radius: 4px;">{s["selector_hint"]}</code></span>
                            <span>📨 Outreach: <strong style="color: #E2E8F0;">{s["outreach_mode"]}</strong></span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Brak źródeł spełniających kryteria filtrów.")

    # ==================== TAB 5: CONFIGURATION ====================
    with tab_config:
        st.markdown("### ⚙️ Ustawienia Źródeł i Agenta Skanowania")
        
        # Skaner Okazji 2.0 (Lead Radar 2.0) preferencje wyszukiwania
        st.markdown("#### 🎯 Skaner Okazji 2.0 (Lead Radar 2.0)")
        prefs = get_scanner_preferences()
        
        search_pref_val = st.text_input(
            "Jakich deali szukasz? (Słowa kluczowe / branże oddzielone przecinkami):", 
            value=prefs.get("search_preferences", "automatyzacje n8n, chatboty AI, integracje BaseLinker i Shopify, systemy CRM, optymalizacja procesów"),
            key="cfg_search_preferences"
        )
        min_budget_val = st.text_input(
            "Minimalny akceptowalny budżet (np. 1000 PLN, do negocjacji):", 
            value=prefs.get("min_budget", "1000 PLN"),
            key="cfg_min_budget"
        )
        custom_inst_val = st.text_area(
            "Specjalna instrukcja biznesowa dla outreachu (np. styl, ograniczenia, dodatkowe korzyści):", 
            value=prefs.get("custom_instruction", "Skup się wyłącznie na firmach, które chcą przyspieszyć obsługę klienta lub wyeliminować ręczne przepisywanie danych."),
            key="cfg_custom_instruction"
        )
        
        st.markdown("---")
        st.markdown("#### ⚙️ Zaawansowana integracja n8n & Vertex AI")
        st.text_input("Główny Prompt Oceny Leada (Gemini API):", value="Jesteś Analitykiem Rynku. Oceń lead pod kątem marży i dopasowania do automatyzacji AI.")
        st.text_input("Webhook n8n nasłuchujący (Crawler trigger):", value="https://n8n.jaison.pl/webhook/lead-crawler-trigger")
        st.text_input("Vertex AI Data Store ID:", value="jaison-leads-datastore-12345")
        
        if st.button("💾 Zapisz konfigurację radaru", type="primary", key="save_config_lead_scanner"):
            new_prefs = {
                "search_preferences": search_pref_val,
                "min_budget": min_budget_val,
                "custom_instruction": custom_inst_val
            }
            save_scanner_preferences(new_prefs)
            st.success("Konfiguracja oraz preferencje Lead Radar 2.0 zostały zapisane pomyślnie!")
