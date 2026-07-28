import streamlit as st

def render():
    st.title("💊 Nowość: Suplementacja Celergize™")
    st.markdown("Innowacyjna linia produktów LifeWave wspierająca zdrowie jelit, mikrobiom oraz detoks na poziomie komórkowym.")

    st.info("Produkty Celergize™ dostępne w Europie od 20 lipca 2026 roku.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card-box'>
            <h3 style='color: #00D2C4;'>🌿 Celergize - Wsparcie Mikrobiomu</h3>
            <p style='color: #94A3B8; font-size: 0.95rem; line-height: 1.5;'>
                [PLACEHOLDER - Tutaj znajdą się szczegółowe informacje o składzie i działaniu produktu na florę bakteryjną i szczelność jelit.]
            </p>
            <button style='background:#333; color:#999; border:none; padding:8px 16px; border-radius:8px; font-weight:700; cursor:not-allowed;'>Wkrótce Dostępne</button>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card-box'>
            <h3 style='color: #C084FC;'>🛡️ Celergize - Detoks i Odporność</h3>
            <p style='color: #94A3B8; font-size: 0.95rem; line-height: 1.5;'>
                [PLACEHOLDER - Tutaj znajdą się szczegółowe informacje o usuwaniu toksyn komórkowych i wsparciu immunologicznym organizmu.]
            </p>
            <button style='background:#333; color:#999; border:none; padding:8px 16px; border-radius:8px; font-weight:700; cursor:not-allowed;'>Wkrótce Dostępne</button>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### 📚 Często Zadawane Pytania (FAQ) - Celergize:")
    with st.expander("Czy Celergize można łączyć z plastrami X39?"):
        st.write("Tak! Suplementacja Celergize wspiera mikrobiom, tworząc lepsze środowisko do wchłaniania składników odżywczych, co doskonale synergizuje się z fotobiomodulacją X39 i nawodnieniem X2O.")
    with st.expander("Jakie są główne wskazania do stosowania?"):
        st.write("[PLACEHOLDER - Wkrótce dodamy pełną listę wskazań opracowaną przez ekspertów medycznych.]")
