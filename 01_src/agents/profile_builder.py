import streamlit as st
from google import genai
from google.genai import types
import os
from pathlib import Path
from datetime import datetime

def get_vertex_client():
    VERTEX_PROJECT = os.environ.get("GCP_PROJECT", "holistic-dashboard-dev")
    VERTEX_LOCATION = os.environ.get("GCP_LOCATION", "us-central1")
    SA_KEY_PATH = r"c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"
    
    if os.path.exists(SA_KEY_PATH):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_KEY_PATH
        
    try:
        return genai.Client(vertexai=True, project=VERTEX_PROJECT, location=VERTEX_LOCATION)
    except Exception:
        return genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def read_baza_wiedzy_folder(folder_name):
    folder_path = Path("Baza_Wiedzy") / folder_name
    if not folder_path.exists():
        return ""
    
    content = ""
    for file in folder_path.glob("*.md"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                content += f"\n--- PLIK: {file.name} ---\n" + f.read() + "\n"
        except UnicodeDecodeError:
            with open(file, "r", encoding="cp1250", errors="ignore") as f:
                content += f"\n--- PLIK: {file.name} ---\n" + f.read() + "\n"
    return content

def render_profile_builder():
    st.title("🕵️ Głęboki Czat Profilujący (AI Biznes Lab)")
    st.markdown("""
    **Interaktywny Asystent Budowy Profilu (Własny Profil)**  
    Zamiast powierzchownego skanu, ten Agent będzie Cię **przesłuchiwał** krok po kroku na podstawie checklist Mirka Burnejko.
    Możesz wklejać swoje notatki, plany, a agent dopyta tylko o to, czego brakuje. Gdy skończycie, zapisze potężny profil w pliku `.md`.
    """)
    
    mb_dir = Path("Baza_Wiedzy/Mirek_Burnejko_AI_Biznes_Lab")
    mb_dir.mkdir(parents=True, exist_ok=True)
    knowledge_context = read_baza_wiedzy_folder("Mirek_Burnejko_AI_Biznes_Lab")
    
    # Inicjalizacja stanu czatu
    if "profile_chat" not in st.session_state:
        st.session_state.profile_chat = [
            {"role": "model", "content": "Cześć! Jestem Twoim Osobistym Profilerem AI. Przeczytałem wytyczne Mirka Burnejko (AI Biznes Lab). Moim zadaniem jest zbudowanie Twojego Głębokiego Profilu Przedsiębiorcy.\n\nJeśli masz jakieś notatki, plany workflow, zarysy ofert – wklej je tutaj. Przeanalizuję je, a następnie zacznę zadawać Ci pytania tylko z tych obszarów checklisty, których brakuje. Jak brzmi Twoje imię i marka?"}
        ]
        
    # Wyświetlanie czatu
    for msg in st.session_state.profile_chat:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.markdown(msg["content"])
            
    # Input użytkownika
    if user_input := st.chat_input("Napisz odpowiedź lub wklej swoje notatki..."):
        st.session_state.profile_chat.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        with st.chat_message("assistant"):
            with st.spinner("Myślę nad kolejnym pytaniem..."):
                client = get_vertex_client()
                
                # Budowanie historii konwersacji w formacie tekstu do promptu
                history_text = ""
                for m in st.session_state.profile_chat:
                    role_name = "Ja (Twórca)" if m["role"] == "user" else "Ty (Profiler)"
                    history_text += f"\n{role_name}: {m['content']}"
                
                prompt = f"""
                Jesteś profesjonalnym Agentem-Profilerem. Działasz wg metodologii Mirka Burnejko (AI Biznes Lab).
                Oto Twoje wytyczne i checklisty z Bazy Wiedzy:
                {knowledge_context[:20000]}
                
                Oto dotychczasowa historia naszej rozmowy:
                {history_text}
                
                Twoje zadanie teraz:
                1. Przeanalizuj moją ostatnią odpowiedź/wklejone notatki.
                2. Sprawdź, jakich kluczowych informacji brakuje nam z checklisty Mirka Burnejko (np. persony, bóle klienta, struktura oferty, filozofia pracy).
                3. ZADANIE: Zadaj mi kolejne JEDNO lub DWA precyzyjne pytania, aby uzupełnić te braki.
                4. Bądź konwersacyjny, ale konkretny. Nie generuj jeszcze całego profilu, tylko prowadz przesłuchanie.
                """
                
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-pro",
                        contents=prompt,
                        config=types.GenerateContentConfig(temperature=0.7)
                    )
                    reply = response.text
                    st.session_state.profile_chat.append({"role": "model", "content": reply})
                    st.markdown(reply)
                    st.rerun()
                except Exception as e:
                    st.error(f"Błąd API: {str(e)}")
                    
    # Przycisk do wygenerowania ostatecznego pliku
    st.divider()
    if st.button("💾 Zakończ przesłuchanie i Wygeneruj Ostateczny Profil (.md)", type="primary"):
        with st.spinner("Generowanie potężnego profilu z całej konwersacji..."):
            client = get_vertex_client()
            history_text = ""
            for m in st.session_state.profile_chat:
                role_name = "Twórca" if m["role"] == "user" else "Profiler"
                history_text += f"\n{role_name}: {m['content']}"
                
            prompt_final = f"""
            Jesteś Agentem-Orkiestratorem. Mamy za sobą długi wywiad profilujący z użytkownikiem wg wytycznych Mirka Burnejko.
            
            Oto cała historia wywiadu:
            {history_text}
            
            Oto oryginalne wytyczne/checklisty AI Biznes Lab:
            {knowledge_context[:20000]}
            
            Twoje zadanie:
            Stwórz ostateczny, gigantyczny i wyczerpujący PROFIL PRZEDSIĘBIORCY (w formacie Markdown).
            Ma on stanowić bazowy plik-matkę (Baza Wiedzy) dla całej autonomicznej firmy.
            Wypełnij go informacjami wyciągniętymi z wywiadu. Podziel na logiczne sekcje (O Mnie, Umiejętności, Oferta, Cele, Persony, Asystenci do stworzenia).
            Zwróć TYLKO czysty kod Markdown.
            """
            try:
                response_final = client.models.generate_content(
                    model="gemini-2.5-pro",
                    contents=prompt_final,
                    config=types.GenerateContentConfig(temperature=0.4)
                )
                final_md = response_final.text
                
                # Usuń znaczniki ```markdown jeśli model je dodał
                if final_md.startswith("```markdown"):
                    final_md = final_md[11:]
                if final_md.endswith("```"):
                    final_md = final_md[:-3]
                    
                client_dir = Path("clients/Moj_Wlasny_Profil")
                client_dir.mkdir(parents=True, exist_ok=True)
                filepath = client_dir / "Holistic_Jason_Profil_AIBiznesLab.md"
                
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(final_md.strip())
                    
                st.success(f"✅ Profil zapisany na stałe w: `{filepath}`")
                st.download_button("Pobierz Plik Profilu", final_md.strip(), "moj_profil.md")
                
                with st.expander("Podgląd Wygenerowanego Profilu"):
                    st.markdown(final_md)
            except Exception as e:
                st.error(f"Błąd przy generowaniu pliku: {str(e)}")
