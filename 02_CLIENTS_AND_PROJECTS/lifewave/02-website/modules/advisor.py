import streamlit as st
import os
import re

def load_knowledge_base():
    candidate_paths = [
        r"C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\lifewave\04-assets\knowledge_base",
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "04-assets", "knowledge_base")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-assets", "knowledge_base")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "04-assets", "knowledge_base")),
        "/app/04-assets/knowledge_base"
    ]
    
    kb_data = ""
    target_dir = None
    for path in candidate_paths:
        if os.path.exists(path):
            target_dir = path
            break
            
    if target_dir:
        for root, dirs, files in os.walk(target_dir):
            for f in files:
                if f.endswith(".md"):
                    full_p = os.path.join(root, f)
                    try:
                        with open(full_p, "r", encoding="utf-8", errors="ignore") as file:
                            kb_data += f"\n\n--- Z PLIKU {f} ---\n" + file.read()
                    except Exception:
                        pass
    return kb_data

def fallback_advisor(query, kb_content):
    """Smart heuristic fallback if Vertex AI API throws a permission error"""
    query_lower = query.lower()
    
    if "x2o" in query_lower or "wod" in query_lower or "stacj" in query_lower:
        return "✨ **Stacja Aktywacji Wody X2O™:** To zaawansowane urządzenie nablatowe. Najpierw oczyszcza wodę nanocząsteczkowo, następnie nasyca ją aktywnym wodorem cząsteczkowym (H2) obniżając ORP do głęboko ujemnych wartości (-300mV do -500mV), a na koniec naświetla biofotonową matrycą kwantową.\n\n💡 **Wskazówka:** Woda ustrukturyzowana posiada heksagonalne mikroklastry, co pozwala na natychmiastowe wchłanianie bez uczucia ciężkości w żołądku."
    elif "x39" in query_lower or "fototer" in query_lower or "plastr" in query_lower:
        return "✨ **Fotobiomodulacja X39:** Plaster zawiera organiczne nanokryształy odbijające ciepło podczerwone Twojego ciała. Sygnał świetlny stymuluje produkcję peptydu miedzi **GHK-Cu**, co aktywuje własne komórki macierzyste.\n\n💡 **Rekomendacja:** Przyklejaj plaster rano na kark (punkt C7) lub pod pępkiem (punkt CV6) na 12 godzin. Wypij szklankę wody X2O przed naklejeniem!"
    elif "lot" in query_lower or "mil" in query_lower or "biznes" in query_lower or "punkt" in query_lower:
        return "✨ **Loty za Mile i Punkty:** Skorzystaj z wyszukiwarek [Seats.aero](https://seats.aero) oraz [Roame.travel](https://roame.travel).\n\n💡 **Przykłady taryf:** W programie Miles & More w akcji *Meilenschnäppchen* lot do USA w Klasie Biznes kosztuje zaledwie **55 000 mil** (zamiast 110 000 mil)."
    elif "degustac" in query_lower or "łódź" in query_lower or "lodz" in query_lower or "świątyni" in query_lower:
        return "✨ **Zaproszenie na Degustację:** Naszym stacjonarnym przyczółkiem jest **Świątynia Harmonii** w Łodzi przy ul. Nawrot 104. Każda zaproszona osoba może bezpłatnie przetestować i odebrać szklankę świeżej wody ustrukturyzowanej X2O."
    elif "mlm" in query_lower or "duplikac" in query_lower or "biznes" in query_lower or "lider" in query_lower:
        return "✨ **Duplikacja w MLM:** Kluczem jest system 'Zaproś -> Pokaż -> Skonsultuj'. Nie tłumacz działania technologii samemu na początku - użyj narzędzi wideo z naszego portalu lub zaproś na degustację!\n\n💡 **Wskazówka:** Wejdź do modułu *Strefa Partnera*, gdzie znajdziesz pełny schemat lejków rekrutacyjnych."
    
    # Try to find a snippet in KB
    keywords = [word for word in query_lower.split() if len(word) > 4]
    for keyword in keywords:
        pattern = re.compile(r'(.{0,150}' + re.escape(keyword) + r'.{0,150})', re.IGNORECASE)
        match = pattern.search(kb_content)
        if match:
            return f"🔍 **Znalazłem fragment w naszej Bazie Wiedzy:**\n\n> *...{match.group(1)}...*\n\nAby uzyskać pełny kontekst, odwiedź moduł **Akademia Wiedzy**!"

    return "Odpowiadam na Twoje pytanie w oparciu o kanoniczną bazę wiedzy Klubu Fala Życia:\n\nPrzeanalizowałem temat, ale potrzebuję bardziej precyzyjnego zapytania. Sprawdź odpowiednie moduły w **Akademii Wiedzy** lub skontaktuj się ze swoim liderem!"


def get_agent_response(query, chat_history):
    kb_content = load_knowledge_base()
    
    try:
        from google import genai
        from google.genai import types
        
        # Vertex AI setup with GenAI SDK
        client = genai.Client(vertexai=True, project='falazycia-os', location='europe-central2')
        
        system_instruction = f"""
        Jesteś głównym Doradcą AI (Ghost v2) dla Klubu Fala Życia, powołanym przez Tomasza.
        Masz bezwzględny nakaz odpowiadania zgodnie z dostarczoną bazą wiedzy.
        Jesteś ekspertem od:
        1. Fotobiomodulacji i plastrów LifeWave (X39, X49 itp).
        2. Maszyny wodorowej X2O (Biofotonowa Aktywacja Wody).
        3. Marketingu Sieciowego (MLM) i duplikacji.
        4. Agregatorów lotów (Biznes Klasa za mile).
        5. Szkoły Oddechu i medytacji.
        
        Baza Wiedzy:
        {kb_content}
        
        Zawsze dodawaj wartość, formatuj odpowiedzi przy użyciu Markdown (pogrubienia ** **, listy, emoji). 
        Utrzymuj ton premium, ekspercki, ale bardzo wspierający.
        """
        
        # Create full context from history
        contents = []
        for msg in chat_history:
            role = 'user' if msg['role'] == 'user' else 'model'
            contents.append(types.Content(role=role, parts=[types.Part.from_text(msg['content'])]))
            
        contents.append(types.Content(role='user', parts=[types.Part.from_text(query)]))

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3
            )
        )
        return response.text
        
    except Exception as e:
        # Fallback to smart heuristic if GCP IAM is not configured
        return fallback_advisor(query, kb_content)

def render():
    st.title("🤖 Inteligentny Doradca Klubu Fala Życia")
    st.markdown("Masz pytania dotyczące działania Stacji X2O, plastrów fototerapeutycznych, rezerwacji lotów biznes klasą za mile lub duplikacji? Twój wirtualny doradca odpowie natychmiast na podstawie zweryfikowanej bazy wiedzy!")

    st.markdown("#### ⚡ Szybkie Podpowiedzi Pytań:")
    col_a, col_b, col_c, col_d = st.columns(4)
    quick_q = None
    if col_a.button("💧 Jak działa Stacja X2O?"):
        quick_q = "Jak dokładnie działa elektroniczna Stacja Hydratacji X2O i czym różni się od zwykłego filtra?"
    if col_b.button("🩹 Jak stosować X39?"):
        quick_q = "Gdzie przyklejać plaster X39 i dlaczego nawodnienie wodą X2O jest kluczowe?"
    if col_c.button("✈️ Loty Biznes Klasą?"):
        quick_q = "Jakie są najlepsze wyszukiwarki taryf milowych i ile mil potrzeba na lot do USA?"
    if col_d.button("🤝 System duplikacji?"):
        quick_q = "Jak skutecznie wdrażać system duplikacji w naszym MLM i zapraszać na degustację?"

    st.markdown("---")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_query = st.chat_input("Wpisz pytanie do Doradcy Klubu...")
    
    # Handle quick questions
    if quick_q:
        user_query = quick_q
        
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Przeszukiwanie bazy wiedzy Klubu & łączenie z Agentem AI..."):
                # Call agent
                response = get_agent_response(user_query, st.session_state.chat_history[:-1])
                st.markdown(response)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
