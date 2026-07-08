# 💻 Instrukcja Migracji Środowiska i Skryptów na Laptop

Ta instrukcja pozwoli Ci przenieść całe skonfigurowane środowisko **Jaison** z komputera stacjonarnego na laptopa przy użyciu przygotowanego pendrive'a **`D:`** i zautomatyzowanego skryptu.

---

## 🛠️ KROK 1: Przygotowanie plików na Pendrive (Wykonane)
Całe Twoje środowisko, pliki globalne oraz lokalne konfiguracje zostały automatycznie spakowane i zsynchronizowane na pendrive **`D:`**.
Na pendrive znajdują się dwa kluczowe pliki:
1.  `setup_laptop.py` — Skrypt instalacyjny.
2.  `jaison_laptop_backup.zip` — Spakowany plik ze wszystkimi skryptami i konfiguracją.

---

## 🚀 KROK 2: Uruchomienie instalacji na Laptopie

Wykonaj poniższe kroki na swoim laptopie:

1.  **Podłącz pendrive** do laptopa (załóżmy, że otrzyma literę dysku `D:`).
2.  Otwórz **PowerShell** jako Administrator:
    *   Wciśnij klawisz `Windows`.
    *   Wpisz `PowerShell`.
    *   Kliknij prawym przyciskiem myszy i wybierz **"Uruchom jako Administrator"**.
3.  Przejdź na dysk pendrive, wpisując komendę:
    ```powershell
    d:
    ```
4.  Uruchom automatyczny skrypt instalacyjny:
    ```powershell
    python setup_laptop.py
    ```

> [!NOTE]
> Skrypt automatycznie utworzy foldery `C:\Aplikacje MVP\Holistic Jason`, rozpakuje konfigurację do profilu użytkownika `~/.gemini/config` oraz zainstaluje wymagane pakiety Pythona i Node.js.

---

## 🔑 KROK 3: Autoryzacja Google Cloud (GCP) na Laptopie

Po zakończeniu działania skryptu, aby mieć pełen dostęp do Vertex AI oraz innych usług chmurowych z poziomu laptopa przy użyciu Twojego głównego konta z pełnymi środkami Free Trial ($300 / 1126 PLN):

1.  **Logowanie do konta Google Cloud (użyj e-maila: `tomaszc4y@gmail.com`):**
    ```powershell
    gcloud auth login tomaszc4y@gmail.com
    ```
2.  **Uwierzytelnienie dla bibliotek programistycznych (Application Default Credentials):**
    ```powershell
    gcloud auth application-default login
    ```
3.  **Ustawienie aktywnego projektu deweloperskiego (`coolfon-project`):**
    ```powershell
    gcloud config set project coolfon-project
    ```

---

## 🔌 KROK 4: Bezpieczne korzystanie z serwerów MCP (Bez zawieszania UI)

Serwery MCP (np. połączenia z n8n) mogą czasami powodować spowolnienia lub zamrożenie interfejsu (UI), jeśli serwer docelowy ma opóźnienia lub jest nieaktywny.

Aby zapobiec zamrażaniu edytora AntiGravity:
1.  **Domyślnie wyłączyliśmy serwery MCP** w pliku konfiguracyjnym, przenosząc je do sekcji `"disabledMcpServers"`.
2.  Jeśli będziesz chciał aktywować połączenie z n8n, otwórz plik:
    `C:\Users\tomas_yq1b9su\.gemini\config\mcp_config.json`
3.  Przenieś wybrany serwer z bloku `"disabledMcpServers"` z powrotem do `"mcpServers"` i przeładuj okno edytora (`Ctrl + Shift + P` -> `Developer: Reload Window`).
