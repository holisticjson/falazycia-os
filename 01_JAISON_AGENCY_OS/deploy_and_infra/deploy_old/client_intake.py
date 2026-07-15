"""
🔍 Client Intake Scanner — Moduł kwalifikacji klientów
Skanuje profile, strony, wizytówki i generuje kompletny brief.
"""
import streamlit as st
import json
from datetime import datetime
from pathlib import Path

import os

IS_CLOUD = os.environ.get("K_SERVICE") is not None
BASE_DIR = Path("/app") if IS_CLOUD else Path(r"c:\Aplikacje MVP\Holistic Jason")

# Folder na briefy klientów
CLIENTS_DIR = BASE_DIR / "clients"
CLIENTS_DIR.mkdir(exist_ok=True)

BUSINESS_TYPES = {
    "🎬 Twórca / Influencer": "creator",
    "🏥 Usługi lokalne (gabinet, klinika, kancelaria)": "local_services",
    "🛒 E-commerce / Sklep internetowy": "ecommerce",
    "💼 Freelancer / Konsultant": "freelancer",
    "🚀 SaaS / Startup": "saas",
    "🏗️ Inny": "other",
}

def render_intake_form():
    """Renderuje formularz kwalifikacyjny klienta"""
    st.header("🔍 Client Intake Scanner")
    st.caption("Wypełnij dane klienta → system automatycznie przygotuje kompletny brief.")
    
    with st.form("intake_form"):
        st.subheader("1️⃣ Podstawowe dane")
        col1, col2 = st.columns(2)
        with col1:
            client_name = st.text_input("Nazwa firmy / twórcy *")
            business_type = st.selectbox("Typ biznesu *", list(BUSINESS_TYPES.keys()))
        with col2:
            contact_name = st.text_input("Osoba kontaktowa")
            contact_email = st.text_input("Email")
        
        niche = st.text_input("Nisza / branża (np. 'medycyna estetyczna', 'fitness online')")
        
        st.subheader("2️⃣ Obecność online")
        col3, col4 = st.columns(2)
        with col3:
            website_url = st.text_input("URL strony internetowej")
            instagram_url = st.text_input("Instagram (link lub @handle)")
            tiktok_url = st.text_input("TikTok (link lub @handle)")
        with col4:
            linkedin_url = st.text_input("LinkedIn (link)")
            youtube_url = st.text_input("YouTube (link)")
            google_business = st.text_input("Google Business (nazwa lub link)")
        
        st.subheader("3️⃣ Sytuacja biznesowa")
        team_size = st.selectbox("Wielkość zespołu", ["Solo", "2-5 osób", "6-15 osób", "16-50 osób", "50+"])
        monthly_revenue = st.selectbox("Przychód miesięczny (PLN)", [
            "Dopiero startuję", "< 5 000", "5 000 - 20 000", 
            "20 000 - 50 000", "50 000 - 200 000", "200 000+"
        ])
        
        current_tools = st.multiselect("Używane narzędzia", [
            "Brak strony", "WordPress", "Shopify", "WooCommerce",
            "Mailchimp", "ActiveCampaign", "HubSpot", "Go High Level",
            "Canva", "Meta Ads", "Google Ads", "Brak CRM", "Excel/Arkusze"
        ])
        
        st.subheader("4️⃣ Główne problemy i cele")
        main_problems = st.text_area(
            "Co jest największym problemem / bólem w biznesie?",
            placeholder="Np. 'Tracę czas na ręczne odpowiadanie na zapytania, nie mam systemu follow-up, klienci się gubią'"
        )
        main_goals = st.text_area(
            "Jaki cel chcesz osiągnąć w ciągu 3-6 miesięcy?",
            placeholder="Np. 'Chcę zautomatyzować lead capture i umawianie spotkań, zwiększyć konwersję o 30%'"
        )
        
        competitors = st.text_area(
            "Główni konkurenci (nazwy lub linki, po jednym w linii)",
            placeholder="Np. 'www.konkurent1.pl\nwww.konkurent2.pl'"
        )
        
        budget = st.selectbox("Budżet na wdrożenie", [
            "Do ustalenia", "< 2 000 PLN", "2 000 - 5 000 PLN",
            "5 000 - 15 000 PLN", "15 000 - 50 000 PLN", "50 000+"
        ])
        
        deep_research = st.checkbox("🔍 Uruchom Deep Research (analiza konkurencji + buyer persona)", value=True)
        
        submitted = st.form_submit_button("🚀 Generuj Brief Klienta", type="primary", use_container_width=True)
    
    if submitted and client_name:
        return {
            "client_name": client_name,
            "business_type": BUSINESS_TYPES[business_type],
            "business_type_label": business_type,
            "contact_name": contact_name,
            "contact_email": contact_email,
            "niche": niche,
            "website_url": website_url,
            "instagram_url": instagram_url,
            "tiktok_url": tiktok_url,
            "linkedin_url": linkedin_url,
            "youtube_url": youtube_url,
            "google_business": google_business,
            "team_size": team_size,
            "monthly_revenue": monthly_revenue,
            "current_tools": current_tools,
            "main_problems": main_problems,
            "main_goals": main_goals,
            "competitors": competitors,
            "budget": budget,
            "deep_research": deep_research,
            "timestamp": datetime.now().isoformat(),
        }
    return None

def build_intake_prompt(data):
    """Buduje prompt orkiestracyjny z danych ankiety"""
    tools_str = ", ".join(data["current_tools"]) if data["current_tools"] else "Brak"
    
    prompt = f"""BRIEF KLIENTA DO ANALIZY I PRZYGOTOWANIA STRATEGII:

## Profil Klienta
- **Firma:** {data['client_name']}
- **Typ biznesu:** {data['business_type_label']}
- **Nisza:** {data['niche']}
- **Zespół:** {data['team_size']}
- **Przychód:** {data['monthly_revenue']}
- **Budżet na wdrożenie:** {data['budget']}

## Obecność Online
- Strona: {data['website_url'] or 'BRAK'}
- Instagram: {data['instagram_url'] or 'BRAK'}
- TikTok: {data['tiktok_url'] or 'BRAK'}
- LinkedIn: {data['linkedin_url'] or 'BRAK'}
- YouTube: {data['youtube_url'] or 'BRAK'}
- Google Business: {data['google_business'] or 'BRAK'}

## Narzędzia: {tools_str}

## Problemy: {data['main_problems']}
## Cele: {data['main_goals']}
## Konkurenci: {data['competitors']}

---

ZADANIE: Przygotuj KOMPLETNĄ strategię dla tego klienta:
1. Dyrektor Marketingu: Strategia lejka i kanałów dotarcia
2. Copywriter: 3 buyer persony (imię, wiek, ból, pragnienie, obiekcje, trigger zakupowy)
3. SEO: Analiza widoczności i rekomendacje
4. Architekt Automatyzacji: Propozycja systemów GHL (workflows, pipeline, calendar)
5. Projektant Ofert: Mockup strony + wycena usług Holistic Operator
{"6. Deep Research: Analiza 3-5 konkurentów, content gaps, pozycjonowanie" if data.get('deep_research') else ""}

Stwórz dokument gotowy do prezentacji klientowi."""
    
    return prompt

def create_client_workspace(data):
    """Tworzy strukturę folderów dla klienta"""
    slug = data["client_name"].replace(" ", "_").replace("/", "-")[:30]
    date = datetime.now().strftime("%Y%m%d")
    client_dir = CLIENTS_DIR / f"{slug}_{date}"
    
    folders = [
        "01_Brief", "02_Branding/Logo", "02_Branding/Kolory_Fonty",
        "03_Content/Copy_Strona", "03_Content/Email_Sequences", "03_Content/Social_Media",
        "04_Grafiki/Posts_IG", "04_Grafiki/Stories", "04_Grafiki/Banery",
        "05_Video/Shorts", "05_Video/Reels",
        "06_Automatyzacja", "07_Raporty"
    ]
    
    for folder in folders:
        (client_dir / folder).mkdir(parents=True, exist_ok=True)
    
    # Zapisz brief
    brief_path = client_dir / "01_Brief" / "brief_kwalifikacyjny.md"
    with open(brief_path, "w", encoding="utf-8") as f:
        f.write(f"# Brief Klienta: {data['client_name']}\n")
        f.write(f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        for key, val in data.items():
            if key != "timestamp":
                f.write(f"- **{key}:** {val}\n")
    
    return client_dir
