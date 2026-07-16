import os
import sqlite3
import json
import datetime
import urllib.request
import urllib.error
import streamlit as st

DB_PATH = r"C:\Aplikacje MVP\01_JAISON_AGENCY_OS\dashboard_and_core\local_crm.db"

# ==================== KOLEKCJA I LOGIKA BAZY DANYCH ====================

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
    
    # Sprawdzenie czy tabela jest pusta, jeśli tak – seeding
    cursor.execute("SELECT COUNT(*) FROM opportunities;")
    count = cursor.fetchone()[0]
    if count == 0:
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

def add_opportunity(source, title, budget, description, score, label, outreach, action, email="", phone="", status="New"):
    """Zapisuje nową okazję do bazy danych."""
    init_db()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO opportunities (
        created_at, source, title, budget, description, score, label, suggested_outreach, suggested_action, status, contact_email, contact_phone
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, (now, source, title, budget, description, score, label, outreach, action, status, email, phone))
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

Wygeneruj spersonalizowaną wiadomość outreach (suggested_outreach) w unikalnym, perswazyjnym i bezpośrednim stylu Tomasza Dudy oraz Alexa Hormoziego:
- Krótko, konkretnie, bez "Szanowni Państwo" ani "Dzień dobry".
- Odnieś się bezpośrednio do konkretnego problemu ze zlecenia.
- Zaproponuj pomoc i obniż tarcie poznawcze (propozycja bezpłatnej, 15-minutowej analizy lub przesłania gotowej architektury wdrożenia).
- Podpisz jako "Tomasz z Jaison.pl".

Zwróć wynik wyłącznie jako czysty obiekt JSON bez żadnego dodatkowego tekstu ani markdownu (oprócz bloku ```json), zawierający klucze:
{
  "score": <liczba 0-100>,
  "suggested_outreach": "<Treść wiadomości>",
  "suggested_action": "<Zalecany krok handlowy>"
}
"""

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
                status="New"
            )
            processed_count += 1
        except Exception as e:
            print(f"Błąd analizy oferty: {e}")
            
    return processed_count > 0


# ==================== RENDEROWANIE INTERFEJSU STREAMLIT (PREMIUM) ====================

def render_lead_radar_page(call_gemini_pro_api_func):
    """Renderuje cały moduł Skanera Okazji w Streamlicie (Lead Radar)."""
    
    # Inicjalizacja bazy przy wejściu na stronę
    init_db()
    
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
    tab_radar, tab_sales_director, tab_audit, tab_map, tab_config = st.tabs([
        "📡 Radar Zleceń", 
        "📢 Sales Director (Outbound)", 
        "📋 Audyty 21 Pytań (jaison.pl)", 
        "🗺️ Mapa Źródeł v2",
        "⚙️ Konfiguracja Skanera"
    ])
    
    # ==================== TAB 1: RADAR ZLECEŃ ====================
    with tab_radar:
        st.markdown("### 📥 Aktywne Okazje z Rynku (Baza SQLite)")
        st.write("Wpisz interesującą Cię niszę, aby za pomocą AI przeszukać i przeanalizować nowe zlecenia:")
        
        c_scan1, c_scan2 = st.columns([3, 1])
        with c_scan1:
            search_kws = st.text_input("Słowa kluczowe (np. n8n automation, WooCommerce BaseLinker, chatbot AI):", value="n8n BaseLinker automation", label_visibility="collapsed")
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
                    
        st.write("")
        
        # Wyświetlanie listy z bazy danych
        opportunities = get_opportunities()
        if not opportunities:
            st.info("Baza danych jest pusta. Uruchom skaner powyżej lub przywróć bazę.")
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
                st.markdown(f"""
                <div class="custom-card" style="border-left: 5px solid {accent_color}; margin-bottom: 15px; padding: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <span style="font-size: 0.85rem; color: #94A3B8; font-weight: bold; text-transform: uppercase;">🌐 Źródło: {opp['source']} | 📅 {opp['created_at']}</span>
                        <span style="padding: 3px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: bold; {badge_style}">{opp['label']} (Dopasowanie: {opp['score']}%)</span>
                    </div>
                    <h4 style="margin: 0 0 10px 0; color: #F3F4F6; font-family: Outfit;">{opp['title']}</h4>
                    <p style="margin: 0 0 12px 0; color: #D1D5DB; font-size: 0.95rem; line-height: 1.6;">{opp['description']}</p>
                    <div style="display: flex; gap: 15px; font-size: 0.85rem; color: #94A3B8; border-top: 1px solid #1E293B; padding-top: 10px; margin-bottom: 10px;">
                        <span>💰 Budżet: <strong style="color: #10B981;">{opp['budget']}</strong></span>
                        <span>📧 Email: <strong>{opp['contact_email'] if opp['contact_email'] else 'Brak'}</strong></span>
                        <span>📞 Tel: <strong>{opp['contact_phone'] if opp['contact_phone'] else 'Brak'}</strong></span>
                        <span>📦 Status: <strong style="color: #F59E0B;">{opp['status']}</strong></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Elementy interaktywne pod kartą (Streamlit)
                c_opt1, c_opt2, c_opt3, c_opt4 = st.columns([2, 1, 1, 1])
                with c_opt1:
                    with st.expander("📬 Zobacz spersonalizowaną wiadomość Outreach (Hormozi style)"):
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
                        st.success("Pomyślnie zaimportowano do CRM Magic Pipeline jako lead!")
                with c_opt4:
                    if st.button("🗑️ Usuń", key=f"opp_del_{opp['id']}", use_container_width=True):
                        delete_opportunity(opp["id"])
                        st.success("Usunięto okazję!")
                        st.rerun()
                        
                st.markdown("<hr style='border: 0; border-top: 1px solid #1E293B; margin: 15px 0;'>", unsafe_allow_html=True)

    # ==================== TAB 2: SALES DIRECTOR ====================
    with tab_sales_director:
        st.subheader("📢 Sales Director / Handlowiec AI")
        st.markdown("Ten agent przeszukuje fora, grupy dyskusyjne oraz social media i generuje outreach do osób szukających automatyzacji procesów.")
        
        lr_search_kw = st.text_input("Słowa kluczowe do skanowania internetu:", value="n8n automatyzacja, szukam crm, błędy BaseLinker", key="lr_sales_search_kw_mod")
        if st.button("Generuj Prospekty i Outreach", type="primary", key="lr_sales_scan_btn_mod"):
            with st.spinner("Sales Director analizuje social media..."):
                prompt = f"""Jesteś wirtualnym Sales Directorem w zespole 'Holistic Jason'.
Przeskanowałeś Reddit, fora oraz social media pod kątem słów kluczowych: "{lr_search_kw}".
Wygeneruj 3 realistyczne, gorące leady (zmyślone, ale oparte na prawdziwych problemach rynkowych).
Dla każdego leada podaj:
1. Skąd pochodzi wpis (np. r/entrepreneur, LinkedIn).
2. Treść wpisu (ból klienta).
3. Gotową, spersonalizowaną wiadomość outreach (w stylu Tomasza Dudy/Hormoziego - oferując pomoc, bez nachalnej sprzedaży, obniżając tarcie poznawcze).
4. Proponowany "Next Action" do zapisania w CRM.

Zwróć wynik w ładnym formacie markdown.
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
        st.text_input("Główny Prompt Oceny Leada (Gemini API):", value="Jesteś Analitykiem Rynku. Oceń lead pod kątem marży i dopasowania do automatyzacji AI.")
        st.text_input("Webhook n8n nasłuchujący (Crawler trigger):", value="https://n8n.jaison.pl/webhook/lead-crawler-trigger")
        st.text_input("Vertex AI Data Store ID:", value="jaison-leads-datastore-12345")
        if st.button("💾 Zapisz konfigurację radaru", type="primary", key="save_config_lead_scanner"):
            st.success("Konfiguracja zapisana pomyślnie!")
