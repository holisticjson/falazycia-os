import os
import sys
import subprocess

ASSETS_DIR = r"C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\lifewave\04-assets"
DEFAULT_URL = "https://www.facebook.com/share/r/1CtHKMRcwp/"

def setup_folders():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)
        print(f"Utworzono katalog na zasoby: {ASSETS_DIR}")

def install_and_get_ytdlp():
    print("Sprawdzam i instaluje/aktualizuje biblioteke yt-dlp...")
    try:
        # Probujemy zainstalowac yt-dlp za pomoca pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])
        print("Biblioteka yt-dlp jest zainstalowana i zaktualizowana.")
        return True
    except Exception as e:
        print(f"Blad instalacji pip: {str(e)}")
        print("Sprobuje uzyc lokalnego wywolania lub standardowego.")
        return False

def download_video(url=None):
    if not url:
        url = DEFAULT_URL
        
    setup_folders()
    install_and_get_ytdlp()
    
    print(f"Rozpoczynam pobieranie filmu z adresu URL: {url}")
    
    # Budujemy szablon nazwy pliku wyjsciowego z ID filmu, aby uniknac dlugich tytulow i bledow zapisu na Windows
    output_template = os.path.join(ASSETS_DIR, "video_%(id)s.%(ext)s")
    
    # Wywolujemy yt-dlp jako proces systemowy, aby zachowac pelna stabilnosc
    try:
        command = [
            "yt-dlp",
            "-o", output_template,
            "--no-playlist",
            "--merge-output-format", "mp4",
            url
        ]
        
        print("Uruchamiam yt-dlp z parametrami:")
        print(" ".join(command))
        
        # Uruchamiamy proces i przekazujemy wyjscie do konsoli
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="ignore")
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                
        rc = process.poll()
        if rc == 0:
            print("\nPobieranie zakoszone sukcesem!")
            print(f"Film zostal zapisany w folderze: {ASSETS_DIR}")
        else:
            print(f"\nBlad pobierania. Kod wyjsciowy: {rc}")
            print("Wskazowka: Niektore linki z Facebooka wymagaja zalogowania lub maja restrykcje prywatnosci. Mozesz sprobowac pobrac je przez przegladarke ze stron typu fdown.net i zapisac w 04-assets.")
            
    except Exception as e:
        print(f"\nKrytyczny blad uruchomienia yt-dlp: {str(e)}")
        print("Upewnij sie, ze zainstalowales python i masz dostep do internetu.")

if __name__ == "__main__":
    url_to_download = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_URL
    download_video(url_to_download)
