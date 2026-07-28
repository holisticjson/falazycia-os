import streamlit as st

def render():
    st.title("💼 Strefa Partnera & Lidera Klubu Fala Życia")
    st.markdown("Generuj gotowe wiadomości zapraszające na WhatsApp z własnym odnośnikiem i udostępniaj zaproszenia na darmową degustację wody X2O w Świątyni Harmonii w Łodzi.")

    st.markdown("### 📲 Generator Zaproszenia na WhatsApp dla Twoich Znajomych:")
    st.info("💡 **Jaki jest cel podawania Twojego ID LifeWave?** \nTwój osobisty identyfikator (ten, którym logujesz się do BackOffice LifeWave) zostanie dynamicznie zaszyty w specjalnym linku partnerskim (reflinku). Gdy zaproszony przez Ciebie gość kliknie ten link, a następnie zdecyduje się wejść do biznesu lub kupić pakiet X39 / X2O, system automatycznie przypisze ten zakup do Twojej struktury binarnej, gwarantując Ci prowizję.")
    
    partner_name = st.text_input("Wpisz swoje Imię lub oficjalne ID LifeWave:", value="Tomasz")
    guest_name = st.text_input("Imię osoby, którą chcesz zaprosić:", placeholder="np. Marek")
    
    if partner_name and guest_name:
        msg_text = f"Cześć {guest_name}! Tutaj {partner_name}. Chciałbym Cię serdecznie zaprosić na bezpłatną degustację żywej wody ustrukturyzowanej X2O oraz krótkie zapoznanie się z fototerapią komórkową w Świątyni Harmonii w Łodzi (ul. Nawrot 104). Sprawdź szczegóły na naszej stronie (ten link jest powiązany ze mną): https://fala-zycia.pl?ref={partner_name.lower().replace(' ', '')}"
        
        st.markdown("#### Gotowy Tekst Wiadomości:")
        st.text_area("Skopiuj tekst i wyślij na WhatsApp:", value=msg_text, height=120)
        
        wa_url = f"https://wa.me/?text={msg_text.replace(' ', '%20')}"
        st.markdown(f"<a href='{wa_url}' target='_blank'><button style='background:#25D366; color:#FFF; border:none; padding:12px 24px; border-radius:12px; font-weight:700; cursor:pointer;'>📲 Wyślij Bezpośrednio na WhatsApp →</button></a>", unsafe_allow_html=True)
