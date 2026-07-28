import streamlit as st

def render(kb_files):
    st.title("🎓 Akademia Wiedzy Klubu Fala Życia")
    st.markdown("Praktyczne poradniki, instrukcje technologiczne oraz wyekstrahowana wiedza ekspercka.")

    tab1, tab2, tab3, tab4 = st.tabs(["💧 Instrukcja Stacji X2O", "☀️ Fotobiomodulacja X39", "📈 Podręcznik Duplikacji MLM", "🧠 Prosperująca Świadomość"])
    
    with tab1:
        st.markdown("### 💧 Instrukcja Obsługi Stacji Hydratacji Wody X2O™")
        st.markdown("""
        **Prawidłowy Proces Uruchomienia i Aktywacji Wody:**
        1. **Podłączenie Urządzenia:** Podłącz Stację X2O do źródła wody (lub napełnij dedykowany zbiornik czystą wodą).
        2. **Filtracja & Wodór H2:** Włącz proces wielostopniowej filtracji nanocząsteczkowej oraz elektrochemicznej infuzji cząsteczkowego wodoru H2.
        3. **Biofotonowa Matryca Świetlna:** Aktywuj panel naświetlania biofotonowego. Woda przepływając przez matrycę absorbuje kody świetlne i układa się w heksagonalne mikroklastry EZ.
        4. **Spożywanie:** Pij szklankę świeżo nalanego płynu co 2-3 godziny. Woda zachowuje najwyższy ujemny potencjał redox (ORP) przez pierwsze 2 godziny od nalania.
        """)

    with tab2:
        st.markdown("### ☀️ Baza Wiedzy Fototerapii X39 & X49")
        if "PHOTOBIOMODULATION_X39_MASTER.md" in kb_files:
            st.markdown(kb_files["PHOTOBIOMODULATION_X39_MASTER.md"])
        else:
            st.info("Trwa aktualizacja centralnej bazy wiedzy. Dokument wkrótce dostępny.")

    with tab3:
        st.markdown("### 📈 Podręcznik Duplikacji Liderów MLM")
        if "MLM_DUPLICATION_MASTER.md" in kb_files:
            st.text_area("Kompletny Skrypt Rozmów & Lejków", kb_files["MLM_DUPLICATION_MASTER.md"][:3500], height=350)
        else:
            st.info("Trwa aktualizacja centralnej bazy wiedzy. Dokument wkrótce dostępny.")

    with tab4:
        st.markdown("### 🧠 Quantum Prosperity & Higiena Energetyczna")
        if "QUANTUM_PROSPERITY_MASTER.md" in kb_files:
            st.markdown(kb_files["QUANTUM_PROSPERITY_MASTER.md"][:2500])
        else:
            st.info("Trwa aktualizacja centralnej bazy wiedzy. Dokument wkrótce dostępny.")
