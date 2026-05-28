import streamlit as st
import json
import os
from datetime import datetime

# Ścieżka do bazy danych Kanban
KANBAN_PATH = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\ADHD\kanban_tasks.json"

def load_kanban_tasks():
    """Wczytuje zadania z bazy danych JSON. Jeśli plik nie istnieje, tworzy domyślną bazę."""
    if not os.path.exists(KANBAN_PATH):
        os.makedirs(os.path.dirname(KANBAN_PATH), exist_ok=True)
        default_tasks = {
            "tasks": [
                {
                    "id": "t1",
                    "title": "Migracja Vertex AI do nowego projektu GCP",
                    "status": "DONE",
                    "category": "⚙️ System",
                    "energy_cost": "High",
                    "points": 50,
                    "created_at": datetime.now().isoformat(),
                    "checklist": [
                        {"item": "Pobrać nowy klucz JSON", "completed": True},
                        {"item": "Zmienić konfigurację w plikach .py i .ps1", "completed": True},
                        {"item": "Przetestować połączenie Vertex AI", "completed": True}
                    ],
                    "notes": "Vertex AI działa teraz poprawnie pod projektem holistic-dashboard-dev."
                },
                {
                    "id": "t2",
                    "title": "Wdrożenie interaktywnej tablicy Kanban",
                    "status": "IN_PROGRESS",
                    "category": "🎨 UX/UI",
                    "energy_cost": "Medium",
                    "points": 80,
                    "created_at": datetime.now().isoformat(),
                    "checklist": [
                        {"item": "Stworzyć silnik bazy danych JSON", "completed": True},
                        {"item": "Zbudować interfejs kolumn w Streamlit", "completed": True},
                        {"item": "Dodać tryb Hiper-Skupienia i Dopamine Boost", "completed": False}
                    ],
                    "notes": "Zaprojektować tak, by redukować visual overload i ułatwiać brain dump."
                },
                {
                    "id": "t3",
                    "title": "Zrzut myśli: Zapisać nowe pomysły biznesowe",
                    "status": "INBOX",
                    "category": "💡 Idea",
                    "energy_cost": "Low",
                    "points": 15,
                    "created_at": datetime.now().isoformat(),
                    "checklist": [
                        {"item": "Odpalić Ingestion Hub", "completed": False}
                    ],
                    "notes": "Szybki brain dump bez presji czasu."
                }
            ]
        }
        with open(KANBAN_PATH, "w", encoding="utf-8") as f:
            json.dump(default_tasks, f, ensure_ascii=False, indent=2)
        return default_tasks
    try:
        with open(KANBAN_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"tasks": []}

def save_kanban_tasks(data):
    """Zapisuje zadania do bazy danych JSON."""
    os.makedirs(os.path.dirname(KANBAN_PATH), exist_ok=True)
    with open(KANBAN_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_kanban_task(title, category="📥 Inbox", energy_cost="Medium", points=25, checklist=None, notes=""):
    """Dodaje nowe zadanie do kolumny INBOX."""
    data = load_kanban_tasks()
    task_id = "t" + str(int(datetime.now().timestamp() * 1000))
    new_task = {
        "id": task_id,
        "title": title,
        "status": "INBOX",
        "category": category,
        "energy_cost": energy_cost,
        "points": points,
        "created_at": datetime.now().isoformat(),
        "checklist": checklist if checklist else [],
        "notes": notes
    }
    data["tasks"].append(new_task)
    save_kanban_tasks(data)
    return new_task

def update_task_status(task_id, new_status, log_dopamine_fn=None):
    """Aktualizuje status zadania. Jeśli przechodzi w DONE, opcjonalnie wywołuje callback dopamine journal."""
    data = load_kanban_tasks()
    for task in data["tasks"]:
        if task["id"] == task_id:
            old_status = task["status"]
            if old_status == new_status:
                return
            task["status"] = new_status
            save_kanban_tasks(data)
            
            # Dopamine Boost przy zakończeniu zadania!
            if new_status == "DONE" and old_status != "DONE" and log_dopamine_fn:
                log_dopamine_fn("🔥 Zadanie", f"Ukończono zadanie: {task['title']}", task.get("points", 25))
            break

def delete_kanban_task(task_id):
    """Usuwa zadanie z tablicy."""
    data = load_kanban_tasks()
    data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
    save_kanban_tasks(data)

def render_kanban_styles():
    """Inżynieria wizualna — wstrzykuje premium CSS do Streamlit."""
    st.markdown("""
    <style>
        /* Styl kontenerów kolumn */
        .kanban-col {
            background: rgba(15, 23, 42, 0.4);
            border-radius: 16px;
            padding: 16px;
            min-height: 500px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            margin-bottom: 20px;
        }
        .kanban-header {
            font-size: 16px;
            font-weight: 700;
            padding: 8px 12px;
            border-radius: 10px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        /* Kolorystyka nagłówków kolumn */
        .hdr-inbox { background: rgba(148, 163, 184, 0.15); color: #cbd5e1; border-left: 4px solid #94a3b8; }
        .hdr-todo { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border-left: 4px solid #3b82f6; }
        .hdr-progress { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border-left: 4px solid #f59e0b; }
        .hdr-done { background: rgba(16, 185, 129, 0.15); color: #34d399; border-left: 4px solid #10b981; }
        
        /* Styl karty zadania */
        .kanban-card {
            background: rgba(30, 41, 59, 0.7);
            border-radius: 12px;
            padding: 14px;
            margin-bottom: 12px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transition: all 0.2s ease-in-out;
        }
        .kanban-card:hover {
            transform: translateY(-2px);
            border-color: rgba(255, 255, 255, 0.15);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
        }
        
        /* Badges i metryki kart */
        .card-tag {
            font-size: 10px;
            font-weight: 600;
            text-transform: uppercase;
            padding: 2px 8px;
            border-radius: 8px;
            margin-right: 4px;
            display: inline-block;
        }
        .tag-category { background: rgba(139, 92, 246, 0.2); color: #c084fc; }
        
        /* Energy cost badges */
        .energy-low { background: rgba(16, 185, 129, 0.15); color: #34d399; }
        .energy-medium { background: rgba(245, 158, 11, 0.15); color: #fbbf24; }
        .energy-high { background: rgba(239, 68, 68, 0.15); color: #f87171; }
        
        .card-points {
            font-size: 11px;
            font-weight: 700;
            color: #10b981;
            float: right;
        }
        .card-title {
            font-size: 13px;
            font-weight: 600;
            margin-top: 8px;
            margin-bottom: 8px;
            color: #f1f5f9;
            line-height: 1.4;
        }
        .progress-text {
            font-size: 11px;
            color: #94a3b8;
            margin-top: 4px;
        }
        
        /* Tryb Hiper Skupienia */
        .focus-banner {
            background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%);
            border-radius: 20px;
            padding: 30px;
            border: 2px solid #8b5cf6;
            box-shadow: 0 0 30px rgba(139, 92, 246, 0.3);
            text-align: center;
            margin-bottom: 24px;
        }
        
        .focus-title {
            font-size: 24px;
            font-weight: 800;
            color: #f8fafc;
            margin-bottom: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

def render_kanban_board(log_dopamine_fn=None):
    """Główna tablica Kanban zoptymalizowana dla ADHD."""
    render_kanban_styles()
    
    # Inicjalizacja stanu widoków
    if "kanban_view" not in st.session_state:
        st.session_state.kanban_view = "board"  # "board", "list" lub "focus"
    if "focus_task_id" not in st.session_state:
        st.session_state.focus_task_id = None
        
    data = load_kanban_tasks()
    tasks = data.get("tasks", [])
    
    # Szybki zrzut myśli (Quick Ingest / Brain Dump) - Zawsze u góry!
    st.markdown('<div class="inflow-card" style="border: 1px solid rgba(139, 92, 246, 0.3);">', unsafe_allow_html=True)
    st.markdown("#### ⚡ Szybka Zrzutnia Myśli (Quick Brain Dump)")
    col_in1, col_in2, col_in3 = st.columns([4, 1, 1])
    with col_in1:
        new_title = st.text_input("Zapisz cokolwiek chodzi Ci po głowie... (Zadanie zostanie wrzucone do Inboxa)", placeholder="np. Zadzwonić do Szopy ws. GBP API...", key="quick_capt_title")
    with col_in2:
        new_cat = st.text_input("Kategoria / Tag:", value="💡 Pomysł", key="quick_capt_cat")
    with col_in3:
        new_energy = st.selectbox("Wysiłek (Energia):", ["Low", "Medium", "High"], key="quick_capt_energy")
        
    if st.button("📥 Zrzut do Inboxa (+15 pkt)", use_container_width=True, type="primary"):
        if new_title:
            points = 15 if new_energy == "Low" else (30 if new_energy == "Medium" else 50)
            add_kanban_task(new_title, category=new_cat, energy_cost=new_energy, points=points)
            if log_dopamine_fn:
                log_dopamine_fn("🧠 Inne", f"Zrobiono szybki brain dump: {new_title}", 15)
            st.toast("🎉 Przechwycono myśl! Bezpiecznie spoczywa w Inboxie.")
            st.rerun()
        else:
            st.warning("Wpisz treść przed zapisem!")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Wybór widoku
    col_v1, col_v2 = st.columns([3, 1])
    with col_v1:
        st.subheader("📋 Twoje Centrum Zadań i Przepływu")
    with col_v2:
        view_opt = st.segmented_control("Widok:", ["Tablica 📊", "Lista 📝"], default="Tablica 📊")
        st.session_state.kanban_view = "board" if "Tablica" in view_opt else "list"
        
    # === TRYB FOCUS (Hiper-Skupienie) ===
    if st.session_state.focus_task_id:
        active_task = next((t for t in tasks if t["id"] == st.session_state.focus_task_id), None)
        if active_task:
            st.markdown(f"""
            <div class="focus-banner">
                <div class="focus-title">🧘 Tryb Hiper Skupienia</div>
                <p style="font-size:16px; color:#cbd5e1; margin-bottom:0;">Tomasz, Twój mózg skupia się teraz wyłącznie na tym jednym wyzwaniu. Wyłącz powiadomienia, wycisz otoczenie.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Karta zadania w trybie Focus
            st.markdown(f"""
            <div class="kanban-card" style="border: 2px solid #10b981; background: rgba(16, 185, 129, 0.05); padding: 24px;">
                <span class="card-tag tag-category">{active_task['category']}</span>
                <span class="card-tag energy-{active_task['energy_cost'].lower()}">⚡ Wysiłek: {active_task['energy_cost']}</span>
                <span class="card-points">💎 {active_task.get('points', 25)} PKT</span>
                <h2 style="color:white; margin-top:12px; margin-bottom:8px;">{active_task['title']}</h2>
                <p style="color:#94a3b8; font-size:14px;">{active_task.get('notes', 'Brak szczegółowych notatek.')}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Checklist w trybie Focus
            st.markdown("### ✅ Checklist Zadania:")
            checklist_changed = False
            for idx, item in enumerate(active_task.get("checklist", [])):
                chk_state = st.checkbox(item["item"], value=item["completed"], key=f"focus_chk_{active_task['id']}_{idx}")
                if chk_state != item["completed"]:
                    active_task["checklist"][idx]["completed"] = chk_state
                    checklist_changed = True
                    
            if checklist_changed:
                save_kanban_tasks(data)
                st.toast("Postęp zaktualizowany!")
                st.rerun()
                
            # Akcje w trybie Focus
            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                if st.button("🏆 Zakończ i Zgłoś Wygraną!", use_container_width=True, type="primary"):
                    # Oznacz jako DONE
                    update_task_status(active_task["id"], "DONE", log_dopamine_fn)
                    st.session_state.focus_task_id = None
                    st.success("🎉 Niesamowita robota Tomasz! Zadanie ukończone!")
                    st.rerun()
            with f_col2:
                if st.button("⏸️ Zawieś (Zwróć do W Trakcie)", use_container_width=True):
                    update_task_status(active_task["id"], "IN_PROGRESS")
                    st.session_state.focus_task_id = None
                    st.rerun()
            with f_col3:
                if st.button("🚪 Wyjdź z trybu Focus", use_container_width=True):
                    st.session_state.focus_task_id = None
                    st.rerun()
            return # Zatrzymujemy renderowanie reszty tablicy podczas Focus Mode!
            
    # === RENDERING LIST VIEW ===
    if st.session_state.kanban_view == "list":
        st.markdown("### 📝 Szybka Lista Zadań")
        if not tasks:
            st.info("Brak zadań na tablicy. Użyj zrzutni u góry!")
        for task in tasks:
            with st.expander(f"[{task['status']}] {task['title']} ({task['category']})", expanded=False):
                # Informacje o zadaniu
                st.markdown(f"**Wysiłek:** {task['energy_cost']} | **Wartość:** {task.get('points', 25)} pkt | **Utworzono:** {task['created_at'][:10]}")
                st.markdown(f"**Notatki:** {task.get('notes', 'Brak')}")
                
                # Checklist
                st.markdown("**Checklist:**")
                chk_changed = False
                for idx, item in enumerate(task.get("checklist", [])):
                    c_val = st.checkbox(item["item"], value=item["completed"], key=f"list_chk_{task['id']}_{idx}")
                    if c_val != item["completed"]:
                        task["checklist"][idx]["completed"] = c_val
                        chk_changed = True
                if chk_changed:
                    save_kanban_tasks(data)
                    st.rerun()
                    
                # Akcje
                col_la, col_lb, col_lc = st.columns(3)
                with col_la:
                    new_st = st.selectbox("Zmień status:", ["INBOX", "TO_DO", "IN_PROGRESS", "DONE"], index=["INBOX", "TO_DO", "IN_PROGRESS", "DONE"].index(task["status"]), key=f"list_status_{task['id']}")
                    if new_st != task["status"]:
                        update_task_status(task["id"], new_st, log_dopamine_fn)
                        st.rerun()
                with col_lb:
                    if st.button("🧘 Hiper-Skupienie", key=f"list_focus_{task['id']}", use_container_width=True):
                        st.session_state.focus_task_id = task["id"]
                        st.rerun()
                with col_lc:
                    if st.button("🗑️ Usuń", key=f"list_del_{task['id']}", use_container_width=True):
                        delete_kanban_task(task["id"])
                        st.rerun()
        return

    # === RENDERING KANBAN BOARD ===
    c_inbox, c_todo, c_progress, c_done = st.columns(4)
    
    # Filtrowanie zadań po statusach
    inbox_tasks = [t for t in tasks if t["status"] == "INBOX"]
    todo_tasks = [t for t in tasks if t["status"] == "TO_DO"]
    progress_tasks = [t for t in tasks if t["status"] == "IN_PROGRESS"]
    done_tasks = [t for t in tasks if t["status"] == "DONE"]
    
    # 📥 1. COLUMN: INBOX
    with c_inbox:
        st.markdown(f'<div class="kanban-header hdr-inbox">📥 Inbox <span>{len(inbox_tasks)}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="kanban-col">', unsafe_allow_html=True)
        for task in inbox_tasks:
            st.markdown(f"""
            <div class="kanban-card">
                <span class="card-tag tag-category">{task['category']}</span>
                <span class="card-tag energy-{task['energy_cost'].lower()}">⚡ {task['energy_cost']}</span>
                <span class="card-points">💎 {task.get('points', 25)} PKT</span>
                <div class="card-title">{task['title']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Kontrolki karty (Progressive Disclosure)
            with st.expander("🛠️ Zarządzaj", expanded=False):
                # Notatki
                task_notes = st.text_area("Szczegóły / Notatki:", value=task.get("notes", ""), key=f"notes_{task['id']}")
                if task_notes != task.get("notes", ""):
                    task["notes"] = task_notes
                    save_kanban_tasks(data)
                    
                # Akcje
                if st.button("🎯 Akceptuj do To Do", key=f"act_todo_{task['id']}", use_container_width=True):
                    update_task_status(task["id"], "TO_DO")
                    st.rerun()
                if st.button("🔥 Rozpocznij natychmiast!", key=f"act_start_{task['id']}", use_container_width=True):
                    update_task_status(task["id"], "IN_PROGRESS")
                    st.session_state.focus_task_id = task["id"] # Od razu wrzucamy w skupienie!
                    st.rerun()
                if st.button("🗑️ Usuń", key=f"act_del_{task['id']}", use_container_width=True):
                    delete_kanban_task(task["id"])
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # 🎯 2. COLUMN: TO DO
    with c_todo:
        st.markdown(f'<div class="kanban-header hdr-todo">🎯 Do Zrobienia <span>{len(todo_tasks)}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="kanban-col">', unsafe_allow_html=True)
        for task in todo_tasks:
            # Liczba podzadań zrobionych
            chk_list = task.get("checklist", [])
            done_count = sum(1 for c in chk_list if c["completed"])
            total_count = len(chk_list)
            progress_str = f"📋 {done_count}/{total_count} kroków" if total_count > 0 else ""
            
            st.markdown(f"""
            <div class="kanban-card">
                <span class="card-tag tag-category">{task['category']}</span>
                <span class="card-tag energy-{task['energy_cost'].lower()}">⚡ {task['energy_cost']}</span>
                <span class="card-points">💎 {task.get('points', 25)} PKT</span>
                <div class="card-title">{task['title']}</div>
                <div class="progress-text">{progress_str}</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🛠️ Zarządzaj / Checklist", expanded=False):
                # Checklist edit
                st.markdown("**Mini kroki (Tiny Step Strategy):**")
                checklist_changed = False
                for idx, chk in enumerate(chk_list):
                    c_val = st.checkbox(chk["item"], value=chk["completed"], key=f"todo_chk_{task['id']}_{idx}")
                    if c_val != chk["completed"]:
                        task["checklist"][idx]["completed"] = c_val
                        checklist_changed = True
                
                # Dodaj nowy krok do checklisty
                new_step = st.text_input("Dodaj mały krok < 60s:", key=f"new_step_{task['id']}", placeholder="np. Otworzyć przeglądarkę...")
                if st.button("➕ Dodaj krok", key=f"btn_add_step_{task['id']}"):
                    if new_step:
                        task.setdefault("checklist", []).append({"item": new_step, "completed": False})
                        checklist_changed = True
                        
                if checklist_changed:
                    save_kanban_tasks(data)
                    st.rerun()
                    
                # Akcje
                if st.button("🔥 Start (Praca)", key=f"todo_start_{task['id']}", use_container_width=True):
                    update_task_status(task["id"], "IN_PROGRESS")
                    st.session_state.focus_task_id = task["id"] # Od razu wrzucamy w tryb skupienia!
                    st.rerun()
                if st.button("📥 Zwróć do Inbox", key=f"todo_ret_{task['id']}", use_container_width=True):
                    update_task_status(task["id"], "INBOX")
                    st.rerun()
                if st.button("🗑️ Usuń", key=f"todo_del_{task['id']}", use_container_width=True):
                    delete_kanban_task(task["id"])
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # 🔥 3. COLUMN: IN PROGRESS (Limit: tylko 1-2 zadania dla focusu!)
    with c_progress:
        st.markdown(f'<div class="kanban-header hdr-progress">🔥 W Trakcie <span>{len(progress_tasks)}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="kanban-col">', unsafe_allow_html=True)
        
        # Ostrzeżenie przed paraliżem wielozadaniowości
        if len(progress_tasks) > 1:
            st.warning("⚠️ Tomasz, skup się tylko na JEDNYM zadaniu na raz! Mózg z ADHD traci wydajność na multitaskingu.")
            
        for task in progress_tasks:
            chk_list = task.get("checklist", [])
            done_count = sum(1 for c in chk_list if c["completed"])
            total_count = len(chk_list)
            progress_str = f"📋 {done_count}/{total_count} kroków" if total_count > 0 else ""
            
            st.markdown(f"""
            <div class="kanban-card" style="border: 1px solid #f59e0b; background: rgba(245, 158, 11, 0.03);">
                <span class="card-tag tag-category">{task['category']}</span>
                <span class="card-tag energy-{task['energy_cost'].lower()}">⚡ {task['energy_cost']}</span>
                <span class="card-points">💎 {task.get('points', 25)} PKT</span>
                <div class="card-title" style="font-weight: 700; color:#fbbf24;">{task['title']}</div>
                <div class="progress-text">{progress_str}</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🛠️ Zarządzaj / Postęp", expanded=False):
                # Checklist
                checklist_changed = False
                for idx, chk in enumerate(chk_list):
                    c_val = st.checkbox(chk["item"], value=chk["completed"], key=f"prog_chk_{task['id']}_{idx}")
                    if c_val != chk["completed"]:
                        task["checklist"][idx]["completed"] = c_val
                        checklist_changed = True
                if checklist_changed:
                    save_kanban_tasks(data)
                    st.rerun()
                    
                # Akcje
                if st.button("🧘 Wejdź w Hiper-Skupienie", key=f"prog_focus_{task['id']}", use_container_width=True, type="primary"):
                    st.session_state.focus_task_id = task["id"]
                    st.rerun()
                if st.button("🏆 Gotowe! (+Dopamine Boost)", key=f"prog_done_{task['id']}", use_container_width=True):
                    update_task_status(task["id"], "DONE", log_dopamine_fn)
                    st.rerun()
                if st.button("🎯 Odłóż (Zwróć do To Do)", key=f"prog_ret_{task['id']}", use_container_width=True):
                    update_task_status(task["id"], "TO_DO")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # ✅ 4. COLUMN: DONE
    with c_done:
        st.markdown(f'<div class="kanban-header hdr-done">✅ Zrobione <span>{len(done_tasks)}</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="kanban-col">', unsafe_allow_html=True)
        for task in done_tasks:
            st.markdown(f"""
            <div class="kanban-card" style="border: 1px solid rgba(16, 185, 129, 0.2); background: rgba(16, 185, 129, 0.02); opacity: 0.85;">
                <span class="card-tag tag-category">{task['category']}</span>
                <span class="card-points" style="text-decoration: line-through; color: #94a3b8;">💎 {task.get('points', 25)} PKT</span>
                <div class="card-title" style="text-decoration: line-through; color: #94a3b8;">{task['title']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("🛠️ Zarządzaj", expanded=False):
                if st.button("🔄 Przywróć do To Do", key=f"done_ret_{task['id']}", use_container_width=True):
                    update_task_status(task["id"], "TO_DO")
                    st.rerun()
                if st.button("🗑️ Usuń permamentnie", key=f"done_del_{task['id']}", use_container_width=True):
                    delete_kanban_task(task["id"])
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
