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
git pull
```

---

## 🔑 3. Autoryzacja Google Cloud (GCP / Vertex AI)
Uruchom te komendy, jeśli system zgłosi brak uprawnień do Vertex AI lub GCP na nowym urządzeniu:

```powershell
# 1. Logowanie do Twojego głównego konta Google:
gcloud auth login tomaszc4y@gmail.com

# 2. Uwierzytelnienie bibliotek deweloperskich (Application Default Credentials):
gcloud auth application-default login

# 3. Ustawienie aktywnego projektu deweloperskiego:
gcloud config set project coolfon-project
```

---

## 🚀 4. Skrypty Wdrożeniowe (Deploy)

### Wdrożenie strony agencyjnej na FTP Hostido (jaison.pl / holisticjson.pl):
```powershell
python deploy_jason.py
```

### Wdrożenie strony agencyjnej na Google Cloud Run (holisticjson.pl):
```powershell
python deploy_cloud_run.py
```

### Kompilacja i wdrożenie Bar Jaś (kurczakujasia.pl) przez FTP:
```powershell
python build_and_deploy_v2.py
```

---

## 💾 5. Szybki Backup na Pendrive (D:)
Jeśli chcesz zrobić szybki backup całego repozytorium na pendrive (dysk `D:`):
```powershell
Compress-Archive -Path "C:\Aplikacje MVP\Holistic Jason\*" -DestinationPath "D:\jaison_laptop_backup.zip" -Force
```
