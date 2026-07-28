import streamlit as st

def render():
    st.title("✈️ Łowca Lotów w Klasie Biznes za Punkty i Mile")
    st.markdown("Kompleksowy poradnik i agregator narzędzi milowych opracowany na podstawie wiedzy z kursu Piotra Lotniczego i Moniki.")

    st.markdown("### 🌐 Najlepsze Agregatory Dostępności Nagród Milowych:")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='card-box'>
            <h3 style='color: #00D2C4;'>🔍 Skanery Taryf w Czasie Rzeczywistym</h3>
            <ul>
                <li><a href='https://seats.aero' target='_blank' style='color:#00D2C4;'><strong>Seats.aero</strong></a> – Błyskawiczny skaner dostępnych taryf I (Business) oraz O (First) we wszystkich sojuszach.</li>
                <li><a href='https://roame.travel' target='_blank' style='color:#00D2C4;'><strong>Roame.travel</strong></a> – Dedykowana wyszukiwarka porównująca 12+ programów milowych.</li>
                <li><a href='https://point.me' target='_blank' style='color:#00D2C4;'><strong>Point.me</strong></a> – Przewodnik transferu punktów kart kredytowych (Amex / Citi).</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='card-box'>
            <h3 style='color: #F59E0B;'>🎯 Przykłady Przeliczników Milowych</h3>
            <p><strong>Warszawa ➔ Nowy Jork / Chicago:</strong></p>
            <p>• Miles & More <em>Meilenschnäppchen</em>: <strong>55 000 mil</strong> w Klasie Biznes (zamiast 110 000 mil)</p>
            <p>• Flying Blue <em>Promo Rewards</em>: <strong>37 500 – 50 000 mil</strong> w Klasie Biznes</p>
            <p>• Virgin Atlantic / Delta: <strong>47 500 mil</strong></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 🧮 Kalkulator Ilu Mil Potrzebujesz na Swój Lot:")
    target_dest = st.selectbox("Wybierz docelowy kierunek podróży:", ["USA / Kanada (Klasa Biznes)", "Azja / Bangkok / Tokio (Klasa Biznes)", "Medyteran / Europa (Klasa Biznes)"])
    if target_dest == "USA / Kanada (Klasa Biznes)":
        st.success("Wymagana liczba mil: **55 000 mil** (Miles & More Meilenschnäppchen) lub ok. 60 000 pkt Amex.")
    elif target_dest == "Azja / Bangkok / Tokio (Klasa Biznes)":
        st.success("Wymagana liczba mil: **70 000 – 85 000 mil** (Turkish Miles&Smiles / Qatar Avios).")
    else:
        st.success("Wymagana liczba mil: **15 000 – 25 000 mil** (LOT / Lufthansa).")
