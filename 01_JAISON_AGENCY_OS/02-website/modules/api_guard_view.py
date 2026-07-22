import os
import re
import streamlit as st

# Central path to the master .env file
BASE_DIR = r"C:\Aplikacje MVP"
MASTER_ENV_PATH = os.path.join(BASE_DIR, ".env")

API_METADATA = {
    "GEMINI_API_KEY": {
        "label": "♊ Gemini API Key",
        "provider": "Google AI Studio",
        "model": "gemini-2.5-pro / gemini-2.5-flash",
        "desc": "Zasila natywne operacje Gemini, multimodalne skanowanie plików i research.",
        "link": "https://aistudio.google.com/",
        "instruction": "Wejdź na Google AI Studio, zaloguj się kontem Google, kliknij 'Get API Key' i utwórz darmowy klucz w nowym projekcie. Wklej go poniżej."
    },
    "TOGETHER_API_KEY": {
        "label": "🧠 Together AI Key",
        "provider": "Together.xyz",
        "model": "DeepSeek R1 / Kimi K3 / GLM-5",
        "desc": "Zasila tańsze, superszybkie i zaawansowane modele logiczne (Reasoning).",
        "link": "https://www.together.ai/",
        "instruction": "Załóż darmowe konto na Together AI, odbierz darmowe 1$ kredytów na start i skopiuj klucz z sekcji API Keys w swoim profilu."
    },
    "NVIDIA_API_KEY": {
        "label": "🟢 NVIDIA NIM Key",
        "provider": "NVIDIA Build",
        "model": "Llama 3.3 70B Instruct",
        "desc": "Używany do operacji na modelach Llama o niskich opóźnieniach.",
        "link": "https://build.nvidia.com/",
        "instruction": "Zaloguj się na NVIDIA Build, kliknij na dowolny model (np. Llama 3) i pobierz klucz z darmowymi kredytami (1000 zapytań gratis)."
    },
    "SYSTEME_IO_API_KEY": {
        "label": "📧 Systeme.io API Key",
        "provider": "Systeme.io",
        "model": "External Service (Email/Funnel)",
        "desc": "Łączy Jaison OS z darmowym systemem wysyłki maili i budowy lejków.",
        "link": "https://systeme.io/",
        "instruction": "Wejdź w Ustawienia konta Systeme.io -> Klucze API publiczne -> Kliknij 'Utwórz' i skopiuj wygenerowany klucz."
    },
    "FAL_KEY": {
        "label": "🎨 Fal.ai API Key",
        "provider": "Fal.ai",
        "model": "FLUX.1 [dev] / LoRA Portrait",
        "desc": "Zasila generowanie fotorealistycznych grafik marketingowych i klonowanie twarzy.",
        "link": "https://fal.ai/",
        "instruction": "Zarejestruj się na Fal.ai, doładuj minimalną kwotę lub skorzystaj z darmowego triala, wygeneruj klucz i wklej poniżej."
    },
    "PEXELS_API_KEY": {
        "label": "📹 Pexels Video API Key",
        "provider": "Pexels Developer",
        "model": "Media Stock (Free)",
        "desc": "Używany w generatorze wideo reels do automatycznego pobierania filmów B-Roll.",
        "link": "https://www.pexels.com/api/",
        "instruction": "Załóż darmowe konto na Pexels, przejdź do sekcji Image & Video API, zgłoś chęć pobrania klucza (akceptacja natychmiastowa) i skopiuj go."
    },
    "PIXABAY_API_KEY": {
        "label": "🎥 Pixabay API Key",
        "provider": "Pixabay Developers",
        "model": "Media Stock Backup (Free)",
        "desc": "Zapasowe źródło darmowego wideo B-Roll dla nisz biznesowych i medycznych.",
        "link": "https://pixabay.com/api/docs/",
        "instruction": "Zarejestruj się darmowo na Pixabay, przejdź do dokumentacji API i w sekcji 'Parameters' znajdziesz swój stały, darmowy klucz API."
    },
    "N8N_API_KEY": {
        "label": "⛓️ n8n Integration Key",
        "provider": "n8n.pl / Local Instance",
        "model": "Workflow Orchestration",
        "desc": "Pozwala agentom na wyzwalanie zaawansowanych przepływów, webhooków i webhooków CRM.",
        "link": "https://n8n.jaison.pl",
        "instruction": "W swojej instancji n8n wejdź w Ustawienia -> Personal API Keys -> Kliknij 'Create API Key' i skopiuj go."
    },
    "POSTHOG_API_KEY": {
        "label": "📊 PostHog RODO Analytics",
        "provider": "PostHog EU Cloud",
        "model": "RODO Analytics",
        "desc": "Lekka, bez-ciasteczkowa analityka zdarzeń i optymalizacja konwersji (CRO).",
        "link": "https://eu.posthog.com",
        "instruction": "Zarejestruj się w PostHog EU Cloud, wejdź w Project Settings i skopiuj Project API Key z sekcji danych."
    },
    "SLACK_BOT_TOKEN": {
        "label": "💬 Slack Bot Token",
        "provider": "Slack Developer Portal",
        "model": "Slack Client (xoxb)",
        "desc": "Umożliwia wysyłanie raportów z wdrożeń i powiadomień o leadach na dedykowany kanał.",
        "link": "https://api.slack.com/apps",
        "instruction": "Utwórz aplikację w Slack API, przejdź do 'OAuth & Permissions', dodaj uprawnienia chat:write i zainstaluj w workspace, by pobrać token 'xoxb-'."
    },
    "STRIPE_SECRET_KEY": {
        "label": "💳 Stripe Secret Key",
        "provider": "Stripe Sandbox",
        "model": "Payment Gateway",
        "desc": "Zasila testy bramek płatniczych i automatyczne aktywowanie subskrypcji.",
        "link": "https://stripe.com/",
        "instruction": "W panelu Stripe włącz 'Test mode', przejdź do Developers -> API Keys i skopiuj Secret Key (sk_test_...)."
    },
    "WP_KURCZAKUJASIA_PASS": {
        "label": "🌐 WordPress Application Pass",
        "provider": "Kurczak u Jasia (WP)",
        "model": "CMS Content Publisher",
        "desc": "Umożliwia agentom automatyczne publikowanie wygenerowanych wpisów blogowych.",
        "link": "https://kurczakujasia.pl",
        "instruction": "W panelu WordPress Kurczaka u Jasia przejdź do Edycji Profilu Użytkownika -> Hasła Aplikacji -> Wygeneruj nowe hasło i skopiuj je."
    },
    "APIFY_API_KEY": {
        "label": "🕸️ Apify API Key",
        "provider": "Apify Portal",
        "model": "Facebook Ads Spy / Scrapers",
        "desc": "Służy do uruchamiania robotów szpiegujących i scrapowania reklam konkurencji na Facebooku.",
        "link": "https://apify.com/",
        "instruction": "Zarejestruj się bezpłatnie na Apify, przejdź do Ustawienia (Settings) -> Integrations -> Skopiuj swój 'Personal API Token' i wklej go poniżej."
    }
}

def read_raw_env():
    """Reads the raw content of the master .env file."""
    if not os.path.exists(MASTER_ENV_PATH):
        return ""
    try:
        with open(MASTER_ENV_PATH, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"# Błąd odczytu pliku .env: {str(e)}"

def save_env_content(new_content):
    """Saves the new env content to the master .env file and creates a backup."""
    try:
        # Create a backup first
        if os.path.exists(MASTER_ENV_PATH):
            backup_path = MASTER_ENV_PATH + ".bak"
            with open(MASTER_ENV_PATH, "r", encoding="utf-8") as src:
                with open(backup_path, "w", encoding="utf-8") as dest:
                    dest.write(src.read())
                    
        # Save new content
        with open(MASTER_ENV_PATH, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True, "Zapisano"
    except Exception as e:
        return False, str(e)

def parse_configured_keys(env_content):
    """Parses env content to detect which keys are validly configured."""
    keys_status = {k: False for k in API_METADATA.keys()}
    for key in keys_status.keys():
        # Match key=value pattern, handle optional quotes and trailing comments
        match = re.search(fr"^\s*{key}\s*=\s*['\"]?(?P<val>[^'\"]+?)['\"]?\s*$", env_content, re.MULTILINE)
        if match:
            val = match.group("val").strip()
            # Ensure it's not a commented/placeholder value
            if val and not val.startswith("#") and not val.startswith("<uzupełnij"):
                keys_status[key] = True
    return keys_status

def render_api_guard():
    """Renders the ultra-premium ADHD-friendly API Guard dashboard in Streamlit."""
    
    # Custom CSS for glassmorphic neon looks
    st.markdown("""
        <style>
        .neon-title {
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #3b82f6 0%, #a855f7 50%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
            letter-spacing: -0.5px;
        }
        .neon-subtitle {
            color: #94a3b8;
            font-size: 1rem;
            margin-bottom: 25px;
        }
        .health-card {
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 20px;
            backdrop-filter: blur(10px);
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        .api-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        .api-card:hover {
            border-color: rgba(59, 130, 246, 0.3);
            box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1);
        }
        .badge-ok {
            background: rgba(16, 185, 129, 0.15);
            color: #10b981;
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 3px 10px;
            border-radius: 99px;
            font-size: 0.75rem;
            font-weight: 700;
        }
        .badge-missing {
            background: rgba(239, 68, 68, 0.15);
            color: #ef4444;
            border: 1px solid rgba(239, 68, 68, 0.3);
            padding: 3px 10px;
            border-radius: 99px;
            font-size: 0.75rem;
            font-weight: 700;
            animation: pulse-border 2s infinite;
        }
        @keyframes pulse-border {
            0% { border-color: rgba(239, 68, 68, 0.3); }
            50% { border-color: rgba(239, 68, 68, 0.8); }
            100% { border-color: rgba(239, 68, 68, 0.3); }
        }
        .provider-text {
            color: #64748b;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 5px;
        }
        .model-badge {
            background: rgba(255, 255, 255, 0.06);
            color: #cbd5e1;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            font-family: monospace;
        }
        .instruction-box {
            background: rgba(30, 41, 59, 0.6);
            border-left: 4px solid #3b82f6;
            padding: 10px 15px;
            border-radius: 0 8px 8px 0;
            margin-top: 10px;
            font-size: 0.85rem;
            color: #cbd5e1;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("<h1 class='neon-title'>🛡️ API Guard & System Status</h1>", unsafe_allow_html=True)
    st.markdown("<p class='neon-subtitle'>Suwerenne centrum kontroli integracji, kluczy API i zdrowia systemu Jaison OS.</p>", unsafe_allow_html=True)
    
    # Read current state
    env_content = read_raw_env()
    keys_status = parse_configured_keys(env_content)
    
    # Calculate health metric
    total_keys = len(API_METADATA)
    active_keys = sum(1 for val in keys_status.values() if val)
    health_pct = active_keys / total_keys if total_keys > 0 else 0
    
    # System Health Widget
    st.markdown("<div class='health-card'>", unsafe_allow_html=True)
    h_col1, h_col2 = st.columns([1, 3])
    with h_col1:
        st.markdown(f"<div style='text-align:center;'><span style='font-size: 3rem;'>🛡️</span><br><b style='font-size:1.1rem; color:#f8fafc;'>Zdrowie Jaison OS</b></div>", unsafe_allow_html=True)
    with h_col2:
        status_text = f"Aktywne integracje: **{active_keys} / {total_keys}** ({int(health_pct * 100)}%)"
        st.write(status_text)
        st.progress(health_pct)
        if health_pct == 1.0:
            st.success("🎉 Niesamowite! Wszystkie klucze są poprawnie skonfigurowane. Jaison OS działa z pełną mocą!")
        elif health_pct >= 0.7:
            st.info("💡 Większość modułów działa sprawnie. Brakuje tylko kilku zapasowych lub drugorzędnych integracji.")
        else:
            st.warning("⚠️ Wymagane uzupełnienie kluczy. Kluczowe agenty i moduły mogą nie mieć zasilania LLM lub zewnętrznego API!")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Two main columns: LEFT = API Keys Status Grid, RIGHT = Safe .env Editor
    main_col1, main_col2 = st.columns([5, 4])
    
    with main_col1:
        st.markdown("### 🧩 Status Integracji Modułów")
        
        # Filter buttons
        filter_status = st.radio("Filtruj moduły:", ["Wszystkie", "Aktywne (🟢)", "Brak konfiguracji (🔴)"], horizontal=True)
        
        for key, meta in API_METADATA.items():
            is_ok = keys_status[key]
            
            # Apply filter
            if filter_status == "Aktywne (🟢)" and not is_ok:
                continue
            if filter_status == "Brak konfiguracji (🔴)" and is_ok:
                continue
                
            st.markdown(f"""
                <div class='api-card'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <strong style='font-size:1.1rem; color:#f1f5f9;'>{meta['label']}</strong>
                        <span class='{"badge-ok" if is_ok else "badge-missing"}'>{"🟢 AKTYWNY" if is_ok else "🔴 BRAK INTEGRACJI"}</span>
                    </div>
                    <div class='provider-text'>{meta['provider']} &bull; <span class='model-badge'>{meta['model']}</span></div>
                    <p style='color:#94a3b8; font-size:0.85rem; margin-top:8px; margin-bottom:5px;'>{meta['desc']}</p>
                    <div class='instruction-box'>
                        <b>Instrukcja wdrożenia:</b><br>{meta['instruction']}<br>
                        <a href='{meta['link']}' target='_blank' style='color:#60a5fa; font-size:0.8rem; text-decoration:underline;'>Pobierz klucz z oficjalnej strony producenta &rarr;</a>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    with main_col2:
        st.markdown("### 📝 Bezpieczny Edytor .env")
        st.markdown("""
            > [!TIP]
            > Edytujesz **centralny plik konfiguracyjny** zlokalizowany w `C:\\Aplikacje MVP\\.env`. 
            > Zmiany dokonane tutaj natychmiast wpływają na wszystkie agenty, moduły i połączone worktrees.
            > Przed zapisem system automatycznie utworzy kopię zapasową `.env.bak`.
        """)
        
        # Text area with raw env content
        edited_env = st.text_area(
            "Zawartość pliku konfiguracyjnego .env (wklejaj klucze bezpośrednio):",
            value=env_content,
            height=480,
            help="Możesz bezpośrednio edytować i wklejać swoje klucze API w formacie KLUCZ=wartosc."
        )
        
        # Save and backup controls
        editor_col1, editor_col2 = st.columns([1, 1])
        with editor_col1:
            if st.button("💾 Zapisz konfigurację", use_container_width=True, type="primary"):
                if edited_env:
                    success, msg = save_env_content(edited_env)
                    if success:
                        st.success("🟢 Pomyślnie zaktualizowano centralny plik .env! Wszystkie agenty i moduły automatycznie wczytały nową konfigurację.")
                        # Rerun to refresh keys status on UI
                        time_sleep = st.empty()
                        import time
                        time.sleep(1.0)
                        st.rerun()
                    else:
                        st.error(f"🔴 Błąd zapisu: {msg}")
                else:
                    st.warning("⚠️ Plik .env nie może być pusty!")
                    
        with editor_col2:
            if st.button("⏪ Przywróć z .env.bak", use_container_width=True):
                backup_path = MASTER_ENV_PATH + ".bak"
                if os.path.exists(backup_path):
                    try:
                        with open(backup_path, "r", encoding="utf-8") as bf:
                            backup_content = bf.read()
                        success, msg = save_env_content(backup_content)
                        if success:
                            st.success("🟢 Pomyślnie przywrócono poprzednią konfigurację z kopii zapasowej!")
                            import time
                            time.sleep(1.0)
                            st.rerun()
                        else:
                            st.error(f"🔴 Błąd przywracania: {msg}")
                    except Exception as ex:
                        st.error(f"🔴 Błąd: {str(ex)}")
                else:
                    st.error("🔴 Brak pliku kopii zapasowej .env.bak!")
                    
        # Additional safety instruction
        st.markdown("""
            <hr style='margin: 15px 0; border-color: rgba(255,255,255,0.05);'>
            <p style='color:#64748b; font-size:0.75rem; text-align:justify;'>
                🛡️ <b>Bezpieczeństwo danych:</b> Twoje hasła i klucze API są przechowywane wyłącznie na Twoim lokalnym dysku w pliku <code>C:\\Aplikacje MVP\\.env</code>. 
                Są one wczytywane bezpośrednio do zmiennych środowiskowych procesu Streamlit bez wysyłania ich do zewnętrznych serwerów pośredniczących.
            </p>
        """, unsafe_allow_html=True)
