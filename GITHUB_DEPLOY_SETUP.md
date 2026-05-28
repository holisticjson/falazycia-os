# 🚀 Deploy przez GitHub — Instrukcja konfiguracji

## Cel
Zamiast wklejać kod przez przeglądarkę SSH → edytujesz lokalnie → `git push` → 
Hermes na GCP robi `git pull`. Koniec z problemami bufora terminala.

---

## KROK 1 — Stwórz prywatne repo GitHub

1. Wejdź na https://github.com/new
2. Nazwa: `holistic-aidhd-os`  
3. Visibility: **Private**
4. NIE dodawaj README (repo będzie niepuste)
5. Kliknij "Create repository"
6. Skopiuj URL: `https://github.com/TWÓJ_USERNAME/holistic-aidhd-os.git`

---

## KROK 2 — Stwórz GitHub Personal Access Token

1. GitHub → Settings → Developer settings → Personal access tokens → **Fine-grained tokens**
2. Token name: `hermes-gcp-deploy`
3. Expiration: 90 days
4. Repository access: **Only selected repositories** → wybierz `holistic-aidhd-os`
5. Permissions:
   - Contents: **Read and Write**
   - Metadata: Read (automatyczne)
6. Kliknij "Generate token" — **skopiuj natychmiast**, zobaczysz go tylko raz!

---

## KROK 3 — Wypchnij lokalny kod do GitHub (PowerShell)

Uruchom te komendy lokalnie (już masz git zainicjalizowany):

```powershell
cd "c:\Aplikacje MVP\Holistic Jason"
git remote add origin https://github.com/TWÓJ_USERNAME/holistic-aidhd-os.git
git branch -M main
git push -u origin main
```
*(Przeglądarka poprosi o zalogowanie do GitHub lub wklej token jako hasło)*

---

## KROK 4 — Skonfiguruj GCP Server przez Hermesa (Telegram lub CLI)

W Hermesie (Telegram lub CLI na SSH) napisz:

```
Chcę połączyć serwer z moim prywatnym repo GitHub o nazwie 
"holistic-aidhd-os" u użytkownika [TWÓJ_GITHUB_USERNAME].

Wykonaj następujące kroki:
1. Sklonuj repo do ~/Agentic_OS/dashboard/ (zastępując obecny app.py)
2. Skonfiguruj git z moim tokenem bezpiecznie (zapisz token do .env, nie do historii)
3. Stwórz skill "deploy-from-github" który wykonuje: 
   cd ~/Agentic_OS/dashboard && git pull origin main
4. Stwórz cron który codziennie o 3:00 w nocy robi git pull i restart streamlit

Token podam przez terminal kontenera, nie przez czat.
```

Potem w SSH na GCP (NIE przez czat Hermesa):
```bash
# Ustaw token bezpiecznie w .env Hermesa
echo 'GITHUB_TOKEN=ghp_TWÓJ_TOKEN_TUTAJ' >> /opt/data/.env
echo 'GITHUB_USERNAME=TWÓJ_USERNAME' >> /opt/data/.env
echo 'GITHUB_REPO=holistic-aidhd-os' >> /opt/data/.env
```

---

## KROK 5 — Pierwszy deploy (test)

Po konfiguracji GitHub na serwerze, pierwszy pull:
```bash
cd ~/Agentic_OS/dashboard
git clone https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/${GITHUB_USERNAME}/${GITHUB_REPO}.git .
python3 -m py_compile app.py && echo "✅ Syntax OK"
pkill -f streamlit; sleep 2
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true > streamlit.log 2>&1 &
```

---

## Workflow na co dzień (po konfiguracji)

### Lokalnie (edycja kodu):
```powershell
cd "c:\Aplikacje MVP\Holistic Jason"
# ... edytujesz app.py w VSCode ...
git add app.py
git commit -m "feat: dodaję moduł X"
git push
```

### Na serwerze GCP (przez Hermesa w Telegram):
```
/deploy  
```
lub napisz do Hermesa: *"zaktualizuj dashboard z GitHuba"*

Hermes wywoła skill `deploy-from-github` który robi `git pull` + restart Streamlit.

---

## Status po konfiguracji

| Co | Status |
|----|--------|
| Lokalny git repo | ✅ Gotowy (77 plików, commit `c92ff30`) |
| .gitignore (sekrety wykluczone) | ✅ Gotowy |
| GitHub repo (prywatne) | ⏳ Czeka na Ciebie (KROK 1) |
| Push do GitHub | ⏳ Czeka na KROK 3 |
| Konfiguracja na GCP przez Hermesa | ⏳ Czeka na KROK 4 |
| Cron nightly sync | ⏳ Czeka na KROK 4 |
