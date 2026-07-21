# app.py - JaiSON Client OS Dashboard (Premium Streamlit Interface)
# Dynamicznie parsuje i wizualizuje WORKSPACE_MEMORY.md z integracją metodologii AI Biznes Lab!

import streamlit as st
import os
import re

# 1. Konfiguracja strony
st.set_page_config(
    page_title="JaiSON Client OS - Panel Kontrolny",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Premium Design i Styling CSS (Glassmorphism, Neon Cyan / Deep Slate Dark Mode)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0d0e15;
        font-family: 'Inter', sans-serif;
        color: #e2e8f0;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Nagłówki */
    h1, h2, h3, h4 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Luksusowe Karty Glassmorphism */
    .glass-card {
        background: rgba(22, 25, 41, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.8rem;
        margin-bottom: 1.2rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.4);
    }
    
    .glass-card-header {
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 0.8rem;
        margin-bottom: 1rem;
    }
    
    /* Kolory i Akcenty */
    .cyan-text {
        color: #00f0ff !important;
        font-weight: 600;
    }
    
    .purple-text {
        color: #bd93f9 !important;
        font-weight: 600;
    }
    
    .tag-neutral {
        display: inline-block;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 6px;
        margin-bottom: 6px;
        border: 1px solid rgba(255, 255, 255, 0.03);
    }
    
    .tag-cyan {
        display: inline-block;
        background: rgba(0, 240, 255, 0.1);
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #00f0ff;
        margin-right: 6px;
        margin-bottom: 6px;
        border: 1px solid rgba(0, 240, 255, 0.2);
    }
    
    .tag-purple {
        display: inline-block;
        background: rgba(189, 147, 249, 0.1);
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #bd93f9;
        margin-right: 6px;
        margin-bottom: 6px;
        border: 1px solid rgba(189, 147, 249, 0.2);
    }
    
    .tag-red {
        display: inline-block;
        background: rgba(255, 75, 75, 0.1);
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.85rem;
        font-weight: 600;
        color: #ff4b4b;
        margin-right: 6px;
        margin-bottom: 6px;
        border: 1px solid rgba(255, 75, 75, 0.2);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #00f0ff;
    }
</style>
""", unsafe_allow_html=True)

# 3. Szukanie pliku WORKSPACE_MEMORY.md
def find_workspace_memory():
    paths_to_try = [
        "../WORKSPACE_MEMORY.md",
        "WORKSPACE_MEMORY.md",
        "./WORKSPACE_MEMORY.md",
        "../../WORKSPACE_MEMORY.md",
        "C:/Aplikacje MVP/02_CLIENTS_AND_PROJECTS/Szablon_Projektu/WORKSPACE_MEMORY.md"
    ]
    for p in paths_to_try:
        if os.path.exists(p):
            return p
    return None

memory_path = find_workspace_memory()

# 4. Sidebar (Nawigacja i Status)
st.sidebar.image("https://www.aitmpl.com/assets/img/logo.png", width=180)
st.sidebar.title("🤖 JaiSON OS")
st.sidebar.markdown("<p style='color: #00f0ff; font-size:0.85rem; font-weight:600; font-style:italic; margin-top:-10px; margin-bottom:15px;'>\"Automatyzuj to, co powtarzalne, twórz to, co unikalne\"</p>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: rgba(255,255,255,0.5); font-size:0.85rem; margin-top:-10px;'>Zarządzanie Projektami & Pętla Pamięci</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

st.sidebar.subheader("📍 10 Silosów Roboczych")
st.sidebar.markdown("""
<div style="font-size: 0.85rem; line-height: 1.6; color: rgba(255,255,255,0.7);">
<strong>00-admin</strong> — Administracja & Audyt 21<br>
<strong>01-brand</strong> — Tożsamość i Głos (Ghost)<br>
<strong>02-website</strong> — Dashboard Streamlit<br>
<strong>03-social</strong> — Kampanie & Social Media<br>
<strong>04-assets</strong> — Kreacje & Grafiki<br>
<strong>05-automation</strong> — Przepływy n8n<br>
<strong>06-crm</strong> — CRM & Systeme.io<br>
<strong>07-deploy</strong> — Deployment, GCP & Hosting<br>
<strong>08-reports</strong> — Analityka & GA4<br>
<strong>09-archive</strong> — Archiwum & SLA Support<br>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 JaiSON Agency OS - Powered by AntiGravity.")

# 5. Panel Główny i Nagłówek
st.title("🏛️ JaiSON Client OS")
st.markdown("<p style='color: #00f0ff; font-size:1.1rem; font-weight:600; font-style:italic; margin-top:-15px; margin-bottom:10px;'>\"Automatyzuj to, co powtarzalne, twórz to, co unikalne\"</p>", unsafe_allow_html=True)
st.write("---")

# 6. Parsowanie pliku WORKSPACE_MEMORY.md (Robust & Safe)
if memory_path:
    with open(memory_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Wyciąganie Danych Podstawowych Profilu
    def extract_val(pattern, text, default="Brak danych"):
        m = re.search(pattern, text)
        return m.group(1).strip() if m else default

    client_name = extract_val(r"- \*\*Imię:\*\* (.*)", content, "Klient")
    client_age_loc = extract_val(r"- \*\*Wiek / Lokalizacja:\*\* (.*)", content)
    client_status = extract_val(r"- \*\*Status zawodowy:\*\* (.*)", content)
    client_niche = extract_val(r"- \*\*Branża / Nisza:\*\* (.*)", content)
    
    client_time = extract_val(r"- \*\*Dostępny czas:\*\* (.*)", content)
    client_budget = extract_val(r"- \*\*Budżet miesięczny \(PLN\):\*\* (.*)", content)
    client_audience = extract_val(r"- \*\*Posiadane Audience:\*\* (.*)", content)
    client_tech = extract_val(r"- \*\*Narzędzia i Technologie:\*\* (.*)", content)
    client_ai_level = extract_val(r"- \*\*Poziom komfortu z AI:\*\* (.*)", content)

    goal_90 = extract_val(r"- \*\*Cel finansowy na 90 dni \(PLN\):\*\* (.*)", content)
    goal_12m = extract_val(r"- \*\*Cel finansowy na 12 miesięcy \(PLN\):\*\* (.*)", content)
    motivation = extract_val(r"- \*\*Głęboka motywacja \(\"DLACZEGO\"\):\*\* (.*)", content)
    problem = extract_val(r"- \*\*Problem do rozwiązania na rynku:\*\* (.*)", content)

    # Wyciąganie Supermocy
    superpowers = []
    powers_matches = re.findall(r"\d+\.\s+\*\*(.*?)\*\*\s+—\s+(.*)", content)
    for p_name, p_desc in powers_matches[:3]:
        superpowers.append((p_name, p_desc))

    # Wyciąganie Czerwonych Linii
    red_lines = []
    lines_section = re.search(r"### 🛑 Czerwone Linie \(NIE ROBIĘ\)\s*\n(.*?)\s*\n\n", content, re.DOTALL)
    if lines_section:
        red_lines = [l.strip("- ").strip() for l in lines_section.group(1).strip().split("\n") if l.strip()]

    # Wyciąganie Rekomendowanych Lejków
    funnels = []
    funnels_matches = re.findall(r"\d+\.\s+\*\*(.*?)\*\*\s*\n\s+-\s+\*Uzasadnienie:\*\s+(.*?)\s*\n\s+-\s+\*Mikro-plan wdrożenia:\*\s+(.*?)\s*(?=\n\d+\.|\n---|\n#|$)", content, re.DOTALL)
    for f_title, f_why, f_plan in funnels_matches:
        funnels.append({
            "title": f_title.strip(),
            "why": f_why.strip(),
            "plan": f_plan.strip()
        })

    # Wyciąganie Silosów (Tabela postępu)
    silos_list = []
    silos_table_match = re.search(r"\|\s*Silos\s*\|\s*Nazwa Silosu\s*\|.*?\|\s*\n(.*?)(?=\n\n|\n#|$)", content, re.DOTALL)
    if silos_table_match:
        rows = [r.strip() for l in silos_table_match.group(1).strip().split("\n") if (r := l.strip())]
        for row in rows:
            cols = [c.strip() for c in row.split("|")[1:-1]]
            if len(cols) >= 3:
                silos_list.append({
                    "id": cols[0],
                    "name": cols[1],
                    "status": cols[2],
                    "desc": cols[3] if len(cols) > 3 else ""
                })

    # Wyciąganie logów decyzji
    logs = []
    logs_section = re.search(r"## 🧠 STRATEGICZNE LOGI DECYZJI.*?\s*\n(.*)", content, re.DOTALL)
    if logs_section:
        logs = [l.strip("- ").strip() for l in logs_section.group(1).strip().split("\n") if l.strip()]

    # Wyświetlanie aktywnego klienta
    st.subheader(f"👤 Klient: {client_name} (Branża: {client_niche})")

    # 3 Główne Zakładki
    tab1, tab2, tab3 = st.tabs(["👤 KARTA KLIENTA (Founder Profile)", "🎯 STRATEGIA LEJKÓW (TOP Touchpoints)", "🏗️ STAN WDROŻENIA (10 Silosów PM)"])

    # ------------------ ZAKŁADKA 1 ------------------
    with tab1:
        c1, col_sp = st.columns([2, 1])
        
        with c1:
            st.markdown("""
            <div class="glass-card">
                <div class="glass-card-header">
                    <h3>🔍 Dane Podstawowe i Finanse</h3>
                </div>
            """, unsafe_allow_html=True)
            
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                st.markdown(f"**📍 Wiek i Lokalizacja:** {client_age_loc}")
                st.markdown(f"**👔 Status zawodowy:** {client_status}")
                st.markdown(f"**⏰ Dostępny czas:** <span class='cyan-text'>{client_time}</span>", unsafe_allow_html=True)
                st.markdown(f"**💰 Budżet miesięczny:** <span class='cyan-text'>{client_budget}</span>", unsafe_allow_html=True)
            with sub_col2:
                st.markdown(f"**📈 Posiadane Audience:** {client_audience}")
                st.markdown(f"**🛠️ Narzędzia/Tech:** {client_tech}")
                st.markdown(f"**🧠 Poziom AI:** <span class='purple-text'>{client_ai_level}</span>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
            <div class="glass-card">
                <div class="glass-card-header">
                    <h3>🎯 Cele, Misja i Motywacja</h3>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"**🏆 Cel na 90 dni:** `{goal_90}`")
            st.markdown(f"**🏆 Cel na 12 miesięcy:** `{goal_12m}`")
            st.markdown(f"**🔥 Motywacja (\"DLACZEGO\"):**\n> *{motivation}*")
            st.markdown(f"**💡 Problem rynkowy do rozwiązania:**\n> {problem}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_sp:
            st.markdown("""
            <div class="glass-card">
                <div class="glass-card-header">
                    <h3>⚡ 3 Supermoce Założyciela</h3>
                </div>
            """, unsafe_allow_html=True)
            if superpowers:
                for idx, (p_name, p_desc) in enumerate(superpowers):
                    st.markdown(f"**{idx+1}. {p_name}**")
                    st.caption(p_desc)
            else:
                st.info("Brak zdefiniowanych supermocy.")
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("""
            <div class="glass-card">
                <div class="glass-card-header">
                    <h3>🛑 Czerwone Linie (Czego NIE robimy)</h3>
                </div>
            """, unsafe_allow_html=True)
            if red_lines:
                for line in red_lines:
                    st.markdown(f"<span class='tag-red'>🛑 {line}</span>", unsafe_allow_html=True)
            else:
                st.info("Brak zdefiniowanych czerwonych linii.")
            st.markdown("</div>", unsafe_allow_html=True)

    # ------------------ ZAKŁADKA 2 ------------------
    with tab2:
        st.markdown("""
        <div class="glass-card">
            <div class="glass-card-header">
                <h3>🏆 TOP 3-5 Rekomendowanych Lejków Sprzedażowych (Mirek Burnejko Standard)</h3>
            </div>
            <p>Poniższe lejki zostały precyzyjnie wyselekcjonowane z bazy 45_touchpoints_database.md w oparciu o budżet, czas i supermoce założyciela.</p>
        </div>
        """, unsafe_allow_html=True)

        if funnels:
            for idx, f in enumerate(funnels):
                st.markdown(f"""
                <div class="glass-card">
                    <h4>{idx+1}. {f['title']}</h4>
                    <p><strong>💡 Uzasadnienie biznesowe (ROI):</strong> {f['why']}</p>
                    <p style="background: rgba(0,240,255,0.05); padding: 12px; border-radius: 8px; border-left: 3px solid #00f0ff;">
                        <strong>🛠️ Plan wdrożenia krok po kroku:</strong><br>{f['plan']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Nie znaleziono jeszcze dopasowanych lejków. Przeprowadź audyt 21 pytań, aby wygenerować rekomendacje!")

    # ------------------ ZAKŁADKA 3 ------------------
    with tab3:
        st.markdown("""
        <div class="glass-card">
            <div class="glass-card-header">
                <h3>🏗️ Stan Zaawansowania Prac (10 Silosów PM)</h3>
            </div>
        """, unsafe_allow_html=True)

        if silos_list:
            completed_count = sum(1 for s in silos_list if s["status"].lower() == "completed")
            in_progress_count = sum(1 for s in silos_list if s["status"].lower() == "in progress")
            total_silos = len(silos_list)

            # Obliczanie realnego postępu projektu
            progress_percent = int(((completed_count * 1.0 + in_progress_count * 0.5) / total_silos) * 100)
            
            col_prog, col_stat = st.columns([3, 1])
            with col_prog:
                st.markdown(f"**Uśredniony Postęp Wdrożenia Całego Projektu:** `{progress_percent}%`")
                st.progress(progress_percent / 100.0)
            with col_stat:
                st.markdown(f"✅ Ukończone: `{completed_count}/{total_silos}`")
                st.markdown(f"⚙️ W toku: `{in_progress_count}/{total_silos}`")
            
            st.markdown("---")

            # Wyświetlanie szczegółowej listy silosów
            for s in silos_list:
                with st.expander(f"📁 Silos {s['id']} — {s['name']}"):
                    st.write(f"**Opis i postępy:** {s['desc']}")
                    if s["status"].lower() == "completed":
                        st.markdown("<span class='tag-cyan'>🟢 Completed</span>", unsafe_allow_html=True)
                    elif s["status"].lower() == "in progress":
                        st.markdown("<span class='tag-purple'>🟡 In Progress</span>", unsafe_allow_html=True)
                    else:
                        st.markdown("<span class='tag-neutral'>⚪ Not Started</span>", unsafe_allow_html=True)
        else:
            st.warning("Nie znaleziono tabeli postępów silosów w WORKSPACE_MEMORY.md.")
        st.markdown("</div>", unsafe_allow_html=True)

        # Sekcja logów decyzji w zakładce 3
        st.markdown("""
        <div class="glass-card">
            <div class="glass-card-header">
                <h3>🧠 Strategic Decision Logs (Pętla B: Decision Memory Sync)</h3>
            </div>
        """, unsafe_allow_html=True)
        if logs:
            for l in logs:
                st.markdown(f"• {l}")
        else:
            st.info("Brak zarejestrowanych decyzji strategicznych.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.error("⚠️ Nie znaleziono pliku `WORKSPACE_MEMORY.md`. Skopiuj szablon projektu, aby zainicjalizować pamięć roboczą!")

st.write("---")
st.caption("© 2026 JaiSON Client OS — Standard Loop Engineering. Wszelkie prawa zastrzeżone.")
