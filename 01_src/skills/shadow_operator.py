import streamlit as st
import json
from pathlib import Path
from datetime import datetime

# Ścieżki danych
INFLUENCERS_DIR = Path(r"c:\Aplikacje MVP\Holistic Jason\influencers")
INFLUENCERS_DIR.mkdir(exist_ok=True)

# Scenariusze Ghost Operator (przeniesione z ghost_operator.py dla spójności)
GHOST_SCENARIOS = {
    "🔍 Audyt Konta Twórcy": "Przeanalizuj konto influencera i przygotuj pełny Audyt Monetyzacji. Profil: [WPISZ @handle, niszę, liczbę followersów]. Pokaż: 1) Engagement analysis, 2) Ile pieniędzy zostawia na stole, 3) Top 3 produkty cyfrowe do stworzenia, 4) Propozycja partnerstwa 70/30.",
    "📦 Zaprojektuj Produkt Cyfrowy": "Na podstawie niszy [WPISZ NISZĘ] zaprojektuj produkt cyfrowy: 1) Unique Value Zone (ultra-specyficzny problem), 2) Struktura produktu (rozdziały/moduły), 3) Oferta High-Ticket (Problem + Rezultat + Mechanizm + Czas), 4) Pricing strategy (anchor pricing).",
    "📱 14-dniowa Sekwencja Stories": "Wygeneruj kompletną 14-dniową sekwencję Instagram Stories do launchu produktu cyfrowego w niszy [WPISZ NISZĘ]. Faza 1 (dni 1-5): rozgrzewka, Faza 2 (dni 6-10): wartość, Faza 3 (dni 11-14): sprzedaż z CTA. Dla każdego dnia: hook, treść, CTA.",
    "📧 Outreach do Twórcy": "Napisz sekwencję 5 wiadomości DM do mikro-twórcy w niszy [WPISZ NISZĘ]. Cel: zaproponować partnerstwo Ghost Operator (70/30). Ton: profesjonalny, nie sprzedażowy. Pokaż wartość (darmowy audyt), nie proś o nic.",
    "🎯 Pełna Kampania": "Zaprojektuj pełną kampanię Ghost Operator od A do Z dla twórcy w niszy [WPISZ NISZĘ, FOLLOWERS, ENGAGEMENT]. Obejmij: audyt, produkt, ofertę, launch sequence, outreach, revenue split setup.",
}

def render_shadow_operator():
    st.markdown("""
    <div class="inflow-card ceo-accent">
        <h1 style="margin:0;">👥 Shadow & Ghost Operator</h1>
        <p style="margin:5px 0 0 0; opacity:0.8;">Kompletny system monetyzacji twórców: od znalezienia partnera po launch produktu.</p>
    </div>
    """, unsafe_allow_html=True)

    # Statystyki sesji
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-tile"><h4>Aktywne Partnerstwa</h4><p>0</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-tile"><h4>Znalezieni Twórcy</h4><p>12</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-tile"><h4>Est. Revenue Split</h4><p>0 PLN</p></div>', unsafe_allow_html=True)

    st.divider()

    tabs = st.tabs(["🔍 1. Hunter (Znajdź Twórcę)", "📊 2. Strategia & Audyt", "🚀 3. Launch & Outreach", "📈 4. Skalowanie"])

    # --- TAB 1: HUNTER ---
    with tabs[0]:
        st.subheader("Krok 1: Identyfikacja Diamentów")
        
        # Ręczne wprowadzanie niszy (zgodnie z prośbą USERA)
        niche_options = ["Fitness", "Biznes/AI", "Psychologia", "Nieruchomości", "Edukacja", "Inne"]
        niche_select = st.selectbox("Wybierz kategorię lub wybierz 'Inne':", niche_options, index=1)
        
        if niche_select == "Inne":
            niche_manual = st.text_input("Wpisz swoją niszę ręcznie:", placeholder="np. Szydełkowanie dla początkujących")
            niche = niche_manual
        else:
            niche = niche_select
            
        min_followers = st.number_input("Minimalna liczba obserwujących:", value=5000, step=1000)
        
        if st.button("🔎 Uruchom Market Radar", type="primary"):
            if not niche:
                st.error("Proszę wpisać lub wybrać niszę!")
            else:
                st.info(f"Agent Shadow Operator skanuje niszę **{niche}** (min. {min_followers} followers)...")
                # Tu w przyszłości realna integracja z scraperem/radarem
                st.markdown(f"""
                ### Propozycje do audytu (Nisza: {niche}):
                1. **@Tworca_X** (25k followers) - Duży engagement, brak linku do sklepu.
                2. **@Tworca_Y** (12k followers) - Promuje tylko cudze produkty (afiliacja).
                3. **@Tworca_Z** (85k followers) - Ma społeczność, brak własnego kursu/ebooka.
                """)
                
                if st.button("➡️ Przejdź do Strategii (Ghost Operator) dla wybranych"):
                    st.info("Przełączam na zakładkę 'Strategia & Audyt'...")
                    # W Streamlit trudno o dynamiczny switch tabów bez session_state, 
                    # ale możemy chociaż dać wizualną podpowiedź lub ustawić stan.
                    st.session_state.last_hunter_results = niche

    # --- TAB 2: STRATEGIA (GHOST) ---
    with tabs[1]:
        st.subheader("Krok 2: Audyt i Projektowanie Produktu")
        
        with st.form("strategy_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                creator_name = st.text_input("Nazwa / @handle Twórcy *")
                followers_val = st.text_input("Liczba obserwujących")
            with col_b:
                creator_niche = st.text_input("Nisza (potwierdź):", value=niche if niche else "")
                platform = st.selectbox("Platforma", ["Instagram", "TikTok", "YouTube", "LinkedIn"])
                
            scenario = st.selectbox("Co generujemy?", [
                "🔍 Audyt Konta Twórcy",
                "📦 Zaprojektuj Produkt Cyfrowy",
                "🎯 Pełna Kampania (A-Z)"
            ])
            
            custom_notes = st.text_area("Dodatkowy kontekst (opcjonalnie)", placeholder="Np. 'Twórca mówi dużo o zarządzaniu czasem, ale nigdy nie wydał o tym kursu'")
            
            run_strategy = st.form_submit_button("🧠 Generuj Strategię Ghost", type="primary", use_container_width=True)

        if run_strategy and creator_name:
            from holistic_ceo import call_agent, SOM_KNOWLEDGE, SMM_KNOWLEDGE
            
            prompt_template = GHOST_SCENARIOS[scenario]
            task = f"""GHOST OPERATOR — ZADANIE: {scenario}
            
            ## Profil Twórcy:
            - Nazwa: {creator_name}
            - Platforma: {platform}
            - Nisza: {creator_niche}
            - Followers: {followers_val}
            
            ## Wytyczne:
            {prompt_template.replace('[WPISZ NISZĘ]', creator_niche).replace('[WPISZ @handle, niszę, liczbę followersów]', f"{creator_name}, {creator_niche}, {followers_val}")}
            
            Wiedza do wykorzystania:
            {SOM_KNOWLEDGE}
            {SMM_KNOWLEDGE}
            
            Dodatkowe uwagi: {custom_notes}
            """
            
            with st.spinner("Ghost Operator analizuje potencjał monetyzacji..."):
                response, tokens = call_agent("👥 Shadow Operator (Partnerstwa)", task)
                st.markdown('<div class="inflow-card">', unsafe_allow_html=True)
                st.markdown(response)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Zapisz raport do folderu influencera
                save_report(creator_name, scenario, response)

    # --- TAB 3: LAUNCH & OUTREACH ---
    with tabs[2]:
        st.subheader("Krok 3: Pozyskiwanie i Sprzedaż")
        
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("#### 📧 Outreach")
            if st.button("Napisz skrypt Cold DM"):
                from holistic_ceo import call_agent
                task = f"Napisz 3 warianty wiadomości DM do twórcy {creator_name} (nisza: {creator_niche}). Cel: Zaproszenie na darmowy audyt monetyzacji. Styl: Nie-sprzedażowy, partnerski."
                with st.spinner("Pisanie skryptów..."):
                    res, _ = call_agent("✍️ Senior Copywriter", task)
                    st.info(res)
                    
        with col_r:
            st.markdown("#### 📱 Launch Content")
            if st.button("Generuj 14-dniowy Launch Sequence"):
                from holistic_ceo import call_agent, EMM_KNOWLEDGE
                task = f"Wygeneruj 14-dniową sekwencję IG Stories dla launchu e-booka/kursu w niszy {creator_niche}. Wykorzystaj: {EMM_KNOWLEDGE}."
                with st.spinner("Planowanie launchu..."):
                    res, _ = call_agent("🎬 Video Producer (Veo 3.1)", task)
                    st.success(res)

    # --- TAB 4: SKALOWANIE ---
    with tabs[3]:
        st.subheader("Optymalizacja Wyników")
        st.info("System monitoruje konwersję i sugeruje poprawki w lejku na podstawie danych z GHL.")
        st.markdown("""
        - **Zalecenie**: Twój obecny model revenue split (70/30) jest rynkowym standardem. 
        - **Upsell**: Dodaj 'Zamkniętą Społeczność' jako upsell po e-booku (podnosi LTV o 40%).
        - **Automatyzacja**: Podepnij Stripe przez Make.com do automatycznego podziału zysków.
        """)

def save_report(creator_name, scenario, report):
    """Zapisuje raport do systemu plików"""
    slug = creator_name.replace("@","").replace(" ","_")[:20]
    ts = datetime.now().strftime('%Y%m%d_%H%M')
    creator_dir = INFLUENCERS_DIR / slug
    creator_dir.mkdir(exist_ok=True)
    
    filepath = creator_dir / f"{scenario[:10]}_{ts}.md"
    content = f"# {scenario}: {creator_name}\n"
    content += f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n{report}"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    st.sidebar.success(f"💾 Zapisano raport: {filepath.name}")

if __name__ == "__main__":
    render_shadow_operator()
