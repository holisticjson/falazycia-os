import os
import re
import urllib.request
from bs4 import BeautifulSoup

# Konfiguracja sciezek projektu LifeWave 4 Life
ASSETS_DIR = r"C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\lifewave\04-assets"
TARGET_URL = "https://lifewave.com/tomaszduda/home/light-into-water"

def setup_folders():
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)
        print(f"Utworzono katalog na zasoby: {ASSETS_DIR}")

def scrape_and_download_pdfs():
    print(f"Rozpoczynam skanowanie publicznej strony partnerskiej: {TARGET_URL}")
    setup_folders()
    
    try:
        # Pobieranie kodu HTML strony
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) JaisonAI/1.0'}
        req = urllib.request.Request(TARGET_URL, headers=headers)
        with urllib.request.urlopen(req) as response:
            html_content = response.read()
            
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Szukanie wszystkich linkow do dokumentow PDF oraz obrazow
        all_links = soup.find_all('a', href=True)
        pdf_urls = []
        
        for link in all_links:
            href = link['href']
            # Szukamy linkow konczacych sie na .pdf lub zawierajacych materialy edukacyjne
            if href.endswith('.pdf') or '/content/' in href or '/downloads/' in href:
                # Obsluga linkow wzglednych
                if href.startswith('/'):
                    href = "https://lifewave.com" + href
                elif not href.startswith('http'):
                    href = "https://lifewave.com/" + href
                pdf_urls.append(href)
                
        print(f"Znaleziono {len(pdf_urls)} potencjalnych dokumentow PDF/materialow.")
        
        # Pobieranie unikalnych PDF-ow
        unique_pdfs = list(set(pdf_urls))
        for url in unique_pdfs:
            filename = url.split('/')[-1].split('?')[0]
            if not filename.endswith('.pdf'):
                filename += ".pdf"
            
            dest_path = os.path.join(ASSETS_DIR, filename)
            print(f"Pobieram plik: {filename}...")
            
            try:
                urllib.request.urlretrieve(url, dest_path)
                print(f"Pomyslnie zapisano: {filename}")
            except Exception as e:
                print(f"Blad pobierania {url}: {str(e)}")
                
    except Exception as e:
        print(f"Blad krytyczny podczas skanowania strony: {str(e)}")

# Funkcja pomocnicza do ekstrakcji grafik z lokalnych PDF-ow
# Moze byc wywolana po umieszczeniu plikow z Backoffice w folderze 04-assets
def extract_images_from_local_pdfs():
    try:
        import fitz  # PyMuPDF (wymaga pip install PyMuPDF)
        print("Rozpoczynam automatyczna ekstrakcje grafik z plikow PDF w folderze 04-assets...")
        
        for file in os.listdir(ASSETS_DIR):
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(ASSETS_DIR, file)
                doc = fitz.open(pdf_path)
                print(f"Skanuje plik: {file} ({len(doc)} stron)")
                
                for page_num in range(len(doc)):
                    page = doc[page_num]
                    image_list = page.get_images(full=True)
                    
                    for img_index, img in enumerate(image_list):
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]
                        
                        img_filename = f"extracted_{file[:-4]}_page{page_num+1}_img{img_index+1}.{image_ext}"
                        img_path = os.path.join(ASSETS_DIR, img_filename)
                        
                        with open(img_path, "wb") as f:
                            f.write(image_bytes)
                        print(f"Wyeksportowano grafike: {img_filename}")
    except ImportError:
        print("Informacja: Aby wyekstrahowac grafiki z PDF-ow lokalnie, zainstaluj PyMuPDF uzywajac: pip install PyMuPDF")
    except Exception as e:
        print(f"Blad podczas ekstrakcji grafik: {str(e)}")

if __name__ == "__main__":
    scrape_and_download_pdfs()
    extract_images_from_local_pdfs()
