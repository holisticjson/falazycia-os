# ⚡ Szybka Ściągawka Jaisona (Popularne Komendy PowerShell)

Ten podręczny plik zawiera wszystkie najczęściej używane polecenia konsolowe do zarządzania **Hermes OS (Streamlit)**, Gitem, chmurą Google Cloud oraz wdrożeniami (deploy).

**Ścieżka projektu na obu komputerach:** `C:\Aplikacje MVP\Holistic Jason`

Skopiuj wybraną komendę i uruchom ją bezpośrednio w PowerShell w tym katalogu.

---

## 🖥️ 1. Uruchomienie Aplikacji Lokalnie (Hermes OS)
Uruchomienie Twojego panelu Streamlit (po restrukturyzacji plik główny jest w `02-os-jaison`):
```powershell
streamlit run 02-os-jaison/app.py
```

---

## 🐙 2. Synchronizacja z Gitem (GitHub)

### Wypchnięcie zmian na GitHub z obecnego komputera:
```powershell
git add -A; git commit -m "Uporzadkowanie repozytorium do standardu 10 folderow"; git push
```

### Pobranie zmian na drugim komputerze (laptopie):
```powershell
# WAŻNE: Najpierw przejdź do katalogu projektu: cd "C:\Aplikacje MVP\Holistic Jason"
git pull
```

---

## 🔑 3. Autoryzacja Google Cloud (GCP / Vertex AI)
Uruchom te komendy na nowym urządzeniu (laptopie), aby zalogować się na konto z pełnymi środkami i dostępem do Vertex AI:

```powershell
# 1. Logowanie na Twoje główne konto agencyjne (holisticjson@gmail.com):
gcloud auth login holisticjson@gmail.com

# 2. Uwierzytelnienie bibliotek deweloperskich (Application Default Credentials):
gcloud auth application-default login

# 3. Ustawienie aktywnego projektu dla agencji i aplikacji Streamlit:
gcloud config set project holistic-dashboard-dev
```

---

## 🚀 JEDNOLITY DEPLOY AGENCJI (Streamlit - Hermes OS):
Aplikacja agencji (obsługująca domeny **`jaison.pl`** oraz **`app.jaison.pl`**) jest uruchamiana i kompilowana jako kontener na **Google Cloud Run** w projekcie **`holistic-dashboard-dev`** za pomocą skryptu Python:
```powershell
python deploy_jaison.py
```

---

## 📱 5. Narzędzia Multimedialne i Generowanie Treści

Dyrektorzy AI dysponują bezpłatnymi, lokalnymi silnikami do dowożenia grafik i materiałów wideo bez płatnych subskrypcji:

### A. Generator Karuzel (Montserrat / SegoeUI + PIL)
Generuje piękny, spójny brandingowo zestaw slajdów PNG (1080x1080) pod LinkedIn / Instagram:
```powershell
# Uruchomienie skryptu generującego slajdy karuzeli:
python 02-os-jaison/integrations/generate_carousel.py
```
*   **Jak działa:** Skrypt dzieli tekst wejściowy oznaczony separatorami `---`, automatycznie zawija wiersze, dobiera kolory marki Jaison (ciemny granat, błękit Sky, biel) i zapisuje slajdy w katalogu `output_carousel/`.

### B. Autonomiczny Generator Wideo (Faceless Reel Generator)
Generuje kompletny pionowy film wideo 9:16 (TikTok, Reels, Shorts) łączący lektora Neural, przebitki HD i napisy:
```powershell
# Zawsze najpierw ustaw klucz Pexels w konsoli (potrzebny do darmowych przebitek HD):
$env:PEXELS_API_KEY="Twój_Klucz_Pexels"

# Uruchomienie generatora wideo:
python 02-os-jaison/src/faceless_generator.py
```
*   **Jak działa:** Pobiera skrypt (GHOST v2) ➜ Generuje darmowego, bardzo realistycznego lektora polskiego przez **Edge-TTS** (głos `pl-PL-MarekNeural`) ➜ Pobiera pionowy klip B-Roll z API **Pexels** ➜ Montuje i przycina wideo za pomocą **MoviePy** ➜ Generuje i nakłada napisy dynamiczne.

### C. Instalacja zależności na nowym komputerze (laptopie)
Przed pierwszym uruchomieniem narzędzi na laptopie, zainstaluj wszystkie wymagane biblioteki (Pillow, edge-tts, MoviePy, Streamlit):
```powershell
pip install -r requirements.txt
```

---

## 💾 6. Szybki Backup na Pendrive (D:)
Jeśli chcesz zrobić szybki backup całego repozytorium na pendrive (dysk `D:`):
```powershell
Compress-Archive -Path "C:\Aplikacje MVP\Holistic Jason\*" -DestinationPath "D:\jaison_laptop_backup.zip" -Force
```
