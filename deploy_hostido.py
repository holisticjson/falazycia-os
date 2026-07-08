import os
import ftplib
from dotenv import load_dotenv

# Wczytujemy dane z .env
load_dotenv()

FTP_HOST = os.getenv("HOSTIDO_FTP_HOST")
FTP_USER = os.getenv("HOSTIDO_FTP_USER")
FTP_PASS = os.getenv("HOSTIDO_FTP_PASS")
REMOTE_DIR = os.getenv("HOSTIDO_REMOTE_DIR", "/public_html")

# Ścieżka do folderu ze stroną Brokera (zwróć uwagę, że wychodzimy poza katalog Jasona)
LOCAL_DIR = r"C:\Aplikacje MVP\Holistyczny Broker\strona www"

def upload_directory(ftp, local_path, remote_path):
    print(f"📁 Zdalny katalog: {remote_path}")
    try:
        ftp.cwd(remote_path)
    except ftplib.error_perm:
        ftp.mkd(remote_path)
        ftp.cwd(remote_path)

    for item in os.listdir(local_path):
        local_item = os.path.join(local_path, item)
        if os.path.isfile(local_item):
            # Tu możemy w przyszłości dodać sprawdzanie daty modyfikacji (aby wysyłać tylko nowe pliki),
            # na razie wysyłamy wszystko, żeby mieć 100% pewności, że strona jest aktualna.
            print(f"  ⬆️ Wgrywanie pliku: {item}")
            with open(local_item, 'rb') as f:
                ftp.storbinary(f'STOR {item}', f)
        elif os.path.isdir(local_item):
            # Rekurencja dla podkatalogów (np. css, js, img)
            upload_directory(ftp, local_item, f"{remote_path}/{item}")
            # Wróć poziom wyżej po wyjściu z podkatalogu
            ftp.cwd("..")

def deploy():
    # Zabezpieczenie przed przypadkowym odpaleniem bez uzupełnienia .env
    if not FTP_HOST or FTP_HOST == "ftp.twojadomena.pl":
        print("❌ BŁĄD: Uzupełnij dane logowania FTP (HOSTIDO_FTP_...) w pliku .env!")
        return

    if not os.path.exists(LOCAL_DIR):
        print(f"❌ BŁĄD: Nie znaleziono folderu ze stroną: {LOCAL_DIR}")
        return

    print(f"🔌 Łączenie z serwerem FTP: {FTP_HOST}...")
    try:
        # Hostido zwykle wymaga bezpiecznego połączenia TLS (jeśli nie, użyj ftplib.FTP)
        ftp = ftplib.FTP_TLS(FTP_HOST)
        ftp.login(user=FTP_USER, passwd=FTP_PASS)
        ftp.prot_p() # Ustawienie szyfrowania danych
        print("✅ Zalogowano pomyślnie!")
        
        # Opcjonalnie włączenie trybu pasywnego (wymagane w 99% sieci)
        ftp.set_pasv(True)
        
        print(f"🚀 Rozpoczynam wdrażanie (Deploy) plików z: {LOCAL_DIR}")
        print("-" * 50)
        
        upload_directory(ftp, LOCAL_DIR, REMOTE_DIR)
        
        ftp.quit()
        print("-" * 50)
        print("🎉 Deploy zakończony sukcesem! Strona Holistycznego Brokera została zaktualizowana.")
        
    except Exception as e:
        print(f"❌ Błąd krytyczny podczas wysyłania na serwer: {e}")
        print("💡 Jeśli to błąd SSL, zmień w kodzie 'ftplib.FTP_TLS' na 'ftplib.FTP'")

if __name__ == "__main__":
    deploy()
