import os
import json
import time
import streamlit as st
from integrations.systeme_io import SystemeIOClient

def render_lab_page(call_gemini_func):
    """
    Renderuje stronę '🎯 Laboratorium Produktu' opartą na metodologii Akademia.pl (Mirek Burnejko).
    Wykorzystuje przekazaną funkcję call_gemini_func do generowania analiz przez LLM.
    """
    st.markdown("<p style='color: #F59E0B; font-family: Outfit; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 2px;'>IV. — BUSINESS & MARKETING • LAB</p>", unsafe_allow_html=True)
    st.title("🎯 Laboratorium Produktu (Akademia.pl)")
    st.markdown("<p style='color: #CBD5E1; font-size: 1.1rem; margin-top: -5px;'>Projektowanie, badanie niszy i automatyzacja lejków sprzedażowych w duchu Low-Cost First i ADHD-friendly.</p>", unsafe_allow_html=True)

    # Inicjalizacja klienta Systeme.io
    systeme_client = SystemeIOClient()
    
    # Zakładki / Kroki Laboratorium
    tab_niche, tab_funnels, tab_mother, tab_systeme = st.tabs([
        "🔍 Krok 1: Badanie Niszy",
        "📐 Krok 2: Wybór Lejka (45 modeli)",
        "📢 Krok 3: Mother Content Pipeline",
        "📧 Krok 4: Integracja Systeme.io"
    ])

    # Słownik z modelami lejków z Akademii.pl (kilka kluczowych modeli na start)
    key_funnels = {
        "Lejek Lead Magnet (Darmowy Magnes)": {
            "description": "Najprostszy i najszybszy lejek do budowy listy e-mailowej. Oferujesz darmową wartość (checklistę, PDF, mini-narzędzie) w zamian za e-mail.",
            "steps": [
                "1. Przygotuj darmowy magnes na leady (np. 'Checklista AI dla Soloprenera').",
                "2. Stwórz prostą stronę lądowania (Landing Page) w Systeme.io z formularzem zapisu.",
                "3. Skonfiguruj automatyczną wysyłkę darmowego PDF po zapisie.",
                "4. Zaprojektuj stronę podziękowania (Thank You Page) z propozycją kolejnego kroku.",
                "5. Uruchom 5-dniową sekwencję e-mail, budując relację i edukując klienta."
            ],
            "metrics": "Liczba odwiedzin strony zapisu, współczynnik konwersji zapisu (cel: >30%), otwarcie pierwszego maila."
        },
        "Lejek Tripwire (Tani Produkt 47 zł)": {
            "description": "Zmienia subskrybenta w kupującego natychmiast po zapisie. Oferuje niesamowitą okazję cenową na stronie podziękowania.",
            "steps": [
                "1. Przyciągnij klienta darmowym magnesem (Lead Magnet).",
                "2. Na stronie podziękowania (Thank You Page) zaprezentuj limitowaną ofertę na tani produkt (Tripwire, np. za 47 zł).",
                "3. Oferta musi mieć wysoki czynnik 'no-brainer' (wartość rynkowa np. 300 zł).",
                "4. Skonfiguruj koszyk zakupowy (order form) bezpośrednio w Systeme.io.",
                "5. Kupującym dostarcz produkt cyfrowy, a niekupujących edukuj dalej mailowo."
            ],
            "metrics": "Konwersja na Tripwire (cel: 3-5% z zapisanych), średnia wartość zamówienia (AOV)."
        },
        "Lejek Konsultacyjny (High-Ticket)": {
            "description": "Idealny dla agencji AI i usług doradczych. Klient zapisuje się na bezpłatną konsultację/audyt, gdzie następuje sprzedaż.",
            "steps": [
                "1. Publikuj treści eksperckie (Thought Leadership) na LinkedIn i YouTube.",
                "2. Zaproś do bezpłatnego audytu lub 'Szybkiej Diagnozy AI' (15 min).",
                "3. Skieruj klienta na stronę z kwestionariuszem kwalifikacyjnym (np. 5 pytań z Prospecting Hub).",
                "4. Jeśli lead jest zakwalifikowany, pozwól mu zarezerwować termin w kalendarzu (np. Cal.com / TidyCal).",
                "5. Przeprowadź rozmowę doradczą i domknij sprzedaż wysokobudżetową."
            ],
            "metrics": "Liczba zakwalifikowanych leadów, współczynnik konwersji z rozmowy na klienta (cel: >20%)."
        },
        "Lejek Webinarowy (Edukacja Masowa)": {
            "description": "Sprzedaż średniopółkowych produktów (np. kurs za 297-997 zł) za pomocą edukacyjnego webinaru live lub evergreen.",
            "steps": [
                "1. Stwórz stronę zapisu na darmowe szkolenie online (webinar).",
                "2. Wyślij serię 3 maili przypominających przed webinarem w celu zwiększenia frekwencji.",
                "3. Przeprowadź 45-minutowe merytoryczne szkolenie kończące się 15-minutową ofertą specjalną.",
                "4. Zapewnij bonusy ograniczone czasowo (scarcity) dla osób, które kupią na webinarze.",
                "5. Wyślij powtórkę webinaru i 3-dniową sekwencję e-mail zamykającą okno sprzedażowe."
            ],
            "metrics": "Współczynnik zapisu, obecność na webinarze (cel: >35%), konwersja sprzedaży (cel: 5-10% obecnych)."
        }
    }

    # ==================== KROK 1: BADANIE NISZY ====================
    with tab_niche:
        st.subheader("🔍 Narzędzie Badania Niszy (Niche Research)")
        st.markdown("""
        To narzędzie realizuje oficjalny **Niche Research Prompt** autorstwa Mirka Burnejko z Akademii.pl.
        Wpisz poniżej typ swojego produktu oraz krótki opis, a AI dokona precyzyjnej analizy grupy docelowej, 
        zidentyfikuje cele, problemy oraz wygeneruje propozycje produktów i argumenty zakupowe.
        """)

        col_n1, col_n2 = st.columns(2)
        with col_n1:
            product_type = st.selectbox(
                "Typ produktu:",
                ["Checklista / Arkusz", "E-book", "Kurs wideo / Mini-kurs", "SaaS / Aplikacja", "Agencja / Usługa automatyzacji", "Newsletter Premium"],
                index=0
            )
        with col_n2:
            niche_desc = st.text_input(
                "Dla kogo i o czym? (Krótki opis):",
                placeholder="np. Narzędzia AI dla zapracowanych soloprenerów z ADHD w Polsce"
            )

        # Wczytanie dotychczasowych badań niszy
        niche_file = os.path.join("data", "niche_research.json")
        saved_niche = {}
        if os.path.exists(niche_file):
            try:
                with open(niche_file, "r", encoding="utf-8") as f:
                    saved_niche = json.load(f)
            except Exception:
                saved_niche = {}

        # Przycisk uruchomienia badania
        if st.button("Uruchom Badanie Niszy 🚀", use_container_width=True, type="primary"):
            if not niche_desc:
                st.warning("⚠️ Proszę wpisać opis niszy przed uruchomieniem badania.")
            else:
                with st.spinner("🧠 AI bada niszę według metodologii Akademii.pl... Może to zająć chwilę."):
                    # Formułowanie promptu systemowego na bazie standardów Mirek Burnejko
                    system_instruction = """
                    Jesteś elitarnym analitykiem biznesowym i psychologiem marketingu specjalizującym się w metodologii Akademii.pl.
                    Twoim zadaniem jest przeprowadzenie pogłębionego badania niszy rynkowej na podstawie typu produktu i opisu użytkownika.
                    Formatuj odpowiedź jako poprawny i czytelny dokument Markdown z wyraźnymi sekcjami, listami punktowymi i pogrubieniami.
                    Unikaj ścian tekstu, pisz konkretnie, przystępnie dla osób z ADHD.
                    """
                    
                    user_prompt = f"""
                    Zrób kompletne badanie niszy rynkowej dla następującego projektu:
                    Typ produktu: {product_type}
                    Opis / Założenie: {niche_desc}
                    
                    Przeanalizuj niszę uwzględniając poniższe punkty:
                    1. **Psychografia Grupy Docelowej**: Dokładnie opisz kogo dotyczy ta nisza, jak wygląda ich codzienność, co odczuwają.
                    2. **10 Największych Problemów**: Z jakimi trudnościami boryka się ta grupa w odniesieniu do tematu.
                    3. **10 Głównych Celów**: Co chcą osiągnąć, jakie są ich marzenia i cele życiowe/biznesowe.
                    4. **10 Powodów Zakupu**: Dlaczego byliby gotowi wydać pieniądze na ten produkt (katalizatory zakupowe).
                    5. **Propozycja 10 Produktów Komplementarnych**: Jakie inne produkty (tanie tripwire, droższe pakiety, usługi) możesz im sprzedać w przyszłości.
                    6. **Rekomendowany Pierwszy Krok MVP**: Jaki konkretny mały produkt (np. checklista za 47 zł) należy wypuścić jako pierwszy.
                    
                    Pisz po polsku, zachowaj wysoki poziom merytoryczny i motywujący styl.
                    """
                    
                    try:
                        # Wywołanie Gemini API
                        messages = [{"role": "user", "content": user_prompt}]
                        ai_response = call_gemini_func(messages, system_instruction=system_instruction)
                        
                        if ai_response:
                            # Zapisanie wyniku do bazy JSON
                            saved_niche = {
                                "product_type": product_type,
                                "description": niche_desc,
                                "analysis": ai_response,
                                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                            }
                            os.makedirs("data", exist_ok=True)
                            with open(niche_file, "w", encoding="utf-8") as f:
                                json.dump(saved_niche, f, indent=4, ensure_ascii=False)
                                
                            st.success("🎉 Badanie niszy zakończone sukcesem! Wynik został zapisany.")
                        else:
                            st.error("❌ Nie udało się uzyskać odpowiedzi od AI.")
                    except Exception as e:
                        st.error(f"❌ Wystąpił błąd podczas badania niszy: {str(e)}")

        # Wyświetlanie zapisanego badania niszy
        if saved_niche and "analysis" in saved_niche:
            st.markdown("---")
            st.markdown(f"### 📋 Ostatnie Badanie: *{saved_niche['product_type']} - {saved_niche['description']}*")
            st.info(f"Ostatnia aktualizacja badania: {saved_niche['timestamp']}")
            
            # Piękne renderowanie markdownu
            st.markdown(saved_niche["analysis"])
            
            # Przycisk do pobrania raportu w formacie tekstowym
            st.download_button(
                label="📥 Pobierz Raport Badania Niszy (TXT)",
                data=saved_niche["analysis"],
                file_name=f"badanie_niszy_{saved_niche['product_type'].replace(' ', '_').lower()}.txt",
                mime="text/plain"
            )
        else:
            st.info("💡 Brak wcześniejszych badań. Wpisz dane powyżej i kliknij 'Uruchom Badanie Niszy', aby wygenerować swój pierwszy raport.")

    # ==================== KROK 2: WYBÓR LEJKA ====================
    with tab_funnels:
        st.subheader("📐 Wybór i Rekomendacja Modelu Lejka")
        st.markdown("""
        W metodologii Akademii.pl istnieje **45 modeli lejków sprzedażowych**. Poniżej znajdziesz 4 najważniejsze, 
        niezawodne modele dla solopreneurów i agencji AI działających w niskim budżecie (*Low-Cost*).
        """)

        selected_funnel_name = st.selectbox(
            "Wybierz model lejka, aby zobaczyć szczegóły i kroki wdrożenia:",
            list(key_funnels.keys())
        )

        funnel_info = key_funnels[selected_funnel_name]
        
        # Wizualna karta lejka
        st.markdown(f"""
        <div style="background-color: #1E293B; padding: 20px; border-radius: 8px; border-left: 5px solid #F59E0B; margin-bottom: 20px;">
            <h4 style="color: #F59E0B; margin-top: 0; font-family: Outfit;">📐 {selected_funnel_name}</h4>
            <p style="color: #E2E8F0; font-size: 1rem; font-style: italic;">{funnel_info['description']}</p>
        </div>
        """, unsafe_allow_html=True)

        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            st.markdown("##### 🛠️ Kroki Wdrożeniowe:")
            for step in funnel_info["steps"]:
                st.markdown(step)
        with col_f2:
            st.markdown("##### 📊 Kluczowe Metryki (KPI):")
            st.info(funnel_info["metrics"])

        # Automatyczna rekomendacja lejka na podstawie ostatniego badania niszy
        st.markdown("---")
        st.subheader("🤖 Rekomendator Lejka AI")
        if saved_niche and "analysis" in saved_niche:
            if st.button("Dopasuj Lejek do mojej Niszy 🧠", use_container_width=True):
                with st.spinner("AI analizuje profil niszy i dobiera optymalną strategię..."):
                    system_instruction = "Jesteś ekspertem ds. lejków sprzedażowych w oparciu o 45 modeli Akademii.pl."
                    user_prompt = f"""
                    Na podstawie poniższego badania mojej niszy i produktu, zarekomenduj 1 główny model lejka oraz 1 alternatywny.
                    Wyjaśnij dlaczego ten wybór jest najlepszy, podaj 5 konkretnych kroków konfiguracji w darmowym planie Systeme.io
                    oraz rozpisz plan mailowy (tematy 3 wiadomości) do wdrożenia natychmiast.
                    
                    Badanie niszy:
                    {saved_niche['analysis'][:3000]}  # limit znaków
                    """
                    try:
                        rec_response = call_gemini_func([{"role": "user", "content": user_prompt}], system_instruction=system_instruction)
                        if rec_response:
                            st.markdown("#### 🎯 Rekomendacja AI:")
                            st.markdown(rec_response)
                        else:
                            st.error("Nie udało się wygenerować rekomendacji.")
                    except Exception as e:
                        st.error(f"Błąd: {str(e)}")
        else:
            st.warning("⚠️ Uruchom najpierw Badanie Niszy w Kroku 1, aby odblokować Rekomendator Lejka AI.")

    # ==================== KROK 3: MOTHER CONTENT PIPELINE ====================
    with tab_mother:
        st.subheader("📢 Mother Content Pipeline")
        st.markdown("""
        **Zasada Mother Content (Mirek Burnejko):** Tworzysz 1 główną treść ekspercką (Core Content), np. skrypt wideo, 
        artykuł na bloga, a AI automatycznie przetwarza ją na **6 formatów social media**, zachowując unikalny 
        głos Twojej marki (Ghost Profile Tomasza).
        """)

        # Wczytywanie profilu ghostwritera
        ghost_profile_content = ""
        ghost_path = "04-ghost/Ghost v2 - Głos Marki Tomasz.md"
        if os.path.exists(ghost_path):
            try:
                with open(ghost_path, "r", encoding="utf-8") as f:
                    ghost_profile_content = f.read()
            except Exception:
                pass

        core_content = st.text_area(
            "Wklej tutaj swój Core Content (główny artykuł lub przemyślenia):",
            height=200,
            placeholder="Wpisz lub wklej tutaj treść merytoryczną, z której chcesz wygenerować posty na social media..."
        )

        if st.button("Uruchom Pipeline i Wygeneruj 6 Formatów 🚀", use_container_width=True, type="primary"):
            if not core_content:
                st.warning("⚠️ Wprowadź Core Content przed uruchomieniem generowania.")
            else:
                with st.spinner("⚡ Ghostwriter przetwarza Core Content na 6 unikalnych formatów..."):
                    system_instruction = f"""
                    Jesteś osobistym Ghostwriterem Tomasza, genialnym copywriterem AI wyspecjalizowanym w budowaniu zaangażowania.
                    Poniżej znajduje się profil Tomasza (głos marki, styl, zasady):
                    
                    {ghost_profile_content[:2000] if ghost_profile_content else "Styl: energiczny, konkretny, przełamujący schematy, dopasowany do osób z ADHD (krótkie zdania, punktor, zero lania wody, autentyczność)."}
                    
                    Twoim zadaniem jest bezwzględne przestrzeganie tego stylu i przetworzenie podanej treści na 6 formatów.
                    """
                    
                    user_prompt = f"""
                    Przetwórz poniższy Core Content na 6 gotowych formatów dystrybucyjnych:
                    
                    CORE CONTENT:
                    {core_content}
                    
                    WYMAGANE FORMATY:
                    1. **Nitka na X/Twitter** (składająca się z min. 3 powiązanych, chwytliwych tweetów z emoji)
                    2. **Post merytoryczny na LinkedIn** (profesjonalny, z mocnym hookiem, lekko prowokacyjny, z wezwaniem do akcji)
                    3. **Koncepcja Karuzeli na Instagram** (slajd po slajdzie: tekst na slajd 1, slajd 2... do slajdu 5-6)
                    4. **Zajawka do Newslettera** (krótki, osobisty e-mail wciągający czytelnika z linkiem do pełnej treści)
                    5. **Skrypt pod pionowe wideo Short/Reel** (30-45 sekund, dynamiczny hook, treść, CTA, z zaznaczonymi wskazówkami wizualnymi)
                    6. **Post społecznościowy na Facebook** (bardziej luźny, zachęcający do dyskusji w komentarzach)
                    
                    Formatuj odpowiedź jako przejrzysty dokument z nagłówkami dla każdego formatu i przyciskami do łatwego kopiowania (oddziel formaty wyraźnymi liniami).
                    """
                    
                    try:
                        generated_formats = call_gemini_func([{"role": "user", "content": user_prompt}], system_instruction=system_instruction)
                        if generated_formats:
                            st.session_state.generated_social_content = generated_formats
                            st.success("🎉 Sukces! Wygenerowano 6 formatów dystrybucyjnych.")
                        else:
                            st.error("Nie udało się wygenerować formatów.")
                    except Exception as e:
                        st.error(f"Błąd generowania: {str(e)}")

        if "generated_social_content" in st.session_state:
            st.markdown("---")
            st.markdown("### 📱 Wygenerowane Formaty Dystrybucyjne:")
            st.markdown(st.session_state.generated_social_content)
            
            st.download_button(
                label="📥 Pobierz Paczkę Contentu (TXT)",
                data=st.session_state.generated_social_content,
                file_name="mother_content_social_pack.txt",
                mime="text/plain"
            )

    # ==================== KROK 4: INTEGRACJA SYSTEME.IO ====================
    with tab_systeme:
        st.subheader("📧 Zarządzanie kontaktami Systeme.io")
        st.markdown("""
        Poniższy panel integruje się bezpośrednio z Twoim darmowym kontem **Systeme.io** za pośrednictwem API.
        Możesz tutaj kontrolować bazę leadów, dodawać nowe kontakty ręcznie, a w przypadku awarii sieci lub braku klucza,
        system automatycznie zapisze dane w pliku awaryjnym (`clients/leads_fallback.json`), chroniąc Twoje leady.
        """)

        # Pokazywanie statusu połączenia
        if systeme_client.api_key:
            st.success(f"🟢 Połączono z Systeme.io (Klucz API obecny w .env)")
        else:
            st.warning("🔴 Brak klucza SYSTEME_IO_API_KEY w .env. System działa w trybie awaryjnym (Lead Fallback active).")

        # Sekcja 1: Dodawanie kontaktu
        st.markdown("### ➕ Dodaj nowy kontakt (Lead)")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            lead_email = st.text_input("E-mail kontaktu:", placeholder="np. jan.kowalski@gmail.com")
        with col_s2:
            lead_name = st.text_input("Imię:", placeholder="np. Jan")

        custom_fields_input = st.text_input("Dodatkowe pola niestandardowe (JSON format, opcjonalnie):", value='{"status": "lead"}')

        if st.button("Zapisz Kontakt 💾", use_container_width=True):
            if not lead_email or not lead_name:
                st.error("⚠️ Adres e-mail i imię są wymagane!")
            else:
                c_fields = {}
                if custom_fields_input:
                    try:
                        c_fields = json.loads(custom_fields_input)
                    except Exception:
                        st.warning("⚠️ Niepoprawny format JSON dla pól niestandardowych. Użyto pustego słownika.")
                
                with st.spinner("Zapisywanie kontaktu..."):
                    res = systeme_client.add_contact(lead_email, lead_name, custom_fields=c_fields)
                    
                    if res.get("status") == "success":
                        st.success(f"🎉 Kontakt {lead_email} dodany pomyślnie do Systeme.io!")
                    elif res.get("status") == "exists":
                        st.info(f"ℹ️ Kontakt {lead_email} już istnieje w Systeme.io.")
                    elif res.get("fallback"):
                        st.warning(f"⚠️ Problem z API. Lead został bezpiecznie zapisany w lokalnym pliku awaryjnym (leads_fallback.json).")
                    else:
                        st.error(f"Błąd zapisu: {res.get('message')}")

        st.markdown("---")

        # Sekcja 2: Wyświetlanie kontaktów i fallbacków
        st.markdown("### 👥 Lista Leadów")
        col_list1, col_list2 = st.columns(2)
        
        with col_list1:
            st.markdown("#### Pobrane z Systeme.io (API)")
            if st.button("Odśwież listę kontaktów 🔄", use_container_width=True):
                if not systeme_client.api_key:
                    st.error("Brak klucza API Systeme.io.")
                else:
                    with st.spinner("Pobieranie kontaktów z Systeme.io..."):
                        contacts_res = systeme_client.get_contacts()
                        if contacts_res.get("status") == "success":
                            st.session_state.systeme_contacts = contacts_res.get("data")
                        else:
                            st.error(f"Nie udało się pobrać kontaktów: {contacts_res.get('message')}")
            
            if "systeme_contacts" in st.session_state:
                contacts = st.session_state.systeme_contacts
                # Sprawdzenie typu danych
                if isinstance(contacts, dict) and "items" in contacts:
                    contacts_list = contacts["items"]
                elif isinstance(contacts, list):
                    contacts_list = contacts
                else:
                    contacts_list = []

                if contacts_list:
                    for c in contacts_list[:20]: # Pokazujemy max 20
                        fields = c.get("fields", [])
                        name = ""
                        for f in fields:
                            if f.get("slug") == "first_name":
                                name = f.get("value", "")
                        st.markdown(f"- **{name}** ({c.get('email')}) — ID: `{c.get('id')}`")
                else:
                    st.info("Brak kontaktów na Twoim koncie lub pusta odpowiedź.")

        with col_list2:
            st.markdown("#### Lokalne Leady Awaryjne (Fallback)")
            fallback_path = os.path.join("clients", "leads_fallback.json")
            if os.path.exists(fallback_path):
                try:
                    with open(fallback_path, "r", encoding="utf-8") as f:
                        fallback_leads = json.load(f)
                    
                    if fallback_leads:
                        st.markdown(f"Znaleziono **{len(fallback_leads)}** kontaktów oczekujących na synchronizację:")
                        for idx, fl in enumerate(fallback_leads):
                            st.markdown(f"{idx+1}. **{fl.get('first_name')}** ({fl.get('email')}) — *{fl.get('timestamp')}*")
                        
                        if systeme_client.api_key and st.button("Zsynchronizuj z Systeme.io ⚡", use_container_width=True):
                            with st.spinner("Trwa synchronizacja kontaktów z Systeme.io..."):
                                success_count = 0
                                failed_count = 0
                                remaining_leads = []
                                success_emails = []
                                failed_emails = []
                                
                                for fl in fallback_leads:
                                    email = fl.get("email")
                                    first_name = fl.get("first_name", "")
                                    custom_fields = fl.get("custom_fields", {})
                                    
                                    if not email:
                                        continue
                                        
                                    try:
                                        s_res = systeme_client.add_contact(email, first_name, custom_fields)
                                        status = s_res.get("status") if s_res else None
                                        
                                        if status in ["success", "exists"]:
                                            success_count += 1
                                            success_emails.append(email)
                                        else:
                                            failed_count += 1
                                            msg = s_res.get("message", "Nieznany błąd") if s_res else "Pusta odpowiedź API"
                                            failed_emails.append(f"{email} ({msg})")
                                            remaining_leads.append(fl)
                                    except Exception as ex:
                                        failed_count += 1
                                        failed_emails.append(f"{email} (Wyjątek: {str(ex)})")
                                        remaining_leads.append(fl)
                                
                                # Zapisanie pozostałych (które się nie zsynchronizowały)
                                try:
                                    with open(fallback_path, "w", encoding="utf-8") as f:
                                        json.dump(remaining_leads, f, indent=4, ensure_ascii=False)
                                except Exception as e_save:
                                    st.error(f"Nie udało się zapisać zaktualizowanej bazy fallback: {e_save}")
                                
                                # Wyświetlenie raportu telemetrycznego
                                st.markdown("### 📊 Raport z synchronizacji")
                                if success_count > 0:
                                    st.success(f"🟢 Pomyślnie zsynchronizowano **{success_count}** kontaktów!")
                                    for sem in success_emails:
                                        st.markdown(f"- ✅ `{sem}`")
                                        
                                if failed_count > 0:
                                    st.warning(f"🟠 Nie udało się zsynchronizować **{failed_count}** kontaktów (zostały zachowane w bazie awaryjnej):")
                                    for fem in failed_emails:
                                        st.markdown(f"- ⚠️ `{fem}`")
                                
                                if success_count > 0 or failed_count > 0:
                                    if st.button("Odśwież panel"):
                                        st.rerun()
                    else:
                        st.success("🎉 Brak lokalnych leadów awaryjnych. Wszystko czyste!")
                except Exception as e:
                    st.error(f"Błąd odczytu fallbacka: {str(e)}")
            else:
                st.success("🎉 Brak lokalnych leadów awaryjnych. Wszystko czyste!")
