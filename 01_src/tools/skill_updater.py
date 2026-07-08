import os
import requests
import time

PLUGIN_DIR = r"C:\Users\tomas_yq1b9su\.gemini\config\plugins\holistic_skills"
# W przyszłości podmienisz URL na własne, chronione repozytorium lub Google Drive / Telegram
SKILL_REPO_URL = "https://raw.githubusercontent.com/twoja-agencja/antigravity-skills/main/skills.json"

def ensure_dir():
    if not os.path.exists(PLUGIN_DIR):
        os.makedirs(PLUGIN_DIR)

def sync_skills():
    ensure_dir()
    print("Rozpoczynam synchronizację Skilli (Agentic Workflow)...")
    
    try:
        # POBIERANIE SKILLI (Przykład: na razie zwraca mock, by uniknąć 404 w Twoim systemie dopóki nie założysz repo)
        # response = requests.get(SKILL_REPO_URL, timeout=10)
        # if response.status_code == 200:
        #     skills = response.json()
        
        skills = {
            "lead_qualifier": {
                "name": "Lead Qualifier",
                "content": "---\nname: lead_qualifier\ndescription: Weryfikuje leada pod kątem budżetu z maila.\n---\n# Instrukcja\nUżyj Gemini do ekstrakcji kwot budżetu..."
            }
        }
        
        for skill_id, skill_data in skills.items():
            skill_folder = os.path.join(PLUGIN_DIR, skill_id)
            if not os.path.exists(skill_folder):
                os.makedirs(skill_folder)
            
            skill_file = os.path.join(skill_folder, "SKILL.md")
            # Nie nadpisuj jeśli istnieje, by nie psuć Twoich własnych zmian, chyba że jest to nowa wersja
            if not os.path.exists(skill_file):
                with open(skill_file, "w", encoding="utf-8") as f:
                    f.write(skill_data["content"])
                print(f"✅ Dodano nowy Skill: {skill_data['name']}")
                # Tutaj dodamy kod wywołujący Telegram MCP by poinformować Tomasza: "Szefie, zainstalowałem nową umiejętność!"
        
        print("Synchronizacja ukończona!")
        
    except Exception as e:
        print(f"Błąd synchronizacji: {str(e)}")

if __name__ == "__main__":
    sync_skills()
