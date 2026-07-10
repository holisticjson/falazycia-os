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

## 🚀 4. Skrypty Wdrożeniowe (Deploy)

### JEDNOLITY DEPLOY AGENCJI (Streamlit - Hermes OS):
Aplikacja agencji (obsługująca domeny **`jaison.pl`** oraz **`app.jaison.pl`**) jest uruchamiana i kompilowana jako kontener na **Google Cloud Run** w projekcie **`holistic-dashboard-dev`** za pomocą skryptu PowerShell:
```powershell
# Uruchom ten skrypt z poziomu PowerShell:
.\02-os-jaison\src\tools\deploy_cloud_run.ps1
```

---

## 💾 5. Szybki Backup na Pendrive (D:)
Jeśli chcesz zrobić szybki backup całego repozytorium na pendrive (dysk `D:`):
```powershell
Compress-Archive -Path "C:\Aplikacje MVP\Holistic Jason\*" -DestinationPath "D:\jaison_laptop_backup.zip" -Force
```



