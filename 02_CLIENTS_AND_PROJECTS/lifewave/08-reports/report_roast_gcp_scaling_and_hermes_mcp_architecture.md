# 🥩 RAPORT ROASTU ARCHITEKTURY GCP, MCP & PORTOWANIA AGENTÓW "FALA ŻYCIA"

---

> [!WARNING] ZAUWAŻONE DZIURY LOGICZNE, RYZYKA BILINGOWE & BŁĘDY SKALOWANIA:
> 
> 1. **Koszmar Autoryzacji Dwóch Kont GCP (Cross-Account IAM Hell):**  
>    Jeśli chatbot na frontendzie (`swiatynia.fala-zycia.pl` lub `monika.fala-zycia.pl`) hostowanym na koncie `falazycia.klub@gmail.com` będzie strzelał do *Vertex AI Agent Builder* w projekcie na koncie `holisticjason@gmail.com`, zderzysz się z błędami CORS, barierą brakujących tokenów ADC i odrzuconymi połączeniami IAM.
>    * **Rozwiązanie:** Musimy stworzyć Service Account w projekcie `holisticjason`, nadać mu rolę `roles/discoveryengine.admin` / `roles/aiplatform.user` i wygenerować plik klucza JSON, który podpinamy jako Secret w środowisku `falazycia.klub`.
> 
> 2. **Dziura Ręcznego Klikania (Brak Agenta w Kodzie — Agent-as-Code):**  
>    Jeśli poklikasz agenty konwersacyjne w GUI konsoli GCP, to po przyznaniu grantu $1000 dla firmy Moniki "SpotOn" będziesz musiał spędzić 3 dni na ręcznym przeklikiwaniu konfiguracji na nowe konto.
>    * **Rozwiązanie:** Wszystkie agenty, ich instrukcje systemowe i podpięte Data Store’y (pliki RAG w GCS) **MUSZĄ być zdefiniowane w kodzie Python (`google-genai` / `vertexai`) lub wyeksportowane do plików JSON/YAML**. Dzięki temu migracja na nowe konto to wywołanie jednej komendy: `python deploy_agent_stack.py`.
> 
> 3. **Risks w MCP Loop & Powielaniu Dashboardu Streamlit:**  
>    Łączenie Streamlita z Hermes Agentic OS przez MCP i puszczenie tego na grupy WhatsApp/Discord stwarza ryzyko **"Infinite Agent Loop"** (agenci rozmawiający ze sobą na grupach i spalający limity API) oraz brak izolacji kluczy API (NVIDIA NIM, fal.ai, Together AI).
>    * **Rozwiązanie:** Centralna kontrola zmiennych w pliku `.env` + Middleware w n8n ze sztywnym filtrem botów (`if msg.author.is_bot: ignore`) oraz awaryjnym przełączaniem (Fallback) na **Gemini 2.5 Flash** (Rule 0 z AGENTS.md), jeśli zewnętrzne API nawali.

---

## ⚡ REKOMENDOWANY PLAN I ARCHITEKTURA PORTOWALNA (STEP-BY-STEP)

```mermaid
graph TD
    A["🌐 Frontend / Landingi Partnerów<br>(swiatynia / monika / x2o)"] -->|1. Web Chatbot / Formularze| B["⚡ Cloud Run Backend<br>(falazycia.klub@gmail.com)"]
    B -->|2. Authenticated API Call (Service Account Key)| C["🤖 Vertex AI Agent Builder / RAG<br>(Projekt na holisticjason@gmail.com — Środki $1000)"]
    B -->|3. Eventy & Webhooki| D["🔄 n8n Middleware + Hermes OS<br>(Zarządzanie WhatsApp / Discord)"]
    D -->|4. MCP Bridge| E["📊 Streamlit Dashboard Fala Życia OS<br>(Zarządzanie Liderami, Treściami, Kalendarzem)"]
```

---

### 📋 REKOMENDOWANE POPRAWKI ARCHITEKTONICZNE (CHECKLISTA DO WDROŻENIA):

- [ ] **1. Izolacja Kluczy i Secretów (`.env.example` Schema):**  
  Utworzyć standaryzowany szablon `.env.example` w projekcie z podziałem na:
  - `GCP_PROJECT_ID_AGENT_BUILDER` (`holisticjason` project)
  - `GCP_SERVICE_ACCOUNT_KEY_PATH` (ścieżka do JSON)
  - `GEMINI_API_KEY` (Gemini 2.5 Flash / Pro)
  - `EXTERNAL_MODEL_KEYS` (NVIDIA, Together, fal.ai)
- [ ] **2. Agent-as-Code (Eksportowalny Konfigurator Agentów):**  
  Zamiast ręcznie wyklikiwać boty w GCP Console, napisać skrypt w Pythonie zasilany plikiem JSON z wiedzą (`mlm_kb.json` / `fala_zycia_rag.json`).
- [ ] **3. Middleware Zabezpieczający n8n & WhatsApp/Discord:**  
  Wdrożyć filtr zapobiegający pętlom agentów i narzucić limity zapytań (Rate Limiting).
- [ ] **4. Uniwersalny Szablon Streamlit Dashboard ("Fala Życia OS"):**  
  Sklonować kod dashboardu z agencji, ale odseparować go tak, aby wczytywał dane dynamicznie z bazy/GCS projektu Fali Życia.
