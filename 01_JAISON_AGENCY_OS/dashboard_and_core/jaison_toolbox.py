# -*- coding: utf-8 -*-
import os
import sys
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def copy_to_clipboard(text):
    try:
        # Use Windows native 'clip' command to avoid external dependencies like pyperclip
        process = subprocess.Popen('clip', stdin=subprocess.PIPE, shell=True)
        process.communicate(input=text.encode('utf-8'))
        return True
    except Exception:
        return False

# Database of useful commands
COMMANDS = [
    # --- GOOGLE CLOUD PLATFORM ---
    {
        "category": "Google Cloud Platform (GCP)",
        "name": "Logowanie do konta GCP (tomaszc4y@gmail.com)",
        "command": "gcloud auth login tomaszc4y@gmail.com",
        "desc": "Uwierzytelnia Twoje główne konto Google Cloud w przeglądarce."
    },
    {
        "category": "Google Cloud Platform (GCP)",
        "name": "Logowanie dla aplikacji lokalnych (ADC)",
        "command": "gcloud auth application-default login",
        "desc": "Generuje lokalne poświadczenia (credentials.json) niezbędne do działania skryptów Vertex AI w Pythonie."
    },
    {
        "category": "Google Cloud Platform (GCP)",
        "name": "Ustawienie aktywnego projektu (coolfon-project)",
        "command": "gcloud config set project coolfon-project",
        "desc": "Przełącza aktywny projekt gcloud na coolfon-project (gdzie masz 1126 zł Free Trial)."
    },
    {
        "category": "Google Cloud Platform (GCP)",
        "name": "Ustawienie aktywnego projektu (GTRM Laptop)",
        "command": "gcloud config set project gtrm-project",
        "desc": "Przełącza aktywny projekt gcloud na projekt kliencki na laptopie."
    },
    {
        "category": "Google Cloud Platform (GCP)",
        "name": "Sprawdzenie aktualnej konfiguracji gcloud",
        "command": "gcloud config list",
        "desc": "Wyświetla zalogowane konto, aktywny projekt oraz ustawioną strefę chmurową."
    },
    
    # --- OLLAMA & LOKALNE MODELE ---
    {
        "category": "Ollama & Lokalne Modele",
        "name": "Uruchomienie modelu Ornith 9B (CPU/GPU)",
        "command": "ollama run deepreinforce/ornith-1.0-9b:q4_k_m",
        "desc": "Uruchamia lokalny model Ornith 9B w konsoli. Jeśli brakuje VRAM, Ollama automatycznie załaduje go do RAM komputera."
    },
    {
        "category": "Ollama & Lokalne Modele",
        "name": "Sprawdzenie listy pobranych modeli lokalnych",
        "command": "ollama list",
        "desc": "Wyświetla listę wszystkich modeli pobranych na Twój komputer oraz ich rozmiary."
    },
    {
        "category": "Ollama & Lokalne Modele",
        "name": "Sprawdzenie aktualnie uruchomionych modeli",
        "command": "ollama ps",
        "desc": "Pokazuje, jakie modele są obecnie załadowane do pamięci RAM/VRAM."
    },

    # --- GIT & GITHUB ---
    {
        "category": "Git & GitHub",
        "name": "Sprawdzenie statusu plików w projekcie",
        "command": "git status",
        "desc": "Pokazuje, które pliki zostały zmienione, dodane lub usunięte od ostatniego zapisu."
    },
    {
        "category": "Git & GitHub",
        "name": "Dodanie wszystkich zmian do poczekalni",
        "command": "git add .",
        "desc": "Przygotowuje wszystkie zmodyfikowane i nowe pliki do zapisu."
    },
    {
        "category": "Git & GitHub",
        "name": "Zapisanie zmian w lokalnej historii (Commit)",
        "command": "git commit -m \"Zapis stanu prac - Jaison OS\"",
        "desc": "Zapisuje zmiany w lokalnym repozytorium z krótkim opisem."
    },
    {
        "category": "Git & GitHub",
        "name": "Wysłanie zmian do chmury GitHub (Push)",
        "command": "git push origin main",
        "desc": "Wysyła Twoje lokalne zapisane commity na prywatne repozytorium GitHub."
    },
    {
        "category": "Git & GitHub",
        "name": "Pobranie najnowszych zmian z GitHub (Pull)",
        "command": "git pull origin main",
        "desc": "Pobiera i scala najnowsze pliki z chmury GitHub na Twój dysk lokalny."
    },

    # --- SERWER (PM2 & HERMES) ---
    {
        "category": "Serwer (PM2 & Hermes)",
        "name": "Start wszystkich usług Hermes",
        "command": "pm2 start ecosystem.config.js",
        "desc": "Uruchamia wszystkie procesy Hermes Agentic OS w tle przy użyciu PM2."
    },
    {
        "category": "Serwer (PM2 & Hermes)",
        "name": "Sprawdzenie statusu usług w PM2",
        "command": "pm2 status",
        "desc": "Wyświetla listę działających procesów w tle, ich zużycie CPU, RAM oraz status restartów."
    },
    {
        "category": "Serwer (PM2 & Hermes)",
        "name": "Restart wybranej usługi",
        "command": "pm2 restart [nazwa_lub_id]",
        "desc": "Restartuje określony proces (np. pm2 restart app lub pm2 restart 0)."
    },
    {
        "category": "Serwer (PM2 & Hermes)",
        "name": "Podgląd logów na żywo (PM2 Logs)",
        "command": "pm2 logs",
        "desc": "Wyświetla strumień logów ze wszystkich usług na żywo. Idealne do debugowania."
    },

    # --- DEPLOYMENT & WDRAŻANIE ---
    {
        "category": "Wdrażanie & Deploy",
        "name": "Uruchomienie skryptu eksportu na USB (Pendrive)",
        "command": "python scratch/export_to_usb.py",
        "desc": "Uruchamia skrypt pakujący czysty projekt i aktywną konwersację bezpośrednio na pendrive D:."
    },
    {
        "category": "Wdrażanie & Deploy",
        "name": "Wdrożenie zmian na serwer Hostido (FTP)",
        "command": "python deploy_ftp.py",
        "desc": "Automatycznie przesyła pliki strony internetowej lub kodu na Twój serwer FTP w Hostido."
    },
    {
        "category": "Wdrażanie & Deploy",
        "name": "Uruchomienie lokalnego serwera testowego Streamlit",
        "command": "streamlit run app.py",
        "desc": "Odpala lokalny interfejs graficzny Jaison Dashboard na Twoim komputerze."
    },

    # --- DIAGNOSTYKA I OCZYSZCZANIE ---
    {
        "category": "Diagnostyka & Czyszczenie",
        "name": "Szybki podgląd zajętości pamięci RAM",
        "command": "Get-Process | Group-Object -Property ProcessName | Select-Object Name, @{Name='WorkingSetMB';Expression={[math]::Round(($_.Group | Measure-Object WorkingSet -Sum).Sum / 1MB, 2)}} | Sort-Object WorkingSetMB -Descending | Select-Object -First 10",
        "desc": "Komenda PowerShell wyświetlająca 10 najbardziej zasobożernych procesów w pamięci RAM."
    }
]

def show_menu():
    print("====================================================================")
    print("   🌐  JAISON TOOLBOX CLI v1.0 — TWOJA BIBLIOTEKA KOMEND  🌐")
    print("====================================================================")
    print(" Wybierz kategorię, aby zobaczyć polecenia, lub wyszukaj słowo kluczowe.\n")
    print(" [1] Google Cloud Platform (GCP)")
    print(" [2] Ollama & Lokalne Modele")
    print(" [3] Git & GitHub (Wersjonowanie i Kopia Zapasowa)")
    print(" [4] Serwer (PM2 & Hermes)")
    print(" [5] Wdrażanie & Deploy (Streamlit / FTP / USB)")
    print(" [6] Diagnostyka & Czyszczenie")
    print(" [s] 🔍 Szybkie Wyszukiwanie (np. 'auth', 'login', 'pm2')")
    print(" [q] Wyjście\n")

def get_category_by_num(choice):
    mapping = {
        "1": "Google Cloud Platform (GCP)",
        "2": "Ollama & Lokalne Modele",
        "3": "Git & GitHub",
        "4": "Serwer (PM2 & Hermes)",
        "5": "Wdrażanie & Deploy",
        "6": "Diagnostyka & Czyszczenie"
    }
    return mapping.get(choice)

def display_commands(commands_list):
    clear_screen()
    print("====================================================================")
    print(f" Wyniki wyszukiwania / Wybrana sekcja (Znaleziono: {len(commands_list)}):")
    print("====================================================================\n")
    
    for idx, cmd in enumerate(commands_list):
        print(f" [{idx + 1}] {cmd['name']}")
        print(f"     👉 Komenda: {cmd['command']}")
        print(f"     📝 Opis:    {cmd['desc']}\n")
        
    print(" [b] Powrót do menu głównego")
    print("--------------------------------------------------------------------")
    
    choice = input(" Wybierz numer komendy, aby AUTOMATYCZNIE skopiować ją do schowka: ").strip()
    
    if choice.lower() == 'b':
        return
        
    try:
        cmd_idx = int(choice) - 1
        if 0 <= cmd_idx < len(commands_list):
            selected_cmd = commands_list[cmd_idx]['command']
            if copy_to_clipboard(selected_cmd):
                print(f"\n ✔️ Sukces! Komenda została skopiowana do schowka: ")
                print(f"   >>> {selected_cmd} <<<")
                print(" Możesz ją teraz po prostu wkleić (Ctrl + V) w swoim terminalu/PowerShell.")
            else:
                print("\n ❌ Wystąpił błąd podczas kopiowania do schowka.")
            input("\n Wciśnij Enter, aby kontynuować...")
        else:
            print("\n ❌ Nieprawidłowy numer komendy.")
            input("\n Wciśnij Enter, aby kontynuować...")
    except ValueError:
        pass

def perform_search():
    clear_screen()
    print("====================================================================")
    print(" 🔍 Szybkie Wyszukiwanie Komend")
    print("====================================================================\n")
    query = input(" Wpisz szukane słowo (np. login, git, ollama, proxy): ").strip().lower()
    
    if not query:
        return
        
    results = []
    for cmd in COMMANDS:
        if (query in cmd['name'].lower() or 
            query in cmd['command'].lower() or 
            query in cmd['desc'].lower() or 
            query in cmd['category'].lower()):
            results.append(cmd)
            
    if results:
        display_commands(results)
    else:
        print("\n ❌ Nie znaleziono żadnych komend pasujących do Twojego zapytania.")
        input("\n Wciśnij Enter, aby kontynuować...")

def main():
    while True:
        clear_screen()
        show_menu()
        choice = input(" Twój wybór: ").strip()
        
        if choice.lower() == 'q':
            print("\n Dziękujemy za korzystanie z Jaison Toolbox. Powodzenia w pracy!")
            break
        elif choice.lower() == 's':
            perform_search()
        elif choice in ["1", "2", "3", "4", "5", "6"]:
            cat_name = get_category_by_num(choice)
            cat_commands = [c for cmd in COMMANDS if cmd['category'] == cat_name for c in [cmd]]
            if cat_commands:
                display_commands(cat_commands)
        else:
            print("\n ❌ Nieprawidłowy wybór. Spróbuj ponownie.")
            input("\n Wciśnij Enter, aby kontynuować...")

if __name__ == "__main__":
    main()
