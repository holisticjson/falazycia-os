# ⚡ Szybka Ściągawka Jaisona (Popularne Komendy PowerShell)

Ten podręczny plik zawiera wszystkie najczęściej używane polecenia konsolowe do zarządzania **Hermes OS (Streamlit)**, Gitem, chmurą Google Cloud oraz wdrożeniami (deploy).

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
# WAŻNE: Najpierw musisz wejść do folderu sklonowanego projektu: cd holistic-jason
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

## 🚀 4. Skrypty Wdrożeniowe (Deploy)

### A. DYNAMICZNY DASHBOARD (Streamlit - Hermes OS):
Działa na subdomenie **`app.jason.pl`** oraz **`app.holisticjson.pl`**.
Jest uruchamiany i kompilowany jako kontener na **Google Cloud Run** w projekcie **`holistic-dashboard-dev`** za pomocą skryptu PowerShell:
```powershell
# Uruchom ten skrypt z poziomu PowerShell:
.\02-os-jaison\src\tools\deploy_cloud_run.ps1
```

### B. STATYCZNA STRONA AGENCJI (Vite Landing Page):
Szybki front-end pod domenami **`jaison.pl`** oraz **`holisticjson.pl`**.
Wdrażana na serwer **FTP Hostido** za pomocą skryptu Python:
```powershell
python deploy_jason.py
```

---

## 💾 5. Szybki Backup na Pendrive (D:)
Jeśli chcesz zrobić szybki backup całego repozytorium na pendrive (dysk `D:`):
```powershell
Compress-Archive -Path "C:\Aplikacje MVP\Holistic Jason\*" -DestinationPath "D:\jaison_laptop_backup.zip" -Force
```

