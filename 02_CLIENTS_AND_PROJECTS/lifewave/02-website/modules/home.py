import streamlit as st

def render():
    st.markdown("""
    <div class='hero-motto'>
        <h1 style='color: #00D2C4; font-weight: 800; font-size: 2.3rem;'>Witaj w Centrum Dowodzenia Klubu Fala Życia! 🌊</h1>
        <p style='color: #E2E8F0; font-size: 1.15rem; max-width: 900px; margin: 15px auto; line-height: 1.6;'>
            Tworzymy suwerenną przestrzeń dla osób poszukujących najwyższych standardów bioregeneracji komórkowej, nowoczesnego biohackingu oraz niezależności finansowej.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='card-box'>
            <h3 style='color: #00D2C4;'>💧 Stacja Hydratacji X2O™</h3>
            <p style='color: #94A3B8; font-size: 0.95rem; line-height: 1.5;'>
                Elektroniczna nablatowa stacja aktywacji wody. Łączy filtrację nanocząsteczkową, nasycanie cząsteczkowym wodorem H2 (ORP do -400mV) oraz naświetlanie biofotonową matrycą świetlną.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card-box'>
            <h3 style='color: #C084FC;'>☀️ Fotobiomodulacja X39™</h3>
            <p style='color: #94A3B8; font-size: 0.95rem; line-height: 1.5;'>
                Opatentownana technologia nanokryształów LifeWave. Odbija podczerwień ciała, stymulując produkcję peptydu miedzi GHK-Cu i otwierając kanały energetyczne w meridianach.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='card-box'>
            <h3 style='color: #38BDF8;'>🤖 Inteligentny Doradca AI</h3>
            <p style='color: #94A3B8; font-size: 0.95rem; line-height: 1.5;'>
                Twój osobisty wirtualny asystent w panelu. Posiada bezpośredni dostęp do bazy wiedzy o wodzie X2O, fototerapii, taryfach milowych na loty biznes klasą oraz podręcznikach Liderów.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🗺️ Instrukcja Nawigacji Po Panelu Członkowskim:")
    st.markdown("""
    * **🤖 Inteligentny Doradca Fala Życia:** Zadawaj pytania w języku naturalnym dotyczące produktów, protokołów fototerapii i strategii duplikacji.
    * **🎓 Akademia Wiedzy & Kursy:** Przeglądaj merytoryczne moduły szkoleniowe, instrukcje aktywacji wody X2O oraz podręcznik duplikacji.
    * **💊 Suplementacja Celergize:** Poznaj nową gamę suplementów wspierających mikrobiom i detoks.
    * **✈️ Agregator Lotów w Biznes Klasie:** Wykorzystaj wiedzę o punktach i milach lojalnościowych, aby podróżować po świecie w najwyższym komforcie za ułamek ceny.
    * **🫁 Szkoła Oddechu Wima Hofa:** Korzystaj z interaktywnego pacera oddechowego wbudowanego bezpośrednio w aplikację oraz prowadzonych sesji wideo.
    * **💼 Strefa Partnera & Lidera:** Generuj gotowe wiadomości WhatsApp z własnym reflinkiem i zapraszaj na darmowe degustacje w Świątyni Harmonii w Łodzi.
    """)
