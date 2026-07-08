# Raport Analizy: Konsolidacja Skilli Dyrektorskich i Strategia Wdrożenia na GCP

## Podsumowanie Ustaleń
Skonsolidowanie skilli dyrektorskich z globalnego katalogu wtyczek `.gemini` oraz `.agents/skills/` do centralnego folderu `skills/` w repozytorium projektu ułatwi zarządzanie tożsamościami agentów. Wdrożenie na serwerze GCP VM polega na modyfikacji skryptu `scratch/sync_to_gcp.py` w celu tworzenia dowiązań symbolicznych (symlinków) na VM z nowej ścieżki w repozytorium do katalogów `.hermes/skills/` oraz `.hermes/profiles/`.

---

## 1. Obserwacje (Observations)

### Lokalne Ścieżki Źródłowe Skilli
1. **Ścieżka globalna wtyczek (`C:\Users\tomas_yq1b9su\.gemini\config\plugins\holistic-virtual-board\skills\`)**:
   Zidentyfikowano **11 podkatalogów** (skilli), z których każdy zawiera pojedynczy plik `SKILL.md`:
   - `cco/SKILL.md`
   - `ceo/SKILL.md`
   - `cfo/SKILL.md`
   - `cmo/SKILL.md`
   - `coo/SKILL.md`
   - `cso/SKILL.md`
   - `cto/SKILL.md`
   - `generate-video-reel/SKILL.md`
   - `ghost/SKILL.md`
   - `hermes-cloud-architect-sop/SKILL.md`
   - `holistic/SKILL.md`

2. **Ścieżka projektowa `.agents/skills/`**:
   Zidentyfikowano katalogi i pliki:
   - **Katalogi z plikami `SKILL.md`**:
     - `karpathy-guidelines/SKILL.md`
     - `n8n-automation-blueprints/SKILL.md`
     - `nlp-copywriting/SKILL.md` (posiada podkatalog `references/nlp_methods_report.md`)
     - `react-bits-integration/SKILL.md`
     - `systeme-io-integration/SKILL.md`
   - **Pliki Markdown** (częściowo z nagłówkami YAML frontmatter):
     - `skill_creator.md` (posiada frontmatter: `name: skill-creator`)
     - `auditor_research_logic.md` (brak frontmatter, ale opisuje rolę `Auditor Agent`)
     - `brain_dump_processing.md` (brak frontmatter, ale opisuje rolę `CEO Jason / Orchestrator`)

### Docelowa Lokacja w Obszarze Roboczym
- Folder docelowy w głównym katalogu roboczym: `c:\Aplikacje MVP\Holistic Jason\skills\` (już istnieje i zawiera 6 innych skilli: `analyze_legal_doc`, `build_systeme_io_funnel`, `create_marketing_campaign`, `hermes_deployment_specialist`, `holistic_broker_real_estate`, `manage_emails`).

### Zachowanie Skryptu `scratch/sync_to_gcp.py`
Z analizy kodu `scratch/sync_to_gcp.py` (linia 26–39) wynika, że skrypt pakuje cały obszar roboczy za pomocą `os.walk` do pliku `holistic_jason.zip`, pomijając jedynie katalogi zdefiniowane w `EXCLUDED_DIRS`. Katalog `skills` nie jest ignorowany, co oznacza, że po konsolidacji wszystkie skille zostaną automatycznie spakowane i przesłane na VM.

W sekcji `remote_cmds` (linia 103–126):
```python
    remote_cmds = [
        # Create directories if not exist
        f"mkdir -p {WORKSPACE_REMOTE}",
        "mkdir -p /home/holisticjson/.gemini",
        
        # Unzip workspace (overwrite existing)
        f"unzip -o /home/holisticjson/{WORKSPACE_ZIP} -d {WORKSPACE_REMOTE} > /dev/null",
        ...
```
Obecnie brak jest jakichkolwiek operacji kopiowania lub linkowania skilli do katalogów roboczych Hermesa (`/home/holisticjson/.hermes/skills/` i `/home/holisticjson/.hermes/profiles/`).

---

## 2. Łańcuch Logiczny (Logic Chain)

1. **Konsolidacja lokalna**:
   - Skopiowanie wszystkich podkatalogów z wtyczek globalnych i `.agents/skills/` bezpośrednio do `skills/` ujednolici strukturę zgodnie z `PROJECT.md` (gdzie `skills/` jest jedynym wskazanym folderem lokalnym).
   - Pliki `skill_creator.md`, `auditor_research_logic.md` i `brain_dump_processing.md` powinny zostać przekształcone w standardowe katalogi ze strukturą `SKILL.md` (np. `skills/skill-creator/SKILL.md`), co zapobiegnie błędom wczytywania przez framework Hermes i zachowa jednolity standard.

2. **Dystrybucja i wdrożenie chmurowe**:
   - Skoro `sync_to_gcp.py` przesyła spakowany obszar roboczy na VM i rozpakowuje go w `/home/holisticjson/Agentic_OS/holistic-aidhd-os`, to po wdrożeniu skille znajdą się w `/home/holisticjson/Agentic_OS/holistic-aidhd-os/skills/`.
   - Aby framework Hermes (działający w oparciu o konfigurację globalną w `/home/holisticjson/.hermes/`) widział te skille jako wbudowane umiejętności i profile agentów, musimy utworzyć dowiązania symboliczne (`ln -sf`).
   - Zamiast kopiowania plików, użycie dowiązań symbolicznych (`symlinks`) zapewnia, że każda kolejna synchronizacja kodu natychmiast aktualizuje aktywne definicje skilli i profili bez konieczności czyszczenia i ponownego kopiowania.
   - Pętla w powłoce Bash wykonywana na serwerze GCP VM po rozpakowaniu archiwum ZIP może automatycznie utworzyć symlink dla każdego skróconego podfolderu w `skills/` do `/home/holisticjson/.hermes/skills/` oraz `/home/holisticjson/.hermes/profiles/`.

---

## 3. Zastrzeżenia (Caveats)

- **Wymagania systemowe symlinków**: Dowiązania symboliczne na systemie Linux (VM) wymagają poprawnych praw dostępu. Uruchamianie komend linkujących pod użytkownikiem `holisticjson` powinno być wystarczające, pod warunkiem, że uprawnienia do folderu `.hermes` należą do tego samego użytkownika (co potwierdzono w ścieżkach domowych `/home/holisticjson/`).
- **Puste katalogi**: Podczas pierwszego uruchomienia należy upewnić się, że foldery `/home/holisticjson/.hermes/skills` oraz `/home/holisticjson/.hermes/profiles` istnieją przed wykonaniem pętli linkującej.

---

## 4. Wnioski i Rekomendacje (Conclusion)

### Plan Działania:
1. **Lokalna Konsolidacja**:
   Przenieść (skopiować) następujące katalogi do `c:\Aplikacje MVP\Holistic Jason\skills\`:
   - Z `C:\Users\tomas_yq1b9su\.gemini\config\plugins\holistic-virtual-board\skills\`:
     `cco`, `ceo`, `cfo`, `cmo`, `coo`, `cso`, `cto`, `generate-video-reel`, `ghost`, `hermes-cloud-architect-sop`, `holistic`.
   - Z `c:\Aplikacje MVP\Holistic Jason\.agents\skills\`:
     `karpathy-guidelines`, `n8n-automation-blueprints`, `nlp-copywriting`, `react-bits-integration`, `systeme-io-integration`.
   - Przekształcić pliki jednoczęściowe z `.agents/skills/` w katalogi:
     - `skills/skill-creator/SKILL.md` (z zawartości `skill_creator.md`)
     - `skills/auditor_research_logic/SKILL.md` (z zawartości `auditor_research_logic.md`)
     - `skills/brain_dump_processing/SKILL.md` (z zawartości `brain_dump_processing.md`)

2. **Aktualizacja `scratch/sync_to_gcp.py`**:
   Wprowadzić modyfikację w bloku `remote_cmds` wewnątrz funkcji `main()`. Poniższy kod powinien zastąpić istniejącą definicję `remote_cmds`:

   ```python
   # Remote execution block
   remote_cmds = [
       # Create directories if not exist
       f"mkdir -p {WORKSPACE_REMOTE}",
       "mkdir -p /home/holisticjson/.gemini",
       "mkdir -p /home/holisticjson/.hermes/skills",
       "mkdir -p /home/holisticjson/.hermes/profiles",
       
       # Unzip workspace (overwrite existing)
       f"unzip -o /home/holisticjson/{WORKSPACE_ZIP} -d {WORKSPACE_REMOTE} > /dev/null",
       
       # Unzip .gemini config
       f"unzip -o /home/holisticjson/{GEMINI_ZIP} -d /home/holisticjson/.gemini/ > /dev/null",
       
       # Link workspace skills to ~/.hermes/skills/ and ~/.hermes/profiles/
       f'for d in {WORKSPACE_REMOTE}/skills/*; do [ -d "$d" ] && name=$(basename "$d") && rm -rf "/home/holisticjson/.hermes/skills/$name" && ln -sf "$d" "/home/holisticjson/.hermes/skills/$name" && rm -rf "/home/holisticjson/.hermes/profiles/$name" && ln -sf "$d" "/home/holisticjson/.hermes/profiles/$name"; done || true',
       
       # Clean up remote ZIP files
       f"rm -f /home/holisticjson/{WORKSPACE_ZIP}",
       f"rm -f /home/holisticjson/{GEMINI_ZIP}",
       
       # Copy .env to workspace directory on VM for API keys
       f"cp -f {WORKSPACE_REMOTE}/.env {WORKSPACE_REMOTE}/.env 2>/dev/null || true",
       
       # Restart Streamlit process
       "pkill -u holisticjson -f 'streamlit run' 2>/dev/null || true",
       "sleep 2",
       f"nohup /home/holisticjson/.local/bin/streamlit run {WORKSPACE_REMOTE}/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true > /tmp/streamlit_os.log 2>&1 & sleep 3",
       "ss -tlnp | grep 8501"
   ]
   ```

   *Kod ten został zaimplementowany jako kompletny plik poglądowy w `.agents/explorer_m1_1/proposed_sync_to_gcp.py`.*

---

## 5. Metoda Weryfikacji (Verification Method)

### Krok 1: Weryfikacja konsolidacji lokalnej
Uruchomić polecenie w PowerShell w głównym katalogu roboczym:
```powershell
Get-ChildItem -Path .\skills -Directory | Select-Object Name
```
*Warunek sukcesu:* Lista powinna zawierać wszystkie przeniesione foldery dyrektorskie (np. `ceo`, `cmo`, `cto`, `ghost`, `nlp-copywriting` itp.).

### Krok 2: Weryfikacja wdrożenia na GCP VM
Po uruchomieniu zaktualizowanego skryptu `sync_to_gcp.py`:
Uruchomić polecenie diagnostyczne bezpośrednio na maszynie VM (lub sprawdzić logi instalacyjne):
```bash
ls -la /home/holisticjson/.hermes/skills/
ls -la /home/holisticjson/.hermes/profiles/
```
*Warunek sukcesu:* Wynik powinien pokazywać poprawne dowiązania symboliczne wskazujące na katalogi w rozpakowanym obszarze roboczym, np.:
`ceo -> /home/holisticjson/Agentic_OS/holistic-aidhd-os/skills/ceo`

### Krok 3: Weryfikacja regresji
Uruchomić testy jednostkowe w repozytorium:
```powershell
pytest
```
*Warunek sukcesu:* Wszystkie testy zwracają status `PASS`.
