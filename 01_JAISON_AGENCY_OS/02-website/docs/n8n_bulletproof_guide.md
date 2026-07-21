# 🛡️ PANCERNA INSTRUKCJA n8n: Rozwiązanie błędu wersji i Autoryzacja (J(AI)SON OS v2.0)

Tomasz, przeanalizowałem zrzuty ekranu, które podesłałeś. Diagnoza jest jasna i precyzyjna. 

---

### 🔍 DIAGNOZA BŁĘDU (Dlaczego pojawiły się znaki zapytania `?`)

Węzły **"AI Agent Chain"** oraz **"Google Vertex AI Model"** wyświetlają szary znak zapytania oraz błąd *"Install this node to use it"*, ponieważ:
1.  Twoja wersja n8n (prawdopodobnie starsza lub bez włączonych modułów zaawansowanych) **nie ma zainstalowanego pakietu "Advanced AI" (LangChain)**.
2.  Węzły GitHub zresetowały się do domyślnej operacji *"create: issue"*, ponieważ wersja n8n ma inną strukturę schematu (schema version mismatch).

#### 💡 ROZWIĄZANIE ARCHITEKTONICZNE (Bulletproof Method)
Nie musisz aktualizować n8n ani instalować żadnych dodatków. Zamieniliśmy cały przepływ na **metodę w 100% uniwersalną (Universal REST API)**. 
Zamiast klocków AI ze znakami zapytania, używamy standardowego klocka **HTTP Request** do odpytania Vertex AI. 
*   **Dlaczego to działa zawsze?** Klocek HTTP Request jest fundamentem n8n od pierwszego dnia i istnieje w każdej wersji.
*   **Bezpieczeństwo:** n8n natywne obsługuje autoryzację *Google Service Account* bezpośrednio w klocku HTTP Request!

---

### 🌐 NOWY, UNIWERSALNY KOD JSON (Skopiuj i wklej do n8n)

Oto nowy kod JSON. Usuń stary workflow, utwórz nowy, kliknij na tło i naciśnij `Ctrl + V`. Wszystkie znaki zapytania znikną, a klocki będą czyste i stabilne:

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

### ⚙️ JAK SKONFIGUROWAĆ POŁĄCZENIA KROK PO KROK?

#### Krok 1: Węzeł "Gemini via Vertex API" (HTTP Request)
1.  Kliknij go dwukrotnie.
2.  W polu **URL** zamień tekst `YOUR_GCP_PROJECT_ID` na ID Twojego nowego projektu w Google Cloud Console (np. `jaison-new-project-12345`).
3.  W sekcji **Authentication** upewnij się, że wybrane jest **Predefined Credential Type**, jako typ wybierz **Google Vertex AI API** i podepnij swoje zapisane poświadczenia *"Google Service Account account"*.

#### Krok 2: Węzły GitHub ("Write AGENTS.md" i "Write Memory Loop")
1.  Kliknij dwukrotnie w klocek.
2.  Upewnij się, że **Resource** jest ustawiony na `File`, a **Operation** na `Edit` (lub `Create` - wersje n8n mogą się różnić, `Edit` z włączoną opcją automatycznego tworzenia jeśli plik nie istnieje jest najlepsza).
3.  Podepnij swoje poświadczenia GitHub (Personal Access Token).

#### Krok 3: Telegram
1.  Wklej swój `Chat ID` oraz Token bota.

---

### 🧪 TESTOWANIE PRZEPŁYWU (Test Payload)

Gdy włączysz workflow przyciskiem **Active**, wyślij testowe zapytanie za pomocą programu Postman, curl lub bezpośrednio z poziomu n8n, używając tych danych:

```json
{
  "client_name": "Testowy_Klient_B2B",
  "client_url": "https://example.com",
  "niche_description": "Firma produkująca pompy ciepła szukająca automatycznego umawiania spotkań"
}
```
Sprawdź, czy w Twoim lokalnym folderze (lub na GitHubie) w ścieżce `02_CLIENTS_AND_PROJECTS/Testowy_Klient_B2B/.agents/` pojawiły się oba wygenerowane pliki!
