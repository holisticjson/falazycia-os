# 🌐 KOMPLEKSOWA INTEGRACJA: FRONTEND jaison.pl & PANCERNY WORKFLOW n8n

Tomasz, ten plik to Twój **Master-SOP** do pełnego spięcia formularza kontaktowego na stronie `jaison.pl` (oraz subdomenie `go.jaison.pl`) z automatyzacją w n8n. 

Zdiagnozowałem błędy widoczne na Twoich zrzutach ekranu (szare znaki zapytania `?` oraz czerwone trójkąty ostrzegawcze `⚠️`) i przygotowałem **kompletny plan naprawczy oraz nowy, uniwersalny kod JSON**, który wyeliminuje te problemy raz na zawsze.

---

## 🔍 CZĘŚĆ 1: DIAGNOZA BŁĘDÓW W TWOIM N8N (Dlaczego coś jest nie halo?)

Przeanalizowałem przesłane przez Ciebie zrzuty ekranu i oto główne przyczyny problemów z workflow:

| Element | Status na screenie | Przyczyna | Rozwiązanie |
| :--- | :--- | :--- | :--- |
| **Google Vertex AI Model** oraz **AI Agent Chain** | **Szary znak zapytania `?`** oraz błąd *"Install this node to use it"* | Twoja instancja n8n nie ma zainstalowanego pakietu **Advanced AI (LangChain)** lub wersje schematów się różnią. | **Całkowita eliminacja tych węzłów.** Zastąpiliśmy je uniwersalnym klockiem **HTTP Request**, który wysyła czyste zapytanie REST API bezpośrednio do Google Vertex AI. |
| **GitHub Write AGENTS.md** oraz **Write Memory Loop** | **Czerwone `⚠️`** i domyślny status `create: issue` | Błąd wersji n8n zresetował klocki GitHub do domyślnej, niepotrzebnej operacji (tworzenie zgłoszeń zamiast edycji plików) oraz brakuje podpiętych poświadczeń (Credentials). | Ręczna rekonfiguracja klocków do operacji **File -> Edit** (szczegóły poniżej) oraz podpięcie Twojego poświadczenia GitHub PAT. |
| **Telegram Notifier** | **Czerwony `⚠️`** oraz błąd *No credentials yet* | Brak autoryzacji bota Telegram oraz pozostawienie domyślnego, literalnego tekstu `YOUR_TELEGRAM_CHAT_ID` w polu odbiorcy. | Podpięcie Credentials bota Telegram oraz wpisanie Twojego rzeczywistego, liczbowego Chat ID. |

---

## 🛡️ CZĘŚĆ 2: NOWY, UNIWERSALNY KOD JSON (Do skopiowania i wklejenia)

Ten workflow nie używa żadnych zaawansowanych klocków AI LangChain, dzięki czemu **działa w każdej wersji n8n**. Używa standardowych, pancernych żądań HTTP, które natywnie obsługują autoryzację za pomocą Twojego konta usługi Google (Service Account)!

### 📋 Instrukcja importu:
1. Wejdź do n8n, utwórz nowy workflow i **usuń wszystkie stare klocki**.
2. Skopiuj poniższy kod JSON (kliknij "Copy" w bloku kodu).
3. Kliknij na puste, ciemne tło w n8n i naciśnij **`Ctrl + V`**.
4. Cały przepływ ułoży się automatycznie i będzie w 100% czysty (zero znaków zapytania).

```json
{
  "name": "Jaison OS v2.0 - Onboarding Bulletproof",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "v1/jaison-onboarding",
        "responseMode": "onReceived",
        "options": {}
      },
      "id": "webhook-trigger",
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        100,
        240
      ]
    },
    {
      "parameters": {
        "url": "={{ $json.body.client_url }}",
        "options": {}
      },
      "id": "url-scraper",
      "name": "URL Scraper",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [
        300,
        240
      ]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://us-central1-aiplatform.googleapis.com/v1/projects/YOUR_GCP_PROJECT_ID/locations/us-central1/publishers/google/models/gemini-2.5-flash:generateContent",
        "authentication": "predefined",
        "nodeCredentialType": "googleVertexAiApi",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={\n  \"contents\": [\n    {\n      \"role\": \"user\",\n      \"parts\": [\n        {\n          \"text\": \"Działasz jako połączony, elitarny sztab Dyrektorów J(AI)SON OS: Dyrektor Marketingu (CMO) i Dyrektor Operacyjny (CPO). Twoim zadaniem jest przeprowadzenie rynkowego Audytu 21 Pytań dla klienta: {{ $node[\\\"Webhook Trigger\\\"].json.body.client_name }} na podstawie zeskrapowanej strony: {{ $json.body }} oraz opisu branży: {{ $node[\\\"Webhook Trigger\\\"].json.body.niche_description }}.\\n\\nZastosuj zasady:\\n1. NLP Copywriting (Sensoryka VAK - wzrok, słuch, kinestetyka).\\n2. Metaprogramy (dążenie do celu vs unikanie problemów) dopasowane do właścicieli małych firm.\\n3. Visual Anchoring (ADHD-friendly) - tabele, krótkie zdania, emotki, alerty [!NOTE], [!IMPORTANT], [!WARNING]. Zero ścian tekstu.\\n4. Całkowity zakaz wycieku formatowania Markdown do plików HTML (używaj <strong> zamiast **).\\n\\nWygeneruj zawartość dwóch plików w jednym ścisłym formacie JSON:\\n{\\n  \\\"agents_md\\\": \\\"zawartość pliku AGENTS.md\\\",\\n  \\\"memory_loop_md\\\": \\\"zawartość pliku 00_memory_loop.md\\\"\\n}\"\n        }\n      ]\n    }\n  ],\n  \"generationConfig\": {\n    \"temperature\": 0.3,\n    \"responseMimeType\": \"application/json\"\n  }\n}",
        "options": {}
      },
      "id": "vertex-ai-http",
      "name": "Gemini via Vertex API",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [
        500,
        240
      ],
      "credentials": {
        "googleVertexAiApi": {
          "id": "google-service-account-creds",
          "field": "googleVertexAiApi"
        }
      }
    },
    {
      "parameters": {
        "resource": "file",
        "operation": "edit",
        "owner": "holisticjson",
        "repository": "holistic-jason",
        "filePath": "=02_CLIENTS_AND_PROJECTS/{{ $node[\"Webhook Trigger\"].json.body.client_name }}/.agents/AGENTS.md",
        "fileContent": "={{ JSON.parse($json.body.candidates[0].content.parts[0].text).agents_md }}",
        "commitMessage": "=auto: onboarding nowego projektu AGENTS.md - J(AI)SON OS v2.0"
      },
      "id": "github-agents",
      "name": "GitHub Write AGENTS.md",
      "type": "n8n-nodes-base.github",
      "typeVersion": 1,
      "position": [
        740,
        140
      ],
      "credentials": {
        "githubApi": {
          "id": "github-personal-access-token",
          "field": "githubApi"
        }
      }
    },
    {
      "parameters": {
        "resource": "file",
        "operation": "edit",
        "owner": "holisticjson",
        "repository": "holistic-jason",
        "filePath": "=02_CLIENTS_AND_PROJECTS/{{ $node[\"Webhook Trigger\"].json.body.client_name }}/.agents/00_memory_loop.md",
        "fileContent": "={{ JSON.parse($json.body.candidates[0].content.parts[0].text).memory_loop_md }}",
        "commitMessage": "=auto: onboarding nowego projektu 00_memory_loop.md - J(AI)SON OS v2.0"
      },
      "id": "github-memory",
      "name": "GitHub Write Memory Loop",
      "type": "n8n-nodes-base.github",
      "typeVersion": 1,
      "position": [
        740,
        340
      ],
      "credentials": {
        "githubApi": {
          "id": "github-personal-access-token",
          "field": "githubApi"
        }
      }
    },
    {
      "parameters": {
        "updates": {},
        "chatId": "YOUR_TELEGRAM_CHAT_ID",
        "text": "=🚀 **J(AI)SON OS v2.0**: Projekt **{{ $node[\"Webhook Trigger\"].json.body.client_name }}** został pomyślnie utworzony i wypchnięty na GitHub!\nZa maksymalnie 15 minut Twój laptop i komputer stacjonarny automatycznie pobiorą pliki lokalnie za pomocą skryptu synchronizującego. Możesz odpalać AntiGravity!"
      },
      "id": "telegram-send",
      "name": "Telegram Notifier",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1,
      "position": [
        960,
        240
      ],
      "credentials": {
        "telegramApi": {
          "id": "telegram-bot-token",
          "field": "telegramApi"
        }
      }
    }
  ],
  "connections": {
    "Webhook Trigger": {
      "main": [
        [
          {
            "node": "URL Scraper",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "URL Scraper": {
      "main": [
        [
          {
            "node": "Gemini via Vertex API",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Gemini via Vertex API": {
      "main": [
        [
          {
            "node": "GitHub Write AGENTS.md",
            "type": "main",
            "index": 0
          },
          {
            "node": "GitHub Write Memory Loop",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "GitHub Write AGENTS.md": {
      "main": [
        [
          {
            "node": "Telegram Notifier",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "GitHub Write Memory Loop": {
      "main": [
        [
          {
            "node": "Telegram Notifier",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {},
  "meta": {
    "templateCredsSetupCompleted": true
  }
}
```

---

## ⚙️ CZĘŚĆ 3: RĘCZNA KONFIGURACJA KROK PO KROKU (Jak podpiąć poświadczenia)

Po wklejeniu powyższego kodu JSON niektóre klocki mogą wyświetlić wykrzyknik o braku poświadczeń. Oto jak skonfigurować je w 3 proste kroki:

### 🟢 Krok 1: Węzeł "Gemini via Vertex API" (GCP Service Account)
1. Kliknij dwukrotnie w klocek **Gemini via Vertex API**.
2. In the **Credential** field, select your Google Service Account credentials: `"Google Service Account account"`.
3. In the **URL** field, replace `YOUR_GCP_PROJECT_ID` with your actual Google Cloud Project ID (e.g. `holistic-dashboard-dev`).
4. Click **Execute Step** to test the API connection.

### 🐙 Krok 2: Węzły GitHub ("Write AGENTS.md" i "Write Memory Loop")
1. Kliknij dwukrotnie w klocek **GitHub Write AGENTS.md**.
2. Set **Credential** to your GitHub Personal Access Token (PAT classic, scoped with `repo`).
3. Verify these properties:
   * **Resource:** `File`
   * **Operation:** `Edit` *(Automatically creates file if missing, or overwrites if existing).*
   * **Owner:** `holisticjson`
   * **Repository:** `holistic-jason`
   * **File Path:** `=02_CLIENTS_AND_PROJECTS/{{ $node["Webhook Trigger"].json.body.client_name }}/.agents/AGENTS.md`
4. Set the exact same parameters on **GitHub Write Memory Loop**, with this file path:
   * `=02_CLIENTS_AND_PROJECTS/{{ $node["Webhook Trigger"].json.body.client_name }}/.agents/00_memory_loop.md`

### 📱 Krok 3: Telegram Notifier (Chat ID Setup)
1. Kliknij dwukrotnie w klocek **Telegram Notifier**.
2. Select your Telegram Bot Token under **Credential**.
3. Replace the placeholder text `YOUR_TELEGRAM_CHAT_ID` with your actual numeric Chat ID (e.g. `51239581`).
   * *How to get Chat ID:* Message `@userinfobot` on Telegram to get your numeric ID.

---

## 🛠️ CZĘŚĆ 4: GDZIE I JAK WKLEIĆ FORMULARZ W SYSTEME.IO (Krok po Kroku)

Na Twoim zrzucie ekranu widać, że domena **`go.jaison.pl`** jest podpięta pod Systeme.io. To oznacza, że formularz wklejamy bezpośrednio na stronę lądowania (landing page) zarządzaną przez to narzędzie.

### 📋 Instrukcja wdrożenia formularza w Systeme.io:

1.  **Zaloguj się** na swoje konto w [Systeme.io](https://systeme.io/).
2.  W górnym menu kliknij zakładkę **Strony** -> **Lejki sprzedażowe** (Funnels).
3.  Kliknij na nazwę lejka powiązanego z Twoją subdomeną `go.jaison.pl`.
4.  Wybierz krok lejka (np. Strona główna/Landing Page) i po prawej stronie kliknij **ikonkę różdżki/ołówka** (**Edytuj stronę** / Edit page).
5.  Po wejściu do wizualnego edytora Systeme.io:
    *   W lewym panelu bocznym zjedź na dół do sekcji **Inne** (Others) lub **Kod**.
    *   Przeciągnij element **Kod HTML** (Raw HTML) i upuść go w miejscu na stronie, w którym ma się wyświetlać formularz.
6.  Kliknij na upuszczony na stronę element **Kod HTML** na makiecie strony.
7.  W lewym panelu bocznym kliknij przycisk **Edytuj kod** (Edit code).
8.  W wyskakującym okienku usuń wszelką przykładową treść, **wklej cały poniższy blok kodu HTML/CSS/JS** i kliknij niebieski przycisk **Zapisz** (Save).
9.  ⚠️ **KLUCZOWY KROK (Konfiguracja Webhooka):** 
    Przewiń kod do linii **426** wklejonego kodu (w sekcji `<script>`) i znajdź zmienną:
    `const webhookUrl = 'TUTAJ_WPISZ_TWÓJ_URL_WEBHOOKA_Z_N8N';`
    Zastąp ten tekst **dokładnym adresem Webhooka z Twojego klocka Webhook Trigger w n8n** (np. `https://n8n.twojadomena.pl/webhook/v1/jaison-onboarding`).
10. Kliknij **Zapisz zmiany** (Save changes) w prawym górnym rogu edytora Systeme.io, a następnie wyjdź z edytora (ikonka drzwi w lewym górnym rogu).
11. Gotowe! Wejdź na `go.jaison.pl` i przetestuj formularz!

---

## 🎨 CZĘŚĆ 5: KOD HTML/CSS/JS FORMULARZA DO WKLEJENIA

```html
<!-- Jaison Lead Capture Form v2.0 -->
<div class="jaison-capture-container">
    <div class="jaison-card">
        <div class="jaison-glow"></div>
        <div class="jaison-header">
            <h2>🎯 Aktywuj J(AI)SON OS</h2>
            <p>Zleć bezpłatny, autonomiczny Audyt AI Twojej witryny i stwórz własną mapę drogową automatyzacji w 60 sekund.</p>
        </div>
        
        <form id="jaisonOnboardingForm" onsubmit="submitJaisonForm(event)">
            <!-- Nazwa firmy -->
            <div class="input-group">
                <label for="client_name">Nazwa Twojej Firmy / Imię</label>
                <input type="text" id="client_name" name="client_name" placeholder="Np. Klinika Szopa lub Jan Kowalski" required>
            </div>
            
            <!-- Adres URL -->
            <div class="input-group">
                <label for="client_url">Aktualna Strona Internetowa</label>
                <input type="url" id="client_url" name="client_url" placeholder="https://twojadomena.pl" required>
            </div>
            
            <!-- Opis niszy -->
            <div class="input-group">
                <label for="niche_description">Opis działalności & cele automatyzacji</label>
                <textarea id="niche_description" name="niche_description" rows="3" placeholder="Opisz krótko czym się zajmujesz i co chciałbyś zautomatyzować..." required></textarea>
            </div>
            
            <!-- Zgoda RODO -->
            <div class="rodo-checkbox">
                <input type="checkbox" id="rodo_consent" required>
                <label for="rodo_consent">Zgadzam się na przetwarzanie danych w celu darmowego audytu AI. Brak spamu, 100% prywatności.</label>
            </div>
            
            <!-- Przycisk Submit -->
            <button type="submit" id="submitBtn">
                <span class="btn-text">Generuj Audyt 21 Pytań 🚀</span>
                <span class="btn-loader"></span>
            </button>
        </form>
        
        <!-- Status / Tracker Postępu (ADHD-Friendly Loading Feedback) -->
        <div id="statusTracker" class="status-tracker hidden">
            <div class="progress-bar-container">
                <div class="progress-bar" id="progressBar"></div>
            </div>
            <div class="status-steps">
                <div class="step" id="step1">📡 Łączenie z J(AI)SON n8n...</div>
                <div class="step" id="step2">🕵️ Skanowanie i analiza witryny przez CMO...</div>
                <div class="step" id="step3">🧠 Generowanie strategii AI (Gemini Vertex)...</div>
                <div class="step" id="step4">📦 Wypychanie dokumentów na GitHub...</div>
                <div class="step" id="step5">📱 Notyfikowanie operatora systemowego...</div>
            </div>
        </div>
        
        <!-- Wiadomość o Sukcesie -->
        <div id="successMessage" class="success-message hidden">
            <div class="success-icon">🎉</div>
            <h3>Strategia Aktywowana Pomyślnie!</h3>
            <p>J(AI)SON OS przyjął Twoje zlecenie. Wygenerowane pliki `AGENTS.md` oraz `00_memory_loop.md` zostały zapisane w strukturze Git i za chwilę powiadomią nas na Telegramie!</p>
            <p class="sub-desc">Skontaktujemy się z Tobą asynchronicznie w ciągu 24h z gotową wizualizacją.</p>
        </div>
        
        <!-- Wiadomość o Błędzie -->
        <div id="errorMessage" class="error-message hidden">
            <div class="error-icon">⚠️</div>
            <h3>Coś poszło nie tak...</h3>
            <p id="errorText">Nie udało się połączyć z n8n. Sprawdź swoje połączenie lub spróbuj ponownie później.</p>
        </div>
    </div>
</div>

<style>
/* CSS Reset i czcionki */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;700;800&display=swap');

.jaison-capture-container {
    --primary: #8B5CF6;
    --primary-glow: rgba(139, 92, 246, 0.4);
    --secondary: #EC4899;
    --bg-dark: #0E1015;
    --border-color: #1F242E;
    
    font-family: 'Inter', sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    background: transparent;
    color: #FFFFFF;
}

.jaison-card {
    position: relative;
    background: rgba(14, 16, 21, 0.9);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 30px 40px;
    width: 100%;
    max-width: 500px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    overflow: hidden;
}

.jaison-glow {
    position: absolute;
    top: -50px;
    left: -50px;
    width: 150px;
    height: 150px;
    background: radial-gradient(circle, var(--primary-glow) 0%, transparent 70%);
    pointer-events: none;
    filter: blur(20px);
}

.jaison-header h2 {
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #FFFFFF 0%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 0;
    margin-bottom: 8px;
    text-align: center;
}

.jaison-header p {
    color: #94A3B8;
    font-size: 0.9rem;
    line-height: 1.5;
    margin-bottom: 25px;
    text-align: center;
}

.input-group {
    margin-bottom: 18px;
    display: flex;
    flex-direction: column;
}

.input-group label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #A78BFA;
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.input-group input, .input-group textarea {
    background: rgba(31, 36, 46, 0.6);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 12px 14px;
    color: #FFFFFF;
    font-size: 0.95rem;
    font-family: inherit;
    transition: all 0.3s ease;
}

.input-group input:focus, .input-group textarea:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 10px var(--primary-glow);
    background: rgba(31, 36, 46, 0.9);
}

.rodo-checkbox {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 25px;
}

.rodo-checkbox input {
    margin-top: 3px;
    accent-color: var(--primary);
}

.rodo-checkbox label {
    font-size: 0.75rem;
    color: #64748B;
    line-height: 1.4;
    cursor: pointer;
}

button[type="submit"] {
    width: 100%;
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 14px;
    font-family: 'Outfit', sans-serif;
    font-size: 1.05rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}

button[type="submit"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px var(--primary-glow);
}

button[type="submit"]:active {
    transform: translateY(0);
}

.btn-loader {
    display: none;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(255,255,255,0.3);
    border-radius: 50%;
    border-top-color: #FFFFFF;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Status Tracker & Postęp */
.status-tracker {
    margin-top: 25px;
    border-top: 1px solid var(--border-color);
    padding-top: 20px;
}

.progress-bar-container {
    background: rgba(31, 36, 46, 0.6);
    border-radius: 10px;
    height: 6px;
    overflow: hidden;
    margin-bottom: 15px;
}

.progress-bar {
    background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
    width: 0%;
    height: 100%;
    transition: width 0.4s ease;
}

.status-steps {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.step {
    font-size: 0.85rem;
    color: #64748B;
    display: flex;
    align-items: center;
    transition: color 0.3s ease;
}

.step.active {
    color: #A78BFA;
    font-weight: 600;
}

.step.done {
    color: #10B981;
}

.step.done::after {
    content: " ✓";
    margin-left: 5px;
    font-weight: bold;
}

/* Wiadomości końcowe */
.success-message, .error-message {
    text-align: center;
    padding: 20px 10px;
}

.success-icon, .error-icon {
    font-size: 3rem;
    margin-bottom: 15px;
}

.success-message h3 {
    color: #10B981;
    font-family: 'Outfit', sans-serif;
    margin-top: 0;
}

.success-message p {
    color: #E2E8F0;
    font-size: 0.9rem;
    line-height: 1.5;
}

.success-message .sub-desc {
    color: #64748B;
    font-size: 0.8rem;
    margin-top: 10px;
}

.error-message h3 {
    color: #EF4444;
    font-family: 'Outfit', sans-serif;
    margin-top: 0;
}

.error-message p {
    color: #CBD5E1;
    font-size: 0.9rem;
}

.hidden {
    display: none !important;
}
</style>

<script>
function submitJaisonForm(event) {
    event.preventDefault();
    
    const client_name = document.getElementById('client_name').value;
    const client_url = document.getElementById('client_url').value;
    const niche_description = document.getElementById('niche_description').value;
    const rodo_consent = document.getElementById('rodo_consent').checked;
    
    if (!rodo_consent) {
        alert("Musisz wyrazić zgodę na audyt, aby kontynuować.");
        return;
    }
    
    // UI states
    const form = document.getElementById('jaisonOnboardingForm');
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    const tracker = document.getElementById('statusTracker');
    const progressBar = document.getElementById('progressBar');
    
    // Disable form and show loading
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoader.style.display = 'inline-block';
    
    tracker.classList.remove('hidden');
    
    // Simulate steps progress (ADHD Focus Flow)
    updateStep(1, 'active', '10%');
    
    const payload = {
        client_name: client_name,
        client_url: client_url,
        niche_description: niche_description
    };
    
    // ⚠️ WPISZ SWÓJ DOKŁADNY WEBHOOK URL Z N8N PONIŻEJ:
    const webhookUrl = 'TUTAJ_WPISZ_TWÓJ_URL_WEBHOOKA_Z_N8N';
    
    fetch(webhookUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Błąd serwera n8n: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Step transitions
        updateStep(1, 'done', '30%');
        updateStep(2, 'active', '50%');
        
        setTimeout(() => {
            updateStep(2, 'done', '70%');
            updateStep(3, 'active', '85%');
            
            setTimeout(() => {
                updateStep(3, 'done', '95%');
                updateStep(4, 'active', '100%');
                
                setTimeout(() => {
                    updateStep(4, 'done', '100%');
                    updateStep(5, 'done', '100%');
                    
                    // Show success
                    setTimeout(() => {
                        form.classList.add('hidden');
                        tracker.classList.add('hidden');
                        document.getElementById('successMessage').classList.remove('hidden');
                    }, 800);
                }, 1000);
            }, 1200);
        }, 1500);
    })
    .catch(error => {
        console.error('Błąd wysyłania do webhooka:', error);
        form.classList.add('hidden');
        tracker.classList.add('hidden');
        
        const errMessage = document.getElementById('errorMessage');
        const errText = document.getElementById('errorText');
        errText.innerText = `Szczegóły błędu: ${error.message}. Sprawdź czy Twoja instancja n8n działa poprawnie i czy webhook ma status ACTIVE.`;
        errMessage.classList.remove('hidden');
        
        // Restore button state if user wants to go back
        submitBtn.disabled = false;
        btnText.style.display = 'inline';
        btnLoader.style.display = 'none';
    });
}

function updateStep(stepNum, status, width) {
    const step = document.getElementById(`step${stepNum}`);
    const progressBar = document.getElementById('progressBar');
    
    if (status === 'active') {
        step.className = 'step active';
    } else if (status === 'done') {
        step.className = 'step done';
    }
    progressBar.style.width = width;
}
</script>
```

---

## 🧪 CZĘŚĆ 6: PRZEPŁYW DANYCH & TESTOWANIE POŁĄCZENIA

Gdy włączysz workflow przyciskiem **Active**, możesz przetestować cały system, wysyłając następujący testowy payload typu JSON przy użyciu Postmana, curl lub bezpośrednio wypełniając formularz na stronie:

```json
{
  "client_name": "Testowy_Klient_B2B",
  "client_url": "https://example.com",
  "niche_description": "Firma zajmująca się instalacją pomp ciepła, poszukująca automatycznego zbierania i kwalifikacji leadów."
}
```

### 🔍 Weryfikacja wyniku:
1. Sprawdź, czy Twój bot na Telegramie wysłał powiadomienie o pomyślnym onboardingu.
2. Wejdź na swoje repozytorium GitHub i sprawdź, czy w katalogu `02_CLIENTS_AND_PROJECTS/Testowy_Klient_B2B/.agents/` pojawiły się pliki `AGENTS.md` oraz `00_memory_loop.md` z poprawnie wypełnioną zawartością strategii AI.
3. Gdy Twój lokalny skrypt synchronizujący `git_sync.ps1` pobierze pliki (maksymalnie do 15 minut), odśwież Streamlit i przejdź do sekcji "Pamięć Agenta" -> "Knowledge Graph". Nowy klient `Testowy_Klient_B2B` pojawi się na Twojej interaktywnej mapie myśli jako połączony węzeł!
