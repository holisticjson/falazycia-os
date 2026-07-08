import os
import ftplib
import sys

# FTP Credentials dla holisticjson.pl
FTP_HOST = "mail.holisticjson.pl"
FTP_USER = "deploy@holisticjson.pl"
FTP_PASS = "Qwerty!!@@1234"
REMOTE_DIR = "/public_html"
LOCAL_DIR = r"C:\Aplikacje MVP\Holistic Jason\04_website\site\dist"

def upload_directory(ftp, local_path, remote_path):
    print(f"Zdalny katalog: {remote_path}")
    try:
        ftp.cwd(remote_path)
    except ftplib.error_perm:
        print(f"  Tworzenie katalogu zdalnego: {remote_path}")
        ftp.mkd(remote_path)
        ftp.cwd(remote_path)

    for item in os.listdir(local_path):
        local_item = os.path.join(local_path, item)
        if os.path.isfile(local_item):
            print(f"  Wgrywanie pliku: {item}")
            with open(local_item, 'rb') as f:
                ftp.storbinary(f'STOR {item}', f)
        elif os.path.isdir(local_item):
            # Rekurencja dla podkatalogów (np. assets)
            upload_directory(ftp, local_item, f"{remote_path}/{item}")
            # Powrot poziom wyzej po wyjsciu z podkatalogu
            ftp.cwd("..")

def deploy():
    if not os.path.exists(LOCAL_DIR):
        print(f"BLAD: Nie znaleziono folderu dystrybucyjnego (dist): {LOCAL_DIR}")
        print("Uruchom najpierw: npm run build")
        return

    print(f"Laczenie z serwerem FTP: {FTP_HOST}...")
    ftp = None
    try:
        # Proba bezpiecznego polaczenia TLS (wymagane w Hostido)
        try:
            print("Proba polaczenia szyfrowanego FTP_TLS...")
            ftp = ftplib.FTP_TLS(FTP_HOST)
            ftp.login(user=FTP_USER, passwd=FTP_PASS)
            ftp.prot_p() # Wymuszenie szyfrowania danych
            print("Zalogowano pomyslnie przez FTPS (szyfrowanie wlaczone)!")
        except Exception as ssl_err:
            print(f"Polaczenie FTPS nie powodlo sie: {ssl_err}")
            print("Proba polaczenia nieszyfrowanego FTP...")
            ftp = ftplib.FTP(FTP_HOST)
            ftp.login(user=FTP_USER, passwd=FTP_PASS)
            print("Zalogowano pomyslnie przez FTP (bez szyfrowania)!")
        
        # Tryb pasywny
        ftp.set_pasv(True)
        
        print(f"Rozpoczynam wdrazanie (Deploy) plikow z: {LOCAL_DIR}")
        print("-" * 60)
        
        upload_directory(ftp, LOCAL_DIR, REMOTE_DIR)
        
        ftp.quit()
        print("-" * 60)
        print("Deploy zakonczony sukcesem! Strona Holistic Jason zostala zaktualizowana na serwerze.")
        
    except Exception as e:
        print(f"Blad krytyczny podczas wysylania na serwer: {e}")
        if ftp:
            try:
                ftp.quit()
            except:
                pass

if __name__ == "__main__":
    deploy()
