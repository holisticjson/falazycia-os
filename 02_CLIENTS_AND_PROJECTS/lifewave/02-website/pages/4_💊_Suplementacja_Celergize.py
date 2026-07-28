import streamlit as st
import os
import sys

# Append parent dir to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules import auth, celergize

st.set_page_config(
    page_title="Suplementacja Celergize",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Dark Mode & Quantum Neon Accents
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
    
    .stButton>button {
        background: linear-gradient(135deg, #00D2C4 0%, #9B51E0 100%);
        color: #03060A;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        box-shadow: 0 4px 18px rgba(0, 210, 196, 0.35);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 210, 196, 0.55);
    }
    
    .card-box {
        background: rgba(10, 25, 41, 0.85);
        border: 1px solid rgba(0, 210, 196, 0.28);
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(12px);
    }
    
    .hero-motto {
        text-align: center;
        padding: 35px 20px;
        background: radial-gradient(circle at 50% 50%, rgba(0, 210, 196, 0.15) 0%, rgba(155, 81, 224, 0.1) 60%, transparent 100%);
        border: 1px solid rgba(0, 210, 196, 0.35);
        border-radius: 24px;
        margin-bottom: 30px;
    }
    
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Pacer breathing circle animation */
    .pacer-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 30px;
        background: rgba(7, 18, 32, 0.9);
        border: 1px solid rgba(0, 210, 196, 0.3);
        border-radius: 24px;
        margin: 20px 0;
    }

    .pacer-circle {
        width: 180px;
        height: 180px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0,210,196,0.8) 0%, rgba(155,81,224,0.3) 70%);
        box-shadow: 0 0 35px rgba(0,210,196,0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        font-weight: 800;
        color: #FFFFFF;
        transition: all 4s ease-in-out;
        font-family: 'Outfit', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

auth.check_auth()
if not st.session_state.authenticated:
    auth.render_login_screen()

# Render page content
celergize.render()
