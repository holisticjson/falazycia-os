import streamlit as st

def render():
    st.title("🫁 Szkoła Oddechu Wima Hofa & Oddechy Holotropowe")
    st.markdown("Odzyskaj pełną kontrolę nad swoim układem nerwowym, podnieś natlenienie krwi i zredukuj stres oksydacyjny.")

    # In-App Interactive Breathing Timer / Pacer
    st.markdown("### ⏱️ Wbudowany Interaktywny Pacer Oddechowy")
    st.markdown("Nie musisz wychodzić z aplikacji. Wykonaj pełną sesję oddechową bezpośrednio na ekranie:")
    
    col_p1, col_p2 = st.columns([1, 2])
    with col_p1:
        st.markdown("""
        <div class='card-box'>
            <h4 style='color: #00D2C4;'>Instrukcja Sesji:</h4>
            <ol>
                <li>Wykonaj <strong>30 głębokich wdechów</strong> (przez nos do brzucha i klatki) oraz luźnych wydechów.</li>
                <li>Po 30. wydechu wypuść powietrze i <strong>wstrzymaj oddech na bezdechu</strong> (Retention).</li>
                <li>Gdy poczujesz potrzebę wdechu, weź głęboki wdech i wstrzymaj na <strong>15 sekund</strong>.</li>
                <li>To kończy 1 Rundy! Powtórz 3-4 razy.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
    with col_p2:
        # Simple HTML/CSS animated pacer
        st.markdown("""
        <style>
        .pacer-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px;
            background: rgba(10, 25, 41, 0.6);
            border-radius: 20px;
            border: 1px solid rgba(0, 210, 196, 0.2);
            text-align: center;
        }
        .pacer-circle {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 30%, rgba(0, 210, 196, 0.8), rgba(0, 119, 182, 0.9));
            box-shadow: 0 0 30px rgba(0, 210, 196, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 24px;
            animation: breathe 8s infinite ease-in-out;
        }
        @keyframes breathe {
            0% { transform: scale(0.8); box-shadow: 0 0 10px rgba(0, 210, 196, 0.3); }
            40% { transform: scale(1.3); box-shadow: 0 0 40px rgba(0, 210, 196, 0.8); }
            50% { transform: scale(1.3); box-shadow: 0 0 40px rgba(0, 210, 196, 0.8); }
            90% { transform: scale(0.8); box-shadow: 0 0 10px rgba(0, 210, 196, 0.3); }
            100% { transform: scale(0.8); box-shadow: 0 0 10px rgba(0, 210, 196, 0.3); }
        }
        </style>
        <div class='pacer-container'>
            <div class='pacer-circle' id='pacer-visual'>
                🫁 ODDYCHAJ
            </div>
            <p style='color: #94A3B8; margin-top: 25px; font-weight: 600; font-size: 1.1rem;'>Podążaj za powiększającym się okręgiem.<br>Pełne dotlenienie (4s Wdech - 4s Wydech)</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎥 Prowadzone Sesje Oddechowe Wideo (YouTube):")

    col_vid1, col_vid2 = st.columns(2)
    with col_vid1:
        st.markdown("#### 🧘 Sesja Wima Hofa (Poziom Podstawowy & Średni):")
        st.markdown("*Prowadzona sesja oddechowa z kanału Chodź na Słówka / Wim Hof Polski*")
        st.video("https://www.youtube.com/watch?v=tybOi4hjZFQ")

    with col_vid2:
        st.markdown("#### ⚡ Zaawansowana Sesja 6 Rund (Synergia Energii):")
        st.markdown("*Głęboki proces transformacyjny oddechu Wima Hofa (6 Rund)*")
        st.video("https://www.youtube.com/watch?v=b4S_iO_P214")
