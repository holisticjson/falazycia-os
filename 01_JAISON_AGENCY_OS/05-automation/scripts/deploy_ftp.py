import os
import ftplib
import argparse
import logging
from pathlib import Path

# Konfiguracja Logowania (Dla Agentów i Orkiestratora)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def deploy_to_ftp(host, username, password, local_dir, remote_dir):
    """
    Skrypt deployu na hosting dla agentów AntiGravity.
    Używany głównie przez CTO_AI i CMO_AI do wgrywania zaktualizowanych Landing Pages (HTML/JS).
    """
    try:
        logging.info(f"Łączenie z hostingiem {host}...")
        ftp = ftplib.FTP(host)
        ftp.login(username, password)
        logging.info(f"Zalogowano pomyślnie. Zmiana katalogu na {remote_dir}...")
        
        try:
            ftp.cwd(remote_dir)
        except ftplib.error_perm:
            logging.warning(f"Katalog docelowy {remote_dir} nie istnieje. Tworzenie...")
            ftp.mkd(remote_dir)
            ftp.cwd(remote_dir)

        local_path = Path(local_dir)
        
        for file in local_path.rglob('*'):
            if file.is_file():
                relative_path = file.relative_to(local_path)
                remote_path = str(relative_path).replace("\\", "/")
                
                # Tworzenie podkatalogów na serwerze
                remote_parent = os.path.dirname(remote_path)
                if remote_parent:
                    try:
                        ftp.cwd(remote_parent)
                        ftp.cwd('/')
                        ftp.cwd(remote_dir)
                    except ftplib.error_perm:
                        # Prosta funkcja upewniająca się, że katalog istnieje
                        dirs = remote_parent.split('/')
                        current_dir = ''
                        for d in dirs:
                            current_dir += f"/{d}"
                            try:
                                ftp.mkd(current_dir)
                            except:
                                pass
                
                logging.info(f"Wysyłanie pliku: {file.name} do {remote_path}")
                with open(file, 'rb') as f:
                    ftp.storbinary(f'STOR {remote_path}', f)
        
        ftp.quit()
        logging.info("Deploy zakończony sukcesem! 🚀")
        return True

    except Exception as e:
        logging.error(f"Błąd krytyczny podczas deployu: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AntiGravity Web Deploy Tool")
    parser.add_argument("--local-dir", required=True, help="Ścieżka do lokalnego folderu z kodem (np. build/)")
    parser.add_argument("--remote-dir", required=True, help="Katalog docelowy na serwerze (np. public_html/holistic)")
    
    args = parser.parse_args()
    
    # Bezpieczne pobieranie kluczy ze zmiennych środowiskowych z `.env`
    HOST = os.environ.get("FTP_HOST")
    USER = os.environ.get("FTP_USER")
    PASS = os.environ.get("FTP_PASS")
    
    if not all([HOST, USER, PASS]):
        logging.error("Brak poświadczeń FTP! Upewnij się, że .env jest załadowany przez Orkiestratora.")
        exit(1)
        
    success = deploy_to_ftp(HOST, USER, PASS, args.local_dir, args.remote_dir)
    if not success:
        exit(1)
