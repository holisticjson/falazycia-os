"""
👻 Ghost Operator — Moduł obsługi influencerów
Model: Iman Gadzhi "Shadow Operating" + Hubert Misiąg scaling framework
Workflow: Analiza konta → Audyt monetyzacji → Produkt cyfrowy → Launch sequence
"""
import streamlit as st
import json
from datetime import datetime
from pathlib import Path

import os

IS_CLOUD = os.environ.get("K_SERVICE") is not None
BASE_DIR = Path("/app") if IS_CLOUD else Path(r"c:\Aplikacje MVP\Holistic Jason")

INFLUENCERS_DIR = BASE_DIR / "influencers"
INFLUENCERS_DIR.mkdir(exist_ok=True)

# --- GHOST OPERATOR SYSTEM PROMPT ---
GHOST_SYSTEM_PROMPT = """Jesteś Ghost Operator — ekspertem od monetyzacji influencerów i mikro-twórców.

TWOJA WIEDZA BAZOWA (Iman Gadzhi Shadow Operating + Scaling Framework):

## FILOZOFIA:
- Prostota: 1 lejek, 1 oferta, 1 cel. Złożoność = wróg egzekucji.
- Build Once, Sell Forever: produkty cyfrowe (e-booki, kursy, szablony) z zerowym kosztem krańcowym.
- Influencer Arbitrage: mikro-twórcy (10k-100k followers) mają lojalną widownię, ale brakuje im produktów i strategii.
- Model współpracy: partnerstwo 70/30 (twórca/operator), nie sprzedaż usług.

## WORKFLOW GHOST OPERATORA:
1. ANALIZA KONTA — engagement rate, nisza, audience quality, top content
2. AUDYT MONETYZACJI — ile pieniędzy twórca "zostawia na stole", gap analysis
3. UNIQUE VALUE ZONE — ultra-specyficzny problem dla wąskiej grupy (nie "odchudzanie" → "odchudzanie dla matek po ciąży bez diet")
4. PRODUKT CYFROWY — e-book/kurs/szablon generowany przez AI na bazie wiedzy twórcy
5. OFERTA HIGH-TICKET — Problem + Rezultat + Unikalny Mechanizm + Czas
6. LAUNCH SEQUENCE — 14-dniowa sekwencja IG Stories (rozgrzewka → wartość → sprzedaż)
7. AUTO-REVENUE SPLIT — bramka płatnicza z automatycznym podziałem 70/30

## CHECKLISTA:
- Profil IG: czyste bio o pomaganiu mikro-twórcom
- Walidacja: ClickBank Gravity, FB Ad Library (reklamy >3 msc)
- Lista 100 twórców (10k-100k, engagement ~3%)
- Darmowy "Audyt Monetyzacji" generowany AI
- Outreach: IG DM/Story z propozycją partnerstwa
- Produkt generowany AI na bazie wiedzy twórcy
- 14-dniowa sekwencja Stories (AI-generated copy)
- Platform WOP/Gumroad z auto-podziałem zysków

Odpowiadaj po polsku. Bądź konkretny, dawaj actionable steps."""

GHOST_SCENARIOS = {
    "🔍 Audyt Konta Twórcy": "Przeanalizuj konto influencera i przygotuj pełny Audyt Monetyzacji. Profil: [WPISZ @handle, niszę, liczbę followersów]. Pokaż: 1) Engagement analysis, 2) Ile pieniędzy zostawia na stole, 3) Top 3 produkty cyfrowe do stworzenia, 4) Propozycja partnerstwa 70/30.",
    "📦 Zaprojektuj Produkt Cyfrowy": "Na podstawie niszy [WPISZ NISZĘ] zaprojektuj produkt cyfrowy: 1) Unique Value Zone (ultra-specyficzny problem), 2) Struktura produktu (rozdziały/moduły), 3) Oferta High-Ticket (Problem + Rezultat + Mechanizm + Czas), 4) Pricing strategy (anchor pricing).",
    "📱 14-dniowa Sekwencja Stories": "Wygeneruj kompletną 14-dniową sekwencję Instagram Stories do launchu produktu cyfrowego w niszy [WPISZ NISZĘ]. Faza 1 (dni 1-5): rozgrzewka, Faza 2 (dni 6-10): wartość, Faza 3 (dni 11-14): sprzedaż z CTA. Dla każdego dnia: hook, treść, CTA.",
    "📧 Outreach do Twórcy": "Napisz sekwencję 5 wiadomości DM do mikro-twórcy w niszy [WPISZ NISZĘ]. Cel: zaproponować partnerstwo Ghost Operator (70/30). Ton: profesjonalny, nie sprzedażowy. Pokaż wartość (darmowy audyt), nie proś o nic.",
    "🎯 Pełna Kampania": "Zaprojektuj pełną kampanię Ghost Operator od A do Z dla twórcy w niszy [WPISZ NISZĘ, FOLLOWERS, ENGAGEMENT]. Obejmij: audyt, produkt, ofertę, launch sequence, outreach, revenue split setup.",
}

def render_ghost_operator():
    """Renderuje moduł Ghost Operator"""
    st.header("👻 Ghost Operator — Monetyzacja Influencerów")
    st.caption("Shadow Operating: Ty dostarczasz produkt + strategię, influencer udostępnia widownię. Model 70/30.")
    
    # Info box
    with st.expander("📖 Jak działa Ghost Operator?", expanded=False):
        st.markdown("""
        **Model biznesowy (Iman Gadzhi / Hubert Misiąg):**
        
        1. 🔍 **Znajdź mikro-twórcę** (10k-100k followers, ~3% engagement)
        2. 📊 **Zrób mu darmowy Audyt Monetyzacji** (AI generuje raport)
        3. 🤝 **Zaproponuj partnerstwo 70/30** (on dostaje 70%, Ty 30%)
        4. 📦 **Stwórz produkt cyfrowy** (AI generuje e-book/kurs na bazie jego wiedzy)
        5. 📱 **Wygeneruj 14-dniową sekwencję Stories** (launch sequence)
        6. 💰 **Auto-revenue split** (bramka płatnicza dzieli automatycznie)
        
        **Ty nie sprzedajesz usług — budujesz partnerstwa.**
        """)
    
    st.divider()
    
    # Formularz influencera
    with st.form("ghost_form"):
        st.subheader("1️⃣ Profil Influencera")
        col1, col2 = st.columns(2)
        with col1:
            creator_name = st.text_input("Nazwa / @handle *")
            niche = st.text_input("Nisza (np. fitness, finanse, beauty)")
            platform = st.selectbox("Główna platforma", ["Instagram", "TikTok", "YouTube", "LinkedIn", "Inna"])
        with col2:
            followers = st.text_input("Liczba followersów")
            engagement = st.text_input("Engagement rate (%) — jeśli znasz")
            profile_url = st.text_input("Link do profilu")
        
        st.subheader("2️⃣ Co chcesz zrobić?")
        scenario = st.selectbox("Scenariusz:", list(GHOST_SCENARIOS.keys()))
        
        custom_notes = st.text_area("Dodatkowe uwagi / kontekst", placeholder="Np. 'Ten twórca ma już e-booka ale się nie sprzedaje'")
        
        submitted = st.form_submit_button("👻 Uruchom Ghost Operator", type="primary", use_container_width=True)
    
    if submitted and creator_name:
        return {
            "creator_name": creator_name,
            "niche": niche,
            "platform": platform,
            "followers": followers,
            "engagement": engagement,
            "profile_url": profile_url,
            "scenario": scenario,
            "scenario_prompt": GHOST_SCENARIOS[scenario],
            "custom_notes": custom_notes,
        }
    return None

def build_ghost_prompt(data):
    """Buduje prompt dla Ghost Operator"""
    prompt = f"""GHOST OPERATOR — ZADANIE: {data['scenario']}

## Profil Twórcy:
- Nazwa: {data['creator_name']}
- Platforma: {data['platform']}
- Nisza: {data['niche']}
- Followers: {data['followers']}
- Engagement: {data['engagement'] or 'nieznany'}
- Profil: {data['profile_url'] or 'brak'}

## Scenariusz:
{data['scenario_prompt'].replace('[WPISZ NISZĘ]', data['niche']).replace('[WPISZ @handle, niszę, liczbę followersów]', f"{data['creator_name']}, {data['niche']}, {data['followers']}")}

## Dodatkowe uwagi:
{data['custom_notes'] or 'Brak'}

---
Działaj zgodnie z metodologią Shadow Operating (Iman Gadzhi) i frameworkiem skalowania produktów cyfrowych.
Bądź KONKRETNY — dawaj gotowe do użycia copy, struktury, skrypty. Nie teoretyzuj."""
    return prompt

def save_ghost_report(data, report):
    """Zapisuje raport Ghost Operator"""
    slug = data["creator_name"].replace("@","").replace(" ","_")[:20]
    ts = datetime.now().strftime('%Y%m%d_%H%M')
    creator_dir = INFLUENCERS_DIR / slug
    creator_dir.mkdir(exist_ok=True)
    
    filepath = creator_dir / f"ghost_{data['scenario'][:20]}_{ts}.md"
    content = f"# 👻 Ghost Operator: {data['creator_name']}\n"
    content += f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    content += f"**Scenariusz:** {data['scenario']}\n\n---\n\n{report}\n"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    return filepath
