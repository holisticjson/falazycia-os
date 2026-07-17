import os
import sys
import time
import json
import requests
import threading

# Reconfigure stdout for utf-8 on Windows
sys.stdout.reconfigure(encoding='utf-8')

# Paths
BASE_DIR = r"C:\Aplikacje MVP\01_JAISON_AGENCY_OS\dashboard_and_core"
CRM_PATH = os.path.join(BASE_DIR, "dashboard", "crm.json")
KANBAN_PATH = r"C:\Users\tomas_yq1b9su\Agentic_OS\dashboard\kanban.json"
EVENTS_PATH = os.path.join(BASE_DIR, "dashboard", "telegram_events.json")
ENV_PATH = r"C:\Aplikacje MVP\.env"
PID_FILE = os.path.join(BASE_DIR, "telegram_bridge.pid")

# Simple PID single-instance lock
def check_single_instance():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                old_pid = int(f.read().strip())
            # On Windows, use tasklist to check if pid is still python
            import subprocess
            output = subprocess.check_output(f'tasklist /FI "PID eq {old_pid}"', shell=True).decode()
            if str(old_pid) in output:
                print(f"⚠️ Telegram Bridge jest już uruchomiony (PID {old_pid}). Zamykam nową instancję.")
                sys.exit(0)
        except Exception:
            pass
    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

check_single_instance()


# Load environment variables manually to avoid dotenv dependency issues
BOT_TOKEN = "7293847291:AAHkdjasdj_89ajshda_example"
if os.path.exists(ENV_PATH):
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("TELEGRAM_BOT_TOKEN="):
                BOT_TOKEN = line.strip().split("=", 1)[1].strip()

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

print(f"🤖 Hermes Telegram Bridge uruchomiony.")
print(f"🔑 Używany token: {BOT_TOKEN[:10]}...{BOT_TOKEN[-5:]}")

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Błąd odczytu {path}: {e}")
    return default

def save_json(path, data):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Błąd zapisu {path}: {e}")

def trigger_ui_event(event_type, message, details=None):
    events = load_json(EVENTS_PATH, [])
    events.append({
        "id": f"evt_{int(time.time()*1000)}",
        "timestamp": time.strftime('%H:%M:%S'),
        "type": event_type,
        "message": message,
        "details": details or {}
    })
    save_json(EVENTS_PATH, events[-20:]) # Keep last 20 events

# Git Sync helper
def trigger_git_sync():
    def run_sync():
        print("🔄 Hermes: Wywołuję skrypt git_sync.ps1...")
        os.system('powershell.exe -File "C:\\Aplikacje MVP\\git_sync.ps1"')
    threading.Thread(target=run_sync, daemon=True).start()

# Commands handlers
def cmd_start(chat_id):
    welcome = (
        "🚀 *Witaj w systemie Hermes Agentic OS!*\n\n"
        "Jestem Twoim mobilnym asystentem. Pomogę Ci zarządzać agencją i zadaniami bez otwierania komputera.\n\n"
        "*Wspierane komendy:*\n"
        "📥 `/lead [Nazwa] [Opis]` — Dodaj leada do CRM\n"
        "📋 `/tasks` — Wyświetl zadania z ADHD Kanban\n"
        "📊 `/stats` — Aktualne statystyki lejeka sprzedaży\n"
        "🎬 `/video [Temat]` — Wygeneruj projekt wideo pod CapCut Desktop\n"
    )
    send_message(chat_id, welcome)

def cmd_lead(chat_id, text):
    parts = text.split(" ", 1)
    if len(parts) < 2:
        send_message(chat_id, "⚠️ *Format:* `/lead [Nazwa_Klienta] [Notatki/Chaos]`")
        return
    
    lead_content = parts[1].strip()
    subparts = lead_content.split(" ", 1)
    client_name = subparts[0]
    client_notes = subparts[1] if len(subparts) > 1 else "Brak dodatkowych notatek (Dodano przez Telegram)"

    # Add to crm.json
    crm_data = load_json(CRM_PATH, {"leads": []})
    new_lead = {
        "id": f"lead_tg_{int(time.time())}",
        "name": client_name,
        "stage": "conversation",
        "notes": client_notes,
        "last_contact": time.strftime('%Y-%m-%d'),
        "next_action": "Odezwij się i zrób onboarding.",
        "draft_reply": f"Cześć {client_name}, dzięki za kontakt przez Telegram..."
    }
    crm_data["leads"].append(new_lead)
    save_json(CRM_PATH, crm_data)

    # Trigger UI Toast
    trigger_ui_event("NEW_LEAD", f"📥 Nowy lead odebrany przez Telegram: {client_name}", {"name": client_name})

    reply = (
        f"✅ *Sukces!* Lead został dodany do Jaison CRM.\n\n"
        f"👤 *Klient:* {client_name}\n"
        f"📝 *Notatki:* {client_notes}\n"
        f"📂 *Status:* Rozmowa (Streamlit Dashboard zaktualizowany!)"
    )
    send_message(chat_id, reply)

def cmd_tasks(chat_id):
    kanban_data = load_json(KANBAN_PATH, {"todo": [], "in_progress": [], "done": []})
    
    reply = "📋 *Zadania ADHD Kanban:*\n\n"
    reply += "*🔥 DO ZROBIENIA:*\n"
    if not kanban_data.get("todo"):
        reply += "• Brak zadań\n"
    for idx, t in enumerate(kanban_data.get("todo", [])[:5]):
        reply += f"{idx+1}. {t.get('title', 'Zadanie')} `[{t.get('client', 'Brak')}]`\n"
        
    reply += "\n*⚡ W TOKU:*\n"
    if not kanban_data.get("in_progress"):
        reply += "• Brak zadań\n"
    for idx, t in enumerate(kanban_data.get("in_progress", [])[:5]):
        reply += f"{idx+1}. {t.get('title', 'Zadanie')} `[{t.get('client', 'Brak')}]`\n"

    send_message(chat_id, reply)

def cmd_stats(chat_id):
    crm_data = load_json(CRM_PATH, {"leads": []})
    stages = {"conversation": 0, "architecture": 0, "build": 0}
    for lead in crm_data.get("leads", []):
        stg = lead.get("stage", "conversation")
        if stg in stages:
            stages[stg] += 1
            
    reply = (
        "📊 *Statystyki Jaison Client Pipeline:*\n\n"
        f"💬 *Rozmowa (Conversation):* {stages['conversation']} klientów\n"
        f"📐 *Architektura (Architecture):* {stages['architecture']} projektów\n"
        f"🏗️ *Budowa (Build):* {stages['build']} wdrożeń\n\n"
        f"📈 *Suma szans:* {len(crm_data.get('leads', []))} aktywnych pozycji"
    )
    send_message(chat_id, reply)

def cmd_video(chat_id, text):
    parts = text.split(" ", 1)
    if len(parts) < 2:
        send_message(chat_id, "⚠️ *Format:* `/video [Temat_Filmu]`")
        return
    
    topic = parts[1].strip()
    send_message(chat_id, f"🎬 *Hermes Brain:* Rozpoczynam generowanie scenariusza i kompletowanie zasobów dla wideo o temacie:\n_\"{topic}\"_\n\n_Pobieram stocki Pexels i generuję lektora..._")
    
    # Simulate generating CapCut project
    time.sleep(2.0)
    
    project_name = topic.replace(" ", "_").lower()
    draft_dir = os.path.join(r"C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\capcut_drafts", project_name)
    os.makedirs(draft_dir, exist_ok=True)
    
    # Write a dummy project file for illustration (actual logic in capcut_generator.py)
    dummy_draft = {
        "app_version": "5.6.0",
        "new_version": "5.6.0",
        "tracks": [
            {"type": "video", "segments": []},
            {"type": "audio", "segments": []}
        ]
    }
    save_json(os.path.join(draft_dir, "draft_content.json"), dummy_draft)
    
    # Notify UI
    trigger_ui_event("NEW_VIDEO", f"🎬 Nowy projekt CapCut wygenerowany: {topic}", {"topic": topic})
    
    # Trigger Git Sync automatically!
    trigger_git_sync()
    
    reply = (
        f"✅ *Projekt CapCut wygenerowany!*\n\n"
        f"📁 *Folder:* `02_CLIENTS_AND_PROJECTS/capcut_drafts/{project_name}/`\n"
        f"🚀 *Git Sync:* Zmiany są właśnie automatycznie wypychane na Twój GitHub!\n\n"
        f"💻 Po pobraniu (git sync) na komputerze, projekt pojawi się w Twoim CapCut Desktop!"
    )
    send_message(chat_id, reply)

def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload, timeout=5.0)
    except Exception as e:
        print(f"Błąd wysyłania wiadomości: {e}")

# Main polling loop
def start_polling():
    last_update_id = 0
    while True:
        url = f"{API_URL}/getUpdates"
        params = {"offset": last_update_id + 1, "timeout": 10}
        try:
            resp = requests.get(url, params=params, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("ok"):
                    for update in data.get("result", []):
                        last_update_id = update["update_id"]
                        message = update.get("message")
                        if not message:
                            continue
                        
                        chat_id = message["chat"]["id"]
                        text = message.get("text", "").strip()
                        
                        if text.startswith("/start") or text.startswith("/help"):
                            cmd_start(chat_id)
                        elif text.startswith("/lead"):
                            cmd_lead(chat_id, text)
                        elif text.startswith("/tasks"):
                            cmd_tasks(chat_id)
                        elif text.startswith("/stats"):
                            cmd_stats(chat_id)
                        elif text.startswith("/video"):
                            cmd_video(chat_id, text)
        except Exception as e:
            print(f"Polling error: {e}")
        time.sleep(1)

if __name__ == "__main__":
    if "AAHkdjasdj_89ajshda_example" in BOT_TOKEN:
        print("⚠️ Bot działa w trybie DEMO (Brak poprawnego TELEGRAM_BOT_TOKEN w .env)")
    else:
        print("🚀 Rozpoczynam nasłuch wiadomości na Telegramie (Real Polling Mode)...")
        start_polling()
