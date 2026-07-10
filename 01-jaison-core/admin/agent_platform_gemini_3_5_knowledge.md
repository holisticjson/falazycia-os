# Gemini 3.5 Flash & Agent Platform (Knowledge Update)

**Status:** Zaktualizowano (Czerwiec 2026)
**Rodzaj:** Architektura LLM / Integracja API
**Platforma:** Gemini Enterprise Agent Platform (nie "Vertex AI")

## Główne Modele
*   **gemini-3.5-flash:** Zapewnia inteligencję na poziomie Pro (near-Pro) w cenie tieru Flash. Posiada poziomy myślenia (Thinking levels), lepsze kodowanie i równoległe wywoływanie narzędzi (Agentic execution). 
*   **gemini-3-pro-preview:** Najpotężniejszy model do kodowania i architektury wieloagentowej, najlepsze możliwości multimodalne.
*   **gemini-3.1-flash-lite:** Najbardziej opłacalny model, zoptymalizowany pod kątem małych opóźnień i masowego ruchu LLM.

## Główne Różnice (API vs 2.5)
1.  **Thinking Level (zamiast Thinking Budget):**
    Cztery stany zastępujące budżet tokenów:
    *   `MINIMAL`: Jak najmniej tokenów (proste zadania).
    *   `LOW`: Duża przepustowość, mała złożoność.
    *   `MEDIUM`: Złoty środek (Domyślny dla 3.5 Flash).
    *   `HIGH`: Najwyższy poziom wnioskowania (planowanie, debugowanie, skomplikowany kod). Odpowiednik starszych modeli PRO.
2.  **Multimodalność:**
    Wprowadzono multimodalne i strumieniowe wywoływanie funkcji. Parametr `MEDIA_RESOLUTION` został ujednolicony.

## Uwierzytelnienie SDK (Python)
Konieczne jest użycie nowego pakietu `google-genai` w trybie enterprise.

```python
from google import genai
from google.genai import types

client = genai.Client(
  enterprise=True, 
  project="YOUR_PROJECT_ID", 
  location="global"
)

# Wywołanie modelu gemini-3.5-flash
response = client.models.generate_content(
  model="gemini-3.5-flash",
  # ... (zawartość)
)
```

## REST API (cURL) / Endpointy Agent Platform
URL dla zapytań:
`https://aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/global/publishers/google/models/${MODEL_ID}:streamGenerateContent`

W LiteLLM i systemie Hermes należy zmienić dotychczasowego dostawcę (Vertex AI) tak, by poprawnie interpretował ten nowy schemat uwierzytelniania Agent Platform dla `gemini-3.5-flash`.

---
*Informacja dla agenta Antigravity: ZAWSZE używaj tego pliku jako referencji do pisania kodu dla Google Gemini na produkcji.*
