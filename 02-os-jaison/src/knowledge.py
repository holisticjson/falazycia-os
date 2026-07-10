import os
from datetime import datetime
from google.cloud import storage

# Upewniamy się, że folder Obsidiana istnieje
OBSIDIAN_DIR = os.getenv("OBSIDIAN_VAULT_PATH", os.path.join(os.getcwd(), "Obsidian_Vault"))
os.makedirs(OBSIDIAN_DIR, exist_ok=True)

# Nazwa bucketa zadeklarowana wcześniej
GCS_BUCKET_NAME = "holistic_kubelek"

def save_idea_to_obsidian_and_gcs(title: str, content: str, source: str = "Wrzutnia Streamlit") -> dict:
    """
    Zapisuje plik markdown lokalnie do Obsidiana, a następnie asynchronicznie przesyła do GCS.
    """
    safe_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip().replace(" ", "_")
    if not safe_title:
        safe_title = "Nowy_Pomysl"
        
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_title}.md"
    local_filepath = os.path.join(OBSIDIAN_DIR, filename)
    
    # Formatowanie nagłówka pod Obsidiana (YAML frontmatter)
    obsidian_content = f"""---
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
source: "{source}"
tags: [idea, hermes_os]
---

{content}
"""
    
    # 1. Zapis LOKALNY
    try:
        with open(local_filepath, "w", encoding="utf-8") as f:
            f.write(obsidian_content)
    except Exception as e:
        return {"status": "error", "message": f"Błąd zapisu lokalnego: {e}"}
        
    # 2. Zapis w GCS (Bucket)
    upload_msg = ""
    try:
        from google.auth.exceptions import DefaultCredentialsError
        # Wyłączamy ostrzeżenia SSL dla weryfikacji lokalnej
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        client = storage.Client()
        bucket = client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(f"wiedza/{filename}")
        
        # Wymuszamy typ MIME na text/plain (Vertex AI natywnie odrzuca text/markdown, co powodowało błędy indeksowania w logach)
        blob.upload_from_filename(local_filepath, content_type="text/plain")
        
        upload_msg = "Przesłano do Google Cloud Storage (RAG)."
    except DefaultCredentialsError:
        upload_msg = "⚠️ BRAK AUTORYZACJI GCP! Otwórz PowerShell i wpisz: gcloud auth application-default login"
    except Exception as e:
        if "SSL" in str(e) or "certificate" in str(e):
             upload_msg = "⚠️ BŁĄD SSL! Otwórz PowerShell jako administrator lub ustaw os.environ['REQUESTS_CA_BUNDLE'] = ''"
        else:
             upload_msg = f"Błąd chmury: {e}"
        
    return {
        "status": "success", 
        "message": f"Zapisano lokalnie jako {filename}. {upload_msg}"
    }

def query_vertex_ai_search(query: str, project_id: str = None, location: str = "global", 
                           collection: str = "default_collection", engine: str = None) -> str:
    """
    Wywołuje Vertex AI Discovery Engine API (Answer API).
    Zgodnie z zasadą Zero Zagadek: proaktywnie waliduje autoryzację i certyfikaty.
    """
    # Dynamiczny wybór silnika na podstawie profilu w Streamlicie (ADHD Context Switcher)
    try:
        import streamlit as st
        active_profile = st.session_state.get("active_profile", "Agencja Jason (Marketing)")
    except Exception:
        active_profile = "Agencja Jason (Marketing)"

    # Default mappings z możliwością nadpisania przez plik .env
    if "Broker" in active_profile:
        profile_project = os.getenv("GCP_PROJECT_BROKER", "holistic-broker")
        profile_engine = os.getenv("VERTEX_ENGINE_BROKER", "broker-search-app-id")
    else:
        profile_project = os.getenv("GCP_PROJECT_AGENCY", "771359551342")
        profile_engine = os.getenv("VERTEX_ENGINE_AGENCY", "holistic-search-app_1780143991783")

    if project_id is None:
        project_id = profile_project
    if engine is None:
        engine = profile_engine

    import requests
    import google.auth
    from google.auth.transport.requests import Request
    from google.auth.exceptions import DefaultCredentialsError
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    try:
        credentials, _ = google.auth.default()
        
        # 1. Brutalne obejście weryfikacji SSL dla biblioteki google-auth (błąd pobierania tokena oauth2)
        import requests
        old_request = requests.Session.request
        def new_request(*args, **kwargs):
            kwargs['verify'] = False
            return old_request(*args, **kwargs)
        requests.Session.request = new_request
        
        # 2. Pobranie tokenu z wyłączoną weryfikacją
        try:
            credentials.refresh(Request())
        finally:
            # 3. Przywrócenie standardowego zachowania po pobraniu tokenu
            requests.Session.request = old_request
            
        token = credentials.token
        
        url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{project_id}/locations/{location}/collections/{collection}/engines/{engine}/servingConfigs/default_search:answer"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "query": {"text": query},
            "relatedQuestionsSpec": {"enable": True},
            "answerGenerationSpec": {
                "ignoreAdversarialQuery": True,
                "ignoreNonAnswerSeekingQuery": False
            }
        }
        
        # verify=False wymusza obejście błędu lokalnego certyfikatu dla Vertex AI
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status()
        
        data = response.json()
        result_text = ""
        
        if "answer" in data and "answerText" in data["answer"]:
            result_text = data["answer"]["answerText"] + "\n\n"
            
        # Wyciąganie fragmentów dokumentów (snippetów), jeśli RAG nie poradził sobie ze złożeniem ładnego zdania
        snippets_found = []
        if "answer" in data and "steps" in data["answer"]:
            for step in data["answer"]["steps"]:
                if "actions" in step:
                    for action in step["actions"]:
                        if "observation" in action and "searchResults" in action["observation"]:
                            for res in action["observation"]["searchResults"]:
                                if "snippetInfo" in res:
                                    for snip in res["snippetInfo"]:
                                        if "snippet" in snip:
                                            snippets_found.append(snip["snippet"])
        
        if snippets_found:
            result_text += "---\n### 📄 Znalezione fragmenty w dokumentach:\n"
            for i, snip in enumerate(snippets_found):
                # Usuwamy znaczniki HTML <b> z wyników Google'a dla czytelności
                clean_snip = snip.replace("<b>", "**").replace("</b>", "**")
                result_text += f"{i+1}. {clean_snip}...\n"
                
        if not result_text.strip():
            return "Brak odpowiedzi i brak fragmentów z RAG. (Baza może być pusta lub w trakcie indeksowania)"
            
        return result_text
        
    except DefaultCredentialsError:
        return "⚠️ **Brak kluczy Google Cloud (ADC)!**\n\nAgent nie może połączyć się z Vertex AI.\n\n**Co musisz zrobić?**\n1. Otwórz terminal (PowerShell).\n2. Wpisz komendę: `gcloud auth application-default login`\n3. Zaloguj się w przeglądarce, która się otworzy.\n4. Zrestartuj aplikację."
    except requests.exceptions.SSLError as ssl_err:
         return f"⚠️ **Problem z Certyfikatem SSL!**\n\nTwój system Windows lub antywirus blokuje bezpieczne połączenie do Google.\nBłąd: `{ssl_err}`\nUpewnij się, że nie korzystasz z VPN blokującego certyfikaty."
    except Exception as e:
        return f"⚠️ **Wewnętrzny błąd API Vertex AI:**\n\nSzczegóły: {e}"

def query_dual_knowledge_base(query: str, data_store_id: str = None) -> dict:
    """
    Kieruje zapytanie do odpowiedniego źródła wiedzy (GCS/Vertex AI Search vs Brain Dump/Obsidian).
    Klasyfikacja odbywa się na podstawie słów kluczowych.
    """
    query_lower = query.lower()
    brain_dump_keywords = ["brain", "dump", "zrzut", "notatk", "lokal", "obsidian", "inbox", "prywat", "pomysł", "pomysl", "idea"]
    
    route_to_brain_dump = any(kw in query_lower for kw in brain_dump_keywords)
    
    if route_to_brain_dump:
        reason = f"Wykryto słowo kluczowe powiązane z notatkami lokalnymi."
        matches = []
        files_searched = 0
        
        # Filtrujemy słowa sterujące/routingowe (np. "notatki", "inbox")
        search_words = [
            w for w in query_lower.split()
            if len(w) > 2 and not any(rkw in w for rkw in brain_dump_keywords)
        ]
        if not search_words:
            search_words = [w for w in query_lower.split() if len(w) > 2]
        
        if os.path.exists(OBSIDIAN_DIR):
            for root, dirs, files in os.walk(OBSIDIAN_DIR):
                for file in files:
                    if file.endswith(".md"):
                        files_searched += 1
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read()
                            if query_lower in content.lower():
                                matches.append((file, content))
                            else:
                                if search_words and all(kw in content.lower() for kw in search_words):
                                    matches.append((file, content))
                        except Exception as e:
                            print(f"Błąd odczytu pliku {file_path}: {e}")
                            
        if matches:
            result_text = f"Znaleziono {len(matches)} dopasowań w lokalnym Obsidian Vault (przeszukano {files_searched} plików):\n\n"
            for idx, (filename, content) in enumerate(matches):
                preview = content[:300].replace("\n", " ")
                if len(content) > 300:
                    preview += "..."
                result_text += f"**{idx + 1}. Plik: {filename}**\nPodgląd: {preview}\n\n"
        else:
            result_text = f"Nie znaleziono dopasowań w lokalnym Obsidian Vault (przeszukano {files_searched} plików) dla zapytania: '{query}'."
            
        return {
            "source": "brain_dump",
            "query": query,
            "result": result_text,
            "routing_reason": reason,
            "files_searched": files_searched,
            "matches_count": len(matches)
        }
    else:
        reason = "Kierowanie do chmury (GCS / Vertex AI Search) na podstawie domyślnej klasyfikacji."
        try:
            if data_store_id:
                result_text = query_vertex_ai_search(query, engine=data_store_id)
            else:
                result_text = query_vertex_ai_search(query)
        except Exception as e:
            result_text = f"Błąd podczas odpytywania Vertex AI Search: {e}"
            
        return {
            "source": "gcs",
            "query": query,
            "result": result_text,
            "routing_reason": reason,
            "files_searched": 0,
            "matches_count": 0
        }
