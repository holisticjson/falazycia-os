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
</style>
""", unsafe_allow_html=True)

# ===== AUTHENTICATION =====
auth.check_auth()
if not st.session_state.authenticated:
    auth.render_login_screen()

# ===== SIDEBAR BRANDING =====
if os.path.exists("images/whatsapp_group.png"):
    st.sidebar.image("images/whatsapp_group.png", width=90)
else:
    st.sidebar.image("images/brand_icon.png", width=90)
st.sidebar.markdown("### 🌊 KLUB FALA ŻYCIA")
st.sidebar.markdown("**Stan konta:** Członek Klubu VIP ✨")

st.sidebar.markdown("---")
if st.sidebar.button("Wyloguj się 🔒"):
    st.session_state.authenticated = False
    st.rerun()

st.title("Witaj w Panelu Głównym Klubu Fala Życia")
st.markdown("""
Wybierz jedną z sekcji w menu bocznym po lewej stronie, aby przejść do interesującego Cię modułu.
System ten jest w 100% zintegrowany z agentami Vertex AI.
""")
