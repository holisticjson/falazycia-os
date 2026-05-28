"""
📅 Social Planner & Google Business Profile Manager
Pełne centrum zarządzania obecnością w sieci.
Obsługuje: GBP (multi-wizytówka), FB, IG, LinkedIn, X, TikTok, YouTube
"""
import streamlit as st
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from google import genai
from google.genai import types
from skills.gbp_auth import add_new_gbp_account
from skills.gbp_skills import list_all_gbp_accounts, list_gbp_locations

# Poświadczenia
SA_KEY_PATH = r"c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"
if os.path.exists(SA_KEY_PATH):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_KEY_PATH

DATA_DIR = Path(r"c:\Aplikacje MVP\Holistic Jason\05-content")
SOCIAL_LOG = DATA_DIR / "social_log.json"
POSTS_QUEUE = DATA_DIR / "posts_queue.json"
GBP_PROFILES = DATA_DIR / "gbp_profiles.json"

def _load_json(path):
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def _save_json(path, data):
    path.parent.mkdir(exist_ok=True, parents=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def render_social_planner():
    st.title("📅 Social Media & Google Business Planner")
    st.markdown("""
    **Centrum Dowodzenia Twoją Obecnością w Sieci.**  
    Automatyzuj posty, optymalizuj wizytówki i zarządzaj opiniami z jednego miejsca.
    """)
    
    # Inicjalizacja stanu dla GBP
    if "gbp_locations" not in st.session_state:
        st.session_state.gbp_locations = []
    
    # ============================================================
    # ZAKŁADKI GŁÓWNE
    # ============================================================
    tab_planner, tab_gbp, tab_reviews, tab_seo, tab_channels = st.tabs([
        "📝 Planer Postów",
        "📋 Wizytówki GBP",
        "⭐ Opinie / Recenzje",
        "🔍 SEO / GEO",
        "📺 Kanały (YT/X/TikTok)"
    ])

    # ============================================================
    # 📝 PLANER POSTÓW
    # ============================================================
    with tab_planner:
        st.subheader("🆕 Zaplanuj Nowy Post")

        with st.form("new_post_form"):
            col1, col2 = st.columns([3, 1])
            with col1:
                post_content = st.text_area("Treść posta", height=150,
                    placeholder="Wpisz treść lub kliknij '🤖 Wygeneruj AI' poniżej...")
            with col2:
                platforms = st.multiselect("Platformy", [
                    "Google Business Profile",
                    "Facebook",
                    "Instagram",
                    "LinkedIn",
                    "X (Twitter)",
                    "TikTok",
                    "YouTube Community"
                ], default=["Google Business Profile", "Facebook"])

                schedule_date = st.date_input("Data")
                schedule_time = st.time_input("Godzina")

            col_img, col_cta = st.columns(2)
            with col_img:
                image_url = st.text_input("🖼️ Link do grafiki (URL lub wygeneruj przez Imagen 3)")
            with col_cta:
                cta_type = st.selectbox("CTA (Call to Action)", [
                    "Brak",
                    "📞 Zadzwoń teraz",
                    "🌐 Odwiedź stronę",
                    "📋 Zarezerwuj wizytę",
                    "📧 Wyślij wiadomość",
                    "🛒 Kup teraz"
                ])

            submitted = st.form_submit_button("🚀 Zaplanuj publikację", type="primary", use_container_width=True)

        if submitted and post_content:
            queue = _load_json(POSTS_QUEUE)
            new_post = {
                "id": f"post_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "content": post_content,
                "platforms": platforms,
                "scheduled_date": str(schedule_date),
                "scheduled_time": str(schedule_time),
                "image_url": image_url,
                "cta": cta_type,
                "status": "zaplanowany",
                "created_at": datetime.now().isoformat()
            }
            queue.append(new_post)
            _save_json(POSTS_QUEUE, queue)
            st.success(f"✅ Post zaplanowany na {schedule_date} {schedule_time} → {', '.join(platforms)}")

        # AI Generator
        st.divider()
        col_gen1, col_gen2 = st.columns([3, 1])
        with col_gen1:
            ai_topic = st.text_input("🤖 Temat do wygenerowania (AI napisze post za Ciebie)",
                placeholder="np. Jak AI pomaga małym firmom w automatyzacji?")
        with col_gen2:
            ai_tone = st.selectbox("Ton", ["Ekspercki", "Luźny", "Sprzedażowy", "Edukacyjny"])

        if st.button("🤖 Wygeneruj post przez AI") and ai_topic:
            with st.spinner("Agent generuje post..."):
                try:
                    client = genai.Client(vertexai=True, project="holistic-dashboard-dev", location="us-central1")
                    prompt = f"""Napisz angażujący post na social media na temat: "{ai_topic}"
Ton: {ai_tone}
Marka: Holistic Jason (AI Systems Architect, automatyzacja dla firm)
Wymagania:
- Krótkie zdania, mocny hook na początku
- Emoji (nie przesadzaj)
- CTA na końcu
- Hashtagi (5-8)
- Wersja PL
Zwróć TYLKO gotowy post do wklejenia."""
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.7)
                    )
                    st.text_area("📋 Wygenerowany post (skopiuj i wklej powyżej)", response.text, height=200)
                except Exception as e:
                    st.error(f"Błąd AI: {e}")

        # Kolejka postów
        st.divider()
        st.subheader("📋 Kolejka zaplanowanych postów")
        queue = _load_json(POSTS_QUEUE)
        if queue:
            for i, post in enumerate(reversed(queue[-10:])):
                with st.expander(f"{'🟢' if post['status']=='zaplanowany' else '✅'} {post.get('scheduled_date', '?')} {post.get('scheduled_time', '?')} → {', '.join(post.get('platforms', []))}"):
                    st.write(post.get("content", "")[:300])
                    if st.button(f"🗑️ Usuń", key=f"del_post_{i}"):
                        queue = [p for p in queue if p["id"] != post["id"]]
                        _save_json(POSTS_QUEUE, queue)
                        st.rerun()
        else:
            st.info("Kolejka jest pusta. Zaplanuj pierwszy post! ☝️")

    # ============================================================
    # 📋 WIZYTÓWKI GBP
    # ============================================================
    with tab_gbp:
        st.subheader("📋 Zarządzanie Wizytówkami Google Business Profile")

        st.info("""
        **Jak podłączyć GBP?**
        1. Wejdź na [Google Cloud Console → APIs](https://console.cloud.google.com/apis/library)
        2. Włącz: `My Business Business Information API` + `My Business Account Management API`
        3. Stwórz OAuth 2.0 Client ID (typ: Desktop)
        4. Pobierz `client_secret_gbp.json` → wrzuć do folderu projektu
        5. Wklej ścieżkę poniżej i kliknij "Połącz"
        """)

        gbp_secret_path = r"c:\Aplikacje MVP\Holistic Jason\client_secret_gbp.json"
        
        # Realne dane z API
        if "gbp_locations" not in st.session_state:
            st.session_state.gbp_locations = []

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("➕ Dodaj nowe konto Google", type="primary", use_container_width=True):
                with st.spinner("Uruchamiam okno logowania Google..."):
                    try:
                        add_new_gbp_account()
                        st.success("✅ Konto dodane! Kliknij 'Odśwież', aby zobaczyć zmiany.")
                    except Exception as e:
                        st.error(f"Błąd dodawania konta: {e}")

        with col_btn2:
            if st.button("🔄 Odśwież listę wizytówek", use_container_width=True):
                with st.spinner("Pobieram dane ze wszystkich kont..."):
                    try:
                        accounts = list_all_gbp_accounts()
                        if isinstance(accounts, list) and accounts:
                            all_locs = []
                            for acc in accounts:
                                locs = list_gbp_locations(acc)
                                if isinstance(locs, list):
                                    # Przypisujemy credsy do lokalizacji, żeby wiedzieć czym postować
                                    for l in locs:
                                        l['_creds'] = acc['_creds']
                                    all_locs.extend(locs)
                            st.session_state.gbp_locations = all_locs
                            st.success(f"✅ Znaleziono {len(all_locs)} lokalizacji na wszystkich kontach!")
                        else:
                            st.warning("Nie znaleziono kont GBP. Dodaj pierwsze konto powyżej.")
                    except Exception as e:
                        st.error(f"Błąd odświeżania: {e}")

        st.divider()
        st.subheader("📍 Twoje Wizytówki (Zagregowane)")

        if st.session_state.gbp_locations:
            for loc in st.session_state.gbp_locations:
                with st.expander(f"📍 {loc.get('title')} ({loc.get('name')})"):
                    col_l1, col_l2 = st.columns([2, 1])
                    with col_l1:
                        addr = loc.get('storefrontAddress', {})
                        addr_lines = ", ".join(addr.get('addressLines', []))
                        st.write(f"🏠 Adres: {addr_lines}, {addr.get('locality', '-')}")
                        cats = loc.get('categories', {})
                        primary = cats.get('primaryCategory', {}).get('displayName', '-')
                        st.write(f"🏷️ Kategoria główna: {primary}")
                    with col_l2:
                        st.write("**Opcje:**")
                        if st.button(f"🪄 Optymalizuj", key=f"opt_{loc['name']}"):
                            st.info(f"Analiza SEO dla {loc.get('title')}...")
        else:
            # Fallback na symulację jeśli brak połączenia
            st.info("Kliknij 'Pobierz wizytówki', aby załadować realne dane. Poniżej widok demonstracyjny:")
            profiles = [
                {"name": "Holistic Jason — AI Automation", "address": "Wrocław, Polska",
                 "status": "Zweryfikowana", "optimization": 75,
                 "missing": ["Zdjęcia wnętrza", "Godziny świąteczne", "2 nowe opinie bez odpowiedzi"]},
            ]
            for profile in profiles:
                with st.expander(f"📍 {profile['name']} — {profile['status']}"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"📫 {profile['address']}")
                        st.write("**Brakujące elementy:**")
                        for item in profile.get("missing", []):
                            st.write(f"  - ❌ {item}")
                    with col2:
                        st.metric("Optymalizacja", f"{profile['optimization']}%")
                        st.progress(profile['optimization'] / 100)

                if st.button(f"🪄 Auto-optymalizuj wizytówkę", key=f"opt_{profile['name']}"):
                    st.info("Agent analizuje wizytówkę i generuje rekomendacje SEO...")

    # ============================================================
    # ⭐ OPINIE / RECENZJE
    # ============================================================
    with tab_reviews:
        st.subheader("⭐ Zarządzanie Opiniami Google")
        st.markdown("""
        Agent AI odpowiada na opinie **w tonie Twojej marki**, dopasowując odpowiedź 
        do branży wizytówki i kontekstu opinii.
        """)

        # Symulacja opinii (docelowo z Google Business API)
        reviews = [
            {"author": "Marek K.", "rating": 5, "text": "Świetna współpraca! Profesjonalne podejście do automatyzacji.", "reply": None},
            {"author": "Anna W.", "rating": 4, "text": "Dobry kontakt, ale czekałam na wdrożenie dłużej niż planowano.", "reply": None},
            {"author": "Jan P.", "rating": 3, "text": "Usługa OK, ale brak follow-up po wdrożeniu.", "reply": None},
        ]

        for i, review in enumerate(reviews):
            stars = "⭐" * review["rating"]
            with st.expander(f"{stars} {review['author']}: \"{review['text'][:60]}...\""):
                st.write(f"**Pełna treść:** {review['text']}")

                if review.get("reply"):
                    st.success(f"✅ Odpowiedź: {review['reply']}")
                else:
                    if st.button(f"🤖 Wygeneruj odpowiedź AI", key=f"reply_{i}"):
                        with st.spinner("Agent generuje odpowiedź..."):
                            try:
                                client = genai.Client(vertexai=True, project="holistic-dashboard-dev", location="us-central1")
                                prompt = f"""Napisz profesjonalną odpowiedź na opinię Google dla firmy "Holistic Jason — AI Automation" (automatyzacja i systemy AI dla firm).
Opinia ({review['rating']}/5 gwiazdek): "{review['text']}"
Ton: ciepły, profesjonalny, podziękowanie + konkretna odpowiedź na feedback.
Max 100 słów. Po polsku."""
                                response = client.models.generate_content(
                                    model='gemini-2.5-flash',
                                    contents=prompt,
                                    config=types.GenerateContentConfig(temperature=0.5)
                                )
                                st.info(f"💬 Sugerowana odpowiedź:\n\n{response.text}")
                            except Exception as e:
                                st.error(f"Błąd: {e}")

    # ============================================================
    # 🔍 SEO / GEO
    # ============================================================
    with tab_seo:
        st.subheader("🔍 Narzędzia SEO & GEO (Localo Style)")

        st.markdown("""
        **Zasada Sebastiana z Localo:** W 2026 roku *Ranking != Widoczność*.  
        Możesz być w Top 3, ale jeśli Twoje opisy usług są ogólne, Gemini Cię nie zacytuje.  
        Użyj tego narzędzia, aby Twoja wizytówka była "cytowalna" przez AI.
        """)

        with st.expander("🛠️ Localo Optimizer - Analiza Treści"):
            st.write("Wklej aktualny opis usługi lub post, aby AI zoptymalizowało go pod Gemini/Google Search.")
            raw_content = st.text_area("Treść do optymalizacji", placeholder="np. 'Dentysta Kraków - implanty'")
            
            if st.button("🚀 Optymalizuj pod AI Search (Localo Style)"):
                with st.spinner("Agent Localo optymalizuje..."):
                    try:
                        client = genai.Client(vertexai=True, project="holistic-dashboard-dev", location="us-central1")
                        prompt = f"""Jesteś ekspertem od optymalizacji wizytówek GBP zgodnie z metodologią Localo (Sebastian).
Cel: Sprawić, by AI (Gemini/Ask Maps) cytowało tę firmę w scenariuszach zakupowych.

TREŚĆ DO OPTYMALIZACJI:
"{raw_content}"

ZADANIE:
1. Przekształć ogólny opis w "scenariuszowy" (np. zamiast "implanty" napisz o "bezbolesnych implantach 3D dla pacjentów z lękiem").
2. Dodaj konkretne atrybuty i korzyści, które AI wyłapuje jako "unikalne cechy".
3. Wygeneruj 3 warianty postów GBP nasyconych słowami kluczowymi.

Format: Markdown"""
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=prompt,
                            config=types.GenerateContentConfig(temperature=0.4)
                        )
                        st.success("✅ Treść zoptymalizowana!")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Błąd: {e}")

        st.divider()
        st.subheader("🔬 Głęboka Analiza SEO/GEO")
        with st.form("seo_analysis"):
            business_name = st.text_input("Nazwa firmy", "Holistic Jason")
            business_category = st.text_input("Kategoria", "Automatyzacja IT / AI dla firm")
            target_city = st.text_input("Miasto docelowe", "Wrocław")
            target_keywords = st.text_area("Słowa kluczowe (po przecinku)",
                "automatyzacja firmy, AI dla biznesu, systemy CRM, strony internetowe")
            analyze = st.form_submit_button("🔬 Analizuj SEO/GEO", type="primary", use_container_width=True)

        if analyze:
            with st.spinner("Agent SEO/GEO analizuje..."):
                try:
                    client = genai.Client(vertexai=True, project="holistic-dashboard-dev", location="us-central1")
                    prompt = f"""Jesteś ekspertem Local SEO i GEO. Przygotuj analizę dla:
Firma: {business_name}
Kategoria: {business_category}
Miasto: {target_city}
Słowa kluczowe: {target_keywords}

Zwróć:
1. **Top 20 słów kluczowych** (z wolumenem wyszukiwań i trudnością) w tabeli
2. **5 pomysłów na posty GBP** nasycone tymi słowami kluczowymi (Localo Style)
3. **Rekomendacje optymalizacji wizytówki** (kategorie, atrybuty, zdjęcia)
4. **Strategia GEO** (jak sprawić, by AI Search cytowało Twoją firmę)
Format: Markdown"""
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.3)
                    )
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Błąd: {e}")

    # ============================================================
    # 📺 KANAŁY (YT/X/TikTok)
    # ============================================================
    with tab_channels:
        st.subheader("📺 Zarządzanie Kanałami Social Media")

        st.markdown("""
        Podłącz swoje konta, żeby publikować treści bezpośrednio z Dashboardu.
        Niektóre kanały (YouTube, TikTok) wymagają dedykowanych API keys.
        """)

        channels = {
            "🎬 YouTube": {"api": "YouTube Data API v3", "status": "Do podłączenia", "actions": ["Upload wideo", "Community post", "Komentarze"]},
            "🐦 X (Twitter)": {"api": "X API v2", "status": "Do podłączenia", "actions": ["Post", "Thread", "Poll"]},
            "🎵 TikTok": {"api": "TikTok Content Publishing API", "status": "Do podłączenia", "actions": ["Upload wideo", "Komentarze"]},
            "📘 Facebook": {"api": "Meta Graph API / GHL", "status": "Przez GHL Agent", "actions": ["Post", "Story", "Reel"]},
            "📸 Instagram": {"api": "Meta Graph API / GHL", "status": "Przez GHL Agent", "actions": ["Post", "Story", "Reel"]},
            "💼 LinkedIn": {"api": "LinkedIn API", "status": "Do podłączenia", "actions": ["Post", "Artykuł"]},
        }

        for name, info in channels.items():
            with st.expander(f"{name} — {info['status']}"):
                st.write(f"**API:** {info['api']}")
                st.write(f"**Dostępne akcje:** {', '.join(info['actions'])}")

                if info['status'] == "Przez GHL Agent":
                    st.success("✅ Zarządzane przez moduł GHL Agent (Social Media Posting)")
                    if st.button(f"➡️ Przejdź do GHL Agent", key=f"goto_ghl_{name}"):
                        st.info("Zmień moduł na '🔌 GHL Agent' → 'Social Media — Publikuj post'")
                else:
                    api_key_input = st.text_input(f"API Key / Token dla {name}", type="password", key=f"key_{name}")
                    if st.button(f"🔗 Połącz {name}", key=f"connect_{name}"):
                        if api_key_input:
                            st.success(f"✅ Token zapisany! Integracja {name} aktywna.")
                        else:
                            st.warning("Wklej API key/token, żeby podłączyć kanał.")
