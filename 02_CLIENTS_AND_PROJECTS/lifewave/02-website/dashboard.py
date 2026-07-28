import streamlit as st
import os
from modules import auth

# ===== CONFIGURATION & THEME =====
st.set_page_config(
    page_title="Dashboard Klubu Fala Życia",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@500;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #03060A;
        color: #F8FAFC;
    }
    
    .stApp {
        background: radial-gradient(circle at 50% 0%, #0c1f36 0%, #03060a 100%);
    }
    
    /* Mobile Responsive Tweaks for Streamlit */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-top: 1.5rem !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            flex-wrap: wrap !important;
            gap: 6px !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 0.85rem !important;
            padding: 8px 12px !important;
        }
        h1 {
            font-size: 1.75rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ===== AUTHENTICATION =====
auth.check_auth()
if not st.session_state.authenticated:
    auth.render_login_screen()

# ===== SIDEBAR BRANDING & NAVIGATION =====
if os.path.exists("images/whatsapp_group.png"):
    st.sidebar.image("images/whatsapp_group.png", width=90)
elif os.path.exists("images/brand_icon.png"):
    st.sidebar.image("images/brand_icon.png", width=90)
st.sidebar.markdown("### 🌊 KLUB FALA ŻYCIA")
st.sidebar.markdown("**Stan konta:** Członek Klubu VIP ✨")

# Load Knowledge Base Files
@st.cache_data(ttl=600)
def load_kb():
    kb = {}
    kb_path = os.path.join(os.path.dirname(__file__), "..", "04-assets", "knowledge_base")
    if os.path.exists(kb_path):
        for f in os.listdir(kb_path):
            if f.endswith(".md"):
                p = os.path.join(kb_path, f)
                try:
                    with open(p, "r", encoding="utf-8") as file:
                        kb[f] = file.read()
                except Exception:
                    pass
    return kb

kb_files = load_kb()

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Nawigacja")
menu_choice = st.sidebar.radio(
    "Wybierz sekcję:",
    [
        "🏠 Strona Główna",
        "🤖 Asystent AI Fala Życia",
        "🎓 Akademia Wiedzy",
        "✈️ Akademia Punktów & Loty",
        "💊 Suplementacja Celergize",
        "🫁 Pacer Oddechowy",
        "💼 Strefa Partnera"
    ]
)

st.sidebar.markdown("---")
if st.sidebar.button("Wyloguj się 🔒"):
    st.session_state.authenticated = False
    st.rerun()

# ===== ROUTING TO MODULES =====
from modules import home, advisor, academy, flight_aggregator, celergize, pacer, partner_zone

if menu_choice == "🏠 Strona Główna":
    home.render()
elif menu_choice == "🤖 Asystent AI Fala Życia":
    advisor.render(kb_files)
elif menu_choice == "🎓 Akademia Wiedzy":
    academy.render(kb_files)
elif menu_choice == "✈️ Akademia Punktów & Loty":
    flight_aggregator.render()
elif menu_choice == "💊 Suplementacja Celergize":
    celergize.render()
elif menu_choice == "🫁 Pacer Oddechowy":
    pacer.render()
elif menu_choice == "💼 Strefa Partnera":
    partner_zone.render()

