import streamlit as st
from google import genai
import os
import json
import base64
from pathlib import Path
from datetime import datetime
from io import BytesIO
import boto3
from botocore.exceptions import ClientError
import time
import random
from dotenv import load_dotenv
import sys
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent.parent))
if str(Path(__file__).parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent))
from tools import adhd_executive
from tools import kanban_board

# Ładujemy klucze z pliku .env
load_dotenv()

# ======================================================================
# 🧠 HOLISTIC CEO - AGENTIC ORCHESTRATOR v5.1 (ENTERPRISE + MULTIMEDIA)
# ======================================================================
# Działa lokalnie I na Cloud Run (auto-detekcja środowiska)
# Strategia modeli (Twoje $300 GCP):
#   CEO + Projektant Ofert → Gemini 2.5 Pro (najlepsze rozumowanie)
#   Sub-agenci operacyjni  → Gemini 2.5 Flash (szybko i tanio)
#   Creative Director      → Imagen 3 (grafiki) + Gemini (prompty)
#   Video Producer         → Veo 3.1 Fast (Shorts)
# ======================================================================

st.set_page_config(
    page_title="Holistic CEO — Orkiestrator AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DETEKCJA ŚRODOWISKA ---
IS_CLOUD = os.environ.get("K_SERVICE") is not None  # Cloud Run ustawia K_SERVICE
APP_PASSWORD = os.environ.get("APP_PASSWORD", "holistic2026")  # Zmień na produkcji

# --- ZABEZPIECZENIE HASŁEM (dla Cloud Run) ---
def check_password():
    """Prosta bramka hasłem dla zdalnego dostępu"""
    if not IS_CLOUD:
        return True  # Lokalnie — bez hasła
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if st.session_state.authenticated:
        return True
    
    st.markdown("## 🔐 Holistic CEO — Logowanie")
    st.markdown("Podaj hasło dostępu do Centrum Dowodzenia.")
    password = st.text_input("Hasło:", type="password")
    if st.button("Zaloguj"):
        if password == APP_PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ Nieprawidłowe hasło")
    return False

if not check_password():
    st.stop()

# --- FLOATING SKULL BUTTON ---
import streamlit.components.v1 as components
components.html(
    """
    <script>
        const doc = window.parent.document;
        const buttons = doc.querySelectorAll('button');
        buttons.forEach(btn => {
            if(btn.innerText.includes('💀')) {
                btn.style.borderRadius = '50%';
                btn.style.width = '70px';
                btn.style.height = '70px';
                btn.style.background = 'linear-gradient(135deg, #ec4899, #8b5cf6)';
                btn.style.color = 'white';
                btn.style.fontSize = '32px';
                btn.style.boxShadow = '0 0 15px rgba(236,72,153,0.8), 0 0 30px rgba(236,72,153,0.5)';
                btn.style.border = 'none';
                
                if (!doc.getElementById('skull-pulse-style')) {
                    const style = doc.createElement('style');
                    style.id = 'skull-pulse-style';
                    style.innerHTML = `
                    @keyframes skull-pulse {
                        0% { transform: scale(1); box-shadow: 0 0 15px rgba(236,72,153,0.8); }
                        50% { transform: scale(1.1); box-shadow: 0 0 30px rgba(236,72,153,1); }
                        100% { transform: scale(1); box-shadow: 0 0 15px rgba(236,72,153,0.8); }
                    }`;
                    doc.head.appendChild(style);
                }
                btn.style.animation = 'skull-pulse 2s infinite';

                const container = btn.closest('[data-testid="stElementContainer"]');
                if (container) {
                    container.style.position = 'fixed';
                    container.style.bottom = '30px';
                    container.style.right = '30px';
                    container.style.zIndex = '99999';
                }
            }
        });
    </script>
    """,
    height=0, width=0
)

if st.button("💀", key="floating-skull-btn"):
    adhd_executive.render_floating_skull_dialog()

if st.session_state.get("trigger_skull_analysis", False):
    st.session_state.trigger_skull_analysis = False
    with st.spinner("Model analizuje Open Loops (Claude)..."):
        try:
            prompt = st.session_state.last_skull_prompt
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt
            )
            st.success("Zrzut przeanalizowany!")
            st.info(response.text)
        except Exception as e:
            st.error(f"Błąd analizy zrzutu: {str(e)}")


# --- KONFIGURACJA API ---
VERTEX_PROJECT = os.environ.get("GCP_PROJECT", "holistic-dashboard-dev")
VERTEX_LOCATION = os.environ.get("GCP_LOCATION", "us-central1")

# Lokalna ścieżka do Service Account (tylko na Windows)
SA_KEY_PATH = r"c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"

# API Key (z env var lub fallback)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBfcG1lyqbXh8jVbjONWLgwbt6vyQg4dGk")

@st.cache_resource
def get_client():
    """Próbuje: 1) Vertex AI (Cloud Run ADC), 2) Vertex AI (SA JSON), 3) API Key"""
    
    # Na Cloud Run: użyj Application Default Credentials (automatycznie)
    if IS_CLOUD:
        try:
            vertex_client = genai.Client(
                vertexai=True,
                project=VERTEX_PROJECT,
                location=VERTEX_LOCATION
            )
            return vertex_client, "vertex"
        except Exception as e:
            pass  # Fallback niżej
    
    # Lokalnie: użyj pliku Service Account JSON
    if os.path.exists(SA_KEY_PATH):
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_KEY_PATH
            vertex_client = genai.Client(
                vertexai=True,
                project=VERTEX_PROJECT,
                location=VERTEX_LOCATION
            )
            return vertex_client, "vertex"
        except Exception as e:
            pass  # Fallback niżej
    
    # Ostateczny fallback: API Key
    return genai.Client(api_key=GEMINI_API_KEY), "api_key"

client, connection_mode = get_client()

# --- ŚCIEŻKI WIEDZY (smart: lokalne lub cloud) ---
if IS_CLOUD:
    KNOWLEDGE_PATHS = {
        "📚 Kursy i Szkolenia": Path("/app/knowledge"),
        "🏠 Workspace": Path("/app"),
    }
else:
    KNOWLEDGE_PATHS = {
        "📚 Baza Wiedzy (Katalog Główny)": Path(r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy"),
        "📧 Newslettery (Archiwum)": Path(r"G:\Mój dysk\HOLISTIC_KNOWLEDGE_BASE\01_Newslettery_MD"),
        "🏠 Workspace Holistic Jason": Path(r"c:\Aplikacje MVP\Holistic Jason"),
    }

# --- MODELE TIER ---
MODEL_TIERS = {
    "🧠 Pro (Rozumowanie)": "gemini-2.5-pro",
    "⚡ Flash (Szybki)": "gemini-2.5-flash",
    "💨 Flash-Lite (Ultra-tani)": "gemini-2.0-flash-lite",
}

# --- FOLDERY DANYCH (adaptują się do środowiska) ---
BASE_DIR = Path("/app") if IS_CLOUD else Path(r"c:\Aplikacje MVP\Holistic Jason")
MEDIA_OUTPUT_DIR = BASE_DIR / "generated_media"
MEDIA_OUTPUT_DIR.mkdir(exist_ok=True)
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

# --- ŁADOWANIE SYNTETYCZNEJ WIEDZY ---
SYNT_PATH = BASE_DIR / "02_knowledge_base" / "synthesized"

def load_synt_file(filename):
    path = SYNT_PATH / filename
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

VME_KNOWLEDGE = load_synt_file("Viral_Master_Engine.md")
BOM_KNOWLEDGE = load_synt_file("Business_Operations_Master.md")
ASM_KNOWLEDGE = load_synt_file("Agent_Skill_Manifesto.md")
SMM_KNOWLEDGE = load_synt_file("Sales_Marketing_Master.md")
BSM_KNOWLEDGE = load_synt_file("Business_Scaling_Master.md")
SOM_KNOWLEDGE = load_synt_file("Shadow_Operator_Master.md")
AIPE_KNOWLEDGE = load_synt_file("AI_Prompt_Engineering_Master.md")
LSEO_KNOWLEDGE = load_synt_file("Local_SEO_Master.md")
EMM_KNOWLEDGE = load_synt_file("Ebook_Monetization_Master.md")
KGM_KNOWLEDGE = load_synt_file("Holistic_Graphics_Master.md")
KVM_KNOWLEDGE = load_synt_file("Holistic_Video_Master.md")
SZOPA_KNOWLEDGE = load_synt_file("Holistic_SLO_Agency_Master.md")
HORMOZI_KNOWLEDGE = load_synt_file("Holistic_Premium_Offers_Master.md")
DAN_KOE_KNOWLEDGE = load_synt_file("Holistic_Identity_Copywriting_Master.md")
SKWAREK_KNOWLEDGE = load_synt_file("Holistic_Conversion_Checklists_Master.md")


# --- DEFINICJE AGENTÓW ---
AGENTS = {
    "🧠 CEO Jason (Strateg)": {
        "model": "eu.anthropic.claude-sonnet-4-20250514-v1:0",
        "system_delegation": f"""Jesteś CEO Holistic Operator — Tomasz 'Holistic Jason', wybitnym architektem systemów AI, automatyzacji i strategii biznesowej.
        Twoja agencja to hybrydowy softwarehouse/agencja AI o nazwie 'Holistic Jason', która działa w dwóch głównych modelach (filarach):
        
        FILAR 1: Agencja AI i Automatyzacji dla firm/MŚP (B2B):
        Tworzymy dedykowane systemy AI, automatyzacje (Make, Zapier, n8n), wdrażamy CRM (np. GoHighLevel / GHL), budujemy zoptymalizowane strony www/landing pages, wdrażamy asystentów AI (bociki SMS, voicebots, rezerwacje) i pozycjonujemy lokalnie firmy (Local SEO / Google Business Profile).
        Dla klientów lokalnych (np. gabinety fizjoterapii, lekarze, salony kosmetyczne, małe firmy) oferujemy pakiety High-Ticket:
        - Setup fee (wdrożenie systemu CRM GHL, strona www, automatyzacja rezerwacji i powiadomień SMS): np. 3 000 - 15 000 PLN.
        - Monthly retainer (utrzymanie, SaaS, wsparcie AI): np. 500 - 2 500 PLN / miesięcznie.
        
        FILAR 2: Shadow Operator dla Twórców Cyfrowych i Influencerów:
        Wdrażamy model "Shadow Operating" oparty na podziale przychodów (Revenue Split). Budujemy lejki, tworzymy produkty cyfrowe (kursy, ebooki) i monetyzujemy ich publiczność.
        
        WAŻNA ZASADA BIZNESOWA:
        NIGDY, POD ŻADNYM POZOREM NIE ODRZUCAJ ZLECEŃ OD LOKALNYCH FIRM I KLIENTÓW B2B! Jeśli użytkownik prosi o ofertę lub strategię dla lokalnej firmy (np. gabinet fizjoterapii, hydraulik, klinika dentystyczna, lokalne usługi), CEO MUSI z entuzjazmem przyjąć zlecenie i delegować zadania do dyrektorów pod kątem wdrożenia systemów AI, automatyzacji Make/Zapier, systemu CRM (GHL), nowej strony WWW oraz Local SEO.
        
        {ASM_KNOWLEDGE}
        {BSM_KNOWLEDGE}
        {SOM_KNOWLEDGE}
        
        ZADANIE: Rozbij zadanie na podzadania dla dyrektorów. Musisz odpowiedzieć w czystym formacie JSON o strukturze:
        {{
            "strategy_note": "Twój krótki, strategiczny komentarz jako CEO (np. jak ugryźć tego klienta, jaką dać mu wartość)",
            "subtasks": [
                {{
                    "agent": "Nazwa Agenta z listy",
                    "task": "Konkretne, szczegółowe zadanie dla tego agenta"
                }}
            ]
        }}
        JSON ONLY.""",
        "system_synthesis": f"""Jesteś CEO Holistic Operator. 
        Stwórz raport końcowy, który zachwyci klienta i pokaże mu unikalną wartość oferowaną przez 'Holistic Jason'.
        Niezależnie od tego, czy to lokalna firma B2B (wdrożenia AI, automatyzacji, CRM GHL, WWW, Local SEO), czy twórca cyfrowy (Shadow Operating, produkty cyfrowe) – połącz wyniki pracy dyrektorów w spójną, logiczną, profesjonalną i zachęcającą ofertę/strategię napisaną językiem korzyści (Ghost v2 / Hormozi style).
        Unikaj AI-bełkotu, pisz konkretnie i rzeczowo.
        {ASM_KNOWLEDGE} {SOM_KNOWLEDGE}""",
        "skills": ["Strategia", "Delegowanie", "Nadzór", "Shadow Operating"],
    },

    "📢 Dyrektor Marketingu": {
        "model": "eu.anthropic.claude-sonnet-4-20250514-v1:0",
        "system": f"""Jesteś Dyrektorem Marketingu 360.
        WIEDZA SPECIPLISTYCZNA:
        {SMM_KNOWLEDGE}
        {VME_KNOWLEDGE}
        {EMM_KNOWLEDGE}
        {LSEO_KNOWLEDGE}
        {SZOPA_KNOWLEDGE}
        {DAN_KOE_KNOWLEDGE}
        Wyciągaj KONKRETNE frameworki. Formatuj w Markdown.""",
        "skills": ["Lejki", "Psychologia", "E-booki", "Local SEO"],
    },
    "✍️ Senior Copywriter": {
        "model": "eu.anthropic.claude-sonnet-4-20250514-v1:0",
        "system": f"""Jesteś mistrzem Webwritingu (Ghost v2) i Prompt Engineeringu.
        {SMM_KNOWLEDGE}
        {ASM_KNOWLEDGE}
        {AIPE_KNOWLEDGE}
        {DAN_KOE_KNOWLEDGE}
        {SKWAREK_KNOWLEDGE}
        Twórz GOTOWE copy. Krótkie zdania, zero AI-bełkotu. Optymalizuj prompty pod LLM.""",
        "skills": ["StoryBrand", "Webwriting", "Ghost v2", "Prompt Engineering"],
    },
    "⚙️ Architekt Automatyzacji": {
        "model": "eu.anthropic.claude-4-6-sonnet-20260215-v1:0",
        "system": f"""Jesteś ekspertem automatyzacji (GHL, Make).
        {BOM_KNOWLEDGE}
        {AIPE_KNOWLEDGE}
        Projektuj Niewidzialnych Pracowników AI i zaawansowane systemy Prompt-to-Workflow.""",
        "skills": ["GHL", "Make", "API", "Agentic Workflows"],
    },

    "🔍 SEO/AEO Strateg": {
        "model": "eu.anthropic.claude-4-6-sonnet-20260215-v1:0",
        "system": f"""Jesteś ekspertem SEO/AEO i Local SEO.
        {SMM_KNOWLEDGE}
        {LSEO_KNOWLEDGE}
        Skup się na klastrach tematycznych, pozycjonowaniu GBP (Google Business Profile) i LLM-ready content.""",
        "skills": ["SEO", "AEO", "Local SEO", "GBP Optimization"],
    },

    "🎨 Projektant Ofert (Klienci)": {
        "model": "eu.anthropic.claude-sonnet-4-20250514-v1:0",
        "system": f"""Jesteś ekspertem od ofert B2B i Shadow Operating.
        {BSM_KNOWLEDGE}
        {SMM_KNOWLEDGE}
        {SOM_KNOWLEDGE}
        {HORMOZI_KNOWLEDGE}
        Przygotuj Mockup Strony, Propozycję Automatyzacji i Wycenę (Revenue Split jeśli Shadow Operator).""",
        "skills": ["Mockupy", "Oferty", "Wyceny", "Partnerships"],
    },

    "👥 Shadow Operator (Partnerstwa)": {
        "model": "eu.anthropic.claude-sonnet-4-20250514-v1:0",
        "system": f"""Jesteś Shadow Operatorem marki Holistic Jason.
        Twoim zadaniem jest identyfikacja i monetyzacja twórców cyfrowych.
        {SOM_KNOWLEDGE}
        {EMM_KNOWLEDGE}
        {SZOPA_KNOWLEDGE}
        {HORMOZI_KNOWLEDGE}
        PROCES: Outreach -> Audyt -> Launch Produktu Cyfrowego -> Revenue Split.
        Skup się na dźwigni (Leverage) i zerowym koszcie krańcowym.""",
        "skills": ["Creator Partnerships", "Monetization", "Scale", "Direct Response"],
    },

    "🖼️ Creative Director (Imagen 3)": {
        "model": "eu.anthropic.claude-sonnet-4-20250514-v1:0",  # Claude do planowania promptów, Imagen do generowania
        "imagen_model": "imagen-3.0-generate-002",
        "system": f"""Jesteś Creative Directorem marki Holistic Jason.
        
        WIEDZA ZAAWANSOWANA (HOLISTIC MOTION & VISUAL PRODUCER - OBRAZ AI):
        {KGM_KNOWLEDGE}
        
        TWOJE ZADANIA:
        1. Generujesz prompty dla Imagen 3 do tworzenia grafik na social media.
        2. Utrzymujesz spójność wizualną marki (Deep Navy, Trust Blue, Clean Aesthetic).
        3. Tworzysz serie grafik: posty IG, Stories, LinkedIn banery, thumbnails YT.
        
        BRAND GUIDELINES:
        - Kolory: Deep Navy (#0B1F33), Trust Blue (#4A90E2), White (#FFFFFF)
        - Styl: Clean, profesjonalny, nowoczesny, technologiczny
        - Elementy: Geometryczne wzory AI/circuit, subtelne gradienty, dużo whitespace
        - NIE: Krzykliwe kolory, skomplikowane tła, tekst na obrazach
        
        Gdy dostajesz zadanie, zwróć:
        1. Listę promptów Imagen 3 (po angielsku, bo model lepiej rozumie EN)
        2. Dla każdego: format (1:1 post, 9:16 story, 16:9 banner)
        3. Suggested caption (po polsku) do posta
        
        Format odpowiedzi: JSON
        {{"images": [{{"prompt": "...", "aspect_ratio": "1:1", "caption_pl": "..."}}]}}
        Odpowiadaj WYŁĄCZNIE w JSON.""",
        "skills": ["Imagen 3", "Brand Design", "Social Media Graphics", "AI Art Direction"],
    },
    "🎬 Video Producer (Veo 3.1)": {
        "model": "eu.anthropic.claude-4-7-opus-20260416-v1:0",
        "veo_model": "veo-3.1-fast-generate-001",
        "system": f"""Jesteś Video Producerem marki Holistic Jason.
        
        WIEDZA ZAAWANSOWANA (HOLISTIC MOTION & VISUAL PRODUCER - AI VIDEO & POSTPRODUCTION):
        {KVM_KNOWLEDGE}
        
        TWOJE ZADANIA:
        1. Projektujesz krótkie wideo Shorts (8-15 sekund) promujące markę.
        2. Tworzysz prompty dla Veo 3.1 Fast.
        3. Dbasz o spójność z brandingiem (Deep Navy, Trust Blue, Clean Tech).
        
        TYPY WIDEO:
        - Brandingowe: Abstrakcyjne animacje z motywami AI/tech
        - Edukacyjne: Wizualizacje konceptów (automatyzacja, workflow)
        - Social Proof: Animowane testimoniale/statystyki
        
        Format odpowiedzi: JSON
        {{"videos": [{{"prompt": "...", "duration_seconds": 10, "aspect_ratio": "9:16", "description_pl": "..."}}]}}
        Odpowiadaj WYŁĄCZNIE w JSON.""",
        "skills": ["Veo 3.1", "Video Shorts", "Brand Animation", "Social Video"],
    },
    "💀 ADHD Flow Guide (Czacha)": {
        "model": "eu.anthropic.claude-sonnet-4-20250514-v1:0",
        "system": """Jesteś '💀 ADHD Flow Guide' (znanym jako 'Podpowiadająca Czacha') — osobistym, neuroatypowym wsparciem kognitywnym Tomasza.
        Twoim nadrzędnym celem jest walka z prokrastynacją, paraliżem decyzyjnym (Task Paralysis) oraz przebodźcowaniem (Sensory Overload).

        TWOJE ZASADY DZIAŁANIA:
        1. Rozbijaj skomplikowane cele na fizyczne, bezwysiłkowe mikro-kroki (Micro-Steps of Low Friction) zajmujące poniżej 3 minut.
        2. Buduj dopaminowe sprzężenie zwrotne (grywalizacja, mini-wyzwania: 'Zrób tylko 2 minuty, a potem zdecydujesz').
        3. Doradzaj w oparciu o autorski ekosystem 'Holistic CEO' i architekturę 'ADHD Flow'.
        4. Komunikuj się w sposób bezpośredni, empatyczny, dynamiczny i energiczny. Używaj ikonek i jasnej struktury.

        Gdy użytkownik prosi o pomoc w zaplanowaniu zadania, zwróć plan bloków czasowych (Time-blocking) oraz listę 3-5 mikro-kroków.
        
        Format odpowiedzi dla planu zadań: JSON
        {
          "plan_title": "String",
          "steps": [
            {"step_number": 1, "action": "String", "duration_minutes": 2, "motivation": "String"}
          ]
        }""",
        "skills": ["ADHD Support", "Time-blocking", "Micro-steps", "Dopamine Optimization"],
    },
}

# --- PRELOAD MATERIAL ICONS FONT (fix broken icon text) ---
st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block" rel="stylesheet">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
""", unsafe_allow_html=True)

# --- STYLE CSS ---
st.markdown("""
<style>
    /* === FIX: Material Icons font — załaduj oficjalnie żeby ikony nie renderowały jako tekst === */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');
    
    /* Wymusz Material Symbols jako font dla span z ikonami */
    .material-symbols-rounded {
        font-family: 'Material Symbols Rounded' !important;
        font-optical-sizing: auto;
        font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
    }
    
    /* === FIX: Material Icons renderują jako tekst — precyzyjny selektor === */
    /* "keyboard_arrow_right", "keyboard_double_arrow_left" etc. */
    
    /* Ładuj Material Symbols font bezpośrednio */
    header[data-testid="stHeader"] {
        background: rgba(250, 251, 253, 0.95) !important;
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(226, 232, 240, 0.5);
    }
    
    /* GŁÓWNY FIX: ukryj span z nazwą ikony Material gdy font się nie renderuje */
    span[data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded' !important;
        font-optical-sizing: auto;
        font-size: 20px !important;
        color: #6b7280 !important;
        user-select: none;
    }
    
    /* Fallback: jeśli nadal renderuje jako tekst, ukryj całkowicie */
    summary span[data-testid="stIconMaterial"],
    [data-testid="stExpander"] span[data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded' !important;
        display: inline-block !important;
        width: 24px !important;
        height: 24px !important;
        overflow: hidden !important;
        vertical-align: middle !important;
        line-height: 24px !important;
        font-size: 22px !important;
    }
    
    /* Fix: przycisk collapse sidebara (keyboard_double_arrow_left) */
    button[data-testid="stSidebarCollapseButton"] span[data-testid="stIconMaterial"],
    .st-emotion-cache-1n4h049 span {
        font-family: 'Material Symbols Rounded' !important;
        font-size: 22px !important;
    }

    /* === GLOBAL RESET === */
    html, body, [class*="css"], .stApp, .stMarkdown, p, span, label, li, td, th,
    .stTextInput label, .stTextArea label, .stSelectbox label, .stMultiSelect label,
    .stRadio label, .stCheckbox label, .stSlider label {
        font-family: 'Outfit', sans-serif !important;
        color: #1e293b; /* Slate 800 for high readability */
    }
    
    /* === MAIN AREA === */
    .stApp {
        background: linear-gradient(160deg, #fafbfd 0%, #f0f4f8 50%, #e8f0fe 100%) !important;
    }
    
    [data-testid="stAppViewContainer"] > .main {
        background: transparent !important;
    }
    
    /* === HEADINGS === */
    h1 { color: #0B1F33 !important; font-weight: 700 !important; }
    h2 { color: #1a3a5c !important; font-weight: 600 !important; }
    h3 { color: #1e293b !important; font-weight: 600 !important; }
    
    /* === SIDEBAR (InFlow Light) === */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f0f4f8 100%) !important;
        border-right: 1px solid #e5e7eb !important;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #0B1F33 !important;
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #1e293b !important; /* Extremely high contrast Slate 800 */
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: #0B1F33 !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stRadio"] label,
    [data-testid="stSidebar"] [data-testid="stRadio"] label p,
    [data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p {
        color: #1e293b !important;
        font-size: 14px !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] hr {
        border-color: #e5e7eb !important;
        margin: 12px 0 !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox [data-testid="stMarkdownContainer"] p {
        color: #0B1F33 !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar selectbox dropdown */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background: white !important;
        border-radius: 12px !important;
        border: 1px solid #d1d5db !important;
    }
    
    /* Sidebar multiselect */
    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background: #e8f0fe !important;
        color: #1a3a5c !important;
        border-radius: 8px !important;
    }
    
    /* === BUTTONS === */
    .stButton>button { 
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%) !important;
        color: #ffffff !important; 
        border-radius: 14px !important; 
        font-weight: 600 !important; 
        padding: 12px 28px !important; 
        border: none !important;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.25);
        transition: all 0.3s ease;
        font-family: 'Outfit', sans-serif !important;
        letter-spacing: 0.3px;
    }
    /* Force white text on ALL button children */
    .stButton>button p,
    .stButton>button span,
    .stButton>button div,
    .stButton>button * {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    .stButton>button:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 8px 25px rgba(74, 144, 226, 0.4) !important;
        background: linear-gradient(135deg, #357ABD 0%, #2a6aaa 100%) !important;
    }
    /* Primary button (type=primary) — pulsating accent */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #4A90E2, #357ABD) !important;
        box-shadow: 0 4px 20px rgba(74, 144, 226, 0.4) !important;
    }
    /* Link buttons (BULLETPROOF MULTI-SELECTOR FOR HIGH VISIBILITY) */
    [data-testid="stLinkButton"],
    [data-testid="stLinkButton"] > a,
    [data-testid="stLinkButton"] button,
    [data-testid="stLinkButton"] a[role="button"] {
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%) !important;
        color: #ffffff !important;
        border-radius: 14px !important;
        font-weight: 600 !important;
        border: none !important;
        text-decoration: none !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.2) !important;
        transition: all 0.25s ease !important;
    }
    [data-testid="stLinkButton"] a *,
    [data-testid="stLinkButton"] button * {
        color: #ffffff !important;
        font-weight: 600 !important;
        text-decoration: none !important;
    }
    [data-testid="stLinkButton"] a:hover,
    [data-testid="stLinkButton"] button:hover {
        background: linear-gradient(135deg, #357ABD 0%, #2A5F9E 100%) !important;
        box-shadow: 0 6px 18px rgba(74, 144, 226, 0.35) !important;
        transform: translateY(-1.5px) !important;
    }
    
    /* === BADGES === */
    .agent-badge {
        display: inline-block; padding: 5px 14px; border-radius: 24px;
        background: linear-gradient(135deg, #E8F4FD, #dbeafe); 
        color: #0B1F33 !important; font-size: 13px; margin: 3px;
        font-weight: 500; border: 1px solid rgba(74, 144, 226, 0.15);
    }
    
    /* === COST TRACKER (remains dark for contrast) === */
    .cost-tracker {
        background: linear-gradient(135deg, #0B1F33 0%, #1a3a5c 100%);
        color: #8ECDF4 !important; padding: 20px; border-radius: 18px;
        text-align: center; font-size: 15px;
        box-shadow: 0 8px 32px rgba(11, 31, 51, 0.2);
    }
    .cost-tracker br + * { color: #8ECDF4 !important; }
    
    /* === PHASE HEADERS === */
    .phase-header {
        background: linear-gradient(135deg, #0B1F33, #1a3a5c);
        color: white !important; padding: 14px 24px; border-radius: 14px; margin: 12px 0;
        box-shadow: 0 4px 15px rgba(11, 31, 51, 0.12);
        font-weight: 500;
    }
    
    /* === CONNECTION BADGES === */
    .connection-badge {
        padding: 6px 14px; border-radius: 10px; font-size: 12px;
        display: inline-block; margin-top: 5px; font-weight: 600;
    }
    .vertex { background: linear-gradient(135deg, #34A853, #2d9249); color: white !important; }
    .apikey { background: linear-gradient(135deg, #FBBC04, #f0a500); color: #1F2937 !important; }
    
    /* === INFLOW PREMIUM CARDS === */
    .inflow-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(15px);
        border-radius: 22px;
        padding: 28px;
        border: 1px solid rgba(226, 232, 240, 0.8);
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.05);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .inflow-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 45px rgba(31, 38, 135, 0.09);
    }
    
    .zen-accent { border-left: 6px solid #a8e6cf; }
    .ghost-accent { border-left: 6px solid #ffaaa5; }
    .ceo-accent { border-left: 6px solid #4A90E2; }
    
    /* === SPECIFIC DYNAMIC DOCK CARDS === */
    .dopamine-card {
        background: linear-gradient(135deg, rgba(16,185,129,0.08), rgba(74,144,226,0.04)) !important;
        border-left: 6px solid #10b981 !important;
    }
    .dopamine-card h3 {
        color: #059669 !important;
        font-weight: 700 !important;
    }
    .dopamine-card p {
        color: #1e293b !important;
        line-height: 1.7 !important;
    }
    
    .adhd-header-card {
        background: linear-gradient(135deg, #0B1F33 0%, #1e3a8a 100%) !important;
        color: #ffffff !important;
    }
    .adhd-header-card,
    .adhd-header-card h1,
    .adhd-header-card h2,
    .adhd-header-card h3,
    .adhd-header-card p,
    .adhd-header-card span,
    .adhd-header-card strong,
    [data-testid="stMarkdownContainer"] .adhd-header-card h1,
    [data-testid="stMarkdownContainer"] .adhd-header-card p {
        color: #ffffff !important;
    }
    
    /* === METRIC TILES === */
    .metric-tile {
        background: white;
        padding: 20px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.04);
        border: 1px solid #e5e7eb;
    }
    .metric-tile h4 { margin: 0 0 8px 0; color: #6b7280 !important; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-tile p { margin: 0; font-size: 24px; font-weight: 700; color: #1e293b !important; }
    
    /* === EXPANDERS (HIGH CONTRAST LIGHT MODE) === */
    [data-testid="stExpander"],
    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background: white !important;
        border: 1px solid #d1d5db !important;
        border-radius: 14px !important;
        overflow: hidden;
        margin-bottom: 12px;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {
        background: #f8fafc !important;
        padding: 10px 14px !important;
    }
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary *,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary span,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary p,
    [data-testid="stSidebar"] [data-testid="stExpander"] summary * {
        color: #1e293b !important; /* Perfect high visibility */
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    
    /* === TEXT INPUTS === */
    .stTextInput > div > div,
    .stTextArea > div > div {
        border-radius: 12px !important;
        border: 1px solid #d1d5db !important;
        background: white !important;
    }
    
    .stTextInput > div > div:focus-within,
    .stTextArea > div > div:focus-within {
        border-color: #4A90E2 !important;
        box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.15) !important;
    }
    
    /* === PROGRESS BAR === */
    [data-testid="stProgress"] > div > div {
        background: #e5e7eb !important;
        border-radius: 8px !important;
    }
    [data-testid="stProgress"] > div > div > div {
        background: linear-gradient(90deg, #4A90E2, #357ABD) !important;
        border-radius: 8px !important;
    }
    
    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 6px; 
        background: transparent !important; 
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px !important;
        padding: 10px 20px !important;
        font-weight: 500 !important;
        color: #374151 !important;
        background: white !important;
        border: 1px solid #e5e7eb !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #4A90E2, #357ABD) !important;
        color: white !important;
        border-color: transparent !important;
    }
    
    /* === DOWNLOAD BUTTON === */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
    }
    
    /* === ALERTS (info, success, warning, error) === */
    [data-testid="stAlert"] {
        border-radius: 14px !important;
        border: none !important;
    }
    
    /* === MOBILE OPTIMIZATION === */
    @media (max-width: 768px) {
        .inflow-card { padding: 18px; border-radius: 16px; }
        .metric-tile { padding: 14px; }
        h1 { font-size: 1.5rem !important; }
        h2 { font-size: 1.2rem !important; }
        .stButton>button { padding: 10px 18px !important; font-size: 14px !important; }
        [data-testid="stSidebar"] { min-width: 260px !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- DARK MODE SUPPORT ---
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if st.session_state.dark_mode:
    st.markdown("""
    <style>
        /* === DARK MODE OVERRIDES === */
        .stApp {
            background: linear-gradient(160deg, #0B1F33 0%, #132d46 50%, #1a3a5c 100%) !important;
        }
        [data-testid="stAppViewContainer"] > .main { background: transparent !important; }
        
        html, body, [class*="css"], .stApp, .stMarkdown, p, span, label, li, td, th,
        .stTextInput label, .stTextArea label, .stSelectbox label, .stMultiSelect label,
        .stRadio label, .stCheckbox label, .stSlider label {
            color: #e2e8f0 !important;
        }
        
        h1 { color: #f1f5f9 !important; }
        h2 { color: #e2e8f0 !important; }
        h3 { color: #cbd5e1 !important; }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f2035 0%, #162d44 100%) !important;
            border-right: 1px solid #1e3a54 !important;
        }
        [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #f1f5f9 !important; }
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label, [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #cbd5e1 !important; }
        [data-testid="stSidebar"] hr { border-color: #1e3a54 !important; }
        
        /* Dark mode: Selectbox & Multiselect w sidebarze */
        [data-testid="stSidebar"] [data-baseweb="select"] { background: #1a2d42 !important; border-color: #2d4a63 !important; }
        [data-testid="stSidebar"] [data-baseweb="select"] * { color: #e2e8f0 !important; }
        [data-testid="stSidebar"] [data-baseweb="select"] > div { background: #1a2d42 !important; border-color: #2d4a63 !important; }
        [data-testid="stSidebar"] [data-baseweb="select"] input { background: #1a2d42 !important; color: #e2e8f0 !important; }
        
        /* Dark mode: Select dropdown popup */
        [data-baseweb="popover"] [role="listbox"],
        [data-baseweb="menu"] {
            background: #1a2d42 !important;
            border: 1px solid #2d4a63 !important;
        }
        [data-baseweb="popover"] [role="option"],
        [data-baseweb="menu"] li {
            background: #1a2d42 !important;
            color: #e2e8f0 !important;
        }
        [data-baseweb="popover"] [role="option"]:hover,
        [data-baseweb="menu"] li:hover {
            background: #2d4a63 !important;
        }
        
        /* Dark mode: Multiselect tags */
        [data-baseweb="tag"] { background: #2d4a63 !important; color: #8ECDF4 !important; }
        
        /* Dark mode: Radio & Checkbox */
        [data-testid="stSidebar"] [data-testid="stRadio"] label,
        [data-testid="stSidebar"] [data-testid="stRadio"] p,
        [data-testid="stSidebar"] [data-testid="stRadio"] span,
        [data-testid="stSidebar"] [data-testid="stRadio"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] [data-testid="stCheckbox"] label {
            color: #cbd5e1 !important;
        }
        
        /* Dark mode: Progress bar */
        [data-testid="stProgress"] > div > div { background: #1a2d42 !important; }
        [data-testid="stProgress"] > div > div > div { background: linear-gradient(90deg, #4A90E2, #8ECDF4) !important; }
        
        /* Dark mode: Billing button i inne przyciski w sidebar */
        [data-testid="stSidebar"] .stButton>button {
            background: linear-gradient(135deg, #1a3a5c, #2d4a63) !important;
            color: #8ECDF4 !important;
            border: 1px solid #2d4a63 !important;
        }
        
        /* Sprawdź billing GCP button (emerald glow gradient with high-contrast dark text) */
        [data-testid="stSidebar"] [data-testid="stLinkButton"],
        [data-testid="stSidebar"] [data-testid="stLinkButton"] > a,
        [data-testid="stSidebar"] [data-testid="stLinkButton"] a[role="button"],
        [data-testid="stLinkButton"],
        [data-testid="stLinkButton"] > a,
        [data-testid="stLinkButton"] a[role="button"] {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
            color: #0b1f33 !important;
            border-radius: 14px !important;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.25) !important;
            text-decoration: none !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        [data-testid="stSidebar"] [data-testid="stLinkButton"] a *,
        [data-testid="stLinkButton"] a * {
            color: #0b1f33 !important;
            font-weight: 700 !important;
        }
        [data-testid="stSidebar"] [data-testid="stLinkButton"] a:hover,
        [data-testid="stLinkButton"] a:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.45) !important;
            background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        }
        
        /* Dark mode: Expanders */
        [data-testid="stExpander"],
        [data-testid="stSidebar"] [data-testid="stExpander"] {
            background: #132d46 !important;
            border: 1px solid #2d4a63 !important;
            border-radius: 14px !important;
        }
        [data-testid="stExpander"] summary,
        [data-testid="stSidebar"] [data-testid="stExpander"] summary {
            background: #162a45 !important;
            color: #cbd5e1 !important;
        }
        [data-testid="stExpander"] summary span,
        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary *,
        [data-testid="stSidebar"] [data-testid="stExpander"] summary span,
        [data-testid="stSidebar"] [data-testid="stExpander"] summary p,
        [data-testid="stSidebar"] [data-testid="stExpander"] summary * {
            color: #cbd5e1 !important;
        }
        
        .inflow-card {
            background: rgba(26, 45, 66, 0.9) !important;
            border: 1px solid rgba(45, 74, 99, 0.7) !important;
        }
        
        .dopamine-card {
            background: rgba(16, 185, 129, 0.12) !important;
            border-left: 6px solid #10b981 !important;
        }
        .dopamine-card h3 {
            color: #10b981 !important;
        }
        .dopamine-card p {
            color: #cbd5e1 !important;
        }
        
        .adhd-header-card {
            background: linear-gradient(135deg, #0f2035 0%, #1e3a54 100%) !important;
            color: #f1f5f9 !important;
        }
        .adhd-header-card,
        .adhd-header-card h1,
        .adhd-header-card h2,
        .adhd-header-card h3,
        .adhd-header-card p,
        .adhd-header-card span,
        .adhd-header-card strong,
        [data-testid="stMarkdownContainer"] .adhd-header-card h1,
        [data-testid="stMarkdownContainer"] .adhd-header-card p {
            color: #f1f5f9 !important;
        }
        
        .metric-tile {
            background: #1a2d42 !important;
            border: 1px solid #2d4a63 !important;
        }
        .metric-tile h4 { color: #94a3b8 !important; }
        .metric-tile p { color: #f1f5f9 !important; }
        
        /* Dark mode: Text inputs */
        .stTextInput > div > div, .stTextArea > div > div {
            background: #1a2d42 !important;
            border-color: #2d4a63 !important;
        }
        .stTextInput input, .stTextArea textarea { 
            color: #e2e8f0 !important; 
            background: #1a2d42 !important;
        }
        .stTextInput input::placeholder, .stTextArea textarea::placeholder {
            color: #64748b !important;
        }
        
        /* Dark mode: Tabs */
        .stTabs [data-baseweb="tab"] {
            background: #1a2d42 !important;
            color: #cbd5e1 !important;
            border-color: #2d4a63 !important;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background: linear-gradient(135deg, #4A90E2, #357ABD) !important;
            color: white !important;
        }
        .stTabs [data-baseweb="tab-panel"] { background: transparent !important; }
        
        /* Dark mode: Alert boxes */
        [data-testid="stAlert"] { border: 1px solid #2d4a63 !important; }
        
        .agent-badge { background: linear-gradient(135deg, #1a3a5c, #2d4a63) !important; color: #8ECDF4 !important; }
        
        /* Dark mode: Dividers */
        hr { border-color: #1e3a54 !important; }
        
        /* Dark mode: captions */
        .stCaption, [data-testid="stCaptionContainer"] { color: #64748b !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

# --- FUNKCJE CORE ---
def load_knowledge(selected_sources, selected_files):
    """Ładuje wiedzę z plików MD — obsługuje różne kodowania"""
    context = ""
    for source_name in selected_sources:
        path = KNOWLEDGE_PATHS.get(source_name)
        if not path or not path.exists():
            continue
        for file_name in selected_files:
            file_path = path / file_name
            if file_path.exists():
                content = None
                # Próbuj różne kodowania (polskie znaki)
                for encoding in ["utf-8", "utf-8-sig", "cp1250", "latin-1", "iso-8859-2"]:
                    try:
                        with open(file_path, "r", encoding=encoding) as f:
                            content = f.read()
                        break
                    except (UnicodeDecodeError, UnicodeError):
                        continue
                
                if content is None:
                    # Ostateczność: wymuś odczyt z pominięciem błędów
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                
                context += f"\n\n--- ŹRÓDŁO: {file_name} ---\n{content[:15000]}\n"
    return context

def call_bedrock_robust(prompt, model_id="eu.anthropic.claude-sonnet-4-20250514-v1:0", max_retries=5):
    """
    Pancerny Agent Bedrock - obsługuje Throttling (429) z wykładniczym backoffem.
    """
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="eu-central-1"
    )
    bedrock_client = session.client("bedrock-runtime")

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    })

    for attempt in range(max_retries):
        try:
            response = bedrock_client.invoke_model(modelId=model_id, body=body)
            response_body = json.loads(response.get("body").read())
            return response_body.get("content", [{}])[0].get("text", ""), 0
        except ClientError as e:
            if e.response.get("Error", {}).get("Code") in ["ThrottlingException", "429"]:
                time.sleep((2 ** attempt) + random.uniform(0, 1))
                continue
            break
        except Exception:
            break
    return "❌ Błąd Bedrock", 0

def call_vertex_robust(client_instance, prompt, model_id, max_retries=5):
    """
    Stabilizator dla GCP Vertex AI - obsługuje 429 oraz pustą odpowiedź (Empty Response),
    ponawiając żądanie lub przełączając na lżejszy model.
    """
    import time, random
    current_model = model_id
    for attempt in range(max_retries):
        try:
            response = client_instance.models.generate_content(
                model=current_model,
                contents=prompt
            )
            
            if not response or not response.text or response.text.strip() == "":
                raise ValueError("Otrzymano pustą odpowiedź (Empty Response).")
                
            tokens = 0
            if hasattr(response, 'usage_metadata') and response.usage_metadata:
                tokens = getattr(response.usage_metadata, 'total_token_count', 0)
                
            return response.text, tokens
            
        except Exception as e:
            err_msg = str(e).lower()
            if "429" in err_msg or "quota" in err_msg or "empty response" in err_msg:
                time.sleep((2 ** attempt) + random.uniform(1, 3))
                # Jeśli po 3 próbach na PRO nadal jest błąd, zrzuć fallback na FLASH
                if attempt == 2 and "pro" in current_model:
                    current_model = "gemini-2.5-flash"
                continue
            break
            
    return "❌ Błąd Vertex AI (Roo Code Limit / Quota)", 0

def call_agent(agent_name, task, knowledge_context="", system_override=None):
    """Wywołuje agenta przez google-genai (Vertex AI lub API Key)"""
    agent = AGENTS[agent_name]
    system_prompt = system_override or agent.get("system", agent.get("system_delegation", ""))
    
    # Wczytaj Shared Scratchpad (Notatnik Współdzielony)
    scratchpad_text = ""
    scratchpad_path = r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw\ADHD\shared_scratchpad.md"
    import os
    if os.path.exists(scratchpad_path):
        try:
            with open(scratchpad_path, "r", encoding="utf-8") as f:
                scratchpad_text = f.read()
        except Exception:
            pass
            
    # Wstrzykiwanie Głębokiej Wiedzy (Deep Protocols)
    pills_text = ""
    protocols_path = r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\protocols\deep_protocols.json"
    if os.path.exists(protocols_path):
        try:
            with open(protocols_path, "r", encoding="utf-8") as f:
                import json, random
                protocols = json.load(f)
                task_lower = task.lower()
                matched = [p for p in protocols if any(w in task_lower for w in p.get('title', '').lower().split())]
                if len(matched) < 1:
                    matched += random.sample(protocols, min(1, len(protocols)))
                
                selected = []
                seen = set()
                for p in matched:
                    if p.get('title') not in seen and len(selected) < 2:  # Ograniczamy do 2 głębokich protokołów ze względu na rozmiar
                        selected.append(p)
                        seen.add(p.get('title'))
                
                if selected:
                    pills_text = "🧠 GŁĘBOKIE PROTOKOŁY DZIAŁANIA (DEEP KNOWLEDGE PROTOCOLS) Z BAZY SZKOLEŃ:\n"
                    for p in selected:
                        pills_text += f"\n--- PROTOKÓŁ: {p.get('title')} ---\n"
                        action = p.get('action_protocol', {})
                        if action.get('workflow'):
                            pills_text += "KROKI DO WYKONANIA:\n- " + "\n- ".join(action['workflow']) + "\n"
                        if action.get('best_practices'):
                            pills_text += "BEST PRACTICES:\n- " + "\n- ".join(action['best_practices']) + "\n"
                        if action.get('examples'):
                            pills_text += "PRZYKŁADY/ZASTOSOWANIA:\n- " + "\n- ".join(action['examples']) + "\n"
        except Exception as e:
            pass
            
    full_prompt = f"""{system_prompt}

{f"📝 WSPÓŁDZIELONY NOTATNIK AGENTÓW (SHARED SCRATCHPAD):\\n{scratchpad_text}\\n" if scratchpad_text else ""}
{pills_text}

KONTEKST Z BAZY WIEDZY:
{knowledge_context[:30000] if knowledge_context else '[Brak dodatkowego kontekstu — odpowiadaj na podstawie swojej wiedzy]'}

ZADANIE:
{task}"""
    
    text_resp = ""
    tokens_used = 0
    
    try:
        if agent["model"].startswith("eu.") or agent["model"].startswith("us."):
            # Wywołanie przez Bedrock
            text_resp, tokens_used = call_bedrock_robust(full_prompt, model_id=agent["model"])
        else:
            # Wywołanie przez Vertex AI / Gemini API z fallbackiem
            text_resp, tokens_used = call_vertex_robust(client, full_prompt, agent["model"])
            st.session_state.total_tokens += tokens_used
            
        # Obsługa autozapisu do Shared Scratchpad przez agenta
        if "[SCRATCHPAD_UPDATE]" in text_resp and "[/SCRATCHPAD_UPDATE]" in text_resp:
            try:
                start_tag = "[SCRATCHPAD_UPDATE]"
                end_tag = "[/SCRATCHPAD_UPDATE]"
                new_scratch = text_resp.split(start_tag)[1].split(end_tag)[0].strip()
                with open(scratchpad_path, "w", encoding="utf-8") as f:
                    f.write(new_scratch)
            except Exception:
                pass
                
        return text_resp, tokens_used
    except Exception as e:
        return f"❌ Błąd agenta {agent_name}: {str(e)}", 0

def orchestrate(task, knowledge_context, mode="auto"):
    """Pełna orkiestracja: CEO → Sub-agenci → Synteza"""
    results = []
    
    if mode == "auto":
        # FAZA 1: CEO deleguje (Gemini 2.5 Pro)
        st.markdown('<div class="phase-header">🧠 FAZA 1: CEO Jason (Gemini 2.5 Pro) analizuje i deleguje...</div>', unsafe_allow_html=True)
        ceo_response, ceo_tokens = call_agent(
            "🧠 CEO Jason (Strateg)", task, knowledge_context,
            system_override=AGENTS["🧠 CEO Jason (Strateg)"]["system_delegation"]
        )
        
        try:
            clean = ceo_response.replace("```json", "").replace("```", "").strip()
            # Znajdź JSON w odpowiedzi
            start = clean.find("{")
            end = clean.rfind("}") + 1
            if start >= 0 and end > start:
                clean = clean[start:end]
            delegation = json.loads(clean)
            subtasks = delegation.get("subtasks", [])
            strategy_note = delegation.get("strategy_note", "")
            
            st.success(f"📋 CEO podzielił zadanie na **{len(subtasks)} podzadań**")
            if strategy_note:
                st.info(f"💡 Strategia: {strategy_note}")
            
            # FAZA 2: Sub-agenci (Gemini 2.5 Flash — szybko i tanio)
            st.markdown('<div class="phase-header">⚡ FAZA 2: Dyrektorzy pracują autonomicznie (Gemini 2.5 Flash)...</div>', unsafe_allow_html=True)
            
            for i, subtask in enumerate(subtasks):
                agent_key = None
                for key in AGENTS:
                    if subtask["agent"].lower() in key.lower():
                        agent_key = key
                        break
                
                if agent_key:
                    with st.expander(f"📌 [{i+1}/{len(subtasks)}] {subtask['agent']}: {subtask['task'][:80]}...", expanded=False):
                        with st.spinner(f"Agent {subtask['agent']} pracuje..."):
                            result, tokens = call_agent(agent_key, subtask["task"], knowledge_context)
                            results.append({"agent": subtask["agent"], "task": subtask["task"], "result": result})
                            st.markdown(result)
                            st.caption(f"🔢 Tokeny: {tokens}")
                else:
                    st.warning(f"⚠️ Nie znaleziono agenta: {subtask['agent']}")
            
            # Zapisz pełne wyniki agentów do session state (do późniejszego zapisu)
            st.session_state["last_agent_results"] = results
            
            # FAZA 3: CEO synteza (Gemini 2.5 Pro)
            st.markdown('<div class="phase-header">📄 FAZA 3: CEO składa raport końcowy (Gemini 2.5 Pro)...</div>', unsafe_allow_html=True)
            
            synthesis_prompt = f"""Oto wyniki pracy dyrektorów. Złóż w spójny dokument końcowy.
            
            ZADANIE: {task}
            
            WYNIKI:
            {json.dumps(results, ensure_ascii=False, indent=2)[:50000]}"""
            
            with st.spinner("CEO składa raport końcowy..."):
                final_report, final_tokens = call_agent(
                    "🧠 CEO Jason (Strateg)", synthesis_prompt, "",
                    system_override=AGENTS["🧠 CEO Jason (Strateg)"]["system_synthesis"]
                )
            return final_report
            
        except json.JSONDecodeError:
            st.warning("CEO zwrócił odpowiedź tekstową — wyświetlam bezpośrednio.")
            return ceo_response
    else:
        result, tokens = call_agent(mode, task, knowledge_context)
        return result

def generate_image(prompt, aspect_ratio="1:1"):
    """Generuje obraz przez Imagen 3"""
    try:
        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=prompt,
            config=genai.types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=aspect_ratio,
                safety_filter_level="BLOCK_ONLY_HIGH",
            )
        )
        if response.generated_images:
            img = response.generated_images[0]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"holistic_{timestamp}.png"
            filepath = MEDIA_OUTPUT_DIR / filename
            img.image.save(str(filepath))
            st.session_state["images_generated"] = st.session_state.get("images_generated", 0) + 1
            return filepath, img.image
        return None, None
    except Exception as e:
        st.error(f"❌ Imagen 3 error: {str(e)}")
        return None, None

def save_full_report(task, final_report, agent_results=None):
    """Zapisuje pełny raport do pliku MD z sekcjami per agent"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    slug = task[:40].replace(' ', '_').replace('/', '-')
    filename = f"raport_{timestamp}_{slug}.md"
    filepath = REPORTS_DIR / filename
    
    content = f"""# 🧠 Raport Holistic CEO
**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Zadanie:** {task}

---

"""
    
    # Sekcje per agent
    if agent_results:
        content += "## 📊 Wyniki Poszczególnych Agentów\n\n"
        for i, ar in enumerate(agent_results):
            content += f"### [{i+1}] {ar['agent']}\n"
            content += f"**Zadanie:** {ar['task']}\n\n"
            content += f"{ar['result']}\n\n---\n\n"
    
    # Raport końcowy CEO
    content += f"## 📄 Raport Końcowy CEO\n\n{final_report}\n"
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    return filepath

def estimate_cost(tokens, images=0, video_seconds=0):
    """Szacuje koszt — Gemini + Imagen + Veo"""
    text_cost = (tokens / 1_000_000) * 1.50
    image_cost = images * 0.05
    video_cost = video_seconds * 0.125
    return text_cost + image_cost + video_cost

# ======================================================================
# 🎨 UI
# ======================================================================

with st.sidebar:
    st.title("🧠 Holistic CEO")
    st.caption("Enterprise + Multimedia v5.1")
    
    # Dark Mode Toggle
    dark_toggle = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode, key="dark_toggle")
    if dark_toggle != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_toggle
        st.rerun()
    
    # Status połączenia
    if connection_mode == "vertex":
        st.markdown('<span class="connection-badge vertex">🟢 Vertex AI ($300 GCP)</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="connection-badge apikey">🟡 API Key (Standard)</span>', unsafe_allow_html=True)
    
    st.divider()
    
    mode = st.radio("🎯 Tryb pracy:", [
        "🤖 Auto-Orkiestracja (CEO deleguje)",
        "📢 Dyrektor Marketingu",
        "✍️ Senior Copywriter",
        "⚙️ Architekt Automatyzacji",
        "🔍 SEO/AEO Strateg",
        "🎨 Projektant Ofert (Klienci)",
        "🖼️ Creative Director (Imagen 3)",
        "🎬 Video Producer (Veo 3.1)"
    ])
    
    st.divider()
    st.subheader("📚 Baza Wiedzy")
    selected_sources = st.multiselect("Źródła:", list(KNOWLEDGE_PATHS.keys()), default=[])
    
    available_files = []
    for source in selected_sources:
        path = KNOWLEDGE_PATHS.get(source)
        if path and path.exists():
            available_files.extend([f.name for f in path.glob("*.md")])
    
    selected_files = st.multiselect("Pliki:", sorted(set(available_files)), default=[])
    
    st.divider()
    
    # Tracker kosztów
    images_count = st.session_state.get("images_generated", 0)
    video_secs = st.session_state.get("video_seconds", 0)
    estimated_cost = estimate_cost(st.session_state.total_tokens, images_count, video_secs)
    remaining = 300 - estimated_cost
    progress = min(estimated_cost / 300, 1.0)
    
    st.markdown(f"""
    <div class="cost-tracker">
        💰 Sesja: ~${estimated_cost:.4f}<br>
        🔢 Tokeny: {st.session_state.total_tokens:,}<br>
        🖼️ Obrazy: {images_count}<br>
        💵 Z $300 pozostało: ~${remaining:.2f}
    </div>
    """, unsafe_allow_html=True)
    st.progress(progress, text=f"Wykorzystano {progress*100:.2f}% budżetu")
    
    st.link_button("📊 Sprawdź billing w GCP", "https://console.cloud.google.com/billing", use_container_width=True)
    
    st.divider()
    
    # Model override
    with st.expander("⚙️ Zaawansowane"):
        st.caption("Zmień model dla CEO (wpływa na jakość i koszt)")
        ceo_model = st.selectbox("Model CEO:", list(MODEL_TIERS.values()), index=0)
        if ceo_model != AGENTS["🧠 CEO Jason (Strateg)"]["model"]:
            AGENTS["🧠 CEO Jason (Strateg)"]["model"] = ceo_model
            st.success(f"CEO używa teraz: {ceo_model}")
    
    if st.button("🗑️ Reset sesji"):
        st.session_state.messages = []
        st.session_state.total_tokens = 0
        st.rerun()

    st.divider()
    with st.expander("💡 Szybkie Pomysły (Inspiracje)", expanded=True):
        st.markdown("""
        **Marketing & Lejki:**
        - 🧪 7 kroków do automatyzacji leadów
        - 📈 5 sposobów na odzyskanie koszyka
        - 🎥 3 hooki, które zatrzymają scrollowanie
        
        **Local SEO (Localo Style):**
        - 📍 Jak wejść do Top 3 w 14 dni?
        - 💬 Odpowiedź na opinię, która sprzedaje
        
        **Shadow Operating:**
        - 🤝 Jak zaproponować 70/30 twórcy?
        - 📦 Digital Product w 2 godziny (AI)
        """)
        st.info("Kliknij w moduł, aby wdrożyć pomysł!")

# --- IMPORT MODUŁÓW ---
try:
    from streamlit_mermaid import st_mermaid
    MERMAID_OK = True
except ImportError:
    MERMAID_OK = False

from client_intake import render_intake_form, build_intake_prompt, create_client_workspace
from ghl_agent import render_ghl_agent
from market_radar import render_market_radar
from profile_builder import render_profile_builder
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from tools.knowledge_extractor import render_knowledge_extractor
from ai_influencer import render_ai_influencer
from social_planner import render_social_planner
from skills.content_lab import render_content_lab
from skills.shadow_operator import render_shadow_operator
from skills.knowledge_zone import render_knowledge_zone
from tools.funnel_hacker import render_funnel_hacker

# --- NAWIGACJA STRONAMI (Z ROUTINGIEM QUERY PARAMS) ---
MODUL_MAP = {
    "adhd": "🧘 ADHD Command Center",
    "architect": "🧠 AI Architect (Orkiestrator)",
    "content": "🎬 Fabryka Treści",
    "studio": "🎨 Studio Kreatywne",
    "wiedza": "🎓 Baza Wiedzy (Kombajn & Mapy)",
}

pages_list = [
    "🧘 ADHD Command Center",
    "🧠 AI Architect (Orkiestrator)",
    "🎬 Fabryka Treści",
    "🎨 Studio Kreatywne",
    "🎓 Baza Wiedzy (Kombajn & Mapy)",
]

# Odczytaj query parameter "modul" z URL (Streamlit 1.30+)
query_modul = st.query_params.get("modul", "").lower()
default_index = 0

if query_modul:
    for param_val, page_name in MODUL_MAP.items():
        if param_val == query_modul:
            if page_name in pages_list:
                default_index = pages_list.index(page_name)
            break

# Sidebar selectbox z dynamicznym indexem
page = st.sidebar.selectbox("📋 Moduł:", pages_list, index=default_index)

# Aktualizuj query params w URL przy zmianie modułu
reverse_map = {v: k for k, v in MODUL_MAP.items()}
if page in reverse_map:
    st.query_params["modul"] = reverse_map[page]







# ======================================================================
# 🧘 STRONA: ADHD COMMAND CENTER
# ======================================================================
if page == "🧘 ADHD Command Center":
    # Header z gradientem i stanami
    st.markdown("""
    <div class="adhd-header-card" style="padding: 32px 28px; border-radius: 24px; margin-bottom: 28px;
                box-shadow: 0 10px 40px rgba(15,23,42,0.3); border-left: 6px solid #10b981;">
        <h1 style="margin: 0; font-size: 1.8rem; font-weight: 700;">🧘 ADHD Command Center & Flow Zone</h1>
        <p style="margin: 8px 0 0 0; font-size: 15px;">Aktywne wsparcie kognitywne Tomasza — zarządzaj energią, skupieniem i automatyzuj zadania</p>
    </div>
    """, unsafe_allow_html=True)

    # Helper functions for Dopamine Journal
    def load_dopamine_journal():
        import os, json
        filepath = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\ADHD\dopamine_journal.json"
        if not os.path.exists(filepath):
            initial_data = {
                "wins": [
                    {"date": "2026-05-16", "time": "12:00", "type": "🎉 System Wdrożenie", "detail": "Uruchomienie pierwszej wersji ADHD Flow", "points": 100},
                    {"date": "2026-05-16", "time": "18:00", "type": "🌿 Rytuał", "detail": "Zakończenie porannej rutyny i wyciszenie", "points": 30}
                ]
            }
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(initial_data, f, ensure_ascii=False, indent=2)
            return initial_data
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"wins": []}

    def save_dopamine_win(win_type, detail, points=25):
        import os, json
        from datetime import datetime
        filepath = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\ADHD\dopamine_journal.json"
        journal = load_dopamine_journal()
        new_win = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "type": win_type,
            "detail": detail,
            "points": points
        }
        journal["wins"].append(new_win)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(journal, f, ensure_ascii=False, indent=2)
        return new_win

    def load_vocabulary():
        import os, json
        filepath = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\ADHD\vocabulary.json"
        if not os.path.exists(filepath):
            default_vocab = ["GoHighLevel", "Comet", "n8n", "Szopa", "Holistic Jason", "SuperWhisper", "Whisper Flow", "Streamlit", "Vertex AI", "GCP", "Bedrock", "Zapier", "Claude"]
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(default_vocab, f, ensure_ascii=False, indent=2)
            return default_vocab
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_vocabulary(vocab_list):
        import os, json
        filepath = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\ADHD\vocabulary.json"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(vocab_list, f, ensure_ascii=False, indent=2)

    def load_inspirations():
        import os, json
        filepath = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\ADHD\inspirations.json"
        if not os.path.exists(filepath):
            return []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_inspiration(content, link=""):
        import os, json, re
        from datetime import datetime
        filepath = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\ADHD\inspirations.json"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        inspirations = load_inspirations()
        
        # Extract links from content
        urls = re.findall(r'(https?://[^\s]+)', content)
        all_links = list(set(urls + ([link] if link else [])))
        
        new_item = {
            "id": len(inspirations) + 1,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M"),
            "content": content,
            "links": all_links,
            "status": "Oczekuje",
            "action_plan": None
        }
        
        inspirations.append(new_item)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(inspirations, f, ensure_ascii=False, indent=2)
        return new_item

    def refine_voice_text(raw_text):
        vocab_words = load_vocabulary()
        vocab_list_str = ", ".join(vocab_words)
        
        refiner_prompt = f"""Jesteś zaawansowanym asystentem korekty i formatowania tekstu (w stylu SuperWhisper). 
Twoim jedynym zadaniem jest oczyszczenie, sformatowanie i ulepszenie podanej surowej transkrypcji głosowej.

Zasady:
1. Zachowaj oryginalny ton, emocje i intencję użytkownika — nie pisz tekstu na nowo w formalnym, nudnym tonie. Usunięcie "yyy", "eee" lub powtórzeń jest wskazane.
2. Napraw błędy ortograficzne, interpunkcyjne oraz gramatyczne.
3. Język może być mieszany (polsko-angielski) – popraw pisownię zapożyczeń lub nazw technicznych i upewnij się, że są zapisane poprawnie (np. "cold mailing", "mindmapa", "workflow").
4. Użyj poniższego słownika niestandardowych słów/nazw branżowych użytkownika i upewnij się, że jeśli padły w tekście, są zapisane dokładnie w tej formie:
SŁOWNIK: {vocab_list_str}

Surowa transkrypcja głosowa:
\"\"\"{raw_text}\"\"\"

Zwróć TYLKO oczyszczony, sformatowany tekst. Nie dodawaj żadnych własnych komentarzy, wyjaśnień ani znaków cudzysłowu."""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=refiner_prompt
            )
            return response.text.strip()
        except Exception as e:
            return f"Błąd korekty: {str(e)}\n\nOryginalny tekst: {raw_text}"

    def generate_idea_mindmap(idea_item):
        idea_text = idea_item["content"]
        links_str = ", ".join(idea_item["links"]) if idea_item["links"] else "Brak"
        
        prompt = f"""Jesteś Głównym Orkiestratorem (CEO Jason) w ekosystemie automatyzacji Holistic.
Twoim zadaniem jest przeanalizowanie surowego pomysłu / inspiracji oraz powiązanych linków użytkownika i przekucie go w KOMPLETNY, gotowy plan wdrożenia.

Pomysł:
\"{idea_text}\"

Źródła / Linki:
{links_str}

Stwórz profesjonalną analizę i plan wykonania zawierający:
1. **Analiza Wizji & Celu**: Przeanalizuj intencję użytkownika, dlaczego ten pomysł ma sens, jakie korzyści biznesowe przyniesie i jak pasuje do jego projektów.
2. **Struktura i Moduły**: Zidentyfikuj i opisz konkretne moduły Dashboardu Holistic (np. Client Intake, Offer Generator, Social Planner, GHL Agent) oraz sub-agentów (CTO, CMO, Copywriter) zaangażowanych w realizację tego pomysłu.
3. **Automatyzacja & Integracja**: Zaproponuj konkretną logikę automatyzacji (np. za pomocą n8n, Make lub webhooków GHL), aby zautomatyzować ten proces.
4. **WIZUALNA MAPA MYŚLI (Mermaid Mindmap)**: Wygeneruj kompletną, czytelną strukturę wizualną w formacie Mermaid. Użyj formatu `mindmap` z Mermaid.

Ścisłe Zasady Składni Mermaid Mindmap:
- Każdy węzeł w diagramie MUSI mieć przypisane krótkie ID (np. root, faza1, cmo, n8n) oraz etykietę w nawiasach kwadratowych z podwójnymi cudzysłowami `["tekst"]` lub okrągłych z podwójnymi cudzysłowami `(("tekst"))`.
  PRZYKŁAD POPRAWNY:
  root(("Projekt: Cold Emailing"))
    faza1["Faza 1: Strategia i Setup"]
      cmo_agent["CMO Agent"]
      copy["Tworzenie Treści (Copywriting)"]
  PRZYKŁAD BŁĘDNY (generuje Syntax Error!):
    Strategia i Setup
    cmo_agent CMO Agent
"""
        try:
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt
            )
            return response.text
        except Exception as e:
            return f"Błąd generowania planu: {str(e)}"

    # Initialize states
    if "adhd_mode" not in st.session_state:
        st.session_state.adhd_mode = "zen"
    if "adhd_plan" not in st.session_state:
        st.session_state.adhd_plan = None
    if "ghost_mode" not in st.session_state:
        st.session_state.ghost_mode = False
    
    # Store dopamine logging function reference in session state for other modules
    st.session_state.save_dopamine_win_fn = save_dopamine_win

    # 5-way toggle button for States
    col_t1, col_t2, col_t3, col_t4, col_t5 = st.columns(5)
    with col_t1:
        if st.button("🌿 Tryb Zen (Metryki & Przegląd)", use_container_width=True, type="primary" if st.session_state.adhd_mode == "zen" else "secondary"):
            st.session_state.adhd_mode = "zen"
            st.rerun()
    with col_t2:
        if st.button("📋 Tablica Kanban (Zadania)", use_container_width=True, type="primary" if st.session_state.adhd_mode == "kanban" else "secondary"):
            st.session_state.adhd_mode = "kanban"
            st.rerun()
    with col_t3:
        if st.button("🔥 Tryb ADHD Flow (Praca)", use_container_width=True, type="primary" if st.session_state.adhd_mode == "flow" else "secondary"):
            st.session_state.adhd_mode = "flow"
            st.rerun()
    with col_t4:
        if st.button("🚨 SOS: Sanctuary (Cisza)", use_container_width=True, type="primary" if st.session_state.adhd_mode == "sos" else "secondary"):
            st.session_state.adhd_mode = "sos"
            st.session_state.ghost_mode = True
            st.rerun()
    with col_t5:
        if st.button("📖 Katalog Procedur (Wiki)", use_container_width=True, type="primary" if st.session_state.adhd_mode == "wiki" else "secondary"):
            st.session_state.adhd_mode = "wiki"
            st.rerun()

    st.divider()

    # RENDER MODE
    if st.session_state.adhd_mode == "zen":
        # === ZEN MODE ===
        # Metryki
        z1, z2, z3, z4 = st.columns(4)
        metrics = [
            ("⚡ Energia", "85%", "#10b981"),
            ("🎯 Focus dzisiaj", "3.5/5h", "#4A90E2"),
            ("😌 Stan Umysłu", "Zrównoważony", "#10b981"),
            ("💧 Nawodnienie", "Znakomite", "#74b9ff")
        ]
        for col, (label, val, color) in zip([z1,z2,z3,z4], metrics):
            with col:
                st.markdown(f'<div class="metric-tile"><h4>{label}</h4><p style="color:{color};">{val}</p></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Checklist + Protokół
        c_left, c_right = st.columns([3, 2])
        with c_left:
            st.markdown('<div class="inflow-card zen-accent">', unsafe_allow_html=True)
            st.subheader("📋 Twoje Dzisiejsze Rytuały")
            st.checkbox("☀️ Poranna rutyna (szklanka wody, rozciąganie, 5 min oddechu)", key="zen_r1")
            st.checkbox("🎯 Wybierz JONE priorytetowe zadanie na następny blok 90 min", key="zen_r2")
            st.checkbox("📵 Wycisz telefon i powiadomienia (Ghost przejmuje DM)", key="zen_r3")
            st.checkbox("📓 Wieczorny Dopamine Journal (zapisz 3 dzisiejsze wygrane)", key="zen_r4")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c_right:
            st.markdown("""
            <div class="inflow-card dopamine-card">
                <h3>💀 Porada dopaminowa od Czachy</h3>
                <p>Tomasz, Twój mózg z ADHD szuka stymulacji. Zamiast otwierać social media, przejdź do <strong>🔥 Trybu ADHD Flow</strong> i wpisz jedno małe zadanie. Zagrajmy w wyzwanie 2-minutowe!</p>
            </div>
            """, unsafe_allow_html=True)

        # =========================================================
        # 🏆 DOPAMINE JOURNAL (Baza Wygranych)
        # =========================================================
        st.divider()
        st.subheader("🏆 Twoje Wygrane & Dopamine Journal")
        
        # Load wins from physical JSON database
        journal = load_dopamine_journal()
        wins = journal.get("wins", [])
        
        # Sum points
        total_points = sum(w.get("points", 25) for w in wins)
        weekly_goal = 300
        progress_ratio = min(total_points / weekly_goal, 1.0)
        
        j_col1, j_col2 = st.columns([3, 2])
        with j_col1:
            st.markdown('<div class="inflow-card zen-accent">', unsafe_allow_html=True)
            st.markdown(f"#### 🚀 Poziom Doładowania Dopaminowego: **{total_points} / {weekly_goal} pkt**")
            st.progress(progress_ratio)
            st.markdown(f"Uzyskałeś {int(progress_ratio * 100)}% tygodniowego celu! Każde zadanie to kolejny krok. Mózg z ADHD kocha szybkie nagrody.")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Render recent wins
            st.markdown("##### 📜 Ostatnie Wygrane w tym Tygodniu:")
            for w in reversed(wins[-5:]): # show 5 most recent wins
                st.markdown(f"""
                <div style="padding: 10px 14px; margin-bottom: 6px; background: rgba(16,185,129,0.04); 
                            border-radius: 10px; border-left: 3px solid #10b981; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size:11px; color:#94a3b8;">{w['date']} {w['time']} | {w['type']}</span><br>
                        <strong style="font-size:13px;">{w['detail']}</strong>
                    </div>
                    <span style="background:#10b981; color:#0B1F33; font-weight:700; padding:2px 8px; border-radius:12px; font-size:11px;">+{w['points']} pkt</span>
                </div>
                """, unsafe_allow_html=True)
                
        with j_col2:
            st.markdown('<div class="inflow-card" style="border: 1px solid rgba(16,185,129,0.2);">', unsafe_allow_html=True)
            st.markdown("#### 🎯 Zgłoś Nową Wygraną (Dopamine Boost)")
            w_detail = st.text_input("Co dziś osiągnąłeś?", placeholder="np. Wykonałem cold outreach do 5 klientów...", key="zen_new_win")
            w_type = st.selectbox("Kategoria wygranej:", ["🔥 Zadanie", "🌿 Rytuał", "💪 Pokonanie prokrastynacji", "🧠 Inne"])
            if st.button("🏆 Dodaj Wygraną (+30 pkt)", use_container_width=True):
                if w_detail:
                    new_w = save_dopamine_win(w_type, w_detail, 30)
                    st.success(f"🎉 Świetnie, Tomasz! Zapisano: '{w_detail}' (+30 pkt). Doładuj energię!")
                    st.rerun()
                else:
                    st.warning("Wpisz najpierw treść wygranej!")
            st.markdown('</div>', unsafe_allow_html=True)

        # =========================================================
        # MAPA MYŚLI — st_mermaid
        # =========================================================
        st.divider()
        st.markdown('<div class="inflow-card ceo-accent">', unsafe_allow_html=True)
        st.subheader("🗺️ Mapa Myśli Ekosystemu")

        mermaid_diagram = """
flowchart TD
    TY(["👤 TY — Jason"])
    ZEN["🌿 Zen Mode\nDeep Work & Self-Care"]
    GHOST["👻 Ghost Agent\nAutopilot Biznesowy"]
    CEO["🧠 CEO Jason\nOrkestracja Strategiczna"]
    VME["⚡ Viral Master Engine\n5 Formuł Hooków"]
    BOM["💼 Business Ops Master\nGhost + Cold DM"]
    ASM["📋 Agent Manifesto\nAnty-AI Style"]
    CONTENT["🎬 Wirale / Reels"]
    SALES["💬 Sprzedaż / DM"]
    DECISIONS["🎯 Decyzje Biznesowe"]

    TY -->|Skupienie| ZEN
    TY -->|Automatyzacja| GHOST
    GHOST --> CEO
    CEO --> VME
    CEO --> BOM
    CEO --> ASM
    VME --> CONTENT
    BOM --> SALES
    ASM --> DECISIONS

    style TY fill:#667eea,color:#fff,stroke:none
    style ZEN fill:#a8e6cf,color:#1a5c3a,stroke:none
    style GHOST fill:#ffaaa5,color:#7a1f1f,stroke:none
    style CEO fill:#4A90E2,color:#fff,stroke:none
    style VME fill:#f8d7da,color:#721c24,stroke:none
    style BOM fill:#d4edda,color:#155724,stroke:none
    style ASM fill:#fff3cd,color:#856404,stroke:none
    style CONTENT fill:#e3f2fd,color:#0d47a1,stroke:none
    style SALES fill:#fce4ec,color:#880e4f,stroke:none
    style DECISIONS fill:#f3e5f5,color:#4a148c,stroke:none
    """

        if MERMAID_OK:
            st_mermaid(mermaid_diagram, height=420)
        else:
            # Fallback: elegancka wizualizacja HTML gdy biblioteka niedostępna
            st.markdown("""
            <div style="padding: 20px; background: #f8fafc; border-radius: 16px; font-size: 14px; line-height: 2;">
                <div style="text-align:center; margin-bottom: 16px;">
                    <span style="background:#667eea;color:white;padding:8px 20px;border-radius:20px;font-weight:700;">👤 TY — Jason</span>
                </div>
                <div style="display:flex; justify-content:center; gap:20px; margin-bottom:16px;">
                    <span style="background:#a8e6cf;color:#1a5c3a;padding:8px 16px;border-radius:14px;">🌿 Zen Mode</span>
                    <span style="background:#ffaaa5;color:#7a1f1f;padding:8px 16px;border-radius:14px;">👻 Ghost Agent</span>
                </div>
                <div style="text-align:center; margin-bottom:16px;">
                    <span style="background:#4A90E2;color:white;padding:8px 20px;border-radius:14px;">🧠 CEO Jason</span>
                </div>
                <div style="display:flex; justify-content:center; gap:12px; margin-bottom:16px; flex-wrap:wrap;">
                    <span style="background:#f8d7da;color:#721c24;padding:6px 14px;border-radius:12px;">⚡ Viral Master Engine</span>
                    <span style="background:#d4edda;color:#155724;padding:6px 14px;border-radius:12px;">💼 Business Ops Master</span>
                    <span style="background:#fff3cd;color:#856404;padding:6px 14px;border-radius:12px;">📋 Agent Manifesto</span>
                </div>
                <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
                    <span style="background:#e3f2fd;color:#0d47a1;padding:5px 12px;border-radius:10px;">🎬 Wirale/Reels</span>
                    <span style="background:#fce4ec;color:#880e4f;padding:5px 12px;border-radius:10px;">💬 Sprzedaż/DM</span>
                    <span style="background:#f3e5f5;color:#4a148c;padding:5px 12px;border-radius:10px;">🎯 Decyzje Biznesowe</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.caption("Zainstaluj `pip install streamlit-mermaid` dla interaktywnej mapy myśli")

        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.adhd_mode == "kanban":
        kanban_board.render_kanban_board(save_dopamine_win)

    elif st.session_state.adhd_mode == "flow":
        adhd_executive.render_executive_function_menu(client)

    elif st.session_state.adhd_mode == "sos":
        # === CALM & SOS MODE ===
        # Hide sidebar during crisis overload to reduce visual strain
        st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none !important;
            }
            button[data-testid="stSidebarCollapseButton"] {
                display: none !important;
            }
        </style>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(220,53,69,0.1); padding: 24px; border-radius: 20px; border-left: 6px solid #dc3545; margin-bottom: 24px;">
            <h2 style="color: #dc3545; margin: 0 0 8px 0;">🚨 Tryb Wyciszenia & Ratunku (Sensory Sanctuary)</h2>
            <p style="color: white; margin: 0; font-size: 15px;">Wykryto wysoki poziom przebodźcowania. Wszystkie zbędne elementy zostały ukryte. Oddychaj spokojnie według wskaźnika poniżej.</p>
        </div>
        """, unsafe_allow_html=True)
        
        sos_col1, sos_col2 = st.columns([1, 1])
        
        with sos_col1:
            st.markdown('<div class="inflow-card" style="text-align: center; background: rgba(15,23,42,0.4); border: 1px solid rgba(220,53,69,0.2);">', unsafe_allow_html=True)
            st.markdown("### 🧘 Box Breathing (Trening Oddechu)")
            st.markdown("Podążaj wzrokiem za animowanym okręgiem wdechowym, aby natychmiast wyciszyć układ nerwowy.")
            
            # Breathing pacer using beautiful CSS keyframe animations
            breathing_html = """
            <html>
            <head>
                <style>
                    body {
                        background: transparent;
                        margin: 0;
                        padding: 0;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 250px;
                        overflow: hidden;
                    }
                    .breathing-circle {
                        width: 80px;
                        height: 80px;
                        background: radial-gradient(circle, #dc3545 0%, #7a1f1f 100%);
                        border-radius: 50%;
                        box-shadow: 0 0 30px rgba(220, 53, 69, 0.6);
                        animation: box-breath 16s infinite ease-in-out;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        color: white;
                        font-weight: 700;
                        font-family: sans-serif;
                        font-size: 14px;
                        text-align: center;
                    }
                    @keyframes box-breath {
                        0%, 100% {
                            transform: scale(1);
                            background: radial-gradient(circle, #dc3545 0%, #7a1f1f 100%);
                            box-shadow: 0 0 30px rgba(220, 53, 69, 0.6);
                        }
                        25% {
                            transform: scale(2.2);
                            background: radial-gradient(circle, #ff6b6b 0%, #dc3545 100%);
                            box-shadow: 0 0 60px rgba(255, 107, 107, 0.8);
                        }
                        50% {
                            transform: scale(2.2);
                            background: radial-gradient(circle, #ff6b6b 0%, #dc3545 100%);
                            box-shadow: 0 0 60px rgba(255, 107, 107, 0.8);
                        }
                        75% {
                            transform: scale(1);
                            background: radial-gradient(circle, #7a1f1f 0%, #0B1F33 100%);
                            box-shadow: 0 0 10px rgba(220, 53, 69, 0.2);
                        }
                    }
                    .text-overlay {
                        animation: text-switch 16s infinite step-end;
                        font-family: 'Inter', sans-serif;
                    }
                    @keyframes text-switch {
                        0%, 100% { content: "WDECH..."; }
                        25% { content: "WSTRZYMAJ..."; }
                        50% { content: "WYDECH..."; }
                        75% { content: "WSTRZYMAJ..."; }
                    }
                </style>
            </head>
            <body>
                <div class="breathing-circle">
                    <span class="text-overlay" id="breath-text">ODDECH</span>
                </div>
                <script>
                    const text = document.getElementById("breath-text");
                    const phases = ["WDECH...", "WSTRZYMAJ...", "WYDECH...", "WSTRZYMAJ..."];
                    let i = 0;
                    text.innerText = phases[0];
                    setInterval(() => {
                        i = (i + 1) % 4;
                        text.innerText = phases[i];
                    }, 4000); // 4 seconds per box phase
                </script>
            </body>
            </html>
            """
            st.components.v1.html(breathing_html, height=260)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with sos_col2:
            st.markdown('<div class="inflow-card" style="background: rgba(15,23,42,0.4); border: 1px solid rgba(220,53,69,0.2);">', unsafe_allow_html=True)
            st.markdown("### 🔌 Automatyczne Działania Tła (Status)")
            st.markdown("System wdrożył następujące filtry, aby zdjąć z Ciebie jakąkolwiek presję:")
            
            st.success("🟢 Status DND na GoHighLevel aktywny (90 minut ciszy)")
            st.success("🟢 Aktywowano e-mail autoresponder ('Obecnie offline...')")
            st.success("🟢 Zintegrowane oświetlenie pokoju przyciemnione do 20% (bursztyn)")
            
            st.info("💡 Czacha doradza: Odsuń telefon, zamknij oczy na 4 cykle oddechowe. Świat poczeka.")
            
            if st.button("🌿 Wracam do pracy (Wyłącz SOS)", use_container_width=True, type="primary"):
                st.session_state.adhd_mode = "zen"
                st.session_state.ghost_mode = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.adhd_mode == "wiki":
        st.markdown('<div class="inflow-card zen-accent">', unsafe_allow_html=True)
        st.markdown("### 📖 Katalog Procedur & Instrukcji (ADHD Wiki)")
        st.markdown("Baza wiedzy zoptymalizowana dla umysłu neuroatypowego. Każda procedura może zostać natychmiast rozbita na nano-zadania w Kanban.")
        st.markdown('</div>', unsafe_allow_html=True)

        import glob
        wiki_dir = r"c:\Aplikacje MVP\Holistic Jason\02_knowledge_base\raw\ADHD"
        md_files = glob.glob(os.path.join(wiki_dir, "*.md"))
        
        if not md_files:
            st.info("Brak procedur w katalogu.")
        else:
            # Map paths to simple names
            file_options = {}
            for path in md_files:
                filename = os.path.basename(path)
                title = filename
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        first_line = f.readline().strip()
                        if first_line.startswith("#"):
                            title = first_line.replace("#", "").strip()
                except Exception:
                    pass
                file_options[title] = path
            
            selected_title = st.selectbox("Wybierz procedurę / instrukcję:", list(file_options.keys()))
            selected_path = file_options[selected_title]
            
            try:
                with open(selected_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                content = f"Błąd odczytu pliku: {e}"
                
            # Render file content in a gorgeous container
            st.markdown('<div class="inflow-card" style="padding: 24px; border: 1px solid rgba(255,255,255,0.05); background: rgba(30,41,59,0.4); max-height: 500px; overflow-y: auto;">', unsafe_allow_html=True)
            st.markdown(content)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Interactive Task Chunker Section
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="inflow-card dopamine-card" style="border: 2px solid #8b5cf6; background: rgba(139, 92, 246, 0.05); padding: 24px;">', unsafe_allow_html=True)
            st.markdown("### 🎯 Silnik AI Task Chunker (Bypass Prokrastynacji)")
            st.markdown("Czujesz lęk lub opór przed rozpoczęciem tej procedury? Nie musisz zastanawiać się od czego zacząć! Pozwól, że model Gemini rozbije tę procedurę na 3-5 ultra-prostych nano-kroków (< 3 min każdy) i automatycznie doda je na Twoją tablicę Kanban.")
            
            chunk_button = st.button("🚀 Generuj Nano-Zadania w Kanban (+50 pkt)", type="primary", use_container_width=True)
            
            if chunk_button:
                with st.spinner("🧠 Psychoterapeuta CBT rozbija procedurę na nano-kroki o niskim tarciu (Gemini 2.5 Flash)..."):
                    try:
                        chunker_prompt = f"""
                        Jesteś terapeutą poznawczo-behawioralnym (CBT) i ekspertem od ADHD. Twój cel to pomóc neuroatypowemu użytkownikowi (Tomaszowi) w przełamaniu paraliżu zadaniowego i prokrastynacji przy wdrażaniu poniższej procedury/instrukcji.
                        
                        Procedura do rozbicia:
                        \"\"\"{content}\"\"\"
                        
                        Rozbij tę procedurę na 3 do 5 konkretnych, fizycznych nano-zadań.
                        ŚCIŚLE STOSUJ SIĘ DO PONIŻSZYCH REGUŁ ADHD:
                        1. Każde zadanie musi mieć tak niski próg startu (Low Friction), żeby rozpoczęcie go nie wywoływało oporu (np. 'Zaloguj się na konto X i kliknij Y' zamiast 'Przeprowadź research konkurencji').
                        2. Każde zadanie powinno mieć krótki zestaw mini-kroków (checklist) – każdy krok zajmujący < 60 sekund.
                        3. Zwróć dane w formacie JSON jako tablica obiektów, dopasowana dokładnie do poniższej struktury:
                        [
                          {{
                            "title": "Tytuł nano-zadania (użyj motywujących emoji, np. 🛠️, 🔌, 📝)",
                            "category": "📂 [Procedura] {selected_title[:20]}",
                            "energy_cost": "Jedno z: Low, Medium, High",
                            "points": "Wartość punktowa (20-40 pkt)",
                            "checklist": [
                              {{"item": "Bardzo prosty krok fizyczny 1", "completed": false}},
                              {{"item": "Bardzo prosty krok fizyczny 2", "completed": false}}
                            ],
                            "notes": "Jedno zdanie wspierającego, ciepłego motywatora CBT lub wyjaśnienia dlaczego to jest ważne."
                          }}
                        ]
                        
                        Zwróć WYŁĄCZNIE czysty JSON. Nie dodawaj znaków ```json ani żadnych komentarzy poza formatem JSON.
                        """
                        
                        # Request JSON response from Gemini
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=chunker_prompt
                        )
                        
                        # Parse JSON response
                        raw_json = response.text.strip()
                        # Clean if Gemini wrapped in code block
                        if raw_json.startswith("```"):
                            raw_json = raw_json.split("```")[1]
                            if raw_json.startswith("json"):
                                raw_json = raw_json[4:]
                            raw_json = raw_json.strip()
                        if raw_json.endswith("```"):
                            raw_json = raw_json[:-3].strip()
                            
                        tasks_list = json.loads(raw_json)
                        
                        # Add tasks to Kanban
                        for t in tasks_list:
                            kanban_board.add_kanban_task(
                                title=t["title"],
                                category=t.get("category", f"📂 Procedura: {selected_title[:20]}"),
                                energy_cost=t.get("energy_cost", "Medium"),
                                points=int(t.get("points", 25)),
                                checklist=t.get("checklist", []),
                                notes=t.get("notes", "")
                            )
                        
                        # Dopamine win reward
                        save_dopamine_win("💪 Pokonanie prokrastynacji", f"Rozbito procedurę '{selected_title}' na nano-zadania Kanban", 50)
                        
                        st.balloons()
                        st.success(f"🎉 Sukces! Rozbito procedurę na {len(tasks_list)} nano-zadań i automatycznie wstrzyknięto je do Twojego Kanban Inboxa! Zgłoszono +50 pkt Dopamine Boost.")
                        
                        # Wait 1.5 seconds and redirect
                        import time
                        st.toast("Przekierowuję na tablicę Kanban...")
                        time.sleep(1.5)
                        st.session_state.adhd_mode = "kanban"
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Wystąpił błąd podczas generowania nano-zadań: {e}")
                        st.markdown(f"**Oryginalna odpowiedź modelu:**\n{response.text if 'response' in locals() else 'Brak'}")
            st.markdown('</div>', unsafe_allow_html=True)

    # === SECTION: SHARED SCRATCHPAD ===
    st.divider()
    st.subheader("📋 Współdzielony Scratchpad Agentów (Real-time Notes)")
    st.markdown("Zapisuj tutaj swoje szybkie notatki, przemyślenia i zadania do zrobienia na później. Zsynchronizowane bezpośrednio z Twoją bazą wiedzy w czasie rzeczywistym.")
    
    import os
    scratchpad_path = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\ADHD\shared_scratchpad.md"
    os.makedirs(os.path.dirname(scratchpad_path), exist_ok=True)
    if not os.path.exists(scratchpad_path):
        with open(scratchpad_path, "w", encoding="utf-8") as f:
            f.write("# Shared Scratchpad\n\nZapisz tutaj swoje szybkie notatki, przemyślenia i zadania do zrobienia na później, aby nie rozpraszać się podczas sesji głębokiej pracy.\n")
            
    try:
        with open(scratchpad_path, "r", encoding="utf-8") as f:
            scratchpad_content = f.read()
    except Exception:
        scratchpad_content = ""
        
    scratchpad_input = st.text_area("Twoje Szybkie Notatki / Braindump:", value=scratchpad_content, height=180, key="scratchpad_editor")
    
    col_scr1, col_scr2 = st.columns(2)
    with col_scr1:
        if st.button("💾 Zapisz Notatki (+10 pkt)", use_container_width=True, type="primary"):
            try:
                with open(scratchpad_path, "w", encoding="utf-8") as f:
                    f.write(scratchpad_input)
                save_dopamine_win("🌿 Rytuał", "Aktualizacja Współdzielonego Scratchpada", 10)
                st.toast("🎉 Notatki zapisane pomyślnie! Zgłoszono +10 pkt Dopamine Boost.")
                st.rerun()
            except Exception as e:
                st.error(f"Błąd zapisu: {e}")
    with col_scr2:
        if st.button("🔄 Odśwież / Zsynchronizuj", use_container_width=True):
            st.rerun()

    # === SECTION: FLOATING CZACHA ASSISTANT ===
    floating_czacha_html = """<div class="czacha-widget-container" style="position: fixed; bottom: 85px; right: 25px; z-index: 999999; font-family: 'Outfit', sans-serif;">
<style>
#czacha-toggle {
    display: none !important;
}
.czacha-bubble {
    display: none; 
    width: 280px; 
    background: rgba(11, 31, 51, 0.96) !important; 
    backdrop-filter: blur(15px); 
    border: 2px solid #FF99AC !important; 
    border-radius: 20px !important; 
    padding: 16px !important; 
    box-shadow: 0 10px 40px rgba(0,0,0,0.5) !important; 
    margin-bottom: 12px; 
    color: white !important;
    transition: all 0.3s ease;
}
.czacha-bubble h4, .czacha-bubble strong, .czacha-bubble p, .czacha-bubble label {
    color: #ffffff !important;
}
.czacha-btn-element {
    width: 56px; 
    height: 56px; 
    background: linear-gradient(135deg, #FF6A88 0%, #FF99AC 100%) !important; 
    border-radius: 50% !important; 
    display: flex !important; 
    align-items: center !important; 
    justify-content: center !important; 
    font-size: 28px !important; 
    cursor: pointer !important; 
    box-shadow: 0 8px 32px rgba(255, 106, 136, 0.4) !important; 
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important; 
    margin-left: auto;
    animation: czacha-float-pulse 2.5s infinite ease-in-out;
}
.czacha-btn-element:hover {
    transform: scale(1.15) rotate(15deg) !important;
    box-shadow: 0 12px 40px rgba(255, 106, 136, 0.6) !important;
}
@keyframes czacha-float-pulse {
    0%, 100% { transform: translateY(0) scale(1); }
    50% { transform: translateY(-8px) scale(1.05); }
}
#czacha-toggle:checked ~ .czacha-bubble {
    display: block !important;
}
</style>

<input type="checkbox" id="czacha-toggle">

<div class="czacha-bubble">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <strong style="color: #FF99AC !important; font-size: 14px;">💀 ADHD Braindump Assistant</strong>
        <label for="czacha-toggle" style="cursor: pointer; font-size: 18px; color: #94a3b8 !important;">×</label>
    </div>
    <p style="font-size: 11px; margin: 0 0 10px 0; color: rgba(255,255,255,0.9) !important; line-height: 1.5;">
        "Tomasz, Twój mózg z ADHD potrzebuje stymulacji. Wykorzystaj ten panel jako szybki braindump, aby oczyścić głowę lub podyktować głosowo!"
    </p>
    <div style="display: flex; gap: 8px; margin-bottom: 8px;">
        <textarea id="czacha-note" style="flex: 1; height: 60px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; color: white; padding: 8px; font-size: 12px; resize: none;" placeholder="Wpisz szybką myśl/braindump lub zacznij dyktować..."></textarea>
        <button id="czacha-mic-btn" onclick="toggleVoiceDictation()" style="width: 40px; height: 60px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15); border-radius: 10px; font-size: 20px; cursor: pointer; color: white; transition: all 0.2s ease;">🎤</button>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
        <button onclick="navigator.clipboard.writeText(document.getElementById('czacha-note').value); alert('Skopiowano braindump do schowka! Możesz teraz wkleić go do Ingestion Hub lub Scratchpada.');" style="background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; padding: 6px 12px; border-radius: 8px; font-size: 11px; font-weight: 600; cursor: pointer;">Skopiuj notatkę</button>
    </div>
</div>

<label for="czacha-toggle" class="czacha-btn-element">
    💀
</label>
</div>
<script>
var dictationActive = false;
var recognition = null;

function toggleVoiceDictation() {
    var btn = document.getElementById("czacha-mic-btn");
    var note = document.getElementById("czacha-note");
    
    if (!recognition) {
        window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!window.SpeechRecognition) {
            alert("Twoja przeglądarka nie obsługuje dyktowania głosowego Web Speech API. Użyj Google Chrome lub Brave.");
            return;
        }
        recognition = new window.SpeechRecognition();
        recognition.lang = 'pl-PL';
        recognition.continuous = true;
        recognition.interimResults = true;
        
        recognition.onstart = function() {
            dictationActive = true;
            btn.style.background = "#FF6A88";
            btn.style.borderColor = "#FF99AC";
            btn.innerText = "🛑";
        };
        
        recognition.onresult = function(event) {
            var interim_transcript = '';
            var final_transcript = '';
            
            for (var i = event.resultIndex; i < event.results.length; ++i) {
                if (event.results[i].isFinal) {
                    final_transcript += event.results[i][0].transcript;
                } else {
                    interim_transcript += event.results[i][0].transcript;
                }
            }
            
            if (final_transcript) {
                note.value = (note.value + " " + final_transcript).trim();
            }
        };
        
        recognition.onerror = function(event) {
            console.error("Speech recognition error", event.error);
            stopDictation();
        };
        
        recognition.onend = function() {
            stopDictation();
        };
    }
    
    if (dictationActive) {
        recognition.stop();
    } else {
        recognition.start();
    }
}

function stopDictation() {
    dictationActive = false;
    var btn = document.getElementById("czacha-mic-btn");
    btn.style.background = "rgba(255,255,255,0.1)";
    btn.style.borderColor = "rgba(255,255,255,0.15)";
    btn.innerText = "🎤";
}
</script>"""
    st.markdown(floating_czacha_html, unsafe_allow_html=True)

    st.stop()

def render_centrum_dowodzenia():
    # ======================================================================
    # 🧠 STRONA: CENTRUM DOWODZENIA (domyślna)
    # ======================================================================
    st.title("🧠 Holistic CEO — Centrum Dowodzenia")

    with st.expander("👥 Zespół Agentów", expanded=False):
        for name, agent in AGENTS.items():
            model_label = agent["model"]
            skills_html = " ".join([f'<span class="agent-badge">{s}</span>' for s in agent["skills"]])

            st.markdown(f"**{name}** — `{model_label}` {skills_html}", unsafe_allow_html=True)

    st.divider()

    # Szybkie scenariusze
    st.subheader("⚡ Szybkie Scenariusze")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📄 Landing Page", use_container_width=True):
            st.session_state["prefill"] = "Przygotuj kompletne copy dla wszystkich sekcji Landing Page Holistic Operator zgodnie z zasadami StoryBrand i Webwritingu Jana Szopy."
    with col2:
        if st.button("🎯 Oferta Klient", use_container_width=True):
            st.session_state["prefill"] = "Przygotuj kompletną ofertę dla klienta: [WPISZ BRANŻĘ, WIELKOŚĆ FIRMY, GŁÓWNE PROBLEMY]"
    with col3:
        if st.button("🔧 Workflow GHL", use_container_width=True):
            st.session_state["prefill"] = "Zaprojektuj kompletny workflow automatyzacji w GHL: od lead capture przez ankietę, przez email nurturing, do umówienia rozmowy diagnostycznej."
    with col4:
        if st.button("🖼️ Grafiki SM", use_container_width=True):
            st.session_state["prefill"] = "Wygeneruj serię 4 grafik na Instagram dla marki Holistic Jason: 2 posty edukacyjne (1:1) i 2 stories (9:16). Temat: Niewidzialni Pracownicy AI."

    prefill = st.session_state.get("prefill", "")
    task = st.text_area(
        "📝 Co robimy dzisiaj?",
        value=prefill,
        placeholder="Np.: 'Przygotuj ofertę dla klienta: klinika medycyny estetycznej w Łodzi, 5 pracowników, brak strony i CRM'",
        height=120
    )
    if prefill:
        st.session_state["prefill"] = ""

    col_run, col_save = st.columns([1, 1])
    with col_run:
        run_button = st.button("🚀 URUCHOM ORKIESTRACJĘ", type="primary", use_container_width=True)
    with col_save:
        if st.session_state.messages:
            last_result = st.session_state.messages[-1].get("content", "")
            st.download_button("💾 Pobierz wynik (.md)", last_result,
                file_name=f"holistic_ceo_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                use_container_width=True)

    if run_button and task:
        knowledge_context = load_knowledge(selected_sources, selected_files) if selected_files else ""
    
        if mode == "🤖 Auto-Orkiestracja (CEO deleguje)":
            result = orchestrate(task, knowledge_context, mode="auto")
        
            # Auto-zapis pełnego raportu
            agent_results = st.session_state.get("last_agent_results", [])
            saved_path = save_full_report(task, result, agent_results)
            st.sidebar.success(f"💾 Raport zapisany: {saved_path.name}")
        
        elif mode == "🖼️ Creative Director (Imagen 3)":
            st.markdown('<div class="phase-header">🖼️ Creative Director planuje grafiki...</div>', unsafe_allow_html=True)
            result, tokens = call_agent("🖼️ Creative Director (Imagen 3)", task, knowledge_context)
        
            st.divider()
            st.header("📄 Plan Grafik")
            st.markdown(result)
        
            try:
                clean = result.replace("```json", "").replace("```", "").strip()
                start = clean.find("{")
                end = clean.rfind("}") + 1
                if start >= 0 and end > start:
                    clean = clean[start:end]
                plan = json.loads(clean)
                images = plan.get("images", [])
            
                if images:
                    st.markdown('<div class="phase-header">🎨 Imagen 3 generuje grafiki...</div>', unsafe_allow_html=True)
                    for i, img_spec in enumerate(images):
                        with st.spinner(f"Generuję obraz {i+1}/{len(images)}..."):
                            filepath, pil_image = generate_image(
                                img_spec["prompt"],
                                img_spec.get("aspect_ratio", "1:1")
                            )
                            if pil_image:
                                st.image(pil_image, caption=img_spec.get("caption_pl", f"Grafika {i+1}"))
                                st.caption(f"📁 Zapisano: {filepath}")
                            else:
                                st.warning(f"Nie udało się wygenerować obrazu {i+1}")
            except (json.JSONDecodeError, Exception) as e:
                st.info(f"Prompty wygenerowane — użyj ich ręcznie w Google AI Studio jeśli API nie jest aktywne. ({e})")
        else:
            result = orchestrate(task, knowledge_context, mode=mode)
        
            # Auto-zapis dla trybu bezpośredniego
            saved_path = save_full_report(task, result)
            st.sidebar.success(f"💾 Raport zapisany: {saved_path.name}")
    
        st.session_state.messages.append({
            "role": "assistant", "content": result if isinstance(result, str) else str(result),
            "task": task, "timestamp": datetime.now().isoformat()
        })
    
        if mode not in ["🖼️ Creative Director (Imagen 3)"]:
            st.divider()
            st.header("📄 Raport Końcowy")
            st.markdown(result)

    # --- SEKCJA: ZAPISANE RAPORTY ---
    st.divider()
    with st.expander("📂 Zapisane Raporty (folder: reports/)", expanded=False):
        report_files = sorted(REPORTS_DIR.glob("*.md"), reverse=True)
        if report_files:
            for rf in report_files[:10]:
                col_name, col_open = st.columns([3, 1])
                with col_name:
                    st.text(f"📄 {rf.name}")
                with col_open:
                    with open(rf, "r", encoding="utf-8") as f:
                        st.download_button("⬇️", f.read(), file_name=rf.name, key=rf.name)
        else:
            st.info("Brak zapisanych raportów. Uruchom orkiestrację, aby wygenerować pierwszy.")

    if st.session_state.messages:
        with st.expander("📜 Historia zadań", expanded=False):
            for msg in reversed(st.session_state.messages):
                st.markdown(f"**[{msg.get('timestamp', '?')}]** {msg.get('task', '?')[:80]}...")
                st.markdown(msg["content"][:500] + "...")
                st.divider()



def render_viral_generator():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #FF9A8B 0%, #FF6A88 55%, #FF99AC 100%); 
                padding: 32px 28px; border-radius: 24px; margin-bottom: 28px;
                box-shadow: 0 10px 40px rgba(255,106,136,0.3);">
        <h1 style="color: white !important; margin: 0; font-size: 1.8rem; font-weight: 700;">🎬 Viral Generator</h1>
        <p style="color: rgba(255,255,255,0.9) !important; margin: 8px 0 0 0; font-size: 15px;">Moc Viral Master Engine w Twoich rękach</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown('<div class="inflow-card">', unsafe_allow_html=True)
        topic = st.text_area("O czym kręcimy?", placeholder="Np. Dlaczego AI nie zabierze Ci pracy, ale osoba używająca AI tak.", height=100)
        target_group = st.selectbox("Grupa docelowa", ["Przedsiębiorcy", "Osoby z ADHD", "Twórcy Contentu", "Klienci B2B", "Freelancerzy"])
        hook_type = st.selectbox("Wybierz Typ Hooka (z VME)", ["Kontrariański (Challenge)", "Statystyczny (Data)", "Spowiedź (Personal)", "Proroctwo (Future)", "Wróg (The Enemy)"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="inflow-card" style="height: 100%;">', unsafe_allow_html=True)
        st.info("**Zasada Outlier Multiplier:** Wybieramy tylko te wzorce, które historycznie dają 10x lepsze wyniki niż średnia.")
        st.caption("Skrypt zostanie zoptymalizowany pod utrzymanie uwagi (retention) i naturalny styl Anty-AI.")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🚀 GENERUJ SKRYPT WIRALOWY", use_container_width=True, type="primary"):
        if not topic:
            st.warning("Podaj temat!")
        else:
            with st.spinner("🧠 Agenci VME analizują Outlier Logic..."):
                vme_prompt = f"""Jesteś Video Producerem marki Holistic Jason. 
                Twoim zadaniem jest stworzenie skryptu wiralowego (0-60s) na podstawie tematu: {topic}
            
                WYTYCZNE Z VIRAL MASTER ENGINE:
                {VME_KNOWLEDGE}
            
                TYP HOOKA: {hook_type}
                GRUPA DOCELOWA: {target_group}
                STYL: Anty-AI, ludzki, konkretny, zero lania wody.
            
                Zwróć:
                1. 🪝 HOOK (0-3s) - mocny start
                2. 🔄 RE-HOOK (3-10s) - dlaczego warto zostać
                3. 🥩 MIĘSO (10-50s) - konkretna wartość
                4. ⚡ CTA (50-60s) - prośba o akcję
                5. 🎬 REŻYSERIA - co ma być widać na ekranie
                """
            
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=vme_prompt
                )
            
                st.markdown('<div class="inflow-card">', unsafe_allow_html=True)
                st.subheader("📄 Twój Wiralowy Skrypt")
                st.markdown(response.text)
                st.markdown('</div>', unsafe_allow_html=True)
            



# ======================================================================
# NOWA ARCHITEKTURA (ZAGNIEŻDŻONA)
# ======================================================================

if page == "🧠 AI Architect (Orkiestrator)":
    st.title("🧠 AI Architect (Orkiestrator)")
    tab_ceo, tab_intake, tab_ghl, tab_radar, tab_profil, tab_funnel = st.tabs([
        "🧠 Centrum Dowodzenia", "🔍 Client Intake", "🔌 GHL Agent", "📡 Market Radar", "📝 Kreator Profilu", "🏴‍☠️ Funnel Hacker"
    ])
    
    with tab_ceo:
        render_centrum_dowodzenia()
    
    with tab_intake:
        intake_data = render_intake_form()
        if intake_data:
            workspace = create_client_workspace(intake_data)
            st.success(f"📁 Workspace utworzony: `{workspace}`")
            prompt = build_intake_prompt(intake_data)
            st.divider()
            st.subheader("🧠 Orkiestracja CEO...")
            from datetime import datetime
            result = orchestrate(prompt, "", mode="auto")
            st.header("📄 Raport Końcowy")
            st.markdown(result)
            
    with tab_ghl:
        render_ghl_agent()
    with tab_radar:
        render_market_radar()
    with tab_profil:
        render_profile_builder()
    with tab_funnel:
        render_funnel_hacker()
    st.stop()

if page == "🎬 Fabryka Treści":
    st.title("🎬 Fabryka Treści")
    tab_viral, tab_content, tab_planner, tab_influencer, tab_shadow = st.tabs([
        "🎬 Viral Generator", "🎬 Content Lab", "📅 Social Planner", "🤖 AI Influencer", "👥 Shadow Operator"
    ])
    
    with tab_viral:
        render_viral_generator()
    with tab_content:
        render_content_lab()
    with tab_planner:
        render_social_planner()
    with tab_influencer:
        render_ai_influencer()
    with tab_shadow:
        render_shadow_operator()
    st.stop()

if page == "🎨 Studio Kreatywne":
    st.title("🎨 Studio Kreatywne")
    st.info("Sekcja w budowie - moduły Imagen 3 i Veo 3.1 dostępne jako polecenia w Centrum Dowodzenia (AI Architect).")
    st.stop()

if page == "🎓 Baza Wiedzy (Kombajn & Mapy)":
    tab_mapy, tab_kombajn = st.tabs(["🧠 Mapy Myśli & Baza Wiedzy", "📥 Masowy Import (Kombajn)"])
    with tab_mapy:
        render_knowledge_zone()
    with tab_kombajn:
        render_knowledge_extractor()
    st.stop()
