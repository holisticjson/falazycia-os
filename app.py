import streamlit as st
import os, json, time

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
    
    /* Zaokrąglone przyciski premium */
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
    
    /* ADHD-friendly akcenty kolorystyczne */
    .dopamine-accent { color: #10B981; font-weight: bold; }
    .burn-accent { color: #EF4444; font-weight: bold; }
    .focus-accent { color: #F59E0B; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Helpery danych
def load_kanban():
    return json.load(open(KANBAN_FILE, "r", encoding="utf-8")) if os.path.exists(KANBAN_FILE) else {"todo":[], "in_progress":[], "done":[]}

def save_kanban(data):
    json.dump(data, open(KANBAN_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=4)

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

# Inicjalizacja stanu sesji
if "one_thing" not in st.session_state:
    st.session_state.one_thing = ""
if "pomodoro_active" not in st.session_state:
    st.session_state.pomodoro_active = False

# PASEK BOCZNY - Skrajnie estetyczny z ikonami
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #7C3AED; font-family: Outfit;'>🧠 Holistic OS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.9rem;'>Zewnętrzny Płat Czołowy v6.0</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    menu = st.radio(
        "Nawigacja:",
        ["🎯 Mission Control", "🗑️ Brain Dump & Cache", "📻 NotebookLM & Obsidian", "🎬 Content Studio", "👥 Wirtualne C-Suite", "📋 ADHD Kanban", "💾 Pristine Memory"]
    )
    st.markdown("---")
    st.markdown("🌐 **Status Systemu:**")
    st.markdown("⚡ *Hermes Agent:* <span style='color:#10B981; font-weight:bold;'>LIVE (Port 9119)</span>", unsafe_allow_html=True)
    st.markdown("📢 *Telegram Chat:* <span style='color:#10B981; font-weight:bold;'>Połączony</span>", unsafe_allow_html=True)
    st.markdown("📝 *Pristine Memory:* <span style='color:#3B82F6; font-weight:bold;'>Aktywna</span>", unsafe_allow_html=True)

# 1. MISSION CONTROL
if menu == "🎯 Mission Control":
    st.title("🧠 Holistic Mission Control")
    st.subheader("Centrum dowodzenia zoptymalizowane pod neuroróżnorodność")
    
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
    
    # Szybki Capture
    st.subheader("⚡ Szybki Capture myśli (Brain Dump)")
    quick_thought = st.text_area("Masz nagły pomysł lub coś Cię rozprasza? Zrzuć to tutaj natychmiast, aby uwolnić pamięć roboczą mózgu:", height=100)
    if st.button("Uwolnij moją pamięć roboczą"):
        if quick_thought:
            save_brain_dump(quick_thought, "", None)
            st.success("Pomysł bezpiecznie zapisany w chmurze w Skarbcu Myśli. Twoja głowa jest wolna.")
            time.sleep(0.5)
            st.rerun()

# 2. BRAIN DUMP & CACHE
elif menu == "🗑️ Brain Dump & Cache":
    st.title("🗑️ Brain Dump & Open Loops Cache")
    st.subheader("Zewnętrzny płat czołowy — uwalnianie pamięci roboczej")
    
    col_in, col_st = st.columns([1, 1])
    
    with col_in:
        st.markdown("""
        <div class="custom-card" style="border-left: 5px solid #EC4899;">
            <h4 style="margin:0; color:#EC4899;">📥 Zrzut z głowy (Brain Dump)</h4>
            <p style="font-size: 0.9rem; color: #94A3B8; margin-top: 6px;">Wpisz pomysły, luźne myśli, linki lub wgraj zrzut ekranu (np. inspirację reklamową).</p>
        </div>
        """, unsafe_allow_html=True)
        
        thought_input = st.text_area("Co Ci chodzi po głowie?", height=150)
        links_input = st.text_input("Linki / Źródła (opcjonalnie):")
        uploaded_file = st.file_uploader("Dodaj plik / zrzut ekranu (PNG, JPG, PDF):", type=["png","jpg","jpeg","pdf"])
        
        if st.button("Prześlij do Skarbca w Chmurze", type="primary"):
            if thought_input or links_input or uploaded_file:
                save_brain_dump(thought_input, links_input, uploaded_file)
                st.success("Zapisano. Pomysł został odciążony z Twojego mózgu.")
                time.sleep(0.5)
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
                        # Oznaczenie jako zarchiwizowane
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

# 3. NOTEBOOKLM & OBSIDIAN
elif menu == "📻 NotebookLM & Obsidian":
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
elif menu == "🎬 Content Studio":
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

# 5. WIRTUALNE C-SUITE
elif menu == "👥 Wirtualne C-Suite":
    st.title("🤖 Zespół C-Suite Agents")
    st.subheader("Twój wirtualny komitet sterujący zasilany Pristine Memory")
    
    st.markdown("""
    <p>Dyrektorzy C-Suite czerpią wiedzę bezpośrednio z wgranych plików pamięci w chmurze. CMO w pełni odzwierciedla Twoją osobistą historię ADHD z pliku <code>o_mnie.md</code>.</p>
    """, unsafe_allow_html=True)
    
    agents = {
        "CEO (Dyrektor Zarządzający)": "Strateg produktu cyfrowego. Pilnuje celów wdrożeniowych MVP, weryfikuje monetyzację oraz zaangażowanie społeczności.",
        "CMO (Dyrektor Marketingu)": "Storyteller. Przekłada Twoje doświadczenia z zaciągniętym hamulcem ADHD i cyfrową demencją na autentyczny, poruszający marketing.",
        "Creative Director (Dyrektor Kreatywny)": "Dba o spójność wizualną wideo na TikToku i YouTube zgodnie z precyzyjnymi schematami montażu Adriana Killara.",
        "CSO (Dyrektor Sprzedaży)": "Wdraża strategie lejkowe (metoda Jan Szopy). Buduje bezwysiłkowe procesy zakupowe produktów cyfrowych.",
        "CTO (Technologia + Anti-Gravity)": "Twój asystent ds. kodu, automatyzacji w n8n/Make, chmury oraz dopieszczania designu interfejsu (czysty fiolet i ciemny grafit)."
    }
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        selected_agent = st.selectbox("Wybierz agenta do konsultacji:", list(agents.keys()))
        st.markdown(f"""
        <div class="custom-card" style="border-left: 5px solid #7C3AED;">
            <h4>{selected_agent}</h4>
            <p><strong>Rola operacyjna:</strong><br>{agents[selected_agent]}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.write(f"### Konsultacja z: {selected_agent}")
        user_msg = st.text_input("Zadaj pytanie swojemu Dyrektorowi:", placeholder="Np. Jak sformułować pierwszą ofertę wideo?")
        if st.button("Konsultuj"):
            if user_msg:
                with st.spinner("Odpowiadanie..."):
                    time.sleep(1.2)
                    if "CMO" in selected_agent:
                        st.markdown(f"**CMO Agent:** \"Tomasz, opierając się na pliku `o_mnie.md` i Twojej metaforze 'zaciągniętego hamulca ręcznego', proponuję, abyśmy w pierwszej rolce uderzyli w ten właśnie obraz. Ludzie z ADHD natychmiast utożsamią się z uczuciem wciskania gazu do dechy, podczas gdy ich własna biologia zaciąga hamulec. Skupmy się na empatycznym tonie, odrzucając radykalną 'produktywność dla neurotypowych'. Pokażmy, że Holistic OS to zewnętrzny płat czołowy, który ten hamulec powoli zwalnia. Co o tym sądzisz?\"")
                    elif "CEO" in selected_agent:
                        st.markdown(f"**CEO Agent:** \"Najważniejsze to realne wdrożenie MVP. Nie traćmy czasu na budowanie skomplikowanych lejków zanim nie będziemy mieli 10 pierwszych aktywnych członków społeczności, którzy dadzą nam feedback. Nasz cel: uruchomić dashboard, udostępnić go i zebrać pierwsze opinie. Skoncentrujmy się na minimalnym zestawie funkcji. Mamy dashboard Streamlit, teraz czas na wrzucenie syntez z NotebookLM.\"")
                    else:
                        st.markdown(f"**{selected_agent}:** \"Zrozumiałem zapytanie: '{user_msg}'. Rekomenduję rozbicie wdrożenia na najprostsze kroki w Kanbanie w celu minimalizacji tarcia poznawczego i dowożenia w trybie 'One Thing'.\"")

# 6. ADHD KANBAN
elif menu == "📋 ADHD Kanban":
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
        st.markdown("###  Zrobione")
        for i, t in enumerate(k["done"]):
            st.markdown(f"<div class='custom-card' style='border-left: 4px solid #10B981; opacity: 0.7;'>{t}</div>", unsafe_allow_html=True)
        if k["done"] and st.button("Wyczyść ukończone"):
            k["done"] = []
            save_kanban(k)
            st.rerun()

# 7. USTAWIENIA PAMIĘCI
elif menu == "💾 Pristine Memory":
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
