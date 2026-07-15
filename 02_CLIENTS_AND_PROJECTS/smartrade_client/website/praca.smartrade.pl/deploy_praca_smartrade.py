import os
import sys
import ftplib

# Konfiguracja FTP (Domyślna)
FTP_HOST = "smartrade.pl"
FTP_USER = "deploy@smartrade.pl"
FTP_PASS = "Kosmos!!1234"

# Ścieżka lokalna
LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))

# Pliki i foldery do wdrożenia
FILES_TO_UPLOAD = [
    "index.html",
    "style.css",
    "app.js",
    "polityka.html",
    "gandia_hero_bg.png",
    "luxury_renovation_spain.png"
]

API_FILES = [
    "api/chat.php",
    "api/config.php"
]

def upload_file(ftp, local_path, remote_path):
    print(f" -> Wgrywanie {os.path.basename(local_path)} do {remote_path}...", end="")
    try:
        with open(local_path, "rb") as f:
            ftp.storbinary(f"STOR {remote_path}", f)
        print(" OK!")
    except Exception as e:
        print(f" BŁĄD: {e}")

def deploy():
    global FTP_USER, FTP_PASS
    print("\n" + "="*50)
    print("        SMARTRADE PRACA - FTP DEPLOYER")
    print("="*50)
    print(f"Łączenie z hostem FTP: {FTP_HOST}...")
    
    try:
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print(f"Pomyślnie zalogowano jako: {FTP_USER}")
        print(f"Aktualny katalog roboczy: {ftp.pwd()}")
    except Exception as e:
        print(f"BŁĄD logowania FTP: {e}")
        return

    # Listowanie plików, by ułatwić diagnozę
    entries = []
    ftp.retrlines('LIST', entries.append)
    is_main_deploy = any("public_html" in entry for entry in entries)
    
    target_dir = "public_html"
    
    if FTP_USER == "deploy@smartrade.pl":
        print("\n[OSTRZEŻENIE] Zalogowano jako deploy@smartrade.pl.")
        print("To konto ma dostęp TYLKO do głównej domeny smartrade.pl.")
        print("Jeśli chcesz wdrożyć pliki na poddomenę praca.smartrade.pl,")
        print("która została dodana jako osobna witryna w DirectAdmin,")
        print("musisz podać dane konta FTP przypisanego do praca.smartrade.pl.")
        print("Np. uruchom: python deploy_praca_smartrade.py deploy@praca.smartrade.pl TwojeHasło\n")
    
    # Próba wejścia do katalogu docelowego (np. public_html)
    try:
        ftp.cwd(target_dir)
        print(f"Wejście do katalogu docelowego: {ftp.pwd()}")
    except Exception as e:
        print(f"BŁĄD: Nie można wejść do katalogu '{target_dir}': {e}")
        ftp.quit()
        return

    # Wyszukiwanie domyślnego pliku index.html lub index.php stworzonego przez DirectAdmin
    print("\nSprawdzanie obecności domyślnych plików DirectAdmin...")
    remote_files = []
    ftp.retrlines('NLST', remote_files.append)
    
    # Usuwanie domyślnych plików zastępczych, jeśli istnieją, by nie zasłaniały naszej strony
    for placeholder in ["index.html", "index.php", "default.html"]:
        if placeholder in remote_files:
            try:
                # Pobierzmy kawałek pliku, by upewnić się, czy to placeholder
                lines = []
                ftp.retrlines(f"RETR {placeholder}", lines.append)
                file_content = "\n".join(lines)
                if "symbol zast" in file_content or "DirectAdmin" in file_content or len(file_content) < 2000:
                    print(f" -> Wykryto domyślny plik DirectAdmin: {placeholder}. Zmiana nazwy na {placeholder}.bak...")
                    try:
                        ftp.delete(f"{placeholder}.bak") # Usuń stary backup jeśli istnieje
                    except Exception:
                        pass
                    ftp.rename(placeholder, f"{placeholder}.bak")
                    print("    OK!")
            except Exception as e:
                print(f" -> Nie można zmienić nazwy {placeholder}: {e}")

    print("\nWgrywanie głównych plików landing page...")
    for file_name in FILES_TO_UPLOAD:
        local_path = os.path.join(LOCAL_DIR, file_name)
        if os.path.exists(local_path):
            upload_file(ftp, local_path, file_name)
        else:
            print(f"Ostrzeżenie: Brak lokalnego pliku {local_path}")

    # Wgrywanie folderu api i jego zawartości
    print("\nKonfiguracja folderu 'api' on serwerze...")
    try:
        ftp.mkd("api")
        print(" -> Utworzono katalog 'api'.")
    except Exception:
        # Prawdopodobnie już istnieje
        pass

    for file_path in API_FILES:
        local_path = os.path.join(LOCAL_DIR, file_path)
        if os.path.exists(local_path):
            upload_file(ftp, local_path, file_path)
        else:
            print(f"Ostrzeżenie: Brak lokalnego pliku {local_path}")

    ftp.quit()
    print("="*50)
    print("        DEPLOMENT ZAKOŃCZONY POMYŚLNIE!")
    print("="*50 + "\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        FTP_USER = sys.argv[1]
    if len(sys.argv) > 2:
        FTP_PASS = sys.argv[2]
    deploy()
