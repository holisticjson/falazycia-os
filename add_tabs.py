import re

with open("C:\\Aplikacje MVP\\Holistic Jason\\app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Sidebar Buttons
sidebar_target = '''    if st.button("📢 Social Media Hub", use_container_width=True, type="primary" if col_menu == "Social Media Hub" else "secondary"):
        st.session_state.current_page = "Social Media Hub"
        st.rerun()'''

sidebar_replacement = '''    if st.button("📢 Social Media Hub", use_container_width=True, type="primary" if col_menu == "Social Media Hub" else "secondary"):
        st.session_state.current_page = "Social Media Hub"
        st.rerun()
        
    if st.button("🌐 AI Website Builder", use_container_width=True, type="primary" if col_menu == "AI Website Builder" else "secondary"):
        st.session_state.current_page = "AI Website Builder"
        st.rerun()
        
    if st.button("📈 Ads & Local SEO", use_container_width=True, type="primary" if col_menu == "Ads & Local SEO" else "secondary"):
        st.session_state.current_page = "Ads & Local SEO"
        st.rerun()'''

if sidebar_target in content:
    content = content.replace(sidebar_target, sidebar_replacement)
else:
    print("Could not find sidebar target")

# 2. Add Page Logic before Social Media Hub
page_target = '''elif menu == "Social Media Hub":'''

new_pages = '''
# -------------------- AI WEBSITE BUILDER --------------------
elif menu == "AI Website Builder":
    st.markdown("<p style='color: #3B82F6; font-family: Outfit; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 2px;'>V. — AI AGENCY • WEBSITE BUILDER</p>", unsafe_allow_html=True)
    st.title("🌐 AI Website Builder (GCP Agent)")
    st.markdown("<p style='color: #CBD5E1; font-size: 1.1rem; margin-top: -5px;'>Generuj oszałamiające Landing Page (Three.js, GSAP, Tailwind) i integruj formularze Systeme.io.</p>", unsafe_allow_html=True)
    
    st.info("💡 Twój agent 'marketing-agency' działający na Google Cloud Vertex AI SDK generuje kod w tle.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### Ustawienia Projektu")
        brand = st.selectbox("Marka:", ["Holistic Jason", "Holistyczny Broker", "Klient Zewnętrzny"])
        style = st.multiselect("Styl / Biblioteki:", ["TailwindCSS", "GSAP (Animacje)", "Three.js (3D)", "React/Next.js", "Czysty HTML/CSS"], default=["TailwindCSS", "GSAP (Animacje)"])
        sys_io = st.text_input("ID formularza Systeme.io (opcjonalnie):", placeholder="Np. form_123xyz")
        
        if st.button("🚀 Generuj Landing Page (GCP Agent)", type="primary"):
            st.session_state.website_generated = True
            st.rerun()
            
    with col2:
        if st.session_state.get("website_generated"):
            st.success("✅ Kod wygenerowany pomyślnie przez Vertex AI!")
            st.markdown("### Podgląd Kodu (index.html)")
            code_mock = """<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>Landing Page</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
</head>
<body class="bg-slate-900 text-white">
    <div class="container mx-auto px-4 py-20 text-center">
        <h1 class="text-5xl font-bold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">Twój Nowy Landing Page</h1>
        <p class="text-xl text-slate-300 mb-10">Zaprojektowany przez AI. Gotowy na konwersję.</p>
        
        <!-- Systeme.io Form Injection -->
        <div id="systeme-io-form-container" class="max-w-md mx-auto bg-slate-800 p-8 rounded-xl shadow-2xl">
            <!-- Tutaj agent wstrzykuje skrypt z Systeme.io -->
            <form action="https://systeme.io/api/contacts" method="POST">
                <input type="email" placeholder="Twój e-mail" class="w-full p-3 mb-4 rounded bg-slate-700 text-white">
                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 p-3 rounded font-bold">Odbierz Ebook</button>
            </form>
        </div>
    </div>
</body>
</html>"""
            st.code(code_mock, language="html")
            st.download_button("Pobierz paczkę ZIP (kod źródłowy)", data="mock_zip_data", file_name="website.zip", mime="application/zip")
        else:
            st.markdown("""
            <div style="border: 2px dashed #334155; border-radius: 10px; padding: 50px; text-align: center; color: #64748B;">
                Tutaj pojawi się wygenerowany przez agenta kod HTML/JS/CSS z wstrzykniętym formularzem Systeme.io.
            </div>
            """, unsafe_allow_html=True)

# -------------------- ADS & LOCAL SEO --------------------
elif menu == "Ads & Local SEO":
    st.markdown("<p style='color: #10B981; font-family: Outfit; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 2px;'>VI. — AI AGENCY • PERFORMANCE</p>", unsafe_allow_html=True)
    st.title("📈 Ads Manager & Local SEO")
    st.markdown("<p style='color: #CBD5E1; font-size: 1.1rem; margin-top: -5px;'>Zarządzaj reklamami Meta/Google i pozycjonowaniem na mapach (Localo Grid) wprost z Dashboardu.</p>", unsafe_allow_html=True)
    
    t_seo, t_ads, t_gsc = st.tabs(["📍 Local SEO (Google Maps)", "🎯 Ads Manager (Meta/Google)", "🔍 Search Console Analytics"])
    
    with t_seo:
        st.markdown("### 🗺️ Localo Grid Tracker (Google Business Profile)")
        st.caption("Wpisz słowo kluczowe i firmę, aby sprawdzić jej pozycję w siatce mapy (Google Places API).")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            biz_name = st.text_input("Nazwa Firmy w Google:", value="Holistyczny Broker Nieruchomości")
        with col_s2:
            kw = st.text_input("Słowo Kluczowe:", value="Hala magazynowa wynajem")
            
        if st.button("Skanuj Pozycje (Localo Grid)"):
            with st.spinner("Odpytywanie Google Places API i rysowanie siatki..."):
                time.sleep(2)
                st.success("Skan zakończony!")
                st.markdown("""
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; max-width: 400px; margin: 20px auto; text-align: center;">
                    <div style="background-color: #10B981; padding: 20px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin: auto;">1</div>
                    <div style="background-color: #10B981; padding: 20px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin: auto;">2</div>
                    <div style="background-color: #F59E0B; padding: 20px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin: auto;">4</div>
                    <div style="background-color: #10B981; padding: 20px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin: auto;">1</div>
                    <div style="background-color: #3B82F6; padding: 20px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin: auto;">📍</div>
                    <div style="background-color: #EF4444; padding: 20px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin: auto;">12</div>
                    <div style="background-color: #10B981; padding: 20px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin: auto;">3</div>
                    <div style="background-color: #F59E0B; padding: 20px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin: auto;">5</div>
                    <div style="background-color: #EF4444; padding: 20px; border-radius: 50%; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-weight: bold; margin: auto;">15</div>
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("---")
        st.markdown("### ⭐ Automatyczne odpowiedzi na opinie")
        st.info("Twój asystent wykrył 2 nowe opinie w Google Business Profile. Oto spersonalizowane szkice odpowiedzi (wpływające pozytywnie na Local SEO).")
        st.markdown("**Klient: Jan K.** (5/5) - *Polecam, świetny kontakt i szybka wycena działki.*")
        st.text_area("Draft od AI:", "Panie Janie, ogromnie dziękuję za 5 gwiazdek i polecenie! Szybka wycena to u nas priorytet. Zapraszamy do kontaktu w przyszłości. - Tomasz, Holistyczny Broker")
        st.button("Zatwierdź i opublikuj (GBP API)", key="pub_review_1")
        
    with t_ads:
        st.markdown("### 🎯 AI Ads Manager")
        st.write("Skonfiguruj pakiet reklamowy. AI przygotuje grafiki i copy, a po zatwierdzeniu wyśle je jako Szkic (Draft) do Meta/Google Ads chroniąc Twoją kartę.")
        platform = st.multiselect("Platforma:", ["Facebook/Insta Ads", "Google Search Ads", "Google Performance Max"])
        budget = st.slider("Dzienny budżet (PLN):", 10, 500, 50)
        goal = st.selectbox("Cel:", ["Lead Generation", "Ruch na stronę", "Rozpoznawalność"])
        if st.button("Generuj i wyślij Draft", type="primary"):
            st.success("Draft utworzony w menedżerze reklam za pomocą webhooka n8n! Możesz teraz wejść na Facebook Ads i włączyć kampanię.")
            
    with t_gsc:
        st.markdown("### 🔍 Search Console & AI SEO Agent")
        st.info("Pobieram dane analityczne z Google Search Console API...")
        st.markdown("""
        **Zalecenia Twojego Agenta SEO:**
        1. Artykuł o "Automatyzacja Make.com" stracił 2 pozycje. **Akcja:** Dodajmy 2 nowe paragrafy o różnicy Make vs n8n.
        2. Wzrost zapytań o "Hale magazynowe Śląsk". **Akcja:** Napiszmy artykuł poradnikowy na bloga Holistyczny Broker.
        """)
        st.button("Zleć napisanie artykułów do CMO")

elif menu == "Social Media Hub":'''

if page_target in content:
    content = content.replace(page_target, new_pages)
else:
    print("Could not find page target")

with open("C:\\Aplikacje MVP\\Holistic Jason\\app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Tabs added successfully to app.py")
