import streamlit as st
import time
import os

def check_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

def render_login_screen():
    st.markdown("<div class='hero-motto'>", unsafe_allow_html=True)
    if os.path.exists("images/whatsapp_group.png"):
        st.image("images/whatsapp_group.png", width=140)
    elif os.path.exists("images/brand_icon.png"):
        st.image("images/brand_icon.png", width=140)
    st.markdown("""
        <h1 style='color: #00D2C4; margin-top: 15px; font-weight: 800; font-size: 2.5rem;'>🌊 KLUB FALA ŻYCIA</h1>
        <p style='font-size: 1.25rem; color: #E2E8F0; font-weight: 700; max-width: 800px; margin: 15px auto; line-height: 1.4;'>
            "Bioregeneracja Komórkowa, Biofotonowa Aktywacja Wody X2O &amp; Suwerenna Akademia Wiedzy"
        </p>
        <p style='color: #38BDF8; font-size: 1.05rem; font-weight: 600; margin-top: 10px;'>
            Ekskluzywna Aplikacja Członkowska, Baza Wiedzy &amp; Centrum Dowodzenia Klubu
        </p>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("<h3 style='text-align: center; color: #00D2C4;'>🔐 Zaloguj się do Aplikacji Klubu</h3>", unsafe_allow_html=True)
            password = st.text_input("Kod Dostępny / Hasło Klubu", type="password", placeholder="Wpisz 'falazycia2026' lub Twój kod partnera")
            submitted = st.form_submit_button("Otwórz Dashboard Klubu 🚀", use_container_width=True)
            
            if submitted:
                if password.strip().lower() in ["falazycia2026", "falazycia", "jaison", "ania", "monika", "tomasz"]:
                    st.session_state.authenticated = True
                    st.success("Autoryzacja udana! Ładowanie Dashboardu...")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Nieprawidłowy kod dostępu. Skontaktuj się ze swoim opiekunem w Klubie Fala Życia.")
    st.stop()
