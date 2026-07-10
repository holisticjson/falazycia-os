import re
import os

with open("C:\\Aplikacje MVP\\Holistic Jason\\app.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update AI Website Builder (Add Pixel and GA4)
target_website_builder = '''        sys_io = st.text_input("ID formularza Systeme.io (opcjonalnie):", placeholder="Np. form_123xyz")
        
        if st.button("🚀 Generuj Landing Page (GCP Agent)", type="primary"):'''

replacement_website_builder = '''        sys_io = st.text_input("ID formularza Systeme.io (opcjonalnie):", placeholder="Np. form_123xyz")
        meta_pixel = st.text_input("Meta Pixel ID (opcjonalnie):", placeholder="Np. 1234567890")
        ga4_id = st.text_input("GA4 Measurement ID (opcjonalnie):", placeholder="Np. G-XXXXXXXXXX")
        
        if st.button("🚀 Generuj Landing Page (GCP Agent)", type="primary"):'''

if target_website_builder in content:
    content = content.replace(target_website_builder, replacement_website_builder)

target_html = '''    <title>Landing Page</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
</head>'''

replacement_html = '''    <title>Landing Page</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
    <!-- Meta Pixel Code -->
    <script>
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '{meta_pixel_placeholder}');
    fbq('track', 'PageView');
    </script>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga4_placeholder}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', '{ga4_placeholder}');
    </script>
</head>'''

if target_html in content:
    content = content.replace(target_html, replacement_html)


# 2. Update Ads & Local SEO (Add GBP Content Planner and Meta/Google Ads text)
target_ads_seo = '''    with t_ads:
        st.markdown("### 🎯 AI Ads Manager")
        st.write("Skonfiguruj pakiet reklamowy. AI przygotuje grafiki i copy, a po zatwierdzeniu wyśle je jako Szkic (Draft) do Meta/Google Ads chroniąc Twoją kartę.")'''

replacement_ads_seo = '''    with t_seo:
        st.markdown("---")
        st.markdown("### 📅 GBP Content Planner (Posty Google)")
        st.info("Agent analizuje Google Keyword Planner i tworzy lokalne wpisy (Oferty/Aktualności), by pozycjonować wizytówkę wyżej.")
        post_topic = st.text_input("Temat lokalnego posta:", value="Wynajem biur w centrum")
        if st.button("Wygeneruj Post & Zaplanuj (GBP API)"):
            st.success("Wygenerowano i zaplanowano post: 'Szukasz biura w centrum? Nasza nowa oferta...' na wtorek 10:00.")
            
    with t_ads:
        st.markdown("### 🎯 AI Ads Manager & Competitor Analysis")
        st.info("Twój asystent (World Class Ads Expert) analizuje Facebook Ads Library oraz Google Ads i przygotowuje dla Ciebie szkice kampanii.")
        st.write("Skonfiguruj pakiet reklamowy. AI przygotuje grafiki i copy, a po zatwierdzeniu wyśle je jako Szkic (Draft) do Meta/Google Ads chroniąc Twoją kartę.")'''

if target_ads_seo in content:
    content = content.replace(target_ads_seo, replacement_ads_seo)

# 3. Update SEO (Add AEO/GEO Agent)
target_seo = '''elif menu == "SEO":
    st.markdown("<p style='color: #3B82F6; font-family: Outfit; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 2px;'>III. — MARKETING • SEO & CONTENT</p>", unsafe_allow_html=True)'''

replacement_seo = '''elif menu == "SEO":
    st.markdown("<p style='color: #3B82F6; font-family: Outfit; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 2px;'>III. — MARKETING • SEO, AEO & CONTENT</p>", unsafe_allow_html=True)
    
    st.markdown("### 🤖 AEO / GEO Optimizer (Answer Engine Optimization)")
    st.info("Zoptymalizuj treść tak, aby AI (ChatGPT, Perplexity, Gemini) cytowały Twoją firmę jako autorytet (JSON-LD FAQ).")
    aeo_topic = st.text_input("Temat/Słowo kluczowe dla AI:", placeholder="Np. jak zainwestować w grunty rolne")
    if st.button("Generuj struktury AEO (JSON-LD & FAQ)"):
        st.success("Wygenerowano kod JSON-LD Schema oraz zestaw odpowiedzi (Entity SEO) dla robotów AI.")
        st.code("""{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Dlaczego warto inwestować w grunty na Śląsku?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Inwestycje w grunty..."
    }
  }]
}""", language="json")
    st.markdown("---")'''

if target_seo in content:
    content = content.replace(target_seo, replacement_seo)

with open("C:\\Aplikacje MVP\\Holistic Jason\\app.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Faza 4.1 added successfully")
