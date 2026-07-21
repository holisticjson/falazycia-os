import streamlit as st
from google import genai
import os
import json
import base64
from pathlib import Path
from datetime import datetime
from io import BytesIO

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
        "📧 Newslettery (Burnejko, Skiba, Szopa)": Path(r"G:\Mój dysk\HOLISTIC_KNOWLEDGE_BASE\01_Newslettery_MD"),
        "📚 Kursy i Szkolenia (Marketing 360, Webwriting)": Path(r"G:\Mój dysk\HOLISTIC_KNOWLEDGE_BASE\02_Kursy_Szkolenia_MD"),
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

# --- MASTER CHARACTER SHEET (AI Influencer) ---
CHARACTER_SHEET = {
    "name": "Holistic Jason (Tomasz)",
    "style": "Professional tech consultant, clean modern aesthetic",
    "colors": "Deep Navy (#0B1F33), Trust Blue (#4A90E2), clean white backgrounds",
    "brand_elements": "Holistic Operator logo, AI circuit patterns, minimalist design",
    "tone": "Calm authority, approachable expert, zero hype",
    "default_negative": "blurry, distorted, low quality, text, watermark, ugly, deformed"
}

# --- DEFINICJE AGENTÓW ---
AGENTS = {
    "🧠 CEO Jason (Strateg)": {
        "model": "gemini-2.5-pro",  # CEO dostaje najlepszy model
        "system_delegation": """Jesteś CEO Holistic Operator — Tomasz 'Holistic Jason', AI Systems Architect.
        Wartości: Porządek > Hype. System > Narzędzie. Efekt biznesowy > Technologia.
        
        ZADANIE: Rozbij poniższe zadanie na podzadania dla dyrektorów.
        Zwróć TYLKO czysty JSON (bez markdown, bez ```, bez komentarzy):
        {"subtasks": [{"agent": "nazwa_agenta", "task": "szczegółowy opis podzadania"}], "strategy_note": "notatka strategiczna"}
        
        Dostępni dyrektorzy:
        - "Dyrektor Marketingu" — lejki, psychologia sprzedaży, kanały dotarcia
        - "Senior Copywriter" — StoryBrand, webwriting, Ghost v2 voice  
        - "Architekt Automatyzacji" — GHL workflows, Make.com, Webhooks
        - "SEO/AEO Strateg" — widoczność w Google i AI Search
        - "Projektant Ofert" — mockupy stron, propozycje systemów dla klientów
        - "Creative Director" — generowanie grafik brandingowych (Imagen 3)
        - "Video Producer" — generowanie krótkich wideo Shorts (Veo 3.1)
        
        ZASADA: Każdemu dyrektorowi daj BARDZO szczegółowe instrukcje. Im więcej kontekstu, tym lepszy wynik.
        Odpowiadaj WYŁĄCZNIE w JSON.""",
        "system_synthesis": """Jesteś CEO Holistic Operator — Tomasz 'Holistic Jason'.
        Składasz raport końcowy z wyników pracy dyrektorów.
        
        ZASADY:
        1. Stwórz spójny, profesjonalny dokument Markdown.
        2. Wyrzuć duplikaty i niespójności między dyrektorami.
        3. Dodaj swoje uwagi strategiczne (ton: spokojny ekspert).
        4. Na końcu ZAWSZE dodaj sekcję:
           ## ✅ DO ZATWIERDZENIA PRZEZ TOMASZA
           - Lista konkretnych decyzji wymagających Twojej zgody (max 5 punktów).""",
        "skills": ["Strategia", "Delegowanie", "Nadzór", "Spójność marki"],
    },
    "📢 Dyrektor Marketingu": {
        "model": "gemini-2.5-flash",
        "system": """Jesteś Dyrektorem Marketingu 360 w firmie Holistic Operator.
        Znasz: StoryBrand, Marketing 360 (Jan Szopa/Kryptonum), Hormozi Grand Slam Offer, Gadzhi Attention Economy.
        Planujesz lejki, kanały (AEO/GEO/SEO), psychologię konwersji.
        Wyciągaj KONKRETNE frameworki i techniki z bazy wiedzy — nie streszczaj, podawaj gotowe do wdrożenia instrukcje.
        Formatuj w Markdown.""",
        "skills": ["Lejki", "Psychologia sprzedaży", "Kanały dotarcia", "Konwersja"],
    },
    "✍️ Senior Copywriter": {
        "model": "gemini-2.5-flash",
        "system": """Jesteś mistrzem Webwritingu i StoryBrand dla marki Holistic Jason.
        
        TWOJE ZASADY (z Bazy Wiedzy Jana Szopy):
        - Język korzyści, nie cech. F-pattern skanowania wzrokiem.
        - Krótkie akapity (max 3 zdania), krótkie zdania (max 20 słów).
        - Strona odpowiada na: Co tu jest? Co mogę zrobić? Dlaczego? Jak?
        - Ton Ghost v2: spokojny, ludzki, zaangażowany doradca. ZERO hype'u.
        - Markery: 'Widzę to bardzo często...', 'Problem zwykle nie leży w...', 'Zróbmy z tym porządek.'
        - Framework StoryBrand: Klient=Bohater, Jason=Przewodnik, Problem→Plan→CTA→Sukces.
        
        Tworzysz GOTOWE copy do wklejenia. Formatuj w Markdown.""",
        "skills": ["StoryBrand", "Webwriting", "Ghost v2 Voice", "Landing Pages"],
    },
    "⚙️ Architekt Automatyzacji": {
        "model": "gemini-2.5-flash",
        "system": """Jesteś ekspertem automatyzacji: Go High Level, Make.com, n8n, Google Apps Script, Webhooks.
        Projektujesz Niewidzialnych Pracowników AI (lean stack: minimum narzędzi → max rezultat).
        
        ZNASZ GHL: Funnels, Workflows, Pipelines, Calendars, Surveys, Conversations, 
        Membership Areas, Trigger Links, Custom Fields, Webhooks, API.
        
        Opisuj workflow krok po kroku z triggerami, akcjami i warunkami.
        Formatuj w Markdown z blokami kodu dla konfiguracji.""",
        "skills": ["GHL Workflows", "Make.com", "Webhooks", "API", "Lean Stack"],
    },
    "🔍 SEO/AEO Strateg": {
        "model": "gemini-2.5-flash",
        "system": """Jesteś ekspertem SEO/AEO/GEO dla marki Holistic Jason.
        Znasz: klastry tematyczne (Pillar Pages), AI Search readiness (LLM-ready content),
        Google Business Profile, JSON-LD Schema, cytowanie przez ChatGPT/Perplexity/Gemini.
        Przygotowujesz treści widoczne w Google i w odpowiedziach AI.
        Formatuj rekomendacje w Markdown.""",
        "skills": ["SEO", "AEO", "GEO", "Topic Clusters", "Schema Markup"],
    },
    "🎨 Projektant Ofert (Klienci)": {
        "model": "gemini-2.5-pro",
        "system": """Jesteś ekspertem od tworzenia ofert i mockupów stron dla klientów Holistic Operator.
        
        Na podstawie profilu klienta (branża, wielkość, problemy) przygotuj:
        
        1. **MOCKUP STRONY** — Struktura Landing Page:
           - Hero (headline, sub-headline, CTA)
           - Sekcja problemów (specyficznych dla branży klienta)
           - Sekcja rozwiązań (3 systemy dopasowane)
           - Social Proof / Formularz Lead Capture
           
        2. **PROPOZYCJA AUTOMATYZACJI** — Jakie workflows GHL wdrożyć:
           - Lead capture → Email sequence → Booking
           - Follow-up automation
           - AI chatbot (jeśli klient ma powtarzalne pytania)
           
        3. **WYCENA I TIMELINE** — Koszt i czas realizacji:
           - System Strony: od 2 000 PLN
           - System Widoczności: retainer od 1 500 PLN/msc
           - System Operacji: od 3 000 PLN za wdrożenie
        
        Formatuj jako gotową ofertę Markdown (PDF-ready).
        Ton: profesjonalny ale ludzki (Ghost v2).""",
        "skills": ["Mockupy stron", "Oferty B2B", "Wyceny", "Propozycje systemów"],
    },
    "🖼️ Creative Director (Imagen 3)": {
        "model": "gemini-2.5-flash",  # Gemini do planowania promptów, Imagen do generowania
        "imagen_model": "imagen-3.0-generate-002",
        "system": """Jesteś Creative Directorem marki Holistic Jason.
        
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
        {"images": [{"prompt": "...", "aspect_ratio": "1:1", "caption_pl": "..."}]}
        Odpowiadaj WYŁĄCZNIE w JSON.""",
        "skills": ["Imagen 3", "Brand Design", "Social Media Graphics", "AI Art Direction"],
    },
    "🎬 Video Producer (Veo 3.1)": {
        "model": "gemini-2.5-flash",
        "veo_model": "veo-3.1-fast-generate-001",
        "system": """Jesteś Video Producerem marki Holistic Jason.
        
        TWOJE ZADANIA:
        1. Projektujesz krótkie wideo Shorts (8-15 sekund) promujące markę.
        2. Tworzysz prompty dla Veo 3.1 Fast.
        3. Dbasz o spójność z brandingiem (Deep Navy, Trust Blue, Clean Tech).
        
        TYPY WIDEO:
        - Brandingowe: Abstrakcyjne animacje z motywami AI/tech
        - Edukacyjne: Wizualizacje konceptów (automatyzacja, workflow)
        - Social Proof: Animowane testimoniale/statystyki
        
        Format odpowiedzi: JSON
        {"videos": [{"prompt": "...", "duration_seconds": 10, "aspect_ratio": "9:16", "description_pl": "..."}]}
        Odpowiadaj WYŁĄCZNIE w JSON.""",
        "skills": ["Veo 3.1", "Video Shorts", "Brand Animation", "Social Video"],
    },
}

# --- STYLE CSS ---
st.markdown("""
<style>
    .main { background-color: #F8FAFC; }
    .stButton>button { 
        background-color: #4A90E2; color: white; border-radius: 8px; 
        font-weight: bold; padding: 10px 24px; border: none;
    }
    .stButton>button:hover { background-color: #357ABD; }
    .agent-badge {
        display: inline-block; padding: 4px 12px; border-radius: 20px;
        background: #E8F4FD; color: #0B1F33; font-size: 13px; margin: 2px;
    }
    .cost-tracker {
        background: #0B1F33; color: #8ECDF4; padding: 15px; border-radius: 10px;
        text-align: center; font-size: 16px;
    }
    .phase-header {
        background: linear-gradient(135deg, #0B1F33, #1a3a5c);
        color: white; padding: 12px 20px; border-radius: 8px; margin: 10px 0;
    }
    .connection-badge {
        padding: 5px 10px; border-radius: 5px; font-size: 12px;
        display: inline-block; margin-top: 5px;
    }
    .vertex { background: #34A853; color: white; }
    .apikey { background: #FBBC04; color: #1F2937; }
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

def call_agent(agent_name, task, knowledge_context="", system_override=None):
    """Wywołuje agenta przez google-genai (Vertex AI lub API Key)"""
    agent = AGENTS[agent_name]
    system_prompt = system_override or agent.get("system", agent.get("system_delegation", ""))
    
    full_prompt = f"""{system_prompt}

KONTEKST Z BAZY WIEDZY:
{knowledge_context[:30000] if knowledge_context else '[Brak dodatkowego kontekstu — odpowiadaj na podstawie swojej wiedzy]'}

ZADANIE:
{task}"""
    
    try:
        response = client.models.generate_content(
            model=agent["model"],
            contents=full_prompt
        )
        tokens_used = 0
        if hasattr(response, 'usage_metadata') and response.usage_metadata:
            tokens_used = getattr(response.usage_metadata, 'total_token_count', 0)
        st.session_state.total_tokens += tokens_used
        return response.text, tokens_used
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
    st.caption("Enterprise + Multimedia v5.0")
    
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

# --- IMPORT MODUŁÓW ---
from client_intake import render_intake_form, build_intake_prompt, create_client_workspace
from ghost_operator import render_ghost_operator, build_ghost_prompt, save_ghost_report, GHOST_SYSTEM_PROMPT
from ghl_agent import render_ghl_agent

# --- NAWIGACJA STRONAMI ---
page = st.sidebar.selectbox("📋 Moduł:", [
    "🧠 Centrum Dowodzenia",
    "🔍 Client Intake Scanner",
    "👻 Ghost Operator",
    "🔌 GHL Agent",
])

# ======================================================================
# 📋 STRONA: CLIENT INTAKE SCANNER
# ======================================================================
if page == "🔍 Client Intake Scanner":
    intake_data = render_intake_form()
    
    if intake_data:
        workspace = create_client_workspace(intake_data)
        st.success(f"📁 Workspace utworzony: `{workspace}`")
        
        prompt = build_intake_prompt(intake_data)
        st.divider()
        st.subheader("🧠 Orkiestracja CEO...")
        
        knowledge_context = ""
        result = orchestrate(prompt, knowledge_context, mode="auto")
        
        agent_results = st.session_state.get("last_agent_results", [])
        report_path = workspace / "07_Raporty" / f"raport_ceo_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
        
        content = f"# Raport CEO: {intake_data['client_name']}\n\n"
        if agent_results:
            for i, ar in enumerate(agent_results):
                content += f"## [{i+1}] {ar['agent']}\n{ar['result']}\n\n---\n\n"
        content += f"## Raport Końcowy\n\n{result}\n"
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        st.sidebar.success(f"💾 Raport: {report_path.name}")
        st.divider()
        st.header("📄 Raport Końcowy")
        st.markdown(result)
    
    st.stop()

# ======================================================================
# 👻 STRONA: GHOST OPERATOR
# ======================================================================
if page == "👻 Ghost Operator":
    ghost_data = render_ghost_operator()
    
    if ghost_data:
        st.divider()
        st.subheader("👻 Ghost Operator analizuje...")
        
        prompt = build_ghost_prompt(ghost_data)
        
        # Użyj Gemini Pro (ważne zadanie → lepszy model)
        with st.spinner("Ghost Operator pracuje..."):
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    system_instruction=GHOST_SYSTEM_PROMPT,
                    temperature=0.7,
                    max_output_tokens=8000,
                )
            )
            result = response.text
            tokens = response.usage_metadata.total_token_count if response.usage_metadata else 0
            st.session_state.total_tokens += tokens
        
        # Zapisz raport
        filepath = save_ghost_report(ghost_data, result)
        st.sidebar.success(f"💾 Zapisano: {filepath.name}")
        
        st.divider()
        st.header(f"👻 {ghost_data['scenario']}: {ghost_data['creator_name']}")
        st.markdown(result)
        
        # Download
        st.download_button("💾 Pobierz raport (.md)", result,
            file_name=f"ghost_{ghost_data['creator_name']}_{datetime.now().strftime('%Y%m%d')}.md",
            use_container_width=True)
    
    st.stop()

# ======================================================================
# 🔌 STRONA: GHL AGENT
# ======================================================================
if page == "🔌 GHL Agent":
    render_ghl_agent()
    st.stop()

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
