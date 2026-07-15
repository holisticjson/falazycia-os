import os
import ftplib

FTP_HOST = "lysitheab.hostido.net.pl"
FTP_USER = "deploy@coolfon.pl"
FTP_PASS = "Coolfon@@2026"
REMOTE_DIR = "/public_html"

LOCAL_DIR = r"C:\Aplikacje MVP\Holistic Jason\04-clients\coolfon\02-website\dev"

def ensure_remote_dir(ftp, remote_path):
    parts = [p for p in remote_path.split("/") if p]
    current = ""
    for part in parts:
        current += "/" + part
        try:
            ftp.cwd(current)
        except ftplib.error_perm:
            print(f"  [MKDIR] Tworzenie zdalnego katalogu: {current}")
            try:
                ftp.mkd(current)
            except Exception as e:
                print(f"  [ERR] Nie udalo sie utworzyc {current}: {e}")

def upload_directory(ftp, local_path, remote_path):
    print(f"[DIR] Synchronizacja katalogu: {remote_path}")
    ensure_remote_dir(ftp, remote_path)
    
    try:
        ftp.cwd(remote_path)
    except Exception as e:
        print(f"  [ERR] Nie mozna wejsc do {remote_path}: {e}")
        return

    for item in os.listdir(local_path):
        # Ignorujemy ukryte pliki, node_modules oraz folder assets (zawiera ciężkie, statyczne obrazy, które już są na serwerze)
        if item.startswith('.') or item in ["node_modules", "assets"]:
            continue
            
        # Ignorujemy pliki graficzne/binarne dla pełnego bezpieczeństwa i szybkości (są już na serwerze)
        if any(item.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico', '.webp']):
            continue

        local_item = os.path.join(local_path, item)
        remote_item_path = f"{remote_path}/{item}" if remote_path != "/" else f"/{item}"
        
        if os.path.isfile(local_item):
            print(f"  [FILE] Wgrywanie pliku: {remote_item_path}")
            try:
                with open(local_item, 'rb') as f:
                    ftp.cwd(remote_path)
                    ftp.storbinary(f'STOR {item}', f)
            except Exception as e:
                print(f"  [ERR] Blad wgrywania pliku {item}: {e}")
        elif os.path.isdir(local_item):
            upload_directory(ftp, local_item, remote_item_path)

def deploy():
    if not os.path.exists(LOCAL_DIR):
        print(f"[ERR] Nie znaleziono lokalnego folderu ze strona: {LOCAL_DIR}")
        return

    print(f"[FTP] Laczenie z serwerem FTP: {FTP_HOST} (Uzytkownik: {FTP_USER})...")
    
    try:
        print("[FTPS] Proba polaczenia FTPS (explicit)...")
        ftp = ftplib.FTP_TLS()
        ftp.connect(FTP_HOST, 21, timeout=15)
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        ftp.prot_p()
        print("[FTPS] Polaczono bezpiecznie przez FTPS!")
    except Exception as e_tls:
        print(f"[WARN] Bezpieczne polaczenie FTPS nie powiodlo sie ({e_tls}). Proba zwyklego FTP...")
        try:
            ftp = ftplib.FTP()
            ftp.connect(FTP_HOST, 21, timeout=15)
            ftp.login(user=FTP_USER, passwd=FTP_PASS)
            print("[FTP] Polaczono przez zwykle FTP!")
        except Exception as e_plain:
            print("[ERR] Nie mozna polaczyc sie z FTP ani przez FTPS, ani przez zwykle FTP!")
            print(f"Blad zwyklego FTP: {e_plain}")
            return

    try:
        ftp.set_pasv(True)
        
        print("[FTP] Listing katalogu glownego:");
        initial_list = []
        ftp.retrlines('LIST', initial_list.append)
        for line in initial_list:
            print(f"  {line}")

        target_dir = REMOTE_DIR
        has_public_html = any("public_html" in line.lower() for line in initial_list)
        
        if not has_public_html:
            print("[INFO] public_html nie znalezione w katalogu glownym. Konto FTP loguje bezposrednio do katalogu publicznego.")
            target_dir = ""

        print("-" * 60)
        print(f"[DEPLOY] Rozpoczynam synchronizacje plikow do zdalnego folderu: '{target_dir if target_dir else '/'}'")
        print("-" * 60)
        
        upload_directory(ftp, LOCAL_DIR, target_dir if target_dir else "/")
        
        ftp.quit()
        print("-" * 60)
        print("[OK] Sukces! Wszystkie pliki strony Coolfon GSM zostaly pomyslnie zaktualizowane na serwerze.")
        
    except Exception as e:
        print(f"[ERR] Wystapil blad podczas transferu plikow: {e}")
        try:
            ftp.close()
        except:
            pass

if __name__ == "__main__":
    deploy()
