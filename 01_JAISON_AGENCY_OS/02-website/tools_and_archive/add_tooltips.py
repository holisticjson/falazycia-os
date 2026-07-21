import re

with open("C:\\Aplikacje MVP\\Holistic Jason\\app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update AI Website Builder (Add tooltips/expanders)
target_website_builder = '''        sys_io = st.text_input("ID formularza Systeme.io (opcjonalnie):", placeholder="Np. form_123xyz")
        meta_pixel = st.text_input("Meta Pixel ID (opcjonalnie):", placeholder="Np. 1234567890")
        ga4_id = st.text_input("GA4 Measurement ID (opcjonalnie):", placeholder="Np. G-XXXXXXXXXX")'''

replacement_website_builder = '''        sys_io = st.text_input("ID formularza Systeme.io (opcjonalnie):", placeholder="Np. form_123xyz")
        with st.expander("ℹ️ Jak znaleźć ID Formularza Systeme.io?"):
            st.markdown("Zaloguj się do **Systeme.io** -> Zakładka *Funnels/Lejki* -> Wybierz krok z formularzem -> Zobacz kod HTML osadzenia. Skopiuj sam identyfikator formularza (zwykle ciąg znaków np. form_123xyz).")
            
        meta_pixel = st.text_input("Meta Pixel ID (opcjonalnie):", placeholder="Np. 1234567890")
        with st.expander("ℹ️ Skąd wziąć Meta Pixel ID?"):
            st.markdown("Wejdź na **business.facebook.com** -> *Ustawienia Firmowe (Koło Zębate)* -> *Źródła danych* -> *Zestawy danych (Dawniej Piksele)*. Wybierz swój piksel. Numer ID wyświetli się pod nazwą (zazwyczaj 15 cyfr).")

        ga4_id = st.text_input("GA4 Measurement ID (opcjonalnie):", placeholder="Np. G-XXXXXXXXXX")
        with st.expander("ℹ️ Skąd wziąć GA4 ID?"):
            st.markdown("Wejdź na **analytics.google.com** -> *Administracja (lewy dół)* -> *Strumienie Danych*. Wybierz swoją stronę internetową. W prawym górnym rogu skopiuj **Identyfikator pomiaru** (Zaczyna się od G-).")'''

if target_website_builder in content:
    content = content.replace(target_website_builder, replacement_website_builder)

# 2. Update Ads & Local SEO (Add tooltips/expanders)
target_ads_seo = '''    with t_ads:
        st.markdown("### 🎯 AI Ads Manager & Competitor Analysis")
        st.info("Twój asystent (World Class Ads Expert) analizuje Facebook Ads Library oraz Google Ads i przygotowuje dla Ciebie szkice kampanii.")
        st.write("Skonfiguruj pakiet reklamowy. AI przygotuje grafiki i copy, a po zatwierdzeniu wyśle je jako Szkic (Draft) do Meta/Google Ads chroniąc Twoją kartę.")
        platform = st.multiselect("Platforma:", ["Facebook/Insta Ads", "Google Search Ads", "Google Performance Max"])'''

replacement_ads_seo = '''    with t_ads:
        st.markdown("### 🎯 AI Ads Manager & Competitor Analysis")
        st.info("Twój asystent (World Class Ads Expert) analizuje Facebook Ads Library oraz Google Ads i przygotowuje dla Ciebie szkice kampanii.")
        
        with st.expander("ℹ️ Asystent Wdrożenia: Jak podpiąć to pod Meta i Google Ads?"):
            st.markdown("""
            **Integracja reklam wymaga podpięcia darmowych Webhooków z Make.com.**
            1. Załóż darmowe konto na **Make.com**.
            2. Stwórz scenariusz: `Custom Webhook` -> `Meta Ads (Create Draft Campaign)`.
            3. W Dashboardzie Streamlit będziemy wywoływać Twój unikalny link webhooka wysyłając mu wygenerowany przez AI tekst i grafikę.
            4. Agent **NIGDY** nie publikuje płatnych reklam od razu. Pieniądze są bezpieczne. Wysyła szkic (Draft), a Ty logujesz się do Ads Managera i klikasz "Uruchom".
            """)
            
        st.write("Skonfiguruj pakiet reklamowy. AI przygotuje grafiki i copy, a po zatwierdzeniu wyśle je jako Szkic (Draft) do Meta/Google Ads chroniąc Twoją kartę.")
        platform = st.multiselect("Platforma:", ["Facebook/Insta Ads", "Google Search Ads", "Google Performance Max"])'''

if target_ads_seo in content:
    content = content.replace(target_ads_seo, replacement_ads_seo)

# 3. Add to GSC
target_gsc = '''    with t_gsc:
        st.markdown("### 🔍 Search Console & AI SEO Agent")
        st.info("Pobieram dane analityczne z Google Search Console API...")'''

replacement_gsc = '''    with t_gsc:
        st.markdown("### 🔍 Search Console & AI SEO Agent")
        with st.expander("ℹ️ Jak aktywować Google Search Console API?"):
            st.markdown("Wejdź na swoje nowe konto **Google Cloud Console** (to z aktywnym Free Trialem). Wyszukaj u góry `Google Search Console API` i kliknij **Włącz (Enable)**. Upewnij się, że strona jest zweryfikowana na tym samym mailu Gmail!")
        st.info("Pobieram dane analityczne z Google Search Console API...")'''

if target_gsc in content:
    content = content.replace(target_gsc, replacement_gsc)


with open("C:\\Aplikacje MVP\\Holistic Jason\\app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Tooltips added successfully to app.py")
