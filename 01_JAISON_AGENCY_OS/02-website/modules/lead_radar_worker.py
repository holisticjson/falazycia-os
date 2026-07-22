import os
import sqlite3
import datetime
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re
import json
import requests

# Ścieżka do bazy danych SQLite
DB_PATH = r"C:\Aplikacje MVP\01_JAISON_AGENCY_OS\02-website\local_crm.db"

def init_db_v2():
    """Inicjalizuje tabelę opportunities i dba o to, by miała wszystkie niezbędne kolumny."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    
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
        contact_phone TEXT,
        url_link TEXT,
        user_feedback INTEGER DEFAULT 0,
        user_feedback_reason TEXT,
        competitor_ads_context TEXT
    );
    """)
    conn.commit()
    
    # Dodanie dodatkowych pól ze specyfikacji Perplexity
    for col_name, col_type in [
        ("published_at", "TEXT"),
        ("source_type", "TEXT"),
        ("lead_type", "TEXT"),
        ("organization", "TEXT"),
        ("city", "TEXT"),
        ("intent_score", "INTEGER DEFAULT 0"),
        ("fit_score", "INTEGER DEFAULT 0"),
        ("freshness_score", "INTEGER DEFAULT 0"),
        ("priority_score", "INTEGER DEFAULT 0")
    ]:
        try:
            cursor.execute(f"ALTER TABLE opportunities ADD COLUMN {col_name} {col_type};")
            conn.commit()
        except sqlite3.OperationalError:
            pass # Kolumna już istnieje
            
    conn.close()

def expand_queries_with_ai(base_keyword):
    """
    Rozszerza zapytania (AI Query Expansion) zgodnie ze specyfikacją Perplexity.
    Zamiast jednego ogólnego słowa, generuje precyzyjną listę powiązanych fraz popytu.
    """
    together_key = os.getenv("TOGETHER_API_KEY", "")
    if not together_key:
        # Fallback do zdefiniowanej listy słów kluczowych, jeśli brak klucza
        return [base_keyword, "chatbot", "automatyzacja", "n8n", "Make", "wdrożenie AI", "integracja API", "strona internetowa"]
        
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {together_key}"
    }
    
    prompt = f"""
    Jako ekspert marketingu i SEO agencji Jaison, rozszerz słowo kluczowe: "{base_keyword}" na 6 powiązanych, precyzyjnych polskich słów/fraz kluczowych, które klienci wpisują w wyszukiwarkach lub zleceniach, gdy szukają usług automatyzacji, stron www, chatbotów lub wdrożeń AI.
    Odpowiedz wyłącznie surową listą JSON z polami (np. ["fraza1", "fraza2", ...]). Nie pisz żadnych dodatkowych tekstów ani markdown.
    """
    
    payload = {
        "model": "deepseek-ai/DeepSeek-R1-distill-qwen-32b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=15)
        if res.status_code == 200:
            content = res.json()["choices"][0]["message"]["content"]
            # Próba wycięcia JSON
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
    except Exception as e:
        print(f"Błąd Query Expansion AI: {e}")
        
    return [base_keyword, f"automatyzacja {base_keyword}", f"chatbot {base_keyword}", "n8n", "Make.com", "wdrożenie AI"]

def scrape_useme(keyword):
    """Pobiera oferty z Useme pod kątem słowa kluczowego."""
    query = urllib.parse.quote(keyword)
    search_url = f"https://useme.com/pl/jobs/?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    jobs = []
    try:
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        pattern = re.compile(r'/pl/jobs/[^/]+,\d+/?$')
        seen = set()
        
        for a in soup.find_all('a', href=True):
            href = a['href']
            if pattern.search(href):
                full_url = f"https://useme.com{href}" if href.startswith("/") else href
                if full_url not in seen:
                    seen.add(full_url)
                    title = a.get_text().strip()
                    jobs.append({
                        "title": title,
                        "url": full_url,
                        "source": "Useme"
                    })
    except Exception as e:
        print(f"Błąd scrapowania Useme ({keyword}): {e}")
    return jobs

def scrape_zleca(keyword):
    """Pobiera oferty ze Zleca.pl (rekomendacja Perplexity Faza 1)."""
    query = urllib.parse.quote(keyword)
    search_url = f"https://zleca.pl/szukaj-zlecen?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    jobs = []
    try:
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        seen = set()
        
        # Analiza struktury Zleca.pl pod kątem linków do zleceń
        for a in soup.find_all('a', href=True):
            href = a['href']
            if "/zlecenie/" in href:
                full_url = f"https://zleca.pl{href}" if href.startswith("/") else href
                if full_url not in seen:
                    seen.add(full_url)
                    title = a.get_text().strip()
                    if len(title) > 5:
                        jobs.append({
                            "title": title,
                            "url": full_url,
                            "source": "Zleca.pl"
                        })
    except Exception as e:
        print(f"Błąd scrapowania Zleca.pl ({keyword}): {e}")
    return jobs

def get_job_description(url, source):
    """Pobiera szczegółowy opis i budżet dla danej oferty."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        
        description = ""
        budget = "Do negocjacji"
        
        if source == "Useme":
            # Opis z Useme
            desc_elem = soup.find(class_="job-details-description") or soup.find(class_="job-description")
            if desc_elem:
                description = desc_elem.get_text().strip()
            # Budżet
            price_elem = soup.find(class_="job-details-price") or soup.find(class_="price")
            if price_elem:
                budget = price_elem.get_text().strip()
        elif source == "Zleca.pl":
            # Opis ze Zleca.pl
            desc_elem = soup.find(class_="announcement-description") or soup.find(class_="description")
            if desc_elem:
                description = desc_elem.get_text().strip()
            # Budżet
            price_elem = soup.find(class_="budget-value") or soup.find(class_="price")
            if price_elem:
                budget = price_elem.get_text().strip()
                
        # Jeśli nie pobrano opisu, użyj tekstu zastępczego
        if not description:
            description = "Pobierz szczegółowy opis bezpośrednio na platformie, klikając w link."
            
        return description, budget
    except Exception as e:
        print(f"Błąd pobierania opisu z {url}: {e}")
        return "Pobierz szczegółowy opis bezpośrednio na platformie, klikając w link.", "Do negocjacji"

def analyze_and_score_lead_with_deepseek(title, description, source):
    """
    Bezlitosne filtrowanie spamu logiczne oraz scoring za pomocą DeepSeek-R1.
    Skanuje pod kątem fałszywych dopasowań (np. zasilacze LED dla frazy LED).
    """
    together_key = os.getenv("TOGETHER_API_KEY", "")
    if not together_key:
        # Fallback do tradycyjnego scoringu słów kluczowych
        return evaluate_traditional_scoring(title, description, source)
        
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {together_key}"
    }
    
    prompt = f"""
    Zanalizuj poniższą ofertę zlecenia pod kątem dopasowania do agencji Jaison (jaison.pl), która wdraża:
    - automatyzacje procesów biznesowych (n8n, Make, zapier, CRM)
    - zaawansowane chatboty i asystentów AI z uziemieniem danych (Vertex AI, OpenAI, Gemini)
    - luksusowe, szybkie strony internetowe / landing page (HTML/CSS/JS, Streamlit)
    - optymalizację lokalnego SEO (GBP / Google Maps)
    
    Tytuł zlecenia: "{title}"
    Opis zlecenia: "{description}"
    Źródło: {source}
    
    ### ZADANIE:
    1. Wykryj bezlitośnie SPAM lub fałszywe dopasowania (np. jeśli fraza to "LED", a zlecenie dotyczy "zasilacza do taśmy LED", "montażu pasków LED w kuchni", "instalacji oświetlenia LED" - to jest to SPAM / BŁĘDNE DOPASOWANIE, ponieważ nie wdrażamy elektryki!).
    2. Odsiej zlecenia dotyczące stałej pracy etatowej (chyba, że dopuszczają współpracę B2B).
    3. Przydziel oceny (0-100):
       - intent_score: Czy klient chce kupić już teraz, ma konkretny budżet i zakres? (0-100)
       - fit_score: Czy zakres zlecenia idealnie pokrywa się z automatyzacją n8n, chatbotem AI, stroną www premium lub lokalnym SEO? (0-100)
       - priority_score: Średnia ważona (fit_score * 0.6 + intent_score * 0.4). Jeśli to SPAM lub zasilacz LED -> priority_score MUSI wynosić 0!
    4. Stwórz porywający, spersonalizowany i perswazyjny draft wiadomości outreach (odpowiedzi na zlecenie) w unikalnym, surowym, zaangażowanym tonie Tomasza (GHOST v2). Używaj wyłącznie tagów <strong> i </strong> do pogrubień (CAŁKOWITY ZAKAZ używania gwiazdek markdown ** w tekście HTML!).
    
    Zwróć odpowiedź w czystym formacie JSON bez bloków ```json:
    {{
        "is_spam": true/false,
        "spam_reason": "powód odrzucenia",
        "lead_type": "automation/chatbot/website/seo/api/spam",
        "intent_score": 85,
        "fit_score": 90,
        "priority_score": 87,
        "suggested_outreach": "Tekst wiadomości z tagami <strong>pogrubienie</strong>, bez gwiazdek markdown"
    }}
    """
    
    payload = {
        "model": "deepseek-ai/DeepSeek-R1-distill-qwen-32b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2
    }
    
    try:
        res = requests.post(url, json=payload, headers=headers, timeout=20)
        if res.status_code == 200:
            content = res.json()["choices"][0]["message"]["content"]
            # Próba wyciągnięcia JSON z tekstu lub myślenia DeepSeek
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group(0))
                # Czyszczenie markdown z tekstu outreach na wypadek wycieku gwiazdek (RULE 13)
                if "suggested_outreach" in parsed:
                    parsed["suggested_outreach"] = parsed["suggested_outreach"].replace("**", "<strong>").replace("<em>", "<em>") # dla bezpieczeństwa
                return parsed
    except Exception as e:
        print(f"Błąd analizy DeepSeek-R1: {e}")
        
    return evaluate_traditional_scoring(title, description, source)

def evaluate_traditional_scoring(title, description, source):
    """Tradycyjny scoring oparty o słowa kluczowe (gdy brak klucza Together AI)."""
    title_lower = title.lower()
    desc_lower = description.lower()
    
    is_spam = False
    spam_reason = ""
    lead_type = "mixed"
    
    # Detekcja spamu LED (zasilacze itp.)
    if "zasilacz" in desc_lower or "taśm" in desc_lower or "montaż" in desc_lower or "elektry" in desc_lower:
        is_spam = True
        spam_reason = "Elektryka / zasilacze LED - brak dopasowania cyfrowego"
        
    fit_score = 50
    intent_score = 60
    
    if "chatbot" in desc_lower or "voicebot" in desc_lower:
        lead_type = "chatbot"
        fit_score += 30
    elif "automatyz" in desc_lower or "n8n" in desc_lower or "make" in desc_lower:
        lead_type = "automation"
        fit_score += 30
    elif "stron" in desc_lower or "landing" in desc_lower:
        lead_type = "website"
        fit_score += 20
    elif "seo" in desc_lower or "wizytów" in desc_lower or "map" in desc_lower:
        lead_type = "seo"
        fit_score += 20
        
    if "pilne" in desc_lower or "budżet" in desc_lower:
        intent_score += 20
        
    priority_score = int(fit_score * 0.6 + intent_score * 0.4)
    if is_spam:
        priority_score = 0
        
    outreach = f"Dzień dobry! Z wielką chęcią pomogę w realizacji zlecenia: <strong>{title}</strong>. Posiadam bogate doświadczenie w automatyzacjach i wdrożeniach systemów IT."
    
    return {
        "is_spam": is_spam,
        "spam_reason": spam_reason,
        "lead_type": lead_type,
        "intent_score": intent_score,
        "fit_score": fit_score,
        "priority_score": priority_score,
        "suggested_outreach": outreach
    }

def run_lead_radar_sync(keyword="strona internetowa"):
    """
    Główna funkcja synchronizacji i orkiestracji Radaru Zleceń.
    Rozszerza słowa kluczowe, pobiera oferty ze źródeł, filtruje przez DeepSeek i zapisuje do SQLite.
    """
    init_db_v2()
    print(f"📡 Start synchronizacji Radaru Zleceń dla słowa kluczowego: '{keyword}'...")
    
    # Rozszerzanie zapytań (AI Query Expansion)
    expanded_keywords = expand_queries_with_ai(keyword)
    print(f"🔑 Rozszerzone frazy kluczowe: {expanded_keywords}")
    
    all_raw_jobs = []
    
    # Scrapowanie dla każdego słowa kluczowego
    for kw in expanded_keywords:
        useme_jobs = scrape_useme(kw)
        zleca_jobs = scrape_zleca(kw)
        all_raw_jobs.extend(useme_jobs)
        all_raw_jobs.extend(zleca_jobs)
        
    # Deduplikacja po URL
    unique_jobs = {}
    for job in all_raw_jobs:
        unique_jobs[job["url"]] = job
        
    print(f"📥 Znaleziono {len(unique_jobs)} unikalnych ogłoszeń. Rozpoczynam pobieranie szczegółów i analizę AI...")
    
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    
    saved_count = 0
    spam_count = 0
    
    for url, job in unique_jobs.items():
        # Sprawdzamy czy oferta już istnieje w bazie
        cursor.execute("SELECT id FROM opportunities WHERE url_link = ?;", (url,))
        exists = cursor.fetchone()
        if exists:
            continue
            
        title = job["title"]
        source = job["source"]
        
        # Pobranie opisu i budżetu
        description, budget = get_job_description(url, source)
        
        # Analiza i scoring za pomocą DeepSeek-R1
        ai_res = analyze_and_score_lead_with_deepseek(title, description, source)
        
        if ai_res.get("is_spam", False):
            print(f"🗑️ Odrzucono SPAM: '{title}' ({ai_res.get('spam_reason', 'Brak powodu')})")
            spam_count += 1
            continue
            
        # Zapis do bazy danych
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute("""
        INSERT INTO opportunities (
            created_at, source, title, budget, description, score, label, 
            suggested_outreach, status, url_link, published_at, source_type, 
            lead_type, intent_score, fit_score, priority_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            now,
            source,
            title,
            budget,
            description,
            ai_res.get("priority_score", 50),
            ai_res.get("lead_type", "mixed").upper(),
            ai_res.get("suggested_outreach", ""),
            "Nowy",
            url,
            now,
            "freelance",
            ai_res.get("lead_type", "mixed"),
            ai_res.get("intent_score", 50),
            ai_res.get("fit_score", 50),
            ai_res.get("priority_score", 50)
        ))
        conn.commit()
        saved_count += 1
        print(f"⭐ Zapisano okazję B2B: '{title}' [Priorytet: {ai_res.get('priority_score', 50)}/100]")
        
    conn.close()
    print(f"📊 Podsumowanie: Zapisano {saved_count} nowych okazji, odrzucono {spam_count} spamu.")
    return saved_count

if __name__ == "__main__":
    run_lead_radar_sync()
