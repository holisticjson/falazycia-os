import streamlit as st
from google import genai
from datetime import datetime
from pathlib import Path
import os
import json

def get_vertex_client():
    """Zwraca klienta Vertex AI (aby wykorzystać darmowe kredyty GCP)"""
    VERTEX_PROJECT = os.environ.get("GCP_PROJECT", "holistic-dashboard-dev")
    VERTEX_LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
    SA_KEY_PATH = r"c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"
    
    if os.path.exists(SA_KEY_PATH):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_KEY_PATH
        
    try:
        return genai.Client(vertexai=True, project=VERTEX_PROJECT, location=VERTEX_LOCATION)
    except Exception:
        return genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def render_market_radar():
    st.title("📡 Market Holistic Radar")
    
    tabs = st.tabs(["🔍 Skaner Leadów/Problemów", "💰 Trending Affiliate Scanner"])
    
    # --- TAB 1: LEAD SCANNER ---
    with tabs[0]:
        st.markdown("""
        **Moduł Skanera Problemów** 
        Agent *Holistic-Researcher* skanuje internet w poszukiwaniu bolączek, które Twoje systemy mogą rozwiązać.
        """)
        
        with st.form("radar_form"):
            niche = st.text_input("🎯 Kogo/czego szukamy?", placeholder="np. polskie agencje marketingowe, problemy e-commerce")
            focus = st.selectbox("🔍 Cel skanowania:", [
                "Identyfikacja problemów i bolączek",
                "Szukanie leadów i partnerów",
                "Analiza konkurencji"
            ])
            submitted = st.form_submit_button("🚀 Uruchom Researchera", type="primary")
            
        if submitted and niche:
            run_deep_search(niche, focus)

    # --- TAB 2: AFFILIATE SCANNER ---
    with tabs[1]:
        st.markdown("""
        **💰 Trending Affiliate Scanner**
        Wyszukuje najbardziej dochodowe produkty i subskrypcje do afiliacji (PL, EU, US).
        """)
        
        with st.form("affiliate_form"):
            region = st.selectbox("🌍 Region:", ["Polska", "Europa (UE)", "Stany Zjednoczone (USA)", "Global"])
            category = st.multiselect("📦 Kategorie:", ["Zdrowie (Biohacking/Supps)", "Biznes (SaaS/AI Tools)", "Finanse (Inwestycje)", "E-commerce", "Edukacja/Kursy"], default=["Zdrowie (Biohacking/Supps)", "Biznes (SaaS/AI Tools)"])
            model_type = st.radio("🔄 Model prowizji:", ["Cykliczna (Subscription/Recurring)", "Jednorazowa (High Ticket)", "Oba"])
            
            submitted_aff = st.form_submit_button("💰 Skanuj Rynek Afiliacyjny", type="primary")
            
        if submitted_aff:
            run_affiliate_search(region, category, model_type)

def run_deep_search(niche, focus):
    with st.spinner("Skanowanie sieci na żywo..."):
        client = get_vertex_client()
        prompt = f"Zrób głęboki research rynkowy dla niszy: {niche}. Cel: {focus}. Wyciągnij GŁÓWNE BÓLE i problemy."
        
        try:
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt,
                config=genai.types.GenerateContentConfig(tools=[{"google_search": {}}], temperature=0.4)
            )
            st.markdown(response.text)
            save_to_sack("Radar", response.text)
        except Exception as e:
            st.error(f"Błąd: {e}")

def run_affiliate_search(region, category, model_type):
    with st.spinner(f"Przeszukiwanie baz afiliacyjnych dla regionu {region}..."):
        client = get_vertex_client()
        
        # Bazy wiedzy wbudowane w prompt na podstawie researchu
        affiliate_knowledge = """
        PORTALE W POLSCE: MyLead, Leadstar, Conversand, Money2Money, ComperiaLead, NutriProfits, Admitad, Awin, WebePartners.
        GLOBALNE: ClickBank, Impact.com, ShareASale, CJ Affiliate, Rakuten, Amazon Associates.
        TRENDY 2026: Biohacking (suplementy personalizowane), AI SaaS (automatyzacje), FinTech (konta z wysokim % + krypto).
        """
        
        prompt = f"""
        Jesteś ekspertem ds. afiliacji (Affiliate Scout). 
        Znajdź top 5 TRENUJĄCYCH produktów/programów afiliacyjnych dla:
        REGION: {region}
        KATEGORIE: {', '.join(category)}
        MODEL: {model_type}
        
        WIEDZA O RYNKU:
        {affiliate_knowledge}
        
        Dla każdego produktu podaj:
        1. Nazwa produktu/programu
        2. Gdzie go znaleźć (portal/sieć)
        3. Estymowana prowizja (i czy jest recurring/cykliczna)
        4. DLACZEGO to trenduje (jaki ból rozwiązuje?)
        5. Propozycja kąta marketingowego dla AI Influencera.
        
        Użyj Google Search, aby znaleźć najświeższe dane z 2026 roku.
        """
        
        try:
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt,
                config=genai.types.GenerateContentConfig(tools=[{"google_search": {}}], temperature=0.4)
            )
            st.markdown('<div class="inflow-card">', unsafe_allow_html=True)
            st.subheader(f"💰 Top Okazje Afiliacyjne: {region}")
            st.markdown(response.text)
            st.markdown('</div>', unsafe_allow_html=True)
            save_to_sack("Affiliate", response.text)
        except Exception as e:
            st.error(f"Błąd: {e}")

def save_to_sack(prefix, content):
    sack_dir = Path("Baza_Wiedzy/Notyfikacje")
    sack_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = sack_dir / f"{prefix}_{timestamp}.md"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    st.sidebar.success(f"✅ Zapisano: {filepath.name}")

if __name__ == "__main__":
    render_market_radar()
