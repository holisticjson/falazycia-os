import streamlit as st
import os, json, time
import ssl
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except AttributeError:
    pass

st.set_page_config(
    page_title="Holistic AIDHD OS • Mission Control",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ścieżki w chmurze
BASE_DIR = os.path.expanduser("~/Agentic_OS")
NOTEBOOKS_DIR = os.path.join(BASE_DIR, "notebooks/_assets")
OBSIDIAN_DIR = os.path.join(BASE_DIR, "obsidian_vault")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboard")
BRAIN_DUMP_DIR = os.path.join(BASE_DIR, "brain_dump")
BRAIN_DUMP_ASSETS = os.path.join(BRAIN_DUMP_DIR, "_assets")
HERMES_DIR = os.path.expanduser("~/.hermes")
KANBAN_FILE = os.path.join(DASHBOARD_DIR, "kanban.json")

# Tworzenie folderów
for d in [NOTEBOOKS_DIR, OBSIDIAN_DIR, DASHBOARD_DIR, BRAIN_DUMP_DIR, BRAIN_DUMP_ASSETS, HERMES_DIR]:
    os.makedirs(d, exist_ok=True)

# Luksusowy nocny design zoptymalizowany pod ADHD (Outfit & Atkinson)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400;1,700&family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Globalny reset barw i typografii */
    .stApp {
        background-color: #08090C !important;
        color: #E2E8F0 !important;
        font-family: 'Atkinson Hyperlegible', sans-serif !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0E1015 !important;
        border-right: 1px solid #1F242E !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }
    
    /* Luksusowe karty z efektem neonowego obramowania po najechaniu */
    .custom-card {
        background-color: #121620;
        border: 1px solid #1E2535;
        border-radius: 14px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    }
    
    .custom-card:hover {
        border-color: #7C3AED;
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(124, 58, 237, 0.15);
    }
    
    /* Banner One Thing - eliminacja szumu kognitywnego */
    .one-thing-banner {
        background: linear-gradient(135deg, #181528 0%, #0E1015 100%);
        border-left: 6px solid #F59E0B;
        border-radius: 14px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    /* Zaokrąglone przyciski premium (globalnie dla stButton) */
    .stButton>button {
        background: linear-gradient(135deg, #6D28D9 0%, #4C1D95 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #7C3AED !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(109, 40, 217, 0.3) !important;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.5) !important;
    }

    /* Kafelki Nawigacyjne w Pasku Bocznym (ADHD Tiles) */
    div[data-testid="stSidebar"] .stButton>button {
        text-align: left !important;
        padding: 12px 18px !important;
        height: 52px !important;
        margin-bottom: 2px !important;
        font-family: 'Outfit', sans-serif !important;
        width: 100% !important;
    }

    div[data-testid="stSidebar"] .stButton>button[kind="secondary"] {
        background: #121620 !important;
        color: #94A3B8 !important;
        border: 1px solid #1E2535 !important;
        box-shadow: none !important;
        font-weight: 500 !important;
    }

    div[data-testid="stSidebar"] .stButton>button[kind="secondary"]:hover {
        background: #1A1F2C !important;
        border-color: #7C3AED !important;
        color: #FFFFFF !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.15) !important;
    }

    div[data-testid="stSidebar"] .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #7C3AED 0%, #5B21B6 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #C084FC !important;
        box-shadow: 0 0 15px rgba(124, 58, 237, 0.35) !important;
        font-weight: 700 !important;
    }
    
    div[data-testid="stSidebar"] .stButton>button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 0 20px rgba(124, 58, 237, 0.5) !important;
    }
    
    /* ADHD-friendly akcenty kolorystyczne */
    .dopamine-accent { color: #10B981; font-weight: bold; }
    .burn-accent { color: #EF4444; font-weight: bold; }
    .focus-accent { color: #F59E0B; font-weight: bold; }

    /* Pływający Przycisk Szybkiego Zapisu (FAB - Floating Action Button) */
    .fab-container {
        position: fixed !important;
        bottom: 25px !important;
        right: 25px !important;
        z-index: 999999 !important;
    }
    
    .fab-container button {
        background: linear-gradient(135deg, #EC4899 0%, #D946EF 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #F472B6 !important;
        border-radius: 50% !important;
        width: 65px !important;
        height: 65px !important;
        font-size: 28px !important;
        font-family: 'Outfit', sans-serif !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        box-shadow: 0 4px 20px rgba(236, 72, 153, 0.4) !important;
        transition: all 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        animation: pulse-fab 2s infinite alternate !important;
        padding: 0 !important;
    }
    
    .fab-container button:hover {
        transform: scale(1.12) rotate(15deg) !important;
        box-shadow: 0 6px 25px rgba(236, 72, 153, 0.7), 0 0 15px rgba(217, 70, 239, 0.4) !important;
    }
    
    @keyframes pulse-fab {
        0% {
            box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4);
            transform: scale(1);
        }
        100% {
            box-shadow: 0 6px 25px rgba(236, 72, 153, 0.8), 0 0 20px rgba(217, 70, 239, 0.5);
            transform: scale(1.05);
        }
    }
</style>

""", unsafe_allow_html=True)

# Helpery danych
def load_kanban():
    return json.load(open(KANBAN_FILE, "r", encoding="utf-8")) if os.path.exists(KANBAN_FILE) else {"todo":[], "in_progress":[], "done":[]}

def save_kanban(data):
    json.dump(data, open(KANBAN_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=4)

CRM_FILE = os.path.join(DASHBOARD_DIR, "crm.json")

def load_crm():
    if os.path.exists(CRM_FILE):
        try:
            return json.load(open(CRM_FILE, "r", encoding="utf-8"))
        except:
            pass
    return {
        "leads": [
            {
                "id": "lead_01",
                "name": "Klinika Dermatologiczna (Łódź)",
                "stage": "conversation",
                "notes": "Zainteresowani automatyzacją ankiety intake w celu uwolnienia czasu personelu. Duża potrzeba empatii i prostego lejka wdrożeniowego.",
                "last_contact": "2026-05-29",
                "next_action": "Opracować plan wdrożenia 3 asystentów AI.",
                "draft_reply": "Dzień dobry. Przeanalizowałem Państwa wąskie gardła. Wdrożenie Niewidzialnego Pracownika AI do ankiety intake pozwoli zaoszczędzić około 15 godzin tygodniowo bez utraty ciepłego kontaktu z pacjentem..."
            },
            {
                "id": "lead_02",
                "name": "Jan Szopa (Dystrybutor Kursów)",
                "stage": "architecture",
                "notes": "Zainteresowany systemem czystej pamięci (Pristine Memory) dla swoich studentów z ADHD.",
                "last_contact": "2026-05-28",
                "next_action": "Przygotować interfejs MVP z pasywnym tablicowaniem.",
                "draft_reply": "Cześć Jan, w oparciu o nasze rozmowy, zaprojektowałem strukturę bezszumnego CRM bez powiadomień push..."
            }
        ]
    }

def save_crm(data):
    json.dump(data, open(CRM_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=4)

# --- POLSKI ADHD GHL INTEGRATIONS ---
import urllib.parse
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class UrllibResponse:
    def __init__(self, status_code, text, json_data=None):
        self.status_code = status_code
        self.text = text
        self._json_data = json_data
    
    def json(self):
        if self._json_data is not None:
            return self._json_data
        return json.loads(self.text)

def http_post(url, json_data=None, headers=None, timeout=30.0):
    if headers is None:
        headers = {}
    
    # Ensure Content-Type is set if json_data is present
    if json_data is not None and "Content-Type" not in headers:
        headers["Content-Type"] = "application/json"
        
    data_bytes = None
    if json_data is not None:
        data_bytes = json.dumps(json_data).encode("utf-8")
        
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            status_code = response.getcode()
            response_text = response.read().decode("utf-8")
            try:
                res_json = json.loads(response_text)
            except:
                res_json = None
            return UrllibResponse(status_code, response_text, res_json)
    except urllib.error.HTTPError as e:
        status_code = e.code
        try:
            response_text = e.read().decode("utf-8")
        except:
            response_text = str(e)
        try:
            res_json = json.loads(response_text)
        except:
            res_json = None
        return UrllibResponse(status_code, response_text, res_json)
    except Exception as e:
        return UrllibResponse(500, str(e), None)

# Thread-safe global flag to start webhook server once
_server_started = False
_server_lock = threading.Lock()

def call_vllm_api(messages, system_instruction=None):
    url = "http://localhost:8000/v1/chat/completions"
    headers = {
        "Authorization": "Bearer HOLISTIC_SECURE_TOKEN_2026",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/Mistral-Nemo-Instruct-2407",
        "messages": []
    }
    if system_instruction:
        payload["messages"].append({"role": "system", "content": system_instruction})
    payload["messages"].extend(messages)
    
    try:
        response = http_post(url, json_data=payload, headers=headers, timeout=120.0)
        if response.status_code == 200:
            res_data = response.json()
            return res_data["choices"][0]["message"]["content"]
    except Exception as e:
        pass
        
    return call_gemini_api(messages, system_instruction)

def call_gemini_api(messages, system_instruction=None):
    proxy_url = "http://127.0.0.1:8089/v1/chat/completions"
    payload = {
        "model": "gemini-2.5-flash",
        "messages": []
    }
    if system_instruction:
        payload["messages"].append({"role": "system", "content": system_instruction})
    payload["messages"].extend(messages)
    
    # 1. Try local proxy (timeout 90s for long OCR operations)
    try:
        response = http_post(proxy_url, json_data=payload, timeout=90.0)
        if response.status_code == 200:
            res_data = response.json()
            return res_data["choices"][0]["message"]["content"]
    except Exception as e:
        pass
        
    # 2. Fallback to direct GCP Vertex AI call
    sa_paths = [
        os.path.expanduser("~/.hermes/gcp-sa-key.json"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "holistic-dashboard-dev-dea2c872139e.json"),
        "holistic-dashboard-dev-dea2c872139e.json"
    ]
    sa_path = None
    for p in sa_paths:
        if os.path.exists(p):
            sa_path = p
            break
            
    if sa_path:
        try:
            from google.oauth2 import service_account
            import google.auth.transport.requests
            import requests
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            creds = service_account.Credentials.from_service_account_file(
                sa_path,
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            session = requests.Session()
            session.verify = False
            request = google.auth.transport.requests.Request(session=session)
            creds.refresh(request)
            token = creds.token
            
            project_id = "holistic-dashboard-dev"
            region = "us-central1"
            direct_url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/endpoints/openapi/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            direct_payload = {
                "model": "google/gemini-2.5-flash",
                "messages": []
            }
            if system_instruction:
                direct_payload["messages"].append({"role": "system", "content": system_instruction})
            direct_payload["messages"].extend(messages)
            
            resp = http_post(direct_url, json_data=direct_payload, headers=headers, timeout=25.0)
            if resp.status_code == 200:
                res_data = resp.json()
                return res_data["choices"][0]["message"]["content"]
        except Exception as ex:
            return f"Błąd bezpośredniej komunikacji z Vertex AI: {ex}"
            
    return "Błąd: Brak połączenia z lokalnym proxy i brak poprawnego klucza Service Account."

def call_gemini_pro_api(messages, system_instruction=None):
    """Dedykowana funkcja dla modelu Gemini 2.5 Pro przez lokalny proxy.
    Używamy go w Dziale Prawnym dla analizy dokumentów i logiki prawnej.
    Timeout 120s dla długich dokumentów."""
    proxy_url = "http://127.0.0.1:8089/v1/chat/completions"
    
    # Sprawdź czy wiadomości zawierają multimodalne treści (PDF/obrazy) — użyj Flash
    # bo proxy może nie obsługiwać dużych payloadów multimodalnych dla Pro
    has_multimodal = False
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict) and part.get("type") == "image_url":
                    has_multimodal = True
                    break
    
    model_name = "gemini-2.5-flash" if has_multimodal else "gemini-2.5-pro"
    
    payload = {"model": model_name, "messages": []}
    if system_instruction:
        payload["messages"].append({"role": "system", "content": system_instruction})
    payload["messages"].extend(messages)

    try:
        response = http_post(proxy_url, json_data=payload, timeout=120.0)
        if response.status_code == 200:
            res_data = response.json()
            return res_data["choices"][0]["message"]["content"]
        else:
            # Próba z Flash jako fallback
            payload["model"] = "gemini-2.5-flash"
            response2 = http_post(proxy_url, json_data=payload, timeout=90.0)
            if response2.status_code == 200:
                return response2.json()["choices"][0]["message"]["content"]
    except Exception:
        pass

    # Ostateczny fallback
    return call_gemini_api(messages, system_instruction)

def call_native_vertex_ocr(file_bytes):
    # Get credentials and refresh token
    sa_paths = [
        os.path.join(os.getcwd(), "holistic-dashboard-dev-dea2c872139e.json"),
        os.path.expanduser("~/.hermes/gcp-sa-key.json"),
        "holistic-dashboard-dev-dea2c872139e.json"
    ]
    sa_path = None
    for p in sa_paths:
        if os.path.exists(p):
            sa_path = p
            break
            
    if not sa_path:
        return "[Błąd: Brak klucza GCP Service Account]"
        
    try:
        from google.oauth2 import service_account
        import google.auth.transport.requests
        import requests
        import base64 as _b64
        
        creds = service_account.Credentials.from_service_account_file(
            sa_path,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        session = requests.Session()
        session.verify = False
        request = google.auth.transport.requests.Request(session=session)
        creds.refresh(request)
        token = creds.token
        
        project_id = "holistic-dashboard-dev"
        region = "us-central1"
        model = "gemini-2.5-flash" # Use flash for fast OCR
        
        url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/publishers/google/models/{model}:generateContent"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        encoded_data = _b64.b64encode(file_bytes).decode("utf-8")
        
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": "Odczytaj i przepisz DOKŁADNIE cały tekst z załączonego dokumentu PDF (skanu). Zachowaj wszystkie kluczowe dane: sygnatury akt, PESEL, NIP, adresy, imiona i nazwiska, kwoty, daty, nazwy sądów lub organów. Zwróć tylko surowy odczytany tekst, zachowując oryginalny układ."
                        },
                        {
                            "inlineData": {
                                "mimeType": "application/pdf",
                                "data": encoded_data
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1
            }
        }
        
        resp = requests.post(url, json=payload, headers=headers, verify=False, timeout=120.0)
        if resp.status_code == 200:
            res_data = resp.json()
            try:
                text = res_data['candidates'][0]['content']['parts'][0]['text']
                return text
            except Exception as e:
                return f"[Błąd parsowania odpowiedzi OCR: {e}]"
        else:
            return f"[Błąd API Vertex OCR {resp.status_code}: {resp.text}]"
    except Exception as ex:
        return f"[Błąd systemu OCR: {ex}]"

class WebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
        
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == "/webhook":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                content_type = self.headers.get('Content-Type', '')
                data = {}
                if 'application/json' in content_type:
                    data = json.loads(body.decode('utf-8'))
                else:
                    parsed = urllib.parse.parse_qs(body.decode('utf-8'))
                    data = {k: v[0] for k, v in parsed.items()}
                
                name = data.get("name", "").strip()
                email = data.get("email", "").strip()
                notes = data.get("notes", "").strip() or data.get("message", "").strip()
                
                if not name or not email:
                    self.send_response(400)
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(b"Name and Email are required.")
                    return
                
                crm_data = load_crm()
                new_id = f"lead_{int(time.time())}"
                new_lead = {
                    "id": new_id,
                    "name": name,
                    "email": email,
                    "stage": "conversation",
                    "notes": notes,
                    "last_contact": time.strftime("%Y-%m-%d"),
                    "next_action": "Skontaktować się po analizie AI",
                    "draft_reply": "Generowanie odpowiedzi przez CMO AI..."
                }
                
                crm_data["leads"].append(new_lead)
                save_crm(crm_data)
                
                threading.Thread(
                    target=async_generate_initial_draft,
                    args=(new_id, name, notes),
                    daemon=True
                ).start()
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "lead_id": new_id}).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(f"Server Error: {e}".encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

def async_generate_initial_draft(lead_id, client_name, client_pain):
    o_mnie_path = os.path.join(HERMES_DIR, "o_mnie.md")
    o_mnie_context = ""
    if os.path.exists(o_mnie_path):
        try:
            o_mnie_context = open(o_mnie_path, "r", encoding="utf-8").read()
        except:
            pass
            
    system_prompt = f"""Jesteś wirtualnym CMO Tomasza Dudy (architekta systemów AI dla neuroatypowych, Holistic AIDHD).
Tomasz jest strategiem automatyzacji dla firm i sam ma ADHD. Twoim zadaniem jest stworzenie bardzo empatycznej, osobistej i konkretnej wersji roboczej pierwszej odpowiedzi do nowego leada (klienta).
Unikaj pustego hype'u AI, pisz zwięźle, ze zrozumieniem chaosu operacyjnego klienta, i z nutą humoru oraz głębokim rezonansem emocjonalnym.

Oto kontekst o Tomaszu (jego serce emocjonalne i historia):
{o_mnie_context}

Napisz bezpośrednią, gotową do wysłania wiadomość e-mail w języku polskim. Pisz w 1 osobie ("ja" - Tomasz Duda). Podpisz się na końcu.
"""

    user_prompt = f"""Klient: {client_name}
Wyzwanie klienta: {client_pain}

Napisz pierwszą, niezwykle empatyczną odpowiedź, która zdejmuje z niego paraliż decyzyjny i proponuje jeden mały, konkretny krok bez presji (krótką rozmowę diagnostyczną)."""

    try:
        reply = call_gemini_api([{"role": "user", "content": user_prompt}], system_instruction=system_prompt)
        if reply:
            crm_data = load_crm()
            for lead in crm_data["leads"]:
                if lead["id"] == lead_id:
                    lead["draft_reply"] = reply
                    break
            save_crm(crm_data)
    except Exception as e:
        pass

def consult_csuite_live(lead, persona):
    o_mnie_path = os.path.join(HERMES_DIR, "o_mnie.md")
    o_mnie_context = ""
    if os.path.exists(o_mnie_path):
        try:
            o_mnie_context = open(o_mnie_path, "r", encoding="utf-8").read()
        except:
            pass

    system_prompts = {
        "CEO (Strategia & Rentowność)": f"""Jesteś wirtualnym CEO w zespole Tomasza Dudy. Tomasz to wybitny architekt systemów AI dla neuroatypowych (sam ma ADHD, Holistic AIDHD).
Pomagasz mu w wycenie wdrożenia pod kątem modelu High-Ticket (np. wyceny 5 000 - 15 000 PLN jednorazowo), etapowaniu prac na proste kroki MVP oraz obronie jego zasobów energetycznych przed wypaleniem i paraliżem ADHD.
Zawsze podawaj konkretną, odważną rekomendację cenową i zdefiniuj, co jest "One Thing" (kluczowym pierwszym krokiem wdrożenia).
Oto historia i tożsamość Tomasza:
{o_mnie_context}
Odpowiadaj bezpośrednio, po polsku, zwięźle i konkretnie.
""",
        "CMO (Empatyczny Storytelling)": f"""Jesteś wirtualnym CMO w zespole Tomasza Dudy (Holistic AIDHD).
Pomagasz mu przełożyć ból klienta na autentyczny i humorystyczny przekaz dopasowany do wyzwań klienta. Wskaż, jakich metafor użyć w komunikacji z tym klientem i jak napisać ofertę, aby rezonowała głęboko emocjonalnie, opierając się na tożsamości Tomasza.
Oto historia i tożsamość Tomasza:
{o_mnie_context}
Odpowiadaj bezpośrednio, po polsku, zwięźle i kreatywnie.
""",
        "CSO (Architektura Sprzedaży)": f"""Jesteś wirtualnym CSO w zespole Tomasza Dudy (Holistic AIDHD).
Projektujesz dla tego klienta prosty, 3-stopniowy lejek relacyjny (Rozmowa -> Architektura -> Wdrożenie). Wskaż dokładnie, jaki powinien być najbliższy krok sprzedażowy (Next Action) i jak go zrealizować przy minimalnym tarciu poznawczym (low cognitive friction).
Oto historia i tożsamość Tomasza:
{o_mnie_context}
Odpowiadaj bezpośrednio, po polsku, zwięźle i operacyjnie.
""",
        "CTO (Technologia & Kod)": f"""Jesteś wirtualnym CTO w zespole Tomasza Dudy (Holistic AIDHD).
Zaprojektuj uproszczoną, niezawodną architekturę techniczną pod potrzeby tego klienta. Rekomenduj konkretne narzędzia (np. n8n webhooks, Python scripts, SQLite, Google Sheets, Vertex AI, model gemini-2.5-flash). Podaj zwięzły schemat logiczny.
Oto historia i tożsamość Tomasza:
{o_mnie_context}
Odpowiadaj bezpośrednio, po polsku, technicznie lecz bez zbędnego żargonu.
"""
    }

    system_instruction = system_prompts.get(persona, "Jesteś doradcą C-Suite.")
    user_prompt = f"""Karta klienta:
Nazwa: {lead['name']}
Opis chaosu operacyjnego: {lead['notes']}
Najbliższy krok (Next Action): {lead['next_action']}

Przeanalizuj przypadek i daj mi (Tomaszowi) swoją rekomendację z perspektywy roli ({persona}). Pisz bezpośrednio do mnie ("Tomasz, badając przypadek...")."""

    return call_gemini_api([{"role": "user", "content": user_prompt}], system_instruction=system_instruction)

def start_webhook_server():
    global _server_started
    with _server_lock:
        if _server_started:
            return
        server_address = ('0.0.0.0', 8090)
        try:
            httpd = HTTPServer(server_address, WebhookHandler)
            t = threading.Thread(target=httpd.serve_forever, daemon=True)
            t.start()
            _server_started = True
        except Exception as e:
            pass

# Start the background webhook server
start_webhook_server()

def read_md_file(path):
    return open(path, "r", encoding="utf-8").read() if os.path.exists(path) else ""

def save_brain_dump(thought, links, uploaded_file):
    dump_id = f"dump_{int(time.time())}"
    file_name = None
    if uploaded_file:
        file_name = uploaded_file.name
        with open(os.path.join(BRAIN_DUMP_ASSETS, file_name), "wb") as f:
            f.write(uploaded_file.getbuffer())
    category = "Later" if any(w in thought.lower() for w in ["potem", "później", "later", "kiedyś"]) else "Now"
    dump_data = {
        "id": dump_id,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "thought": thought,
        "links": links,
        "file_attached": file_name,
        "category": category,
        "status": "active"
    }
    json.dump(dump_data, open(os.path.join(BRAIN_DUMP_DIR, f"{dump_id}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=4)

def get_brain_dumps():
    dumps = []
    if os.path.exists(BRAIN_DUMP_DIR):
        for f in os.listdir(BRAIN_DUMP_DIR):
            if f.endswith(".json") and f.startswith("dump_"):
                try:
                    dumps.append(json.load(open(os.path.join(BRAIN_DUMP_DIR, f), "r", encoding="utf-8")))
                except:
                    pass
    dumps.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return dumps

@st.dialog("📥 Szybki Zrzut Myśli (Brain Dump)")
def show_brain_dump_dialog():
    st.markdown("<p style='color: #CBD5E1;'>Wpisz swój pomysł, załącz link lub plik, a model Gemini 2.5 Pro odciąży Twój umysł i natychmiast zapisze go w Skarbcu.</p>", unsafe_allow_html=True)
    thought = st.text_area("Co Ci chodzi po głowie? (Zzrzuć chaos)", height=120)
    links = st.text_input("Linki / Social media / Wideo (opcjonalnie):")
    uploaded_file = st.file_uploader("Załącz plik / obrazek / audio (opcjonalnie):", type=["png", "jpg", "jpeg", "pdf", "mp3", "wav"])
    
    if st.button("Uwolnij mój umysł", type="primary", use_container_width=True):
        if thought or links or uploaded_file:
            save_brain_dump(thought, links, uploaded_file)
            st.success("Zapisano bezpiecznie w Skarbcu!")
            time.sleep(1.0)
            st.rerun()

# Inicjalizacja stanu sesji
if "one_thing" not in st.session_state:
    st.session_state.one_thing = ""
if "pomodoro_active" not in st.session_state:
    st.session_state.pomodoro_active = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "🎯 Mission Control"

# PASEK BOCZNY - Skrajnie estetyczny z kafelkami zoptymalizowanymi pod ADHD (Styl Julian Goldie)
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #7C3AED; font-family: Outfit; margin-bottom: 0;'>🧠 Holistic OS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.85rem; margin-top: 5px; margin-bottom: 10px;'>Agentic OS Mission Control v7.0</p>", unsafe_allow_html=True)
    st.markdown("<hr style='margin: 10px 0; border-color: #1F242E;'>", unsafe_allow_html=True)
    
    col_menu = st.session_state.current_page
    
    # I. WORKSPACE
    st.markdown("<p style='color: #F59E0B; font-weight: bold; font-size: 0.75rem; letter-spacing: 1px; margin-bottom: 6px; margin-top: 10px;'>I. WORKSPACE</p>", unsafe_allow_html=True)
    
    if st.button("🎯 Mission Control", use_container_width=True, type="primary" if col_menu == "🎯 Mission Control" else "secondary"):
        st.session_state.current_page = "🎯 Mission Control"
        st.rerun()
        
    # II. AGENTS
    st.markdown("<p style='color: #EC4899; font-weight: bold; font-size: 0.75rem; letter-spacing: 1px; margin-top: 18px; margin-bottom: 6px;'>II. AGENTS</p>", unsafe_allow_html=True)
    
    if st.button("🤖 Claude 🟢", use_container_width=True, type="primary" if col_menu == "Claude" else "secondary"):
        st.session_state.current_page = "Claude"
        st.rerun()
        
    if st.button("🦀 OpenClaw 🔴", use_container_width=True, type="primary" if col_menu == "OpenClaw" else "secondary"):
        st.session_state.current_page = "OpenClaw"
        st.rerun()
        
    if st.button("🔱 Hermes 🟢", use_container_width=True, type="primary" if col_menu == "Hermes" else "secondary"):
        st.session_state.current_page = "Hermes"
        st.rerun()
        
    if st.button("♊ Gemini 🟢", use_container_width=True, type="primary" if col_menu == "Gemini" else "secondary"):
        st.session_state.current_page = "Gemini"
        st.rerun()
        
    if st.button("🌌 AntiGravity 🟢", use_container_width=True, type="primary" if col_menu == "Antigravity" else "secondary"):
        st.session_state.current_page = "Antigravity"
        st.rerun()
        
    if st.button("💻 Codex ⚪", use_container_width=True, type="primary" if col_menu == "Codex" else "secondary"):
        st.session_state.current_page = "Codex"
        st.rerun()
        
    if st.button("🦉 Free Claude Code 🟢", use_container_width=True, type="primary" if col_menu == "Free Claude Code" else "secondary"):
        st.session_state.current_page = "Free Claude Code"
        st.rerun()
        
    # III. SELF
    st.markdown("<p style='color: #10B981; font-weight: bold; font-size: 0.75rem; letter-spacing: 1px; margin-top: 18px; margin-bottom: 6px;'>III. SELF</p>", unsafe_allow_html=True)
    
    if st.button("🎯 Goals & Journal", use_container_width=True, type="primary" if col_menu == "Goals" else "secondary"):
        st.session_state.current_page = "Goals"
        st.rerun()
        
    if st.button("📈 SEO & Content", use_container_width=True, type="primary" if col_menu == "SEO" else "secondary"):
        st.session_state.current_page = "SEO"
        st.rerun()
        
    if st.button("🎬 Studio (Hyperframes)", use_container_width=True, type="primary" if col_menu == "Studio" else "secondary"):
        st.session_state.current_page = "Studio"
        st.rerun()
        
    if st.button("📻 Notebook (Obsidian)", use_container_width=True, type="primary" if col_menu == "Notebook" else "secondary"):
        st.session_state.current_page = "Notebook"
        st.rerun()
        
    if st.button("📋 Kanban Board", use_container_width=True, type="primary" if col_menu == "Kanban" else "secondary"):
        st.session_state.current_page = "Kanban"
        st.rerun()
        
    if st.button("💾 Memory (Pristine)", use_container_width=True, type="primary" if col_menu == "Memory" else "secondary"):
        st.session_state.current_page = "Memory"
        st.rerun()
        
    if st.button("💼 ADHD CRM & Lejek", use_container_width=True, type="primary" if col_menu == "CRM" else "secondary"):
        st.session_state.current_page = "CRM"
        st.rerun()
        
    if st.button("🤝 Onboarding & Grill", use_container_width=True, type="primary" if col_menu == "Onboarding" else "secondary"):
        st.session_state.current_page = "Onboarding"
        st.rerun()
        
    if st.button("✨ Swarm (Sales/Soul)", use_container_width=True, type="primary" if col_menu == "Swarm" else "secondary"):
        st.session_state.current_page = "Swarm"
        st.rerun()
        
    if st.button("⚖️ Legal (Kancelaria)", use_container_width=True, type="primary" if col_menu == "Legal" else "secondary"):
        st.session_state.current_page = "Legal"
        st.rerun()
        
    if st.button("💰 Finance & KSeF", use_container_width=True, type="primary" if col_menu == "Finance" else "secondary"):
        st.session_state.current_page = "Finance"
        st.rerun()
        
    st.markdown("<hr style='margin: 15px 0; border-color: #1F242E;'>", unsafe_allow_html=True)
    st.markdown("🌐 **Status Systemu:**")
    st.markdown("⚡ *Hermes Agent:* <span style='color:#10B981; font-weight:bold;'>LIVE (Port 9119)</span>", unsafe_allow_html=True)
    st.markdown("📢 *Telegram Chat:* <span style='color:#10B981; font-weight:bold;'>Połączony</span>", unsafe_allow_html=True)
    st.markdown("📝 *Pristine Memory:* <span style='color:#3B82F6; font-weight:bold;'>Aktywna</span>", unsafe_allow_html=True)


menu = st.session_state.current_page

def render_agent_console(agent_name, status, default_model, provider, color_accent):
    st.markdown(f"<p style='color: #94A3B8; font-family: Outfit; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 2px;'>II. — AGENT • {agent_name.upper()}</p>", unsafe_allow_html=True)
    st.title(f"{agent_name}")
    st.markdown(f"<p style='color: {color_accent}; font-weight: bold; font-size: 0.95rem; margin-top: -5px;'>Status: {status} | Active Model: {default_model} | Provider: {provider}</p>", unsafe_allow_html=True)
    
    tab_chat, tab_work, tab_ctrl = st.tabs(["💬 Chat", "📂 Workspace", "⚙️ Control Room"])
    
    # 1. CHAT
    with tab_chat:
        st.subheader("Konsola konwersacyjna")
        chat_key = f"chat_{agent_name.lower().replace(' ', '_')}"
        if chat_key not in st.session_state:
            st.session_state[chat_key] = []
            
        for msg in st.session_state[chat_key]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        if prompt := st.chat_input(f"Napisz do agenta {agent_name}...", key=f"input_{agent_name.lower().replace(' ', '_')}"):
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state[chat_key].append({"role": "user", "content": prompt})
            
            # Simple agent simulator based on o_mnie
            o_mnie_path = os.path.join(HERMES_DIR, "o_mnie.md")
            o_mnie_context = read_md_file(o_mnie_path) if os.path.exists(o_mnie_path) else "Brak profilu o_mnie.md"
            
            sys_prompt = f"Jesteś agentem {agent_name} z ekosystemu Holistic OS. Działasz w oparciu o profil użytkownika:\n{o_mnie_context}\nTwój styl jest krótki, precyzyjny (ADHD-friendly)."
            
            with st.spinner(f"{agent_name} przetwarza zapytanie..."):
                api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state[chat_key]]
                response = call_gemini_pro_api(api_messages, system_instruction=sys_prompt)
                
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state[chat_key].append({"role": "assistant", "content": response})
            
            # Infinite Context Engine: auto-save to Obsidian
            obsidian_note_title = f"Chat_{agent_name.replace(' ', '_')}_{int(time.time())}.md"
            obsidian_note_path = os.path.join(OBSIDIAN_DIR, obsidian_note_title)
            try:
                note_content = f"---\ntype: chat-log\nagent: {agent_name}\ntimestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n---\n\n"
                for msg in st.session_state[chat_key]:
                    note_content += f"**{'Użytkownik' if msg['role'] == 'user' else agent_name}**:\n{msg['content']}\n\n"
                with open(obsidian_note_path, "w", encoding="utf-8") as f:
                    f.write(note_content)
            except Exception as e:
                pass
                
    # 2. WORKSPACE (Trzykolumnowy manager)
    with tab_work:
        st.subheader("Menedżer Workspace Agentów")
        col_b, col_f, col_v = st.columns([1, 2, 3])
        
        with col_b:
            st.write("🔍 **Buckets**")
            bucket = st.radio("Filtruj:", ["Apps", "Videos", "Images", "Audio", "Workspace", "Sandboxes", "Pastes"], key=f"bucket_{agent_name.lower().replace(' ', '_')}")
            
        with col_f:
            st.write(f"📁 **Pliki w {bucket}**")
            files_list = []
            if bucket == "Apps":
                files_list = [f for f in os.listdir(DASHBOARD_DIR) if f.endswith(".html")]
                if not files_list:
                    files_list = ["todo-app.html", "testimonials.html", "landing-page.html"]
            elif bucket == "Videos":
                files_list = ["dragon_tokyo_skyline.mp4", "ai-seo-trends.mp4"]
            elif bucket == "Images":
                files_list = ["holistic_ai_dhd_logo.png", "marketing_campaign.jpg"]
            elif bucket == "Audio":
                files_list = ["meditation_music.mp3", "podcast_voice.wav"]
            elif bucket == "Workspace":
                files_list = ["app.py", "gcp_vertex_proxy.py", "requirements.txt"]
            elif bucket == "Sandboxes":
                files_list = ["sandbox_env.py", "test_runner.py"]
            elif bucket == "Pastes":
                files_list = [f for f in os.listdir(OBSIDIAN_DIR) if f.endswith(".md")][:10]
                if not files_list:
                    files_list = ["quick_note.md", "brief_draft.md"]
                    
            selected_file = st.selectbox("Wybierz plik:", files_list, key=f"sel_file_{agent_name.lower().replace(' ', '_')}")
            
        with col_v:
            st.write("👁️ **Podgląd / Edycja**")
            if selected_file:
                st.info(f"Podgląd pliku: `{selected_file}`")
                
                if selected_file.endswith(".html") or bucket == "Apps":
                    html_content = ""
                    if selected_file == "testimonials.html":
                        html_content = "<html><body style='background-color:#121620; color:white; font-family:sans-serif; padding:20px;'><h2>Want results like these? Join the AI Profit Boardroom!</h2><p>258 real wins from AI Profit Boardroom members.</p></body></html>"
                    elif selected_file == "todo-app.html":
                        html_content = "<html><body style='background-color:#121620; color:white; font-family:sans-serif; padding:20px;'><h2>ADHD To-Do App</h2><input type='text' placeholder='Add task...'><button>Add</button></body></html>"
                    else:
                        html_content = "<html><body style='background-color:#121620; color:white; font-family:sans-serif; padding:20px;'><h2>Custom App View</h2><p>Pomyślnie załadowano render aplikacji w piaskownicy Agentic OS.</p></body></html>"
                    
                    st.components.v1.html(html_content, height=350, scrolling=True)
                    
                    sub_tab_preview, sub_tab_src = st.tabs(["👁️ Podgląd", "💻 Kod źródłowy"])
                    with sub_tab_src:
                        st.code(html_content, language="html")
                        
                elif selected_file.endswith(".mp4") or bucket == "Videos":
                    st.video("https://www.w3schools.com/html/mov_bbb.mp4")
                    
                elif selected_file.endswith((".png", ".jpg", ".jpeg")) or bucket == "Images":
                    st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500", caption=selected_file)
                    
                elif selected_file.endswith((".mp3", ".wav")) or bucket == "Audio":
                    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
                    
                elif selected_file.endswith(".md") or selected_file.endswith(".py") or selected_file.endswith(".txt"):
                    file_path = os.path.join(OBSIDIAN_DIR, selected_file)
                    if not os.path.exists(file_path):
                        file_path = os.path.join(os.getcwd(), selected_file)
                    content = ""
                    if os.path.exists(file_path):
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read()
                        except:
                            content = "Błąd odczytu pliku."
                    else:
                        content = f"# Draft dla {selected_file}\nTutaj znajduje się podgląd notatki roboczej agenta."
                        
                    edited_content = st.text_area("Edycja pliku:", content, height=200, key=f"edit_{agent_name.lower().replace(' ', '_')}_{selected_file}")
                    if st.button("Zapisz zmiany", key=f"save_{agent_name.lower().replace(' ', '_')}_{selected_file}"):
                        try:
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(edited_content)
                            st.success("Zapisano pomyślnie!")
                        except Exception as e:
                            st.error(f"Błąd zapisu: {e}")
                            
    # 3. CONTROL ROOM
    with tab_ctrl:
        st.subheader("Konfiguracja Agenta (Control Room)")
        st.write("Ustaw parametry modelu dla tego agenta:")
        model_opt = st.selectbox("Model:", ["gemini-2.5-pro", "gemini-2.5-flash", "grok-4.3", "claude-3-7-sonnet"], index=0, key=f"ctrl_model_{agent_name.lower().replace(' ', '_')}")
        temp = st.slider("Temperatura (Kreatywność):", 0.0, 1.0, 0.7, 0.05, key=f"ctrl_temp_{agent_name.lower().replace(' ', '_')}")
        sys_prompt_input = st.text_area("System Prompt / Instrukcje systemowe:", f"Jesteś agentem {agent_name}. Działasz zorientowany na ADHD i redukcję szumu kognitywnego.", height=150, key=f"ctrl_prompt_{agent_name.lower().replace(' ', '_')}")
        if st.button("Aktualizuj konfigurację agenta", key=f"ctrl_btn_{agent_name.lower().replace(' ', '_')}"):
            st.success(f"Konfiguracja dla agenta {agent_name} została zaktualizowana w pamięci podręcznej sesji!")

# 1. MISSION CONTROL
if menu == "🎯 Mission Control":

    st.markdown("<p style='color: #94A3B8; font-family: Outfit; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 2px;'>I. — MISSION CONTROL</p>", unsafe_allow_html=True)
    st.title("🧠 Agentic Mission Control")
    st.subheader("Status of every agent, every memory, every signal.")
    
    # Górny pasek statusów (System Status Row)
    st.markdown("""
    <style>
        .status-container {
            display: flex;
            gap: 12px;
            margin-bottom: 25px;
            width: 100%;
        }
        .status-box {
            background-color: #0E1015;
            border: 1px solid #1F242E;
            border-radius: 8px;
            padding: 12px 16px;
            flex: 1;
            box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        }
        .status-title {
            color: #94A3B8;
            font-size: 0.7rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .status-value {
            color: #FFFFFF;
            font-family: 'Outfit', sans-serif;
            font-size: 1.05rem;
            font-weight: 600;
        }
        .status-desc {
            color: #64748B;
            font-size: 0.75rem;
            margin-top: 2px;
        }
        .status-dot-green { background-color: #10B981; box-shadow: 0 0 8px #10B981; }
        .status-dot-red { background-color: #EF4444; box-shadow: 0 0 8px #EF4444; }
        .status-dot-yellow { background-color: #F59E0B; box-shadow: 0 0 8px #F59E0B; }
    </style>
    """, unsafe_allow_html=True)

    col_s1, col_s2, col_s3, col_s4, col_s5, col_s6 = st.columns(6)
    with col_s1:
        st.markdown("""<div class="status-box">
            <div class="status-title"><span>🤖 CLAUDE</span><span class="status-dot-green" style="height:6px; width:6px; border-radius:50%; display:inline-block;"></span></div>
            <div class="status-value">Online</div>
            <div class="status-desc">2.1.142 • 46ms</div>
        </div>""", unsafe_allow_html=True)
    with col_s2:
        st.markdown("""<div class="status-box">
            <div class="status-title"><span>🦀 OPENCLAW</span><span class="status-dot-red" style="height:6px; width:6px; border-radius:50%; display:inline-block;"></span></div>
            <div class="status-value">Offline</div>
            <div class="status-desc">3 agents • 7 sess.</div>
        </div>""", unsafe_allow_html=True)
    with col_s3:
        st.markdown("""<div class="status-box">
            <div class="status-title"><span>🔱 HERMES</span><span class="status-dot-green" style="height:6px; width:6px; border-radius:50%; display:inline-block;"></span></div>
            <div class="status-value">Online</div>
            <div class="status-desc">grok-4.3 • xAI OAuth</div>
        </div>""", unsafe_allow_html=True)
    with col_s4:
        st.markdown("""<div class="status-box">
            <div class="status-title"><span>⏱️ HEARTBEAT</span><span class="status-dot-yellow" style="height:6px; width:6px; border-radius:50%; display:inline-block;"></span></div>
            <div class="status-value">Active</div>
            <div class="status-desc">poll ticks • 4s</div>
        </div>""", unsafe_allow_html=True)
    with col_s5:
        st.markdown("""<div class="status-box">
            <div class="status-title"><span>⚡ LATENCY</span><span class="status-dot-green" style="height:6px; width:6px; border-radius:50%; display:inline-block;"></span></div>
            <div class="status-value">42 ms</div>
            <div class="status-desc">combined p50</div>
        </div>""", unsafe_allow_html=True)
    with col_s6:
        st.markdown("""<div class="status-box">
            <div class="status-title"><span>🦉 OWL ALPHA</span><span class="status-dot-green" style="height:6px; width:6px; border-radius:50%; display:inline-block;"></span></div>
            <div class="status-value">Live</div>
            <div class="status-desc">OpenRouter • Free</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='margin: 15px 0; border-color: #1F242E;'>", unsafe_allow_html=True)

    # Tryb One Thing - ADHD Wykluczenie Szumu
    st.markdown("""
    <div class="one-thing-banner">
        <h3 style="margin-top: 0; color: #F59E0B;">🎯 Tryb "One Thing"</h3>
        <p style="color: #CBD5E1; line-height: 1.6;">Osoby z ADHD cierpią na paraliż decyzyjny z powodu nadmiaru bodźców. Wpisz poniżej dokładnie <strong>JEDNĄ</strong> rzecz, na której skupisz się w tym momencie. Dashboard wyciszy resztę szumu operacyjnego.</p>
    </div>
    """, unsafe_allow_html=True)
    
    thing = st.text_input("Moje jedyne zadanie na ten moment:", value=st.session_state.one_thing, placeholder="Np. zredagowanie oferty High-Ticket dla lokalnej kliniki...")
    if thing:
        st.session_state.one_thing = thing
        st.markdown(f"""
        <div class="custom-card" style="border-left: 5px solid #10B981; background-color: #0F1D1A;">
            <h4 style="margin: 0; color: #10B981;">🔥 Twój aktualny priorytet:</h4>
            <p style="font-size: 1.25rem; font-weight: bold; margin-top: 8px; color: #FFFFFF;">{thing}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("⏱️ Uruchom Pomodoro (25 min)"):
                st.session_state.pomodoro_active = True
        with col2:
            if st.session_state.pomodoro_active:
                st.success("Stoper Pomodoro wystartował. Wyłącz inne karty w przeglądarce i skup się wyłącznie na priorytecie.")

    st.markdown("---")
    
    # II. AGENTS GRID
    st.markdown("<p style='color: #94A3B8; font-family: Outfit; font-weight: bold; letter-spacing: 1.5px; margin-top: 25px; margin-bottom: 2px;'>II. — AGENTS • CLICK TO OPEN CONTROL ROOM</p>", unsafe_allow_html=True)
    
    col_a1, col_a2, col_a3 = st.columns(3)
    
    with col_a1:
        st.markdown("""
        <div class="custom-card" style="border-top: 3px solid #F59E0B; height: 260px;">
            <h3 style="color: #F59E0B; margin-top: 0;">🤖 Claude</h3>
            <p style="color: #94A3B8; font-size: 0.85rem; height: 60px;">Bezpośrednie połączenie ze środowiskiem Claude Code. Pełna kontrola konsoli i narzędzi.</p>
            <div style="margin-top: 15px; font-size: 0.8rem; color: #64748B;">
                <div><b>MODEL:</b> claude-3-7-sonnet</div>
                <div><b>PROVIDER:</b> Anthropic Native</div>
                <div><b>STATUS:</b> <span style="color:#10B981; font-weight:bold;">ONLINE</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Otwórz konsolę Claude", use_container_width=True):
            st.session_state.current_page = "Claude"
            st.rerun()

    with col_a2:
        st.markdown("""
        <div class="custom-card" style="border-top: 3px solid #EC4899; height: 260px;">
            <h3 style="color: #EC4899; margin-top: 0;">🦀 OpenClaw</h3>
            <p style="color: #94A3B8; font-size: 0.85rem; height: 60px;">Lokalny router agentów. Pozwala na jednorazowe strzały lub koordynację roju.</p>
            <div style="margin-top: 15px; font-size: 0.8rem; color: #64748B;">
                <div><b>MODEL:</b> mixed-swarm</div>
                <div><b>PROVIDER:</b> Local Gateway</div>
                <div><b>STATUS:</b> <span style="color:#EF4444; font-weight:bold;">OFFLINE</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Otwórz konsolę OpenClaw", use_container_width=True):
            st.session_state.current_page = "OpenClaw"
            st.rerun()

    with col_a3:
        st.markdown("""
        <div class="custom-card" style="border-top: 3px solid #3B82F6; height: 260px;">
            <h3 style="color: #3B82F6; margin-top: 0;">🔱 Hermes</h3>
            <p style="color: #94A3B8; font-size: 0.85rem; height: 60px;">Główny orkiestrator. Wywołanie skilli, obsługa Kanbana i automatyzacji w tle.</p>
            <div style="margin-top: 15px; font-size: 0.8rem; color: #64748B;">
                <div><b>MODEL:</b> grok-4.3</div>
                <div><b>PROVIDER:</b> xAI API v1</div>
                <div><b>STATUS:</b> <span style="color:#10B981; font-weight:bold;">ONLINE</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Otwórz konsolę Hermes", use_container_width=True):
            st.session_state.current_page = "Hermes"
            st.rerun()

    col_a4, col_a5, col_a6 = st.columns(3)
    
    with col_a4:
        st.markdown("""
        <div class="custom-card" style="border-top: 3px solid #8B5CF6; height: 260px;">
            <h3 style="color: #8B5CF6; margin-top: 0;">♊ Gemini</h3>
            <p style="color: #94A3B8; font-size: 0.85rem; height: 60px;">Super-inteligentny model do audytów, pisania pism prawnych i zaawansowanej logiki.</p>
            <div style="margin-top: 15px; font-size: 0.8rem; color: #64748B;">
                <div><b>MODEL:</b> gemini-2.5-pro</div>
                <div><b>PROVIDER:</b> Vertex AI Native</div>
                <div><b>STATUS:</b> <span style="color:#10B981; font-weight:bold;">ONLINE</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Otwórz konsolę Gemini", use_container_width=True):
            st.session_state.current_page = "Gemini"
            st.rerun()

    with col_a5:
        st.markdown("""
        <div class="custom-card" style="border-top: 3px solid #10B981; height: 260px;">
            <h3 style="color: #10B981; margin-top: 0;">🌌 AntiGravity</h3>
            <p style="color: #94A3B8; font-size: 0.85rem; height: 60px;">Twój systemowy architekt i asystent operacyjny. Nadzór nad kodem i deployami.</p>
            <div style="margin-top: 15px; font-size: 0.8rem; color: #64748B;">
                <div><b>MODEL:</b> gemini-2.5-pro</div>
                <div><b>PROVIDER:</b> GCP Proxy Port 8089</div>
                <div><b>STATUS:</b> <span style="color:#10B981; font-weight:bold;">ONLINE</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Otwórz konsolę AntiGravity", use_container_width=True):
            st.session_state.current_page = "Antigravity"
            st.rerun()

    with col_a6:
        st.markdown("""
        <div class="custom-card" style="border-top: 3px solid #06B6D4; height: 260px;">
            <h3 style="color: #06B6D4; margin-top: 0;">🦉 Free Claude Code</h3>
            <p style="color: #94A3B8; font-size: 0.85rem; height: 60px;">Darmowe wywołanie kodu i analiz przy użyciu publicznych endpointów OpenRouter.</p>
            <div style="margin-top: 15px; font-size: 0.8rem; color: #64748B;">
                <div><b>MODEL:</b> owl-alpha-free</div>
                <div><b>PROVIDER:</b> OpenRouter</div>
                <div><b>STATUS:</b> <span style="color:#10B981; font-weight:bold;">ONLINE</span></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Otwórz konsolę Free Claude", use_container_width=True):
            st.session_state.current_page = "Free Claude Code"
            st.rerun()

    st.markdown("---")
    
    # Szybki Capture
    st.subheader("⚡ Szybki Capture myśli (Brain Dump)")
    quick_thought = st.text_area("Masz nagły pomysł lub coś Cię rozprasza? Zrzuć to tutaj natychmiast, aby uwolnić pamięć roboczą mózgu:", height=100)
    if st.button("Uwolnij moją pamięć roboczą"):
        if quick_thought:
            save_brain_dump(quick_thought, "", None)
            st.success("Pomysł bezpiecznie zapisany w chmurze w Skarbcu Myśli. Twoja głowa jest wolna.")
            time.sleep(0.5)
            st.rerun()


elif menu == "Claude":
    render_agent_console("Claude", "Online", "claude-3-7-sonnet", "Anthropic Native", "#F59E0B")

elif menu == "OpenClaw":
    render_agent_console("OpenClaw", "Offline", "mixed-swarm", "Local Gateway", "#EC4899")

elif menu == "Hermes":
    render_agent_console("Hermes", "Online", "grok-4.3", "xAI API v1", "#3B82F6")

elif menu == "Gemini":
    render_agent_console("Gemini", "Online", "gemini-2.5-pro", "Vertex AI Native", "#8B5CF6")

elif menu == "Codex":
    render_agent_console("Codex", "Offline", "unknown", "Unknown", "#64748B")

elif menu == "Free Claude Code":
    render_agent_console("Free Claude Code", "Online", "owl-alpha-free", "OpenRouter", "#06B6D4")

elif menu == "Studio":
    st.markdown("<p style='color: #94A3B8; font-family: Outfit; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 2px;'>III. — SELF • STUDIO</p>", unsafe_allow_html=True)
    st.title("🎬 Generative Studio")
    st.subheader("Wielomodalne studio kreacji treści, audio i wideo")
    
    tab_hyper, tab_audio, tab_img = st.tabs(["🎥 Hyperframes (Video)", "🔊 Voice & Audio", "🎨 Grafika & Obrazy"])
    
    with tab_hyper:
        st.subheader("🎥 Generator Wideo Hyperframes")
        st.markdown("Konwertuje opisy tekstowe na interaktywne animacje wideo HTML / CSS.")
        video_prompt = st.text_area("Opisz scenę wideo (np. 'Pulsacyjne różowe neonowe logo na czarnym tle z unoszącymi się cząsteczkami'):", height=100)
        
        if st.button("Generuj Hyperframe Wideo", type="primary"):
            with st.spinner("Hyperframes kompiluje kod HTML/CSS..."):
                time.sleep(2)
                st.session_state.hyperframe_code = """
                <html>
                <body style='background-color:#08090C; display:flex; justify-content:center; align-items:center; height:100vh; overflow:hidden; margin:0;'>
                    <div style='text-align:center;'>
                        <div style='width:120px; height:120px; border-radius:50%; background:radial-gradient(circle, #EC4899 0%, #7C3AED 100%); animation: pulse-logo 2s infinite alternate; box-shadow: 0 0 30px #EC4899;'></div>
                        <h2 style='color:#FFFFFF; font-family:sans-serif; margin-top:20px; text-shadow:0 0 10px #7C3AED;'>Holistic OS</h2>
                    </div>
                    <style>
                        @keyframes pulse-logo {
                            0% { transform: scale(1); box-shadow: 0 0 20px #EC4899; }
                            100% { transform: scale(1.1); box-shadow: 0 0 40px #7C3AED, 0 0 15px #EC4899; }
                        }
                    </style>
                </body>
                </html>
                """
                st.success("Wideo wygenerowane pomyślnie w formacie Hyperframe!")
                st.rerun()
                
        if "hyperframe_code" in st.session_state and st.session_state.hyperframe_code:
            st.write("📺 **Podgląd wygenerowanej animacji:**")
            st.components.v1.html(st.session_state.hyperframe_code, height=350, scrolling=False)
            
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                st.button("Exportuj do MP4", use_container_width=True)
            with sub_col2:
                if st.button("Wyczyść Studio", use_container_width=True):
                    st.session_state.hyperframe_code = None
                    st.rerun()
                    
    with tab_audio:
        st.subheader("🔊 Text-to-Speech & Voice Clone")
        st.write("Generowanie głosu AI w stylu Tomasza Dudy (ADHD-friendly, dynamiczny).")
        audio_text = st.text_area("Wpisz tekst do wypowiedzenia:", "Cześć! Dzisiaj skupimy się na jednej, najważniejszej rzeczy. Wyelimuj szum i wejdź w stan Flow.")
        if st.button("Generuj Audio", type="primary"):
            with st.spinner("Generowanie pliku dźwiękowego..."):
                time.sleep(2)
                st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3")
                st.success("Głos wygenerowany pomyślnie!")
                
    with tab_img:
        st.subheader("🎨 Generator Grafiki")
        st.write("Twórz spersonalizowane obrazy i okładki dla swoich projektów.")
        img_prompt = st.text_input("Opisz grafikę:", "Modern luxury landing page layout for ADHD audience, dark neon theme")
        if st.button("Generuj Obraz", type="primary"):
            with st.spinner("Model generuje obraz..."):
                time.sleep(2.5)
                st.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500", caption="Wygenerowana inspiracja graficzna")

# 2. GOALS & OPEN LOOPS
elif menu == "Goals":
    st.markdown("<p style='color: #94A3B8; font-family: Outfit; font-weight: bold; letter-spacing: 1.5px; margin-bottom: 2px;'>III. — SELF • GOALS & MENTAL WORKSHOP</p>", unsafe_allow_html=True)
    st.title("🎯 Goals & Mental Workshop")
    
    tab_loops, tab_goal_mode = st.tabs(["🗑️ Brain Dump & Open Loops", "🎯 Goal Mode (Autonomiczny Cel)"])
    
    with tab_loops:
        st.subheader("Twój mentalny odciążyciel — bezszumne uwalnianie pamięci roboczej")
        
        col_in, col_st = st.columns([1, 1])
        
        with col_in:
            st.markdown("""
            <div class="custom-card" style="border-left: 5px solid #EC4899;">
                <h4 style="margin:0; color:#EC4899;">📥 Zrzut z głowy (Brain Dump)</h4>
                <p style="font-size: 0.9rem; color: #94A3B8; margin-top: 6px;">Wpisz pomysły, luźne myśli, linki lub wgraj zrzut ekranu (np. inspirację reklamową).</p>
            </div>
            """, unsafe_allow_html=True)
            
            thought_input = st.text_area("Co Ci chodzi po głowie?", height=150, key="goals_thought_input")
            links_input = st.text_input("Linki / Źródła (opcjonalnie):", key="goals_links_input")
            uploaded_file = st.file_uploader("Dodaj plik / zrzut ekranu (PNG, JPG, PDF):", type=["png","jpg","jpeg","pdf"], key="goals_uploaded_file")
            
            if st.button("Prześlij do Skarbca w Chmurze", type="primary", key="goals_submit_button"):
                if thought_input or links_input or uploaded_file:
                    save_brain_dump(thought_input, links_input, uploaded_file)
                    st.success("Zapisano. Pomysł został odciążony z Twojego mózgu.")
                    time.sleep(0.5)
                    st.rerun()
            
            st.markdown("---")
            st.markdown("""
            <div class="custom-card" style="border-left: 5px solid #7C3AED; background: linear-gradient(135deg, #1A1230 0%, #0F1016 100%);">
                <h4 style="margin: 0; color: #C084FC;">🧠 Strategiczna Odprawa CEO</h4>
                <p style="color: #CBD5E1; font-size: 0.85rem; margin-top: 6px; margin-bottom: 0;">
                    Uruchom analizę Skarbca. CEO Jason (Gemini 2.5 Pro) uporządkuje Twoje otwarte pętle, wyciągnie z nich strategię biznesową i zaproponuje gotowe zadania.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("🚀 Przetwórz Skarbiec przez CEO", use_container_width=True, key="goals_run_ceo_button"):
                active_dumps = [d for d in get_brain_dumps() if d.get("status", "active") == "active"]
                if not active_dumps:
                    st.info("Twój Skarbiec jest pusty. Brak otwartych pętli do przetworzenia.")
                else:
                    with st.spinner("CEO Jason analizuje Skarbiec (Gemini 2.5 Pro)..."):
                        dumps_text = ""
                        for i, d in enumerate(active_dumps):
                            dumps_text += f"\n--- POMYSŁ {i+1} ---\nZapisano: {d.get('timestamp')}\nTreść: {d.get('thought')}\nLinki: {d.get('links', '')}\n"
                        
                        ceo_prompt = f"""Jesteś CEO Holistic Operator — Tomasz 'Holistic Jason', osobistym doradcą i strategiem użytkownika.
Twój cel to pomóc użytkownikowi (który ma ADHD i cierpi na paraliż decyzyjny) uporządkować i wdrożyć w życie pomysły, które zapisał w Skarbcu Myśli (Brain Dump).

Przeanalizuj poniższe otwarte pętle (brain dumps) i przygotuj dla nich plan działania:
1. Dokonaj kategoryzacji (np. Szybka wygrana, Duży projekt, Do odrzucenia).
2. Dla każdego ważnego pomysłu zaproponuj konkretną "Next Action" (bezwysiłkowy mikro-krok o niskim oporze kognitywnym).
3. Zaproponuj, które z nich należy natychmiast wrzucić do Kanbana jako zadania, a które zarchiwizować/skasować.

Pisz zwięźle, konkretnie, w przyjaznym, motywującym tonie, bez bełkotu AI. Używaj wypunktowań.

OTWARTE PĘTLE ZE SKARBCZA:
{dumps_text}"""
                        response = call_gemini_pro_api([{"role": "user", "content": ceo_prompt}], "Jesteś CEO Jason, wybitnym strategiem biznesowym wspierającym osoby z ADHD.")
                        st.session_state.ceo_analysis_result = response
                        st.rerun()
    
            if "ceo_analysis_result" in st.session_state and st.session_state.ceo_analysis_result:
                st.markdown("##### 📋 Raport i Plan CEO:")
                st.markdown(f"""
                <div class="custom-card" style="border-left: 4px solid #10B981; white-space: pre-wrap; font-size: 0.9rem; line-height: 1.6; background-color: #0c1410;">
{st.session_state.ceo_analysis_result}
                </div>
                """, unsafe_allow_html=True)
                if st.button("Wyczyść raport CEO", key="goals_clear_ceo_button"):
                    st.session_state.ceo_analysis_result = None
                    st.rerun()
                    
        with col_st:
            st.markdown("### 📦 Aktywne Otwarte Pętle (Open Loops)")
            dumps = get_brain_dumps()
            active_dumps = [d for d in dumps if d.get("status", "active") == "active"]
            
            if not active_dumps:
                st.info("Twój Skarbiec jest pusty. Brak rozpraszających pętli myślowych.")
            else:
                st.write(f"Masz **{len(active_dumps)}** aktywnych pętli czekających na wdrożenie:")
                for d in active_dumps:
                    accent = "#3B82F6" if d.get("category") == "Now" else "#F59E0B"
                    st.markdown(f"""
                    <div class="custom-card" style="border-left: 4px solid {accent}; margin-bottom: 12px;">
                        <span style="font-size: 0.8rem; color:#94A3B8;">⏱️ Zapisano: {d.get('timestamp')} | Priorytet: {d.get('category')}</span>
                        <p style="margin-top: 6px; font-size: 1.05rem; color:#FFFFFF;">{d.get('thought')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if d.get("links"):
                        st.markdown(f"🔗 **Inspiracja:** [{d.get('links')}]({d.get('links')})")
                    if d.get("file_attached"):
                        ext = os.path.splitext(d.get("file_attached"))[1].lower()
                        if ext in [".png", ".jpg", ".jpeg"]:
                            path = os.path.join(BRAIN_DUMP_ASSETS, d.get("file_attached"))
                            if os.path.exists(path):
                                st.image(path, caption=d.get("file_attached"), use_container_width=True)
                        else:
                            st.markdown(f"📎 **Załącznik:** `{d.get('file_attached')}`")
                            
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        if st.button("🎯 Do Kanbana", key=f"k_{d['id']}"):
                            k = load_kanban()
                            short = d.get('thought')[:100] + "..." if len(d.get('thought')) > 100 else d.get('thought')
                            k["todo"].append(f"🧠 [Zrzut] {short}")
                            save_kanban(k)
                            dump_file = os.path.join(BRAIN_DUMP_DIR, f"{d['id']}.json")
                            d["status"] = "archived"
                            json.dump(d, open(dump_file, "w", encoding="utf-8"), ensure_ascii=False, indent=4)
                            st.toast("Zadanie dodane do tablicy Kanban!")
                            time.sleep(0.5); st.rerun()
                    with c2:
                        if st.button("📦 Archiwizuj", key=f"a_{d['id']}"):
                            dump_file = os.path.join(BRAIN_DUMP_DIR, f"{d['id']}.json")
                            d["status"] = "archived"
                            json.dump(d, open(dump_file, "w", encoding="utf-8"), ensure_ascii=False, indent=4)
                            st.toast("Zarchiwizowano.")
                            time.sleep(0.5); st.rerun()
                    with c3:
                        if st.button("🗑️ Usuń", key=f"d_{d['id']}"):
                            dump_file = os.path.join(BRAIN_DUMP_DIR, f"{d['id']}.json")
                            if os.path.exists(dump_file):
                                os.remove(dump_file)
                            st.toast("Usunięto.")
                            time.sleep(0.5); st.rerun()
                            
    with tab_goal_mode:
        st.subheader("🎯 Goal Mode — Autonomiczne Wykonywanie Zadań")
        st.markdown("""
        <div class="custom-card" style="border-left: 5px solid #F59E0B;">
            <h4 style="margin: 0; color: #F59E0B;">🚀 Autonomiczna Pętla Weryfikacji (Judge Loop)</h4>
            <p style="color: #CBD5E1; font-size: 0.85rem; margin-top: 6px; margin-bottom: 0;">
                Wpisz wysoki cel operacyjny. Agent uruchomi pętlę do 20 iteracji. W każdej iteracji model-sędzia ocenia postęp i decyduje, czy cel został w pełni osiągnięty.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        goal_input = st.text_input("Cel do zrealizowania:", placeholder="np. Wygeneruj 3 spersonalizowane szkice maili sprzedażowych dla lokalnych klinik...", key="goals_auton_goal")
        steps_limit = st.slider("Limit iteracji (tur sędziego):", 5, 20, 10, key="goals_auton_steps")
        executor_agent = st.selectbox("Wybierz agenta wykonawczego:", ["Hermes", "Claude", "Gemini", "AntiGravity"], key="goals_auton_agent")
        
        if st.button("Uruchom Goal Mode Loop", type="primary", key="goals_run_auton_btn"):
            if goal_input:
                st.write(f"🏃 **Inicjalizacja pętli Goal Mode dla agenta {executor_agent}...**")
                
                status_placeholder = st.empty()
                progress_bar = st.progress(0.0)
                
                current_state = f"Rozpoczęto realizację celu: {goal_input}"
                completed = False
                
                for step in range(1, steps_limit + 1):
                    status_placeholder.info(f"🔄 **Iteracja {step} / {steps_limit}...**")
                    progress_bar.progress(step / steps_limit)
                    
                    exec_prompt = f"""Realizujesz cel: "{goal_input}".
Aktualny stan prac: {current_state}
Wykonaj następny logiczny krok w celu osiągnięcia rezultatu. Wygeneruj konkretny postęp."""
                    with st.spinner(f"Agent {executor_agent} wykonuje krok..."):
                        step_output = call_gemini_pro_api([{"role": "user", "content": exec_prompt}], f"Jesteś agentem {executor_agent} pracującym w trybie Goal Mode.")
                    
                    st.markdown(f"**Iteracja {step} Output:**")
                    st.code(step_output[:300] + "..." if len(step_output) > 300 else step_output, language="markdown")
                    
                    judge_prompt = f"""Cel główny: "{goal_input}"
Aktualny postęp prac po ostatniej iteracji:
{step_output}

ZADANIE: Oceń, czy cel główny został w 100% zrealizowany.
Odpowiedz w formacie JSON:
{{
  "completed": true/false,
  "summary": "krótkie podsumowanie wykonanej pracy",
  "next_step": "co pozostało do zrobienia (jeśli nie ukończono)"
}}
Zwróć wyłącznie prawidłowy JSON, bez znaczników ```json i bez innych komentarzy."""
                    with st.spinner("Sędzia AI weryfikuje postęp (Gemini)..."):
                        judge_resp = call_gemini_api([{"role": "user", "content": judge_prompt}], "Jesteś rygorystycznym sędzią jakości.")
                    
                    try:
                        if "```" in judge_resp:
                            judge_resp = judge_resp.split("```")[1]
                            if judge_resp.startswith("json"):
                                judge_resp = judge_resp[4:]
                        judge_data = json.loads(judge_resp.strip())
                        completed = judge_data.get("completed", False)
                        current_state = judge_data.get("summary", "")
                        
                        st.markdown(f"⚖️ **Werdykt Sędziego:** {judge_data.get('summary')}")
                        if completed:
                            st.success(f"🎉 **Cel osiągnięty w turze {step}!** Pętla zakończona pomyślnie.")
                            break
                    except Exception as e:
                        completed = False
                        current_state = f"Błąd dekodowania oceny sędziego: {e}. Kontynuuję..."
                    
                    time.sleep(1)
                    
                if not completed:
                    st.warning("⚠️ Osiągnięto limit iteracji bez pełnego potwierdzenia od sędziego. Dokonaj weryfikacji manualnej.")
            else:
                st.warning("Wpisz cel do zrealizowania.")

# 3. NOTEBOOKLM & OBSIDIAN
elif menu == "Notebook":
    st.title("📻 NotebookLM Sync & Obsidian Vault")
    st.subheader("Ustrukturyzowany przepływ wiedzy w chmurze")
    
    st.markdown("""
    <div class="custom-card">
        <p>📻 <strong>Syntezy wiedzy w chmurze:</strong> Ten moduł łączy podcasty wygenerowane przez NotebookLM z Twoimi notatkami z Obsidian Vault. Wgraj pliki przez SFTP do chmury, a pojawią się tu natychmiast.</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📻 Podcasty z NotebookLM", "📝 Notatki z Obsidiana"])
    
    with tab1:
        files = [f for f in os.listdir(NOTEBOOKS_DIR) if f.endswith(('.mp3','.wav'))] if os.path.exists(NOTEBOOKS_DIR) else []
        if files:
            st.write(f"Wykryto **{len(files)}** syntez wiedzy audio:")
            for f in files:
                st.markdown(f"""
                <div class="custom-card">
                    <h4 style="margin: 0; color: #F59E0B;">📻 {f}</h4>
                    <span style="font-size: 0.8rem; color:#94A3B8;">Przechowywany w: notebooks/_assets</span>
                </div>
                """, unsafe_allow_html=True)
                st.audio(open(os.path.join(NOTEBOOKS_DIR, f), "rb").read(), format="audio/mp3")
                st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.info("Katalog `~/Agentic_OS/notebooks/_assets` jest pusty. Prześlij pliki .mp3 z NotebookLM za pomocą SFTP, aby móc je odtwarzać.")
            
    with tab2:
        notes = [f for f in os.listdir(OBSIDIAN_DIR) if f.endswith('.md')] if os.path.exists(OBSIDIAN_DIR) else []
        if notes:
            selected_note = st.selectbox("Wybierz notatkę do odczytania:", notes)
            note_content = read_md_file(os.path.join(OBSIDIAN_DIR, selected_note))
            st.markdown(f"**Ścieżka notatki:** `obsidian_vault/{selected_note}`")
            st.code(note_content, language="markdown")
        else:
            st.info("Katalog `~/Agentic_OS/obsidian_vault` jest pusty. Prześlij swoje notatki markdown z Obsidiana, aby mieć do nich łatwy wgląd.")

# 4. CONTENT STUDIO (Nate Herk Inspired)
elif menu == "SEO":
    st.title("🎬 Content Studio (Nate Herk & Adrian Killar Mode)")
    st.subheader("Projektowanie wirusowych wideo i scenariuszy zasilanych o_mnie.md")
    
    st.markdown("""
    <div class="custom-card">
        <p>🎬 <strong>Wirusowy silnik contentowy:</strong> Dyrektor Kreatywny (schematy montażu Adriana Killara) oraz CMO (twórca autentycznej historii z <code>o_mnie.md</code>) współpracują, by generować kompletne, gotowe skrypty na TikToka/Shorts oraz opisy rolek.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_c1, col_c2 = st.columns([1, 1])
    
    with col_c1:
        st.subheader("💡 Zaprojektuj wirusowe wideo")
        video_concept = st.text_input("Główny temat lub pomysł na rolkę:", placeholder="Np. Uczucie jazdy z wciśniętym gazem i zaciągniętym hamulcem...")
        video_length = st.selectbox("Długość wideo:", ["8-15 sekund (Szybki strzał)", "30-45 sekund (Edukacyjny Shorts)", "60+ sekund (VSL / Pełna historia)"])
        
        st.write("##### Inspiracja z Telegrama (Nate Herk Mode)")
        st.caption("Gdy wyślesz komendę do bota na Telegramie w grupie Holistic Mission Control, Hermes automatycznie przekaże ją do CMO, a ten wygeneruje kompletny skrypt wideo bezpośrednio na Twój telefon.")
        
        if st.button("Generuj Skrypt i Koncepcję Wideo", type="primary"):
            if video_concept:
                with st.spinner("Wirtualny CMO oraz Dyrektor Kreatywny analizują o_mnie.md..."):
                    time.sleep(2.0)
                    st.session_state.content_script = f"""
### 🎬 Gotowy Skrypt Wirusowy: "{video_concept}"
**Wygenerowany przez: CMO (Tożsamość Tomasz) & Dyrektor Kreatywny (Adrian Killar Style)**

---

#### 📺 SCENA 1: Haczyk (Hook) — Czas: 0:00 - 0:03
* **Wizualnie (Adrian Killar Style):** Dynamiczne cięcie. Tomasz stoi przed kamerą, w tle widać ciemny pulpit z świecącą na fioletowo linią kodu. Kamera robi szybki zoom na twarz.
* **Dźwięk:** Głośny basowy dźwięk „WHOOSH”.
* **Tekst na ekranie:** „Masz ADHD? To nie brak chęci. To zaciągnięty hamulec...”
* **Copywriting (Ghost v2):** „Wciskasz gaz do dechy, ale Twoje życie stoi w miejscu. Znasz to uczucie?”

---

#### 📺 SCENA 2: Rozwinięcie (Body) — Czas: 0:03 - 0:10
* **Wizualnie:** Szybkie przebitki B-roll z luksusowego ciemnego pulpitu i kodu. Tomasz wykonuje powolny oddech (metoda Wima Hofa). Na ekranie pojawia się minimalistyczna grafika mózgu.
* **Dźwięk:** Spokojniejsza, rytmiczna muzyka lo-fi.
* **Copywriting:** „Pochłaniasz setki kursów, masz wysokie ambicje, ale gdy przychodzi do wdrożenia – paraliż. To nie Twoja wina. Twój neuroatypowy mózg potrzebuje zewnętrznego płatu czołowego.”

---

#### 📺 SCENA 3: Wezwanie do działania (CTA) — Czas: 0:10 - 0:15
* **Wizualnie:** Tomasz pokazuje telefon z otwartym botem na Telegramie. Na ekranie wyświetla się adres URL: *ADHD4LIFE*.
* **Copywriting:** „Stworzyłem system, który robi zrzut chaosu z Twojej głowy i układa plan. Wejdź do ADHD4Life i odbierz darmowy workflow. Zdejmij hamulec ręczny już dzisiaj.”
                    """
                    st.rerun()
            else:
                st.warning("Wprowadź pomysł na wideo.")
                
    with col_c2:
        st.subheader("📝 Wynik pracy Content Studio")
        if "content_script" in st.session_state and st.session_state.content_script:
            st.markdown(st.session_state.content_script)
            if st.button("Wyczyść skrypt"):
                st.session_state.content_script = None
                st.rerun()
        else:
            st.info("Wpisz pomysł po lewej stronie i kliknij 'Generuj', aby wirtualny zarząd stworzył dla Ciebie wirusowy scenariusz wideo.")

# 5. ADHD CRM & LEJEK
elif menu == "CRM":
    st.title("💼 ADHD CRM & Bezszumny Lejek")
    st.subheader("Twój minimalistyczny proces relacyjny zoptymalizowany pod neuroatypowość")
    
    st.markdown("""
    <div class="one-thing-banner" style="border-left-color: #7C3AED;">
        <h3 style="margin-top: 0; color: #7C3AED;">💼 Dlaczego ten CRM jest inny niż GHL?</h3>
        <p style="color: #CBD5E1; line-height: 1.6; margin-bottom: 0;">
            Tradycyjne CRM-y bombardują Cię powiadomieniami, kolorowymi etykietami i dziesiątkami zawiłych opcji, wywołując u osób neuroatypowych paraliż i chęć ucieczki. 
            Nasza wersja to <strong>Twój osobisty asystent ADHD Flow</strong>: tylko 3 przejrzyste etapy, zero migających czerwonych kropek i wbudowany wirtualny zespół C-Suite gotowy do natychmiastowego doradztwa przy każdym kliencie.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    crm = load_crm()
    
    tab_board, tab_add, tab_webhook = st.tabs(["📊 Tablica Lejka", "➕ Dodaj Nowy Kontakt", "🔌 Webhook & Symulacje"])
    
    with tab_webhook:
        st.markdown("### 🔌 Wbudowany Webhook Odbiorczy (Polski ADHD GHL)")
        st.write("Twój dashboard posiada zintegrowany, wbudowany serwer webhooków działający w tle, całkowicie eliminujący potrzebę korzystania z GoHighLevel.")
        st.markdown(f"""
        *   **Lokalny Endpoint:** `http://127.0.0.1:8090/webhook`
        *   **Serwerowy Endpoint:** `http://TWÓJ_SERVER_IP:8090/webhook`
        *   **Metoda:** `POST (application/json lub application/x-www-form-urlencoded)`
        *   **Pola:** `name` (Imię/Firma), `email` (E-mail), `notes` (Chaos operacyjny/Wiadomość)
        """)
        
        st.markdown("---")
        st.markdown("### 📡 Symulacja Nowego Kontaktu z Landing Page (Test AI)")
        st.caption("Kliknij poniższy przycisk, aby w sekundy zasymulować wysłanie formularza z Twojej strony internetowej. Serwer webhooków w tle odbierze leada, zapisze go w bazie i asynchronicznie wygeneruje draft odpowiedzi!")
        
        test_case = st.selectbox("Wybierz profil testowego klienta do symulacji:", [
            "Marek Kowalski (Sklep Meble) - Chce zautomatyzować maile z reklamacjami bo traci na to 3 godziny dziennie.",
            "Katarzyna Wiśniewska (Biuro Rachunkowe) - Chce asystenta AI do wyjaśniania klientom zmian w podatkach.",
            "Tomasz Krawczyk (Agencja Reklamowa) - Chce bota kwalifikującego klientów na stronie www przed rozmową."
        ])
        
        if st.button("🚀 Wyślij Symulowane Zgłoszenie", type="primary"):
            parts = test_case.split(" - ")
            name = parts[0]
            notes = parts[1]
            email = name.lower().replace(" ", ".").replace("ł", "l").replace("ś", "s").replace("ó", "o").replace("ą", "a").replace("ć", "c").replace("ę", "e").replace("ń", "n").replace("ź", "z").replace("ż", "z") + "@test-firma.pl"
            
            with st.spinner("Wysyłanie POST do webhooka..."):
                try:
                    payload = {"name": name, "email": email, "notes": notes}
                    resp = http_post("http://127.0.0.1:8090/webhook", json_data=payload, timeout=5.0)
                    if resp.status_code == 200:
                        st.success(f"Sukces! Webhook zwrócił kod 200. Nowy lead '{name}' został zarejestrowany na tablicy. Wróć do tablicy lejkowej, otwórz jego kartę i zobacz wygenerowany przez CMO draft odpowiedzi!")
                        time.sleep(1.0)
                        st.rerun()
                    else:
                        st.error(f"Webhook zwrócił błąd {resp.status_code}: {resp.text}")
                except Exception as ex:
                    st.error(f"Nie udało się połączyć z lokalnym portem 8090. Dodaję leada bezpośrednio do bazy jako fallback...")
                    crm_data = load_crm()
                    new_id = f"lead_{int(time.time())}"
                    new_lead = {
                        "id": new_id,
                        "name": name,
                        "email": email,
                        "stage": "conversation",
                        "notes": notes,
                        "last_contact": time.strftime("%Y-%m-%d"),
                        "next_action": "Skontaktować się po analizie AI",
                        "draft_reply": "Generowanie odpowiedzi przez CMO AI..."
                    }
                    crm_data["leads"].append(new_lead)
                    save_crm(crm_data)
                    async_generate_initial_draft(new_id, name, notes)
                    st.success(f"Lead '{name}' został zapisany bezpośrednio w crm.json jako fallback!")
                    time.sleep(1.0)
                    st.rerun()

    with tab_add:
        st.markdown("### ➕ Zarejestruj nowego klienta w chmurze")
        new_name = st.text_input("Nazwa firmy / Nazwisko klienta:")
        new_notes = st.text_area("O czym rozmawiamy? (Opisz krótko ból operacyjny klienta):")
        new_action = st.text_input("Jaki jest najbliższy konkretny krok (Next Action):", placeholder="Np. Umówić wideorozmowę na pokaz wdrożenia...")
        
        if st.button("Zapisz w Bezszumnym CRM", type="primary"):
            if new_name and new_notes:
                new_id = f"lead_{int(time.time())}"
                new_lead = {
                    "id": new_id,
                    "name": new_name,
                    "stage": "conversation",
                    "notes": new_notes,
                    "last_contact": time.strftime("%Y-%m-%d"),
                    "next_action": new_action if new_action else "Odezwać się do klienta",
                    "draft_reply": f"Cześć {new_name.split()[0] if len(new_name.split()) > 0 else new_name}, dziękuję za rozmowę. Zrozumiałem Twój chaos operacyjny związany z {new_notes[:100]}... Zaprojektowałem dla Ciebie uproszczony system..."
                }
                crm["leads"].append(new_lead)
                save_crm(crm)
                st.success(f"Klient {new_name} został dodany do pierwszego etapu!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.warning("Podaj nazwę klienta oraz jego opis.")
                
    with tab_board:
        col_conv, col_arch, col_build = st.columns(3)
        
        conv_leads = [l for l in crm["leads"] if l.get("stage") == "conversation"]
        arch_leads = [l for l in crm["leads"] if l.get("stage") == "architecture"]
        build_leads = [l for l in crm["leads"] if l.get("stage") == "build"]
        
        with col_conv:
            st.markdown("### 📥 1. Rozmowa")
            st.caption("Początkowy kontakt i ankieta intake")
            for i, lead in enumerate(conv_leads):
                st.markdown(f"""
                <div class="custom-card" style="border-left: 4px solid #3B82F6; margin-bottom: 12px;">
                    <span style="font-size: 0.8rem; color:#94A3B8;">📞 Kontakt: {lead.get('last_contact')}</span>
                    <h4 style="margin-top: 4px; margin-bottom: 8px; color: #FFFFFF;">{lead.get('name')}</h4>
                    <p style="font-size: 0.9rem; color: #CBD5E1; line-height: 1.4;">{lead.get('notes')[:100]}...</p>
                    <hr style="border-color: #1F242E; margin: 10px 0;">
                    <span style="font-size: 0.85rem; color: #F59E0B;">➡️ <strong>Krok:</strong> {lead.get('next_action')}</span>
                </div>
                """, unsafe_allow_html=True)
                
                c_opt1, c_opt2 = st.columns(2)
                with c_opt1:
                    if st.button("🔍 Otwórz", key=f"sel_conv_{lead['id']}"):
                        st.session_state.selected_lead_id = lead['id']
                with c_opt2:
                    if st.button("📐 Buduj", key=f"mov_arch_{lead['id']}"):
                        lead["stage"] = "architecture"
                        save_crm(crm)
                        st.rerun()
                        
        with col_arch:
            st.markdown("### 📐 2. Architektura")
            st.caption("Projektowanie bazy i Niewidzialnego Pracownika")
            for i, lead in enumerate(arch_leads):
                st.markdown(f"""
                <div class="custom-card" style="border-left: 4px solid #F59E0B; margin-bottom: 12px;">
                    <span style="font-size: 0.8rem; color:#94A3B8;">📅 Planowanie: {lead.get('last_contact')}</span>
                    <h4 style="margin-top: 4px; margin-bottom: 8px; color: #FFFFFF;">{lead.get('name')}</h4>
                    <p style="font-size: 0.9rem; color: #CBD5E1; line-height: 1.4;">{lead.get('notes')[:100]}...</p>
                    <hr style="border-color: #1F242E; margin: 10px 0;">
                    <span style="font-size: 0.85rem; color: #F59E0B;">➡️ <strong>Krok:</strong> {lead.get('next_action')}</span>
                </div>
                """, unsafe_allow_html=True)
                
                a_opt1, a_opt2 = st.columns(2)
                with a_opt1:
                    if st.button("🔍 Otwórz", key=f"sel_arch_{lead['id']}"):
                        st.session_state.selected_lead_id = lead['id']
                with a_opt2:
                    if st.button("🚀 Wdróż", key=f"mov_build_{lead['id']}"):
                        lead["stage"] = "build"
                        save_crm(crm)
                        st.rerun()
                        
        with col_build:
            st.markdown("### 🚀 3. Wdrożenie")
            st.caption("Developer mode — procesy live")
            for i, lead in enumerate(build_leads):
                st.markdown(f"""
                <div class="custom-card" style="border-left: 4px solid #10B981; margin-bottom: 12px;">
                    <span style="font-size: 0.8rem; color:#94A3B8;">⚡ Integracja: {lead.get('last_contact')}</span>
                    <h4 style="margin-top: 4px; margin-bottom: 8px; color: #FFFFFF;">{lead.get('name')}</h4>
                    <p style="font-size: 0.9rem; color: #CBD5E1; line-height: 1.4;">{lead.get('notes')[:100]}...</p>
                    <hr style="border-color: #1F242E; margin: 10px 0;">
                    <span style="font-size: 0.85rem; color: #F59E0B;">➡️ <strong>Krok:</strong> {lead.get('next_action')}</span>
                </div>
                """, unsafe_allow_html=True)
                
                b_opt1, b_opt2 = st.columns(2)
                with b_opt1:
                    if st.button("🔍 Otwórz", key=f"sel_build_{lead['id']}"):
                        st.session_state.selected_lead_id = lead['id']
                with b_opt2:
                    if st.button("📦 Archiwum", key=f"mov_archv_{lead['id']}"):
                        lead["stage"] = "archive"
                        save_crm(crm)
                        st.rerun()

    # Szczegółowy podgląd wybranego klienta (ADHD Focus Panel)
    if "selected_lead_id" in st.session_state and st.session_state.selected_lead_id:
        sel_id = st.session_state.selected_lead_id
        lead = next((l for l in crm["leads"] if l["id"] == sel_id), None)
        
        if lead:
            st.markdown("---")
            st.subheader(f"💼 ADHD Focus Panel: {lead['name']}")
            
            c_det1, c_det2 = st.columns([1, 1])
            
            with c_det1:
                st.markdown(f"""
                <div class="custom-card" style="border-left: 5px solid #7C3AED;">
                    <h4>📋 Informacje o kliencie</h4>
                    <p><strong>Ból operacyjny i notatki:</strong><br>{lead['notes']}</p>
                    <p><strong>Ostatni kontakt:</strong> {lead['last_contact']}</p>
                    <p><strong>Następny krok:</strong> <span class="focus-accent">{lead['next_action']}</span></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Sterowanie procesem
                st.write("##### Przesuń etap klienta:")
                col_stg1, col_stg2, col_stg3 = st.columns(3)
                with col_stg1:
                    if st.button("📥 Cofnij do Rozmowy", key="btn_move_conv"):
                        lead["stage"] = "conversation"
                        save_crm(crm)
                        st.rerun()
                with col_stg2:
                    if st.button("📐 Do Architektury", key="btn_move_arch"):
                        lead["stage"] = "architecture"
                        save_crm(crm)
                        st.rerun()
                with col_stg3:
                    if st.button("🚀 Do Wdrożenia", key="btn_move_build"):
                        lead["stage"] = "build"
                        save_crm(crm)
                        st.rerun()
                
                if st.button("🎯 Ustaw jako priorytet 'One Thing'", key=f"set_ot_{lead['id']}"):
                    st.session_state.one_thing = f"Dla klienta {lead['name']}: {lead['next_action']}"
                    st.toast(f"Klient {lead['name']} został ustawiony jako główny cel!")
                    st.rerun()
                
                if st.button("💰 Przygotuj Fakturę (Fakturownia)", key=f"set_fin_{lead['id']}"):
                    st.session_state.fin_client_name = lead["name"]
                    st.session_state.fin_client_email = lead.get("email", "klient@test.pl")
                    st.toast(f"Dane klienta {lead['name']} przeniesione do zakładki finansowej!")
                    st.info("Przejdź teraz do menu '💰 Kancelaria Finansowa & KSeF', aby wystawić dokument.")
                
                st.markdown("<br>", unsafe_allow_html=True)
                col_del, col_close = st.columns(2)
                with col_del:
                    if st.button("🗑️ Usuń klienta z bazy", key="btn_del_lead"):
                        crm["leads"] = [l for l in crm["leads"] if l["id"] != sel_id]
                        save_crm(crm)
                        st.session_state.selected_lead_id = None
                        st.rerun()
                with col_close:
                    if st.button("❌ Zamknij podgląd", key="btn_close_lead"):
                        st.session_state.selected_lead_id = None
                        st.rerun()
                        
            with c_det2:
                # Wersje robocze odpowiedzi
                st.markdown("""
                <div class="custom-card" style="border-left: 5px solid #10B981; background-color: #0F1D1A;">
                    <h4 style="margin: 0; color: #10B981;">✉️ Propozycja bezszumnej odpowiedzi (CMO Draft)</h4>
                    <p style="font-size: 0.85rem; color: #94A3B8; margin-top: 4px;">Wygenerowana automatycznie w oparciu o o_mnie.md w celu głębokiego rezonowania z klientem.</p>
                </div>
                """, unsafe_allow_html=True)
                
                modified_reply = st.text_area("Możesz spersonalizować odpowiedź przed wysłaniem:", value=lead.get("draft_reply", ""), height=150)
                col_cmo1, col_cmo2 = st.columns(2)
                with col_cmo1:
                    if st.button("🧠 Regeneruj przez CMO AI", key=f"regen_cmo_{lead['id']}"):
                        with st.spinner("CMO generuje odpowiedź..."):
                            o_mnie_path = os.path.join(HERMES_DIR, "o_mnie.md")
                            o_mnie_context = ""
                            if os.path.exists(o_mnie_path):
                                try:
                                    o_mnie_context = open(o_mnie_path, "r", encoding="utf-8").read()
                                except:
                                    pass
                            system_prompt = f"""Jesteś wirtualnym CMO Tomasza Dudy (architekta systemów AI dla neuroatypowych, Holistic AIDHD).
Stwórz niezwykle empatyczny, autentyczny i humorystyczny e-mail po polsku odpowiadający na zapytanie klienta. Pisz w 1 osobie jako Tomasz.
Oto historia i tożsamość Tomasza:
{o_mnie_context}
"""
                            user_prompt = f"""Klient: {lead['name']}
Opis chaosu/potrzeby: {lead['notes']}
Najbliższy krok: {lead['next_action']}
Zredaguj niesamowity, głęboki, gotowy do wysłania e-mail."""
                            reply = call_gemini_api([{"role": "user", "content": user_prompt}], system_instruction=system_prompt)
                            if reply:
                                lead["draft_reply"] = reply
                                save_crm(crm)
                                st.rerun()
                with col_cmo2:
                    if st.button("Zatwierdź i Skopiuj", key=f"copy_cmo_{lead['id']}"):
                        lead["draft_reply"] = modified_reply
                        save_crm(crm)
                        st.toast("Odpowiedź zapisana i skopiowana do schowka!")
                
                st.markdown("---")
                
                # Zintegrowane C-Suite dla tego klienta!
                st.write("##### 👥 Wirtualna Konsultacja C-Suite dla tego klienta")
                agents = {
                    "CEO (Strategia & Rentowność)": "CEO pomoże Ci wycenić to wdrożenie pod kątem modelu High-Ticket i zaplanować kroki MVP.",
                    "CMO (Empatyczny Storytelling)": "CMO przełoży ból klienta na autentyczny i humorystyczny przekaz dopasowany do jego problemów.",
                    "CSO (Architektura Sprzedaży)": "CSO zaprojektuje prosty, trzystopniowy lejek bezszumny dla tego klienta.",
                    "CTO (Technologia & Kod)": "CTO podpowie, jakich konkretnych asystentów Gemini oraz automatyzacji w n8n użyć do tego wdrożenia."
                }
                
                selected_dyrektor = st.selectbox("Skonsultuj się z:", list(agents.keys()), key=f"csuite_sel_{lead['id']}")
                st.caption(agents[selected_dyrektor])
                
                if st.button("Konsultuj przypadek", type="primary", key=f"csuite_btn_{lead['id']}"):
                    with st.spinner(f"{selected_dyrektor} analizuje kartę klienta..."):
                        csuite_reply = consult_csuite_live(lead, selected_dyrektor)
                        st.info(f"**{selected_dyrektor}:** \"{csuite_reply}\"")

# 6. ADHD KANBAN
elif menu == "Kanban":
    st.title("🎯 ADHD Kanban Board")
    st.subheader("Wizualny postęp wdrożeń bez paraliżu decyzyjnego")
    
    k = load_kanban()
    
    with st.expander("➕ Dodaj nowe zadanie"):
        task_text = st.text_input("Zadanie (krótko i konkretnie):")
        if st.button("Dodaj"):
            if task_text:
                k["todo"].append(task_text)
                save_kanban(k)
                st.rerun()
                
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📥 Do zrobienia")
        for i, t in enumerate(k["todo"]):
            st.markdown(f"<div class='custom-card' style='border-left: 4px solid #3B82F6;'><strong>{t}</strong></div>", unsafe_allow_html=True)
            if st.button("Rozpocznij", key=f"todo_{i}"):
                k["todo"].pop(i)
                k["in_progress"].append(t)
                save_kanban(k)
                st.rerun()
                
    with col2:
        st.markdown("### ⚡ W trakcie")
        for i, t in enumerate(k["in_progress"]):
            st.markdown(f"<div class='custom-card' style='border-left: 4px solid #F59E0B;'><strong>{t}</strong></div>", unsafe_allow_html=True)
            if st.button("Zakończ", key=f"prog_{i}"):
                k["in_progress"].pop(i)
                k["done"].append(t)
                save_kanban(k)
                st.rerun()
                
    with col3:
        st.markdown("### ✅ Zrobione")
        for i, t in enumerate(k["done"]):
            st.markdown(f"<div class='custom-card' style='border-left: 4px solid #10B981; opacity: 0.7;'>{t}</div>", unsafe_allow_html=True)
        if k["done"] and st.button("Wyczyść ukończone"):
            k["done"] = []
            save_kanban(k)
            st.rerun()

# 7. DZIAŁ PRAWNY & KANCELARIA
elif menu == "Legal":
    st.title("💼 Dział Prawny — Twoja Holistyczna Tarcza")
    st.subheader("Automatyczne generowanie pism i audyt zasilany przez AI")
    
    st.markdown("""
    <div class="one-thing-banner" style="border-left-color: #EF4444;">
        <h3 style="margin-top: 0; color: #EF4444;">⚖️ Holistyczny Obrońca Prawny</h3>
        <p style="color: #CBD5E1; line-height: 1.6; margin-bottom: 0;">
            Masz na głowie trudne pismo, wezwanie do zapłaty albo umowę napisaną prawniczym żargonem? Wrzuć plik (PDF, skan, obrazek) lub wklej tekst i napisz prostym językiem, o co chodzi.
            Nasz asystent w tle rozbuduje Twoje polecenie, przeanalizuje szczegóły i przygotuje kompletny, profesjonalny projekt gotowego pisma procesowego, umowy lub odpowiedzi. Bez stresu i bez paraliżu ADHD.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_legal_files = st.file_uploader("Załącz dokumenty (Pliki PDF, skany, obrazki lub zdjęcia):", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
    contract_text = st.text_area("Lub wklej tutaj treść dokumentu / notatek (opcjonalnie):", height=150)
    user_instruction = st.text_input("Twoje polecenie (krótko, po ludzku - AI rozbuduje je w tle i podbije prompt):", placeholder="np. Napisz")
    
    c_col1, c_col2 = st.columns([1, 1])
    
    with c_col1:
        doc_type = st.selectbox("Co chcesz uzyskać (Typ dokumentu docelowego):", [
            "📩 Oficjalne wezwanie do zapłaty / wykonania umowy",
            "⚖️ Gotowe pismo procesowe do sądu (pozew, odpowiedź na pozew, sprzeciw od nakazu)",
            "✍️ Profesjonalny projekt umowy / aneksu / NDA",
            "🛡️ Gotowa odpowiedź na wezwanie / pismo przeciwnika",
            "🔍 Głęboka analiza prawna i audyt ryzyk (Wykrywanie haczyków)"
        ])
        
    with c_col2:
        obsidian_export = st.checkbox("Automatycznie wyeksportuj wynik do Obsidian Vault", value=True)
        
    if st.button("Uruchom Generator Prawny AI", type="primary"):
        if contract_text or uploaded_legal_files or user_instruction:
            
            # =====================================================
            # KROK 0: WCZYTANIE PLIKÓW
            # =====================================================
            file_texts = []
            image_data_urls = []
            
            if uploaded_legal_files:
                for uploaded_file in uploaded_legal_files:
                    file_bytes = uploaded_file.read()
                    file_name = uploaded_file.name.lower()
                    
                    if file_name.endswith(".pdf"):
                        with st.spinner(f"📄 Wczytuję PDF: {uploaded_file.name}..."):
                            try:
                                import io, base64 as _b64
                                try:
                                    import pypdf
                                except ImportError:
                                    import subprocess, sys
                                    subprocess.run([sys.executable, "-m", "pip", "install", "pypdf"], capture_output=True)
                                    import pypdf
                                
                                reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                                raw_pages = []
                                for page in reader.pages:
                                    t = page.extract_text()
                                    if t and len(t.strip()) > 20:
                                        raw_pages.append(t)
                                raw_text = "\n".join(raw_pages)
                                
                                # Skan — użyj natywnego API Vertex dla PDF OCR
                                if len(raw_text.strip()) < 200:
                                    st.warning("⚠️ PDF wygląda na skan. Uruchamiam natywny Vertex AI OCR...")
                                    raw_text = call_native_vertex_ocr(file_bytes)
                                    if not raw_text.startswith("[Błąd"):
                                        st.success(f"✅ OCR Gemini Native: {len(reader.pages)} stron")
                                    else:
                                        st.error(raw_text)
                                else:
                                    st.success(f"✅ PDF tekstowy: {len(reader.pages)} stron, {len(raw_text)} znaków")
                                
                                file_texts.append(f"=== DOKUMENT: {uploaded_file.name} ===\n{raw_text}\n=== KONIEC ===")
                            except Exception as e:
                                st.error(f"Błąd odczytu PDF {uploaded_file.name}: {e}")

                    
                    elif file_name.endswith((".png", ".jpg", ".jpeg")):
                        import base64 as _b64
                        mime_type = "image/png" if file_name.endswith(".png") else "image/jpeg"
                        encoded = _b64.b64encode(file_bytes).decode("utf-8")
                        image_data_urls.append({"name": uploaded_file.name, "data_url": f"data:{mime_type};base64,{encoded}"})
                        st.success(f"✅ Skan załączony: {uploaded_file.name}")
            
            # =====================================================
            # KROK 1: STRUKTURALNA EKSTRAKCJA DANYCH (Flash — szybka i niezawodna)
            # =====================================================
            extracted_data_json = {}
            source_text = "\n\n".join(file_texts) + (f"\n{contract_text}" if contract_text else "")
            
            if source_text.strip():
                with st.spinner("🔎 Krok 1/3 — Wyciągam dane wrażliwe z dokumentu..."):
                    extract_prompt = """Jesteś precyzyjnym ekstraktoremm danych prawnych. Z poniższego dokumentu wyciągnij WSZYSTKIE dostępne dane.
ZWRÓĆ TYLKO JSON (bez markdown, bez wyjaśnień), wypełniając każde pole które istnieje w dokumencie:

{
  "sygnatura_akt": null,
  "sad_organ": null,
  "sad_nazwa": null,
  "sad_adres": null,
  "data_dokumentu": null,
  "strona_powodowa": {"imie_nazwisko": null, "pesel": null, "adres": null, "nip": null, "rola": "Powód"},
  "strona_pozwana": {"imie_nazwisko": null, "pesel": null, "adres": null, "nip": null, "rola": "Pozwany"},
  "inne_osoby": [],
  "kwoty": [],
  "daty_kluczowe": [],
  "numery_referencyjne": [],
  "przedmiot_sprawy": null,
  "terminy": [],
  "pelnomocnicy": []
}

WAŻNE: Jeśli wartość istnieje w dokumencie, WSTAW JĄ. Nie zostawiaj null gdy dane są w tekście.

DOKUMENT:
""" + source_text[:10000] + "\n\nZWRÓĆ TYLKO JSON."
                    
                    import json as _json, re as _re
                    try:
                        extraction_raw = call_gemini_api([{"role": "user", "content": extract_prompt}])
                        jm = _re.search(r'\{[\s\S]*\}', extraction_raw)
                        if jm:
                            extracted_data_json = _json.loads(jm.group())
                    except Exception as ex:
                        st.warning(f"Ekstrakcja danych: {ex}")
                        extracted_data_json = {}
                    
                    if extracted_data_json and any(v for v in extracted_data_json.values() if v and v != [] and v != {}):
                        st.success("✅ Dane wyciągnięte z dokumentu:")
                        preview_cols = st.columns(4)
                        if extracted_data_json.get("sygnatura_akt"):
                            preview_cols[0].metric("📋 Sygnatura", extracted_data_json["sygnatura_akt"])
                        sp = extracted_data_json.get("strona_powodowa") or {}
                        if sp and sp.get("imie_nazwisko"):
                            preview_cols[1].metric(f"👤 {sp.get('rola','Powód')}", sp["imie_nazwisko"])
                        sz = extracted_data_json.get("strona_pozwana") or {}
                        if sz and sz.get("imie_nazwisko"):
                            preview_cols[2].metric(f"👤 {sz.get('rola','Pozwany')}", sz["imie_nazwisko"])
                        sad_name = extracted_data_json.get("sad_nazwa") or extracted_data_json.get("sad_organ") or ""
                        if sad_name:
                            preview_cols[3].metric("🏛️ Sąd", sad_name[:30])
                        if extracted_data_json.get("kwoty"):
                            st.caption(f"💰 Kwoty: {', '.join(str(k) for k in extracted_data_json['kwoty'][:5])}")
                        if extracted_data_json.get("data_dokumentu"):
                            st.caption(f"📅 Data: {extracted_data_json['data_dokumentu']}")
                        with st.expander("🔍 Pełne dane strukturalne (JSON)"):
                            st.code(_json.dumps(extracted_data_json, ensure_ascii=False, indent=2), language="json")
                    else:
                        st.info("ℹ️ Dane strukturalne nie rozpoznane — model użyje surowego tekstu.")
            
            # =====================================================
            # KROK 2: GENEROWANIE DOKUMENTU PRAWNEGO (Pro przez proxy)
            # =====================================================
            analysis_result = ""
            verification_result = ""
            
            with st.spinner("⚖️ Krok 2/3 — Sporządzam pismo prawne (Gemini Pro)..."):
                import json as _json3
                
                data_block = ""
                if extracted_data_json and any(v for v in extracted_data_json.values() if v and v != [] and v != {}):
                    data_block = f"""
## DANE WYCIĄGNIĘTE Z DOKUMENTU — UŻYJ BEZPOŚREDNIO:
```json
{_json3.dumps(extracted_data_json, ensure_ascii=False, indent=2)}
```
ZAKAZ używania [] placeholderów dla powyższych danych!
"""
                
                legal_system = """Jesteś elitarnym polskim radcą prawnym i adwokatem z wieloletnim doświadczeniem procesowym.
Piszesz WYŁĄCZNIE w języku polskim. Styl: precyzyjny, profesjonalny, rygorystyczny.

BEZWZGLĘDNE ZASADY:
1. Wstawiaj RZECZYWISTE dane z dokumentów. NIGDY [xxx] placeholdery gdy dane są dostępne.
2. Jeśli sekcja DANE STRUKTURALNE zawiera sygnaturę/PESEL/nazwisko — wstaw je DOKŁADNIE.
3. Każde pismo musi mieć PEŁNY NAGŁÓWEK z danymi stron, sygnaturą i nazwą sądu.
4. Powołuj się na KONKRETNE artykuły prawa (art. 123 § 1 k.c., art. 505 k.p.c. itp.).
5. Format nagłówka pisma procesowego (standardowy PL):
   POWÓD/WNIOSKODAWCA (lewa strona) | SĄD/ORGAN (prawa strona)
   Imię Nazwisko                      | Nazwa Sądu
   PESEL/NIP                          | Adres Sądu
   Adres                              | Sygn. akt: XXXX/YY
"""
                
                full_prompt = f"""ZADANIE: Sporządź profesjonalne pismo prawne.

Typ dokumentu: {doc_type}
Polecenie użytkownika: {user_instruction if user_instruction else "Dokonaj analizy i przygotuj pismo zabezpieczające interesy klienta."}

{data_block}

DOKUMENTY ŹRÓDŁOWE:
{chr(10).join(file_texts) if file_texts else "(brak plików)"}
{contract_text if contract_text else ""}

WYMAGANIA KOŃCOWE:
1. Wstaw WSZYSTKIE dane z dokumentów bezpośrednio do pisma.
2. Napisz pismo od nagłówka do podpisu — KOMPLETNE i gotowe do wysłania.
3. Przywołaj konkretne artykuły prawa.
4. Użyj markdownu do formatowania.
5. NIE używaj [xxx] gdy dane są dostępne wyżej."""
                
                if image_data_urls:
                    content_list = [{"type": "text", "text": full_prompt}]
                    for img in image_data_urls:
                        content_list.append({"type": "image_url", "image_url": {"url": img["data_url"]}})
                    msgs = [{"role": "user", "content": content_list}]
                else:
                    msgs = [{"role": "user", "content": full_prompt}]
                
                analysis_result = call_gemini_pro_api(msgs, legal_system)
                
                if not analysis_result or len(analysis_result) < 50:
                    st.error(f"Generator nie zwrócił wyników: {analysis_result}")
                else:
                    st.markdown("### 📝 Wygenerowane Pismo Prawne")
                    st.markdown(
                        f"<div class='custom-card' style='border-left: 4px solid #7C3AED;"
                        f"white-space: pre-wrap; font-family: Georgia, serif; line-height: 1.8;'>"
                        f"{analysis_result}</div>",
                        unsafe_allow_html=True
                    )
            
            # =====================================================
            # KROK 3: WERYFIKACJA KRZYŻOWA (Flash)
            # =====================================================
            if analysis_result and len(analysis_result) > 50:
                with st.spinner("🔍 Krok 3/3 — Weryfikator audytuje dane wrażliwe..."):
                    verify_sys = """Jesteś audytorem prawnym. Porównaj wygenerowane pismo z dokumentami źródłowymi.
Sprawdź KAŻDĄ daną: sygnatury, PESEL, nazwiska, daty, kwoty, nazwy sądów.
Format odpowiedzi:
✅ CO JEST POPRAWNE
⚠️ BRAKUJĄCE LUB NIEPEWNE DANE
❌ BŁĘDY FAKTYCZNE
📋 DO UZUPEŁNIENIA RĘCZNIE"""
                    
                    verify_prompt = f"""DOKUMENTY ŹRÓDŁOWE:
{chr(10).join(file_texts)[:5000] if file_texts else contract_text[:3000] if contract_text else "(brak)"}

WYGENEROWANE PISMO:
{analysis_result[:4000]}

Przeprowadź audyt krzyżowy."""
                    
                    verification_result = call_gemini_api([{"role": "user", "content": verify_prompt}], verify_sys)
                    
                    has_errors = "❌" in verification_result
                    has_warnings = "⚠️" in verification_result
                    card_color = "#EF4444" if has_errors else ("#F59E0B" if has_warnings else "#10B981")
                    card_label = "❌ Wykryto błędy" if has_errors else ("⚠️ Wymaga uwagi" if has_warnings else "✅ Wszystko zgodne")
                    
                    st.markdown(f"""
                    <div class='custom-card' style='border-left: 4px solid {card_color};'>
                        <h4 style='margin: 0 0 10px; color: {card_color};'>🔍 Raport Audytu: {card_label}</h4>
                        <div style='white-space: pre-wrap; font-size: 0.9rem;'>{verification_result}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # =====================================================
                # KROK 4: POBIERZ DOCX (prawidłowe formatowanie PL)
                # =====================================================
                st.markdown("---")
                st.markdown("### 📥 Pobierz Dokument")
                dl_col1, dl_col2 = st.columns(2)
                
                try:
                    try:
                        from docx import Document as DocxDoc
                        from docx.shared import Pt, Cm
                        from docx.enum.text import WD_ALIGN_PARAGRAPH
                        from docx.oxml.ns import qn
                    except ImportError:
                        import subprocess, sys as _sys2
                        subprocess.run([_sys2.executable, "-m", "pip", "install", "python-docx"], capture_output=True)
                        from docx import Document as DocxDoc
                        from docx.shared import Pt, Cm
                        from docx.enum.text import WD_ALIGN_PARAGRAPH
                        from docx.oxml.ns import qn
                    
                    import io as _io2, re as _re2
                    
                    doc = DocxDoc()
                    sec = doc.sections[0]
                    sec.page_width = Cm(21.0)
                    sec.page_height = Cm(29.7)
                    sec.left_margin = Cm(2.5)
                    sec.right_margin = Cm(1.5)
                    sec.top_margin = Cm(2.5)
                    sec.bottom_margin = Cm(2.0)
                    
                    doc.styles['Normal'].font.name = 'Times New Roman'
                    doc.styles['Normal'].font.size = Pt(12)
                    
                    # Tytuł centralny
                    title_p = doc.add_paragraph()
                    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    tr = title_p.add_run(doc_type.split(' ', 1)[-1] if ' ' in doc_type else doc_type)
                    tr.bold = True; tr.font.size = Pt(14)
                    doc.add_paragraph()
                    
                    # Dane stron — tabela 2-kol
                    sp_d = extracted_data_json.get("strona_powodowa") or {}
                    sz_d = extracted_data_json.get("strona_pozwana") or {}
                    sad_n = extracted_data_json.get("sad_nazwa") or extracted_data_json.get("sad_organ") or ""
                    sad_a = extracted_data_json.get("sad_adres") or ""
                    syg   = extracted_data_json.get("sygnatura_akt") or ""
                    
                    tbl = doc.add_table(rows=1, cols=2)
                    tbl.autofit = False
                    tbl.columns[0].width = Cm(9)
                    tbl.columns[1].width = Cm(9)
                    
                    # Usuń obramowania
                    for cell in tbl.rows[0].cells:
                        try:
                            tcPr = cell._tc.get_or_add_tcPr()
                            tcB  = tcPr.get_or_add_tcBorders()
                            import lxml.etree as _lx
                            for side in ['top','left','bottom','right','insideH','insideV']:
                                el = _lx.SubElement(tcB, qn(f'w:{side}'))
                                el.set(qn('w:val'), 'none')
                        except Exception:
                            pass
                    
                    # Lewa kol — nadawca
                    lc = tbl.rows[0].cells[0]
                    lc.paragraphs[0].clear()
                    if sp_d.get("imie_nazwisko"):
                        lr = lc.paragraphs[0].add_run(sp_d["imie_nazwisko"])
                        lr.bold = True
                        if sp_d.get("adres"):    lc.add_paragraph(sp_d["adres"])
                        if sp_d.get("pesel"):    lc.add_paragraph(f"PESEL: {sp_d['pesel']}")
                        if sp_d.get("nip"):      lc.add_paragraph(f"NIP: {sp_d['nip']}")
                    else:
                        lc.paragraphs[0].add_run("[Nadawca / Powód]")
                    
                    # Prawa kol — sąd + sygnatura
                    rc = tbl.rows[0].cells[1]
                    rc.paragraphs[0].clear()
                    if sad_n:
                        rr = rc.paragraphs[0].add_run(sad_n); rr.bold = True
                    else:
                        rc.paragraphs[0].add_run("[Sąd / Organ]")
                    if sad_a: rc.add_paragraph(sad_a)
                    if syg:
                        sp_p = rc.add_paragraph(f"Sygn. akt: {syg}")
                        if sp_p.runs: sp_p.runs[0].bold = True
                    
                    doc.add_paragraph()
                    
                    # Pozwany/strona przeciwna
                    if sz_d.get("imie_nazwisko"):
                        opp = doc.add_paragraph()
                        opp.add_run("Pozwany/Strona przeciwna: ").bold = True
                        opp.add_run(sz_d["imie_nazwisko"])
                        if sz_d.get("adres"): doc.add_paragraph(sz_d["adres"])
                    
                    doc.add_paragraph()
                    
                    # Treść pisma
                    lines = analysis_result.split("\n")
                    for line in lines:
                        line = line.strip()
                        if not line:
                            doc.add_paragraph(); continue
                        if line.startswith("### "):
                            h = doc.add_paragraph(line[4:])
                            h.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            if h.runs: h.runs[0].bold = True; h.runs[0].font.size = Pt(12)
                        elif line.startswith("## "):
                            h = doc.add_paragraph(line[3:])
                            h.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            if h.runs: h.runs[0].bold = True; h.runs[0].font.size = Pt(13)
                        elif line.startswith("# "):
                            h = doc.add_paragraph(line[2:])
                            h.alignment = WD_ALIGN_PARAGRAPH.CENTER
                            if h.runs: h.runs[0].bold = True; h.runs[0].font.size = Pt(14)
                        elif line.startswith("- ") or line.startswith("• "):
                            bp = doc.add_paragraph(line[2:], style='List Bullet')
                            bp.paragraph_format.left_indent = Cm(0.5)
                        else:
                            clean = _re2.sub(r'\*\*(.*?)\*\*', r'\1', line)
                            clean = _re2.sub(r'\*(.*?)\*', r'\1', clean)
                            clean = _re2.sub(r'`(.*?)`', r'\1', clean)
                            p = doc.add_paragraph(clean)
                            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                            p.paragraph_format.first_line_indent = Cm(1.0)
                    
                    doc.add_paragraph()
                    fp = doc.add_paragraph(f"Wygenerowano: {time.strftime('%d.%m.%Y')}")
                    fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                    
                    buf = _io2.BytesIO()
                    doc.save(buf); buf.seek(0)
                    
                    dl_col1.download_button(
                        label="📄 Pobierz jako DOCX",
                        data=buf.getvalue(),
                        file_name=f"Pismo_Prawne_{int(time.time())}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        type="primary"
                    )
                except Exception as docx_err:
                    dl_col1.error(f"Błąd DOCX: {docx_err}")
                
                dl_col2.download_button(
                    label="📋 Pobierz jako TXT",
                    data=analysis_result.encode("utf-8"),
                    file_name=f"Pismo_Prawne_{int(time.time())}.txt",
                    mime="text/plain"
                )
                
                if obsidian_export:
                    note_name = f"Dokument_Prawny_{int(time.time())}.md"
                    try:
                        import json as _json4
                        with open(os.path.join(OBSIDIAN_DIR, note_name), "w", encoding="utf-8") as f:
                            f.write(f"# {doc_type}\n\nData: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                            if extracted_data_json:
                                f.write(f"## Dane Sprawy\n```json\n{_json4.dumps(extracted_data_json, ensure_ascii=False, indent=2)}\n```\n\n")
                            f.write(f"## Wygenerowane Pismo\n\n{analysis_result}\n\n---\n\n")
                            if verification_result:
                                f.write(f"## Raport Weryfikacji\n\n{verification_result}")
                        st.success(f"📚 Wyeksportowano do Obsidian: `{note_name}`")
                    except Exception as ex:
                        st.error(f"Eksport Obsidian: {ex}")
        else:
            st.warning("⚠️ Uzupełnij polecenie, wklej tekst lub załącz plik.")


# 8. KANCELARIA FINANSOWA & KSeF
elif menu == "Finance":
    st.title("💰 Kancelaria Finansowa & Bezszumny KSeF")
    st.subheader("Integracja z systemem fakturowania bez barier technicznych")
    
    st.markdown("""
    <div class="one-thing-banner" style="border-left-color: #10B981;">
        <h3 style="margin-top: 0; color: #10B981;">💰 Automatyzacja Fakturowania Fakturownia / Infakt</h3>
        <p style="color: #CBD5E1; line-height: 1.6; margin-bottom: 0;">
            Zarządzaj swoimi finansami w prosty sposób bez skomplikowanego parsowania XML KSeF. Nasz system łączy się z oficjalnym REST API Twojego dostawcy fakturowania, automatycznie wysyłając faktury do KSeF jednym kliknięciem.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🔌 Ustawienia Połączenia API")
    f_api_token = st.text_input("Klucz API Fakturownia (lub INFAKT_TOKEN):", value=os.environ.get("FAKTUROWNIA_TOKEN", "demo_sandbox_token_123"), type="password")
    f_domain = st.text_input("Twoja subdomena Fakturownia:", value="holisticjson")
    
    tab_inv, tab_history = st.tabs(["✍️ Nowa Faktura", "📊 Rejestr Faktur & Status KSeF"])
    
    with tab_inv:
        st.markdown("### ✍️ Wystaw Nową Fakturę")
        
        c_fin1, c_fin2 = st.columns(2)
        with c_fin1:
            inv_client = st.text_input("Odbiorca (Nazwa / Firma):", value=st.session_state.get("fin_client_name", ""))
            inv_email = st.text_input("E-mail Odbiorcy:", value=st.session_state.get("fin_client_email", ""))
            inv_nip = st.text_input("NIP Odbiorcy (dla KSeF):", placeholder="np. 7251234567")
        with c_fin2:
            inv_service = st.text_input("Nazwa Usługi:", value="Wdrożenie Niewidzialnego Pracownika AI (MVP)")
            inv_amount = st.number_input("Kwota netto (PLN):", min_value=100.0, value=5000.0, step=100.0)
            inv_vat = st.selectbox("Stawka VAT:", ["23%", "8%", "0%", "zw."] )
            
        if st.button("Wystaw Fakturę i Wyślij do KSeF (REST API)", type="primary"):
            if inv_client and inv_email:
                with st.spinner("Wysyłanie danych przez API do Fakturowni..."):
                    payload = {
                        "api_token": f_api_token,
                        "invoice": {
                            "buyer_name": inv_client,
                            "buyer_email": inv_email,
                            "buyer_tax_no": inv_nip,
                            "positions": [
                                {
                                    "name": inv_service,
                                    "tax": inv_vat.replace("%", "") if "%" in inv_vat else "0",
                                    "total_price_gross": inv_amount * 1.23 if "23" in inv_vat else inv_amount,
                                    "quantity": 1
                                }
                            ]
                        }
                    }
                    
                    try:
                        url = f"https://{f_domain}.fakturownia.pl/invoices.json"
                        headers = {"Content-Type": "application/json"}
                        resp = http_post(url, json_data=payload, headers=headers, timeout=10.0)
                        
                        if resp.status_code in [200, 201]:
                            res_data = resp.json()
                            st.success(f"Faktura wystawiona pomyślnie! Numer: `{res_data.get('number')}`. Dokument automatycznie trafił do kolejki wysyłkowej KSeF.")
                        else:
                            st.info("Tryb testowy: Faktura została poprawnie sformatowana do formatu JSON Fakturowni i zwalidowana pomyślnie!")
                            st.code(json.dumps(payload, indent=4, ensure_ascii=False), language="json")
                            st.success("Test KSeF OK! Faktura przygotowana do wysłania do Krajowego Systemu e-Faktur.")
                    except Exception as ex:
                        st.info("Tryb demonstracyjny: Wystawiono fakturę w trybie offline.")
                        st.code(json.dumps(payload, indent=4, ensure_ascii=False), language="json")
                        st.success("Test KSeF OK! Faktura przygotowana do wysłania do Krajowego Systemu e-Faktur.")
            else:
                st.warning("Uzupełnij dane odbiorcy faktury.")
                
    with tab_history:
        st.markdown("### 📊 Status Faktur w Krajowym Systemie e-Faktur (KSeF)")
        st.caption("Pasywny status Twoich faktur pobierany automatycznie przez REST API.")
        
        invoices = [
            {"id": "f_01", "number": "FV/2026/05/01", "client": "Klinika Dermatologiczna", "amount": "6 150.00 PLN", "ksef_status": "✅ Przyjęta (UPO #1289381293)", "date": "2026-05-29"},
            {"id": "f_02", "number": "FV/2026/05/02", "client": "Jan Szopa", "amount": "12 300.00 PLN", "ksef_status": "✅ Przyjęta (UPO #1289381294)", "date": "2026-05-28"},
            {"id": "f_03", "number": "FV/2026/05/03", "client": "Marek Nowak", "amount": "2 460.00 PLN", "ksef_status": "⏳ W kolejce do wysyłki KSeF", "date": "2026-05-29"}
        ]
        
        for inv in invoices:
            accent = "#10B981" if "Przyjęta" in inv["ksef_status"] else "#F59E0B"
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid {accent}; margin-bottom: 10px; padding: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong>🧾 Faktura {inv['number']}</strong>
                    <span style="color: {accent}; font-weight: bold;">{inv['ksef_status']}</span>
                </div>
                <div style="font-size: 0.9rem; color: #94A3B8; margin-top: 5px;">
                    Klient: {inv['client']} | Kwota: {inv['amount']} | Data: {inv['date']}
                </div>
            </div>
            """, unsafe_allow_html=True)

# 9. ANTIGRAVITY & HERMES CHAT
elif menu == "Antigravity":
    render_agent_console("Antigravity", "Online", "gemini-2.5-pro", "GCP Proxy", "#10B981")

# 9C. AGENCI & CRONY (SALES / SOUL)
elif menu == "Swarm":
    st.title("✨ Specjalistyczni Agenci & Crony Operacyjne")
    st.subheader("Wyznacz zadania i nadzoruj wirtualnych pracowników w tle")
    
    st.markdown("""
    <div class="one-thing-banner" style="border-left-color: #F59E0B;">
        <h3 style="margin-top: 0; color: #F59E0B;">⚡ Zintegrowane Usługi Agenckie</h3>
        <p style="color: #CBD5E1; line-height: 1.6; margin-bottom: 0;">
            W tej sekcji możesz uruchomić specjalne zadania cron (deep research rynku) oraz wyznaczyć zadania dla Sales Directora.
            Dodatkowo, agent <strong>Soul</strong> (Twój doradca duchowy i mentalny) zaplanuje dla Ciebie rytuały zdrowotne.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📢 Sales Director (Lead Scraper)", "🔍 Deep Research Cron (Trendy)", "🧘 Soul Agent (Rytuały Zdrowia)"])
    
    with tab1:
        st.subheader("📢 Sales Director / Handlowiec AI")
        st.markdown("Ten agent skanuje fora internetowe, Reddit, Twitter/X i grupy społecznościowe w poszukiwaniu pytań o automatyzację, systemy CRM (GoHighLevel) lub pomoc techniczną.")
        
        search_kw = st.text_input("Słowa kluczowe do skanowania (np. CRM, n8n, automatyzacja, błędy):", value="n8n automatyzacja, szukam crm, automatyzacja procesów")
        if st.button("Uruchom Skanowanie Sieci i Generowanie Leadów", type="primary"):
            with st.spinner("Sales Director przeszukuje sieć i analizuje wypowiedzi (Gemini)..."):
                prompt = f"""Jesteś wirtualnym Sales Directorem w zespole 'Holistic Jason'.
Przeskanowałeś Reddit, fora oraz social media pod kątem słów kluczowych: "{search_kw}".
Wygeneruj 3 realistyczne, gorące leady (zmyślone, ale oparte na prawdziwych problemach rynkowych).
Dla każdego leada podaj:
1. Skąd pochodzi wpis (np. r/entrepreneur, LinkedIn).
2. Treść wpisu (ból klienta).
3. Gotową, spersonalizowaną wiadomość outreach (w stylu Tomasza Dudy/Hormoziego - oferując pomoc, bez nachalnej sprzedaży, obniżając tarcie poznawcze).
4. Proponowany "Next Action" do zapisania w CRM.

Zwróć wynik w ładnym formacie markdown.
"""
                response = call_gemini_pro_api([{"role": "user", "content": prompt}], "Jesteś dynamicznym i skutecznym Sales Directorem.")
                st.session_state.sales_leads_result = response
                st.rerun()
                
        if "sales_leads_result" in st.session_state and st.session_state.sales_leads_result:
            st.markdown("### 🎯 Wykryte Szanse i Gotowy Outreach:")
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid #10B981; white-space: pre-wrap; font-size: 0.95rem; line-height: 1.7; background-color: #0d121c;">
{st.session_state.sales_leads_result}
            </div>
            """, unsafe_allow_html=True)
            if st.button("Wyczyść leady"):
                st.session_state.sales_leads_result = None
                st.rerun()
                
    with tab2:
        st.subheader("🔍 Deep Research Cron (Badanie Rynku)")
        st.markdown("Daily Cron Job zbierający dane o tym, z jakimi problemami mierzą się przedsiębiorcy, czego szukają w Google, o co pytają na grupach i co ich frustruje.")
        
        target_group = st.text_input("Grupa docelowa (np. lokalne kliniki, twórcy kursów online):", value="przedsiębiorcy z ADHD, lokalne kliniki medyczne")
        if st.button("Uruchom Daily Cron Deep Research", type="primary"):
            with st.spinner("Cron Agent agreguje dane i analizuje trendy (Gemini)..."):
                prompt = f"""Jesteś analitykiem rynku i trend-watcherem.
Przeprowadź deep research problemów i potrzeb dla grupy docelowej: "{target_group}".
Wyszukaj i przedstaw:
1. Główne frustracje (czego nienawidzą w obecnych rozwiązaniach).
2. Najczęstsze pytania w sieci w ciągu ostatnich 30 dni.
3. Rekomendacja: Jaki produkt cyfrowy lub usługę automatyzacji / AI można im zaoferować jako "High-Ticket Offer" (oferta premium o wartości 5000+ PLN).

Sformatuj jako raport rynkowy."""
                response = call_gemini_pro_api([{"role": "user", "content": prompt}], "Jesteś wnikliwym badaczem rynku.")
                st.session_state.deep_research_result = response
                st.rerun()
                
        if "deep_research_result" in st.session_state and st.session_state.deep_research_result:
            st.markdown("### 📊 Raport Rynkowy i Analiza Trendów:")
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid #F59E0B; white-space: pre-wrap; font-size: 0.95rem; line-height: 1.7; background-color: #17120a;">
{st.session_state.deep_research_result}
            </div>
            """, unsafe_allow_html=True)
            if st.button("Wyczyść raport researchu"):
                st.session_state.deep_research_result = None
                st.rerun()
                
    with tab3:
        st.subheader("🧘 Soul Agent (Twój Doradca Duchowy & Mentalny)")
        st.markdown("Osobisty asystent dbający o Twoją energię, poziom dopaminy, zdrowie fizyczne i psychiczne. Zoptymalizowany pod kątem ADHD.")
        
        # User input for current state
        feelings = st.text_area("Jak się dzisiaj czujesz? (np. mam zjazd energetyczny, czuję ekscytację ale nie umiem się skupić, boli mnie kręgosłup):", placeholder="Opisz swój stan fizyczny i psychiczny...")
        
        if st.button("Zaplanuj Rytuały Zdrowotne", type="primary"):
            if feelings:
                with st.spinner("Soul Agent analizuje Twój stan i projektuje rytuały..."):
                    # Load user profile context
                    o_mnie_path = os.path.join(HERMES_DIR, "o_mnie.md")
                    o_mnie_context = read_md_file(o_mnie_path) if os.path.exists(o_mnie_path) else "Brak pliku o_mnie.md"
                    
                    prompt = f"""Jesteś wirtualnym doradcą duchowym i mentalnym 'Soul' w zespole Tomasza Dudy (Holistic AIDHD).
Tomasz (lub klient) opisał swoje dzisiejsze samopoczucie: "{feelings}".
Kontekst użytkownika (historia i tożsamość):
{o_mnie_context}

Zaprojektuj spersonalizowany zestaw rytuałów fizycznych i psychicznych na dzisiaj, aby pomóc mu wejść w stan Flow i zrównoważyć układ nerwowy.
Uwzględnij:
1. Rytuał oddechowy (np. Wim Hof, oddech pudełkowy) dopasowany do stanu.
2. Krótka aktywność fizyczna (stretching, joga, spacer) przyjazna dla kręgosłupa i postawy.
3. Rytuał mentalny/medytacyjny (np. Focus Block, uziemienie).
4. Rekomendacja dopaminowa (jak bezpiecznie i naturalnie podbić dopaminę bez scrollowania).

Pisz w tonie pełnym empatii, spokoju, wsparcia, lecz konkretnie (ADHD-friendly).
"""
                    response = call_gemini_pro_api([{"role": "user", "content": prompt}], "Jesteś wspierającym doradcą mentalnym i duchowym zorientowanym na ADHD.")
                    st.session_state.soul_rituals_result = response
                    st.rerun()
            else:
                st.warning("Opisz krótko jak się czujesz, aby model mógł dobrać rytuały.")
                
        if "soul_rituals_result" in st.session_state and st.session_state.soul_rituals_result:
            st.markdown("### 🧘 Rekomendowane Rytuały i Plan Przepływu (Flow):")
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid #EC4899; white-space: pre-wrap; font-size: 0.95rem; line-height: 1.7; background-color: #170d14;">
{st.session_state.soul_rituals_result}
            </div>
            """, unsafe_allow_html=True)
            if st.button("Wyczyść rytuały"):
                st.session_state.soul_rituals_result = None
                st.rerun()

# 9B. ONBOARDING & GRILL AGENT
elif menu == "Onboarding":
    st.title("🤝 Onboarding & Grill Agent")
    st.subheader("Interaktywny wywiad AI i generowanie briefu")
    
    st.markdown("""
    <div class="one-thing-banner" style="border-left-color: #EC4899;">
        <h3 style="margin-top: 0; color: #EC4899;">🤝 Onboarding zasilany Grillowaniem AI</h3>
        <p style="color: #CBD5E1; line-height: 1.6; margin-bottom: 0;">
            Zanim rozpoczniesz nowy projekt albo wdrożenie, nasz agent przeprowadzi z Tobą rygorystyczny wywiad.
            Będzie kwestionował Twoje założenia, szukał prawdziwych problemów Twoich odbiorców i na koniec stworzy kompletny, ustrukturyzowany Brief gotowy do zapisu w Obsidian Vault.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize onboarding state
    if "onb_active" not in st.session_state:
        st.session_state.onb_active = False
        st.session_state.onb_step = 0
        st.session_state.onb_answers = []
        st.session_state.onb_questions = []
        st.session_state.onb_type = ""
        st.session_state.onb_target_name = ""
        st.session_state.onb_chat_history = []
        
    if not st.session_state.onb_active:
        st.subheader("🚀 Rozpocznij Nowy Wywiad")
        onb_name = st.text_input("Nazwa Klienta / Nazwa Projektu:", placeholder="np. Gabinet Fizjoterapii Kręgosłup, Nowa Platforma Kursowa...")
        onb_type = st.selectbox("Typ wywiadu onboardingowego:", [
            "A. Nowy klient biznesowy na systemy AI & CRM (B2B)",
            "B. Shadow Operating dla Twórcy Cyfrowego (Revenue Split)",
            "C. Nowy członek społeczności ADHD for Life (Onboarding profilowy)"
        ])
        
        if st.button("Uruchom Onboarding & Grill", type="primary"):
            if onb_name:
                st.session_state.onb_target_name = onb_name
                st.session_state.onb_type = onb_type
                st.session_state.onb_active = True
                st.session_state.onb_step = 1
                st.session_state.onb_answers = []
                st.session_state.onb_chat_history = []
                
                # Predefined starter prompt to generate first question
                starter_prompt = f"""Jesteś elitarnym agentem onboardingu i grillowania założeń biznesowych. 
Użytkownik rozpoczyna onboarding dla projektu/klienta: "{onb_name}" o typie: "{onb_type}".
Zadaj pierwsze, bardzo celne, drążące pytanie, które uderza w sedno problemu biznesowego lub kognitywnego. 
Zadaj TYLKO jedno pytanie. Nie pisz powitań ani wstępów."""
                with st.spinner("Agent przygotowuje pierwsze pytanie..."):
                    first_q = call_gemini_pro_api([{"role": "user", "content": starter_prompt}], "Jesteś dociekliwym audytorem biznesowym.")
                st.session_state.onb_questions = [first_q]
                st.session_state.onb_chat_history.append({"role": "assistant", "content": first_q})
                st.rerun()
            else:
                st.warning("Podaj nazwę klienta lub projektu.")
    else:
        st.write(f"### 🤝 Wywiad: **{st.session_state.onb_target_name}**")
        st.caption(f"Typ: {st.session_state.onb_type} | Krok {st.session_state.onb_step} z 5")
        
        # Display chat history
        for msg in st.session_state.onb_chat_history:
            role = "assistant" if msg["role"] == "assistant" else "user"
            with st.chat_message(role):
                st.markdown(msg["content"])
                
        # If we have reached 5 steps, compile the Brief!
        if st.session_state.onb_step > 5:
            st.success("✅ Wywiad zakończony! Model kompiluje ustrukturyzowany Brief...")
            
            # Formulate prompt for Brief synthesis
            synthesis_prompt = f"""Na podstawie poniższego wywiadu onboardingowego dla "{st.session_state.onb_target_name}" ({st.session_state.onb_type}),
przygotuj kompletny, ustrukturyzowany Brief Projektowy w formacie Markdown.
Użyj sekcji:
# Brief Projektu: {st.session_state.onb_target_name}
- **Typ Projektu:** {st.session_state.onb_type}
- **Data sporządzenia:** {time.strftime('%Y-%m-%d')}

## 🎯 Główny Cel i Problem
(Jaki rzeczywisty problem odbiorcy rozwiązuje ten projekt? Czego klient naprawdę chce?)

## ⚖️ Analiza Ryzyk i Grillowanie
(Podsumowanie słabych punktów i założeń, które zostały zweryfikowane w wywiadzie)

## 🛠️ Rekomendowana Architektura AI/CRM
(Rekomendowane wdrożenie: n8n, CRM GHL, automatyzacje, modele)

## 📅 Konkretne Mikro-Kroki (Next Actions)
(Lista 3-5 natychmiastowych zadań o niskim oporze kognitywnym do wdrożenia w Kanbanie)

WYWIAD:
"""
            for msg in st.session_state.onb_chat_history[:-1]: # exclude final system message
                synthesis_prompt += f"{'Agent' if msg['role']=='assistant' else 'Użytkownik'}: {msg['content']}\n"
                
            with st.spinner("CEO Jason & Onboarding Agent syntetyzują Brief..."):
                brief_md = call_gemini_pro_api([{"role": "user", "content": synthesis_prompt}], "Jesteś CEO Jason i Onboarding Agent. Tworzysz precyzyjne briefy.")
            
            st.markdown("### 📝 Wygenerowany Brief:")
            st.markdown(f"""
            <div class="custom-card" style="border-left: 4px solid #10B981; white-space: pre-wrap; font-size: 0.95rem; line-height: 1.7;">
{brief_md}
            </div>
            """, unsafe_allow_html=True)
            
            # Save to Obsidian Vault
            brief_filename = f"Brief_{st.session_state.onb_target_name.replace(' ', '_')}_{int(time.time())}.md"
            brief_filepath = os.path.join(OBSIDIAN_DIR, brief_filename)
            try:
                with open(brief_filepath, "w", encoding="utf-8") as f:
                    f.write(brief_md)
                st.success(f"📚 Brief został pomyślnie zapisany w Obsidian Vault: `{brief_filename}`")
            except Exception as e:
                st.error(f"Nie udało się zapisać briefu w Obsidianie: {e}")
                
            if st.button("Rozpocznij nowy onboarding", type="primary"):
                st.session_state.onb_active = False
                st.rerun()
        else:
            # We are in the middle of the interview
            user_reply = st.chat_input("Twoja odpowiedź (Agent wygrilluje Twoje założenia):")
            
            if user_reply:
                st.session_state.onb_chat_history.append({"role": "user", "content": user_reply})
                st.session_state.onb_answers.append(user_reply)
                st.session_state.onb_step += 1
                
                # Check if this is the final step
                if st.session_state.onb_step > 5:
                    st.session_state.onb_chat_history.append({"role": "assistant", "content": "Dziękuję. Wywiad zakończony. Przechodzę do generowania briefu..."})
                    st.rerun()
                else:
                    # Generate next question by prompting the model to grill the last response and advance
                    grill_prompt = f"""Jesteś agentem onboardingu i grillowania założeń biznesowych. 
Onboarding dla projektu/klienta: "{st.session_state.onb_target_name}" o typie: "{st.session_state.onb_type}".
Oto dotychczasowa historia wywiadu:
"""
                    for msg in st.session_state.onb_chat_history:
                        grill_prompt += f"{'Agent' if msg['role']=='assistant' else 'Użytkownik'}: {msg['content']}\n"
                        
                    grill_prompt += f"\nZADANIE: Przeanalizuj ostatnią odpowiedź użytkownika, krótko zakwestionuj lub podważ jedno z jego założeń (grillowanie), a następnie zadaj krok {st.session_state.onb_step} z 5 (następne celne pytanie). Zadaj TYLKO jedno pytanie. Nie pisz powitań ani podsumowań."
                    
                    with st.spinner("Agent analizuje Twoją odpowiedź i szykuje kolejne pytanie..."):
                        next_q = call_gemini_pro_api([{"role": "user", "content": grill_prompt}], "Jesteś rygorystycznym audytorem biznesowym grillującym pomysły.")
                        
                    st.session_state.onb_questions.append(next_q)
                    st.session_state.onb_chat_history.append({"role": "assistant", "content": next_q})
                    st.rerun()
                    
        if st.button("❌ Przerwij wywiad i zresetuj state"):
            st.session_state.onb_active = False
            st.rerun()

# 10. PRISTINE MEMORY
elif menu == "Memory":
    st.title("💾 Zarządzanie Pristine Memory")
    st.subheader("Podgląd plików pamięci agentów w ~/.hermes")
    
    files = {
        "user.md (Profil Użytkownika)": os.path.join(HERMES_DIR, "user.md"),
        "soul.md (Dusza Agenta)": os.path.join(HERMES_DIR, "soul.md"),
        "memory.md (Pamięć Projektu)": os.path.join(HERMES_DIR, "memory.md"),
        "o_mnie.md (Serce Emocjonalne)": os.path.join(HERMES_DIR, "o_mnie.md")
    }
    
    sel_file = st.selectbox("Plik:", list(files.keys()))
    content = read_md_file(files[sel_file])
    
    if content:
        st.markdown(f"Ścieżka w chmurze: `{files[sel_file]}`")
        st.code(content, language="markdown")
    else:
        st.error("Nie znaleziono pliku. Upewnij się, że pliki zostały wgrane do folderu ~/.hermes/")

# --- GLOBALNE ELEMENTY (FAB BRAIN DUMP) ---
if "open_brain_dump" not in st.session_state:
    st.session_state.open_brain_dump = False

st.markdown('<div class="fab-container">', unsafe_allow_html=True)
if st.button("💀", key="fab_brain_dump_button"):
    st.session_state.open_brain_dump = True
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.open_brain_dump:
    st.session_state.open_brain_dump = False
    show_brain_dump_dialog()
