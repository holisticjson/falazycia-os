# app.py - JaiSON Client OS Dashboard (Streamlit Template Entrypoint)
# Automatycznie parsuje i wizualizuje plik WORKSPACE_MEMORY.md, laczac pamiec agentow z pieknym UI!

import streamlit as st
import os
import re

# Konfiguracja strony
st.set_page_config(
    page_title="JaiSON Client OS - Panel Kontrolny",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stylizacja CSS dla efektu Glassmorphism i luksusowej typografii
st.markdown("""
<style>
    .reportview-container {
        background: #0a0b10;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        font-family: 'Outfit', 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    .glass-card {
        background: rgba(21, 23, 34, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    .highlight-cyan {
        color: #00f0ff;
        font-weight: bold;
    }
    .highlight-purple {
        color: #bd93f9;
        font-weight: bold;
    }
    .stProgress > div > div > div > div {
        background-color: #00f0ff;
    }
</style>
""", unsafe_allow_path=True)

# Funkcja pomocnicza do wyszukiwania WORKSPACE_MEMORY.md
def find_workspace_memory():
    # Sprawdzamy biezacy katalog, katalog nadrzedny oraz katalogi projektowe
    paths_to_try = [
        "../WORKSPACE_MEMORY.md",
        "WORKSPACE_MEMORY.md",
        "./WORKSPACE_MEMORY.md",
        "../../WORKSPACE_MEMORY.md"
    ]
    for p in paths_to_try:
        if os.path.exists(p):
            return p
    return None

memory_path = find_workspace_memory()

# Menu boczne (Sidebar)
st.sidebar.image("https://www.aitmpl.com/assets/img/logo.png", width=180, output_format="PNG")
st.sidebar.title("🤖 JaiSON OS")
st.sidebar.markdown("---")
st.sidebar.subheader("📍 Nawigacja Silosów")
st.sidebar.info("""
- **00-admin:** Administracja & Brief
- **01-brand:** Brand Book & Voice
- **02-website:** Ten Dashboard & Kod
- **03-social:** Kampanie Social Media
- **05-automation:** Przeplywy n8n
- **06-crm:** Baza leadow & Systeme
- **07-deploy:** Hosting, DNS & Serwer
- **08-reports:** Statystyki GA4 & GA
""")

# Panel Glowny
st.title("🏛️ JaiSON Client OS")
st.write("---")

if memory_path:
    with open(memory_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Wyciaganie informacji za pomoca prostych regexow
    project_name = "Klient"
    project_match = re.search(r"# MEMORY - (.*)", content)
    if project_match:
        project_name = project_match.group(1).strip()

    st.subheader(f"💼 Aktywny Projekt: {project_name}")
    
    # Podzial na dwie kolumny (Podsumowanie i Kamienie Milowe)
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown(f'<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Status Projektu & Pętla Pamięci")
        
        # Wyciagamy status projektu
        status_match = re.search(r"- \*\*Status:\*\* (.*)", content)
        last_up_match = re.search(r"- \*\*Ostatnia aktualizacja:\*\* (.*)", content)
        goal_match = re.search(r"- \*\*Biezacy cel glowny:\*\* (.*)", content)
        
        status = status_match.group(1).strip() if status_match else "Nieokreslony"
        last_update = last_up_match.group(1).strip() if last_up_match else "Brak danych"
        main_goal = goal_match.group(1).strip() if goal_match else "Brak zdefiniowanego celu głównego"
        
        st.markdown(f"**🔴 Bieżący Status:** <span class='highlight-cyan'>{status}</span>", unsafe_allow_html=True)
        st.markdown(f"**⏰ Ostatnia synchronizacja:** `{last_update}`")
        st.markdown(f"**🎯 Główny cel biznesowy:**\n> {main_goal}")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🛠️ Architektura Systemu (Tech Stack)")
        
        # Wyciagamy tech stack
        frontend_match = re.search(r"- \*\*Frontend:\*\* (.*)", content)
        auto_match = re.search(r"- \*\*Automatyzacja:\*\* (.*)", content)
        ai_match = re.search(r"- \*\*Sztuczna Inteligencja \(AI\):\*\* (.*)", content)
        db_match = re.search(r"- \*\*Baza Danych and Storage:\*\* (.*)", content)
        
        st.markdown(f"🖥️ **Frontend:** {frontend_match.group(1).strip() if frontend_match else 'Streamlit'}")
        st.markdown(f"⚙️ **Automatyzacja:** {auto_match.group(1).strip() if auto_match else 'n8n Webhooks'}")
        st.markdown(f"🧠 **AI Engine:** {ai_match.group(1).strip() if ai_match else 'Gemini 2.5 Flash'}")
        st.markdown(f"💾 **Data & Storage:** {db_match.group(1).strip() if db_match else 'Local files'}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 🏆 Kamienie Milowe & Lista TODO")
        
        # Parowanie TODO list z WORKSPACE_MEMORY
        todos = re.findall(r"- \[( [xX]?)\] \*\*(.*?):\*\* (.*)", content)
        
        if todos:
            completed = 0
            for done, milestone, desc in todos:
                is_done = done.strip().lower() == 'x'
                if is_done:
                    completed += 1
                
                # Renderowanie piekniejszych widgetow TODO
                st.checkbox(label=f"**{milestone}** - {desc}", value=is_done, disabled=True, key=f"todo_{milestone}")
            
            # Pasek postepu (Progress Bar)
            progress = int((completed / len(todos)) * 100) if todos else 0
            st.markdown(f"**Postęp wdrożenia:** {progress}%")
            st.progress(progress / 100.0)
        else:
            st.warning("Nie znaleziono ustrukturyzowanych zadań TODO w WORKSPACE_MEMORY.md.")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Ostatnie Aktywności Agentów")
        # Wyciagamy log aktywnosci
        log_section = re.search(r"## LOG AKTYWNOSCI\s*\n(.*)", content, re.DOTALL)
        if log_section:
            logs = log_section.group(1).strip().split("\n")
            for log in logs[:4]: # Pokazujemy max 4 ostatnie wpisy
                if log.strip():
                    st.markdown(f"• {log.strip()}")
        else:
            st.info("Brak wpisów w dzienniku aktywności.")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.warning("⚠️ Nie znaleziono pliku `WORKSPACE_MEMORY.md`. Upewnij się, że uruchomiłeś skrypt synchronizacji pętli pamieci roboczej.")
    st.info("Tworzę domyślny podgląd systemu...")

st.write("---")
st.caption("© 2026 JaiSON Agency OS - Powered by AntiGravity Loop Engineering standard.")
