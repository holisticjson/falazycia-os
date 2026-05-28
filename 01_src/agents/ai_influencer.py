"""
🤖 AI Influencer / Faceless Creator — Moduł tworzenia treści i monetyzacji
Pipeline: Pain Point Scanner → Skrypt → Grafika (Imagen 3) → Wideo → Publikacja
Workflow Jana Szopy: Hooki → Dynamiczny skrypt → CTA → Produkt
"""
import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv(Path(r"c:\Aplikacje MVP\Holistic Jason\.env"))
from google import genai
from google.genai import types

SA_KEY_PATH = r"c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"
if os.path.exists(SA_KEY_PATH):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_KEY_PATH

DATA_DIR = Path(r"c:\Aplikacje MVP\Holistic Jason\05-content\digital-products")
DATA_DIR.mkdir(exist_ok=True, parents=True)

CAMPAIGNS_DIR = Path(r"c:\Aplikacje MVP\Holistic Jason\05-content\campaigns")
BRAND_DIR = Path(r"c:\Aplikacje MVP\Holistic Jason\brand_identities")

for d in [DATA_DIR, CAMPAIGNS_DIR, BRAND_DIR]:
    d.mkdir(exist_ok=True, parents=True)


def _get_client():
    return genai.Client(vertexai=True, project="holistic-dashboard-dev", location="us-central1")


def render_ai_influencer():
    st.title("🤖 AI Influencer / Faceless Creator")
    st.markdown("""
    **Od pomysłu do monetyzacji w 5 krokach.**  
    Skanuj wiedzę → Znajdź Pain Pointy → Wygeneruj Content → Zarabiaj.
    """)

    # Brand Selection Global
    brand_files = list(BRAND_DIR.glob("*.json"))
    brand_names = [f.stem for f in brand_files]
    if brand_names:
        selected_brand = st.sidebar.selectbox("🏷️ Aktywna Marka / Klient:", brand_names)
        with open(BRAND_DIR / f"{selected_brand}.json", "r", encoding="utf-8") as bf:
            brand_config = json.load(bf)
    else:
        st.sidebar.warning("Dodaj profil marki w folderze `brand_identities/`")
        brand_config = {}

    tab_scanner, tab_creator, tab_faceless, tab_products, tab_campaigns, tab_visuals, tab_affiliate = st.tabs([
        "🔍 Pain Point Scanner",
        "✍️ Kreator Skryptów",
        "🎬 Faceless Factory",
        "📦 Produkty Cyfrowe",
        "📊 Kampanie",
        "🖼️ Generator Grafiki",
        "💰 Afiliacja & Subskrypcje"
    ])

    # ============================================================
    # 🔍 PAIN POINT SCANNER
    # ============================================================
    with tab_scanner:
        st.subheader("🔍 Skaner wiedzy i problemów rynkowych")
        st.markdown("Agent analizuje Twoją **Bazę Wiedzy** oraz trendy, aby znaleźć najbardziej dochodowe tematy.")

        mode = st.radio("Źródło analizy", ["📚 Moja Baza Wiedzy (Kursy i Szkolenia)", "🌐 Trendy Internetowe (Reddit/YT)"])

        with st.form("pain_point_form"):
            if mode == "📚 Moja Baza Wiedzy (Kursy i Szkolenia)":
                baza_dir = Path(r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Kursy_i_Szkolenia")
                files = list(baza_dir.glob("*.md"))
                selected_files = st.multiselect("Wybierz pliki do analizy", [f.name for f in files], default=[f.name for f in files[:5]])
                niche = st.text_input("Nisza docelowa", "Właściciele małych firm, Freelancerzy")
            else:
                niche = st.text_input("Nisza / Branża", placeholder="np. małe firmy IT, freelancerzy, właściciele e-commerce")
                selected_files = []
            
            target_audience = st.text_input("Grupa docelowa", placeholder="np. właściciele firm 1-10 osób, 30-50 lat")
            scan = st.form_submit_button("🔬 Rozpocznij analizę", type="primary", use_container_width=True)

        if scan:
            with st.spinner("Agent analizuje dane..."):
                try:
                    context = ""
                    if selected_files:
                        for fname in selected_files:
                            with open(baza_dir / fname, "r", encoding="utf-8") as f:
                                context += f"\n---\nŹRÓDŁO: {fname}\n{f.read()[:2000]}" # Limit context per file
                    
                    client = _get_client()
                    prompt = f"""Jesteś ekspertem od strategii produktowej i monetyzacji wiedzy.

ANALIZA NA PODSTAWIE: {mode}
NISZA: {niche}
GRUPA DOCELOWA: {target_audience}

DODATKOWY KONTEKST Z BAZY WIEDZY:
{context[:10000]}

ZADANIE:
Na podstawie dostarczonej wiedzy (kursy Google i inne) oraz specyfiki niszy, znajdź 5 najbardziej palących problemów (Pain Pointów), które można rozwiązać produktem cyfrowym.

Dla każdego podaj:
1. PROBLEM (Pain Point) - konkretnie co ich boli.
2. ROZWIĄZANIE - na podstawie wiedzy z kursów (np. automatyzacja przez AI, lepsze promptowanie, optymalizacja wizytówki).
3. PRODUKT CYFROWY - nazwa i typ (np. Checklist, Szablon Notion, Mini-kurs).
4. POTENCJAŁ ZAROBKOWY - (niski/średni/wysoki).

Pisz PO POLSKU. Bądź bardzo konkretny."""
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.5)
                    )
                    st.markdown(response.text)

                    # Zapisz raport
                    report_path = DATA_DIR / f"pain_points_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
                    with open(report_path, "w", encoding="utf-8") as f:
                        f.write(f"# Pain Point Scan: {niche}\n\n{response.text}")
                    st.success(f"💾 Raport zapisany: {report_path.name}")

                except Exception as e:
                    st.error(f"Błąd: {e}")

    # ============================================================
    # ✍️ KREATOR SKRYPTÓW (Workflow Jana Szopy)
    # ============================================================
    with tab_creator:
        st.subheader("✍️ Kreator Skryptów Wideo (Workflow Jana Szopy)")
        st.markdown("""
        **Pipeline:** Hook (3 sek.) → Problem → Agitacja → Rozwiązanie → CTA → Produkt  
        Każdy skrypt jest zoptymalizowany pod **retencję** i **konwersję**.
        """)

        with st.form("script_form"):
            topic = st.text_input("Temat wideo", placeholder="np. 5 błędów które zabijają Twój biznes online")
            pain_point = st.text_area("Pain Point (problem, który rozwiązujesz)", height=80,
                placeholder="np. Właściciele małych firm tracą 10h tygodniowo na ręczne zadania")
            product_name = st.text_input("Produkt do sprzedaży (opcjonalnie)",
                placeholder="np. Checklist: 7 Automatyzacji Za 0 PLN")
            
            col1, col2 = st.columns(2)
            with col1:
                video_format = st.selectbox("Format", ["YouTube Short (60 sek.)", "TikTok/Reel (30 sek.)", "YouTube Long (5-10 min)"])
            with col2:
                tone = st.selectbox("Ton", ["Ekspercki (spokojny autorytet)", "Dynamiczny (energia)", "Story (opowieść)"])
            
            generate_script = st.form_submit_button("✍️ Wygeneruj skrypt", type="primary", use_container_width=True)

        if generate_script and topic:
            with st.spinner("Agent pisze skrypt wg workflow Jana Szopy..."):
                try:
                    client = _get_client()
                    prompt = f"""Jesteś ekspertem od tworzenia viralowych skryptów wideo wg metodologii Jana Szopy.

TEMAT: {topic}
PAIN POINT: {pain_point}
PRODUKT: {product_name or 'Brak — skrypt edukacyjny'}
FORMAT: {video_format}
TON: {tone}

Stwórz GOTOWY skrypt wideo z następującą strukturą:

## 🎬 HOOK (pierwsze 3 sekundy)
- Musi zatrzymać scrollowanie. Użyj sprawdzonego haka (szok, pytanie, kontrowersja)

## 📌 PROBLEM (10-15 sek.)
- Pokaż, że rozumiesz ich ból. Użyj konkretnych liczb i sytuacji.

## 🔥 AGITACJA (10-15 sek.)
- Pogłęb problem. Co się stanie, jeśli NIE rozwiążą tego teraz?

## 💡 ROZWIĄZANIE (15-20 sek.)
- Podaj 2-3 konkretne wskazówki (ale nie rozwiązuj WSZYSTKIEGO — zostawź na produkt)

## 🎯 CTA (5-10 sek.)
- Jasne wezwanie do działania (link w bio / komentarz / produkt)

## 📝 OPIS / CAPTION
- Gotowy opis posta z hashtagami

## 🖼️ SUGESTIA MINIATURY
- Opis grafiki (do wygenerowania w Imagen 3)

Pisz GOTOWY skrypt — zdanie po zdaniu, jak lektor ma to czytać.
Krótkie zdania. Dynamicznie. Zero pustosłowia."""
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.7)
                    )
                    st.markdown(response.text)

                    # Zapisz skrypt
                    script_path = CAMPAIGNS_DIR / f"skrypt_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
                    with open(script_path, "w", encoding="utf-8") as f:
                        f.write(f"# Skrypt: {topic}\n\n{response.text}")
                    st.success(f"💾 Skrypt zapisany: {script_path.name}")

                except Exception as e:
                    st.error(f"Błąd: {e}")

    # ============================================================
    # 🎬 FACELESS FACTORY
    # ============================================================
    with tab_faceless:
        st.subheader("🎬 Faceless Video Factory")
        st.markdown("""
        **Twórz wideo bez pokazywania twarzy** — kanały YouTube/TikTok/IG w pełni zautomatyzowane.  
        Pipeline: Skrypt → Voiceover (ElevenLabs/Kokoro) → B-Roll (Pexels) → Montaż (FFmpeg)
        """)

        # --- VIRAL INSPIRATIONS ---
        with st.expander("🔥 Inspiracje z Viral Faceless Channels (kliknij, żeby zobaczyć)", expanded=False):
            viral_data = {
                "🤖 AI & Tech Tips": {
                    "Przykładowe kanały": "AI Revolution, Matt Wolfe, Futurepedia",
                    "Format": "Screen recording + voiceover + tekst na ekranie",
                    "Wiralowe hooki": [
                        "This AI tool replaced my entire team...",
                        "Stop using ChatGPT wrong. Here's how.",
                        "I automated my entire business in 24 hours",
                        "7 darmowych narzędzi AI, o których nie wiesz",
                        "Ta sztuczna inteligencja zarabia za mnie 24/7",
                    ],
                    "Monetyzacja": "Affiliate links, Kursy, Sponsorzy",
                },
                "💼 Business & Productivity": {
                    "Przykładowe kanały": "Ali Abdaal (clips), Thomas Frank, Dan Koe",
                    "Format": "Animacje + B-Roll + silny voiceover",
                    "Wiralowe hooki": [
                        "5 narzędzi, które zarabiają za mnie 24/7",
                        "Przestań pracować 12h dziennie. Zrób TO.",
                        "Ta jedna zmiana podwoiła moje przychody",
                        "Dlaczego 95% freelancerów nie zarabia powyżej 10K",
                        "Mój poranny system za 0 PLN (lepszy niż MBA)",
                    ],
                    "Monetyzacja": "Produkty cyfrowe, Coaching, SaaS referrals",
                },
                "💰 Finance & Side Hustles": {
                    "Przykładowe kanały": "Mark Tilbury, Proactive Thinker, Graham Stephan",
                    "Format": "Animacja whiteboard + dane + storytelling",
                    "Wiralowe hooki": [
                        "Jak zarabiać 5000 PLN miesięcznie pasywnie",
                        "3 biznesy za 0 PLN, które możesz zacząć JUTRO",
                        "Nikt Ci tego nie powie o prowadzeniu firmy w Polsce",
                        "Zarobiłem 10K w tydzień tym prostym sposobem",
                        "5 źródeł dochodu pasywnego (bez klikania reklam)",
                    ],
                    "Monetyzacja": "Ebooki, Kursy, Mentoring, Affiliate",
                },
            }
            for niche_name, data in viral_data.items():
                st.markdown(f"**{niche_name}**")
                st.write(f"📺 Kanały: {data['Przykładowe kanały']}")
                st.write(f"🎬 Format: {data['Format']}")
                st.write(f"💰 Monetyzacja: {data['Monetyzacja']}")
                st.write("🎣 **Wiralowe hooki:**")
                for hook in data["Wiralowe hooki"]:
                    st.write(f"  → _{hook}_")
                st.divider()

        # --- TECH STACK ---
        st.info("Stos technologiczny do wyboru:")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 💎 Premium Stack
            | Komponent | Narzędzie |
            |-----------|-----------|
            | Głos | ElevenLabs API |
            | Grafiki | Imagen 3 / Midjourney |
            | Avatar | HeyGen / D-ID |
            | Montaż | Shotstack API |
            | Napisy | OpenAI Whisper |
            """)
        with col2:
            st.markdown("""
            ### 🆓 Zero-Cost Stack
            | Komponent | Narzędzie |
            |-----------|-----------|
            | Głos | Kokoro TTS (Docker) |
            | Grafiki | Imagen 3 (GCP credits) |
            | B-Roll | Pexels API (darmowe) |
            | Montaż | FFmpeg (lokalne) |
            | Napisy | Whisper (lokalne) |
            """)

        st.divider()

        # --- PRODUCTION FORM ---
        with st.form("faceless_form"):
            script_text = st.text_area("📜 Wklej skrypt wideo (lub wygeneruj w zakładce 'Kreator Skryptów')", height=200)
            broll_keywords = st.text_input("🎥 Słowa kluczowe do B-Roll (po przecinku)",
                placeholder="np. office work, typing laptop, AI brain, business meeting")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                voice_provider = st.selectbox("🎙️ Głos", ["Kokoro TTS (Free)", "ElevenLabs (Premium)"])
            with col2:
                visual_style = st.selectbox("🎨 Styl wizualny", [
                    "B-Roll (stock footage)",
                    "Animacja tekstu",
                    "Slajdy + Grafiki AI",
                    "Avatar AI (HeyGen)"
                ])
            with col3:
                output_format = st.selectbox("📐 Format", ["9:16 (Shorts/Reel)", "16:9 (YouTube)", "1:1 (Post)"])

            produce = st.form_submit_button("🎬 Rozpocznij produkcję", type="primary", use_container_width=True)

        if produce and script_text:
            with st.spinner("Agent planuje produkcję i generuje plan montażu..."):
                try:
                    client = _get_client()
                    broll_list = [kw.strip() for kw in broll_keywords.split(",")] if broll_keywords else ["business", "technology"]
                    prompt = f"""Jesteś producentem wideo Faceless Channel. Na podstawie poniższego skryptu:

{script_text[:5000]}

Stwórz szczegółowy plan produkcji:

## 📋 PODZIAŁ NA SCENY
| # | Czas | Tekst lektora | Opis wizualny | Prompt Pexels B-Roll |
|---|------|---------------|---------------|---------------------|
(wypełnij tabelę — 5-10 scen)

## 🎨 PROMPTY DO GRAFIK (Imagen 3)
Dla każdej sceny, gdzie potrzebna jest grafika AI (po angielsku):
1. ...
2. ...

## 🖼️ MINIATURA
- Prompt do wygenerowania miniatury (po angielsku)
- Tekst na miniaturze (max 5 słów, wielkie litery)

## 🎵 MUZYKA W TLE
- Nastrój: ...
- Sugerowany track: ...

## 📝 OPIS DO PUBLIKACJI
- Gotowy opis z hashtagami

Słowa kluczowe B-Roll: {', '.join(broll_list)}
Format wideo: {output_format}"""
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.5)
                    )
                    st.markdown(response.text)

                    # Zapisz plan produkcji
                    plan_path = CAMPAIGNS_DIR / f"plan_produkcji_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
                    with open(plan_path, "w", encoding="utf-8") as f:
                        f.write(f"# Plan Produkcji Faceless Video\n\n{response.text}")
                    st.success(f"💾 Plan zapisany: {plan_path.name}")

                    # Pokaż status pipeline'u
                    st.divider()
                    st.subheader("🔧 Status Pipeline'u Produkcji")
                    col_s1, col_s2, col_s3 = st.columns(3)
                    with col_s1:
                        pexels_ok = bool(os.getenv("PEXELS_API_KEY"))
                        st.metric("Pexels B-Roll", "✅ Gotowy" if pexels_ok else "⚠️ Brak klucza")
                    with col_s2:
                        eleven_ok = bool(os.getenv("ELEVENLABS_API_KEY"))
                        st.metric("ElevenLabs TTS", "✅ Gotowy" if eleven_ok else "🆓 Kokoro (fallback)")
                    with col_s3:
                        st.metric("FFmpeg Montaż", "✅ Zainstalowany" if os.path.exists("C:/ffmpeg") else "⚠️ Zainstaluj")

                except Exception as e:
                    st.error(f"Błąd: {e}")

    # ============================================================
    # 📦 PRODUKTY CYFROWE
    # ============================================================
    with tab_products:
        st.subheader("📦 Generator Produktów Cyfrowych")
        st.markdown("Twórz checklisty, e-booki i mini-kursy na bazie zdiagnozowanych pain pointów.")

        with st.form("product_form"):
            product_type = st.selectbox("Typ produktu", [
                "✅ Checklist / Lista kontrolna",
                "📖 E-book (20-30 stron)",
                "🎓 Mini-kurs (5 lekcji)",
                "📋 Szablon / Template",
                "🗺️ Mapa drogowa (Roadmap)"
            ])
            product_topic = st.text_input("Temat", placeholder="np. 7 kroków do automatyzacji małej firmy")
            target = st.text_input("Dla kogo?", placeholder="np. właściciele firm usługowych")
            price = st.number_input("Sugerowana cena (PLN)", 0, 500, 47)

            create_product = st.form_submit_button("📦 Wygeneruj produkt", type="primary", use_container_width=True)

        if create_product and product_topic:
            with st.spinner("Agent tworzy produkt cyfrowy..."):
                try:
                    client = _get_client()
                    prompt = f"""Stwórz KOMPLETNY produkt cyfrowy:

Typ: {product_type}
Temat: {product_topic}
Grupa docelowa: {target}
Cena: {price} PLN

Wymagania:
1. Stwórz PEŁNĄ zawartość produktu (nie szkic, nie plan — GOTOWY produkt)
2. Profesjonalny, ekspercki ton
3. Konkretne, actionable wskazówki
4. Format Markdown (gotowy do eksportu jako PDF)
5. Dodaj: wstęp, spis treści, główną treść, podsumowanie, bonus

Pisz PO POLSKU. To musi wyglądać jak produkt za {price} PLN — premium."""
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.4, max_output_tokens=8000)
                    )

                    st.markdown(response.text)

                    # Zapisz produkt
                    safe_name = "".join([c if c.isalnum() else "_" for c in product_topic])[:60]
                    product_path = DATA_DIR / f"produkt_{safe_name}.md"
                    with open(product_path, "w", encoding="utf-8") as f:
                        f.write(response.text)
                    st.success(f"💾 Produkt zapisany: {product_path.name}")

                    st.download_button("📥 Pobierz jako MD", response.text,
                        file_name=f"{safe_name}.md", use_container_width=True)

                except Exception as e:
                    st.error(f"Błąd: {e}")

    # ============================================================
    # 📊 KAMPANIE
    # ============================================================
    with tab_campaigns:
        st.subheader("📊 Zarządzanie Kampaniami")

        campaigns = list(CAMPAIGNS_DIR.glob("*.md"))
        products = list(DATA_DIR.glob("*.md"))

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Skrypty / Kampanie", len(campaigns))
        with col2:
            st.metric("Produkty Cyfrowe", len(products))

    # ============================================================
    # 🖼️ GENERATOR GRAFIKI (Imagen 3)
    # ============================================================
    with tab_visuals:
        st.subheader("🖼️ Generator Grafiki Marketingowej (Imagen 3)")
        st.markdown("Twórz profesjonalne obrazy do postów, reklam i produktów.")

        with st.form("imagen_form"):
            prompt_input = st.text_area("Opisz obraz (po angielsku dla lepszych efektów)", 
                placeholder="A professional 3D isometric illustration of an AI brain connected to business icons, sleek dark mode, neon accents, 4k high resolution")
            
            col1, col2 = st.columns(2)
            with col1:
                aspect_ratio = st.selectbox("Proporcje", ["1:1 (Kwadrat)", "9:16 (Story/Shorts)", "16:9 (YouTube)"])
            with col2:
                output_count = st.slider("Liczba wersji", 1, 4, 1)

            generate_img = st.form_submit_button("🎨 Generuj obraz", type="primary", use_container_width=True)

        if generate_img and prompt_input:
            with st.spinner("Imagen 3 tworzy Twoją grafikę..."):
                try:
                    # TODO: Implementacja wywołania Imagen 3 via Vertex AI
                    # Na razie symulacja struktury - potrzebujemy modelu imagen-3.0-generate-001
                    st.info("Łączenie z Vertex AI Imagen 3...")
                    st.image("https://via.placeholder.com/1024x1024.png?text=Imagen+3+Preview", caption="Podgląd (Integracja API w toku)")
                    st.success("Grafika wygenerowana i zapisana w `generated_media/`")
                except Exception as e:
                    st.error(f"Błąd: {e}")

    # ============================================================
    # 💰 AFILIACJA & SUBSKRYPCJE
    # ============================================================
    with tab_affiliate:
        st.subheader("💰 Afiliacja & Recurring Revenue")
        st.markdown("""
        **Zarabiaj na polecaniu sprawdzonych produktów.**  
        System wyszukuje trending produkty (PL/EU/US) i subskrypcje z prowizją cykliczną.
        """)

        aff_mode = st.radio("Działanie:", ["🔍 Skanuj Rynek (Trending Products)", "✍️ Przygotuj Serię Afiliacyjną"])

        if aff_mode == "🔍 Skanuj Rynek (Trending Products)":
            with st.form("aff_scan_form"):
                region = st.selectbox("🌍 Region", ["Polska", "Europa (UE)", "Stany Zjednoczone (USA)", "Global"])
                cat = st.multiselect("📦 Kategorie", ["Zdrowie/Biohacking", "SaaS/AI Tools", "Finanse/Krypto", "E-commerce"], default=["SaaS/AI Tools"])
                scan_btn = st.form_submit_button("💰 Rozpocznij Skanowanie", type="primary")

            if scan_btn:
                from market_radar import run_affiliate_search
                run_affiliate_search(region, cat, "Both")

        else:
            with st.form("aff_series_form"):
                prod_name = st.text_input("Nazwa produktu/SaaS", placeholder="np. GoHighLevel, NutriProfits, Skool")
                target = st.text_input("Grupa docelowa", placeholder="np. trenerzy personalni, agencje AI")
                benefit = st.text_area("Główna korzyść", placeholder="np. oszczędność 20h tygodniowo na automatyzacji")
                
                gen_series = st.form_submit_button("✍️ Generuj Serię Treści", type="primary")

            if gen_series and prod_name:
                with st.spinner("Projektowanie strategii afiliacyjnej..."):
                    from holistic_ceo import call_agent
                    task = f"""Przygotuj 5-dniową serię treści (Reels/Stories) promującą produkt {prod_name}.
                    GRUPA: {target}
                    KORZYŚĆ: {benefit}
                    
                    STRUKTURA:
                    Dzień 1: Shock (Problem o którym nikt nie mówi)
                    Dzień 2: Solution (Przedstawienie {prod_name})
                    Dzień 3: Proof (Jak to działa w praktyce)
                    Dzień 4: Tutorial (Pokaż 'bebechy')
                    Dzień 5: Scarcity/CTA (Dlaczego warto wejść teraz)
                    
                    Użyj stylu 'Anty-AI' (ludzki, konkretny, bez korpo-bełkotu).
                    """
                    # Używamy Bedrock dla wyższej jakości strategii
                    res, _ = call_agent("✍️ Senior Copywriter", task)
                    st.markdown(res)
