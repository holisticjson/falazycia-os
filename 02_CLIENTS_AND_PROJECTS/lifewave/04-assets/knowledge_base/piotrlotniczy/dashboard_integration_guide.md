# 🖥️ Instrukcja Integracji Agenta w Dashboardzie Aplikacji Fala Życia

> **Konto GCP**: `lifelifewave@gmail.com`  
> **Projekt GCP**: `falazycia-os`

---

## Opcja A: Osadzenie Gotowego Widgetu Czatowego HTML/JS

Wklej poniższy fragment w kodzie HTML dashboardu klubowego (przed zamykającym tagiem `</body>`):

```html
<!-- Widget Vertex AI Agent Builder Chat -->
<script src="https://cloud.google.com/ai/gen-app-builder/client?appId=TWOJE_APP_ID_Z_AGENT_BUILDER"></script>

<!-- Przycisk / Kontener czatu -->
<gen-search-widget
  configId="TWOJA_KONFIGURACJA_ID"
  triggerId="open-flight-hacking-agent">
</gen-search-widget>

<button id="open-flight-hacking-agent" class="btn-primary">
  ✈️ Otwórz Asystenta Flight Hacking (Piotr Łotowski)
</button>
```

---

## Opcja B: Połączenie przez REST API z Backendem PHP/Node/Python Dashboardu

Jeśli chcesz, aby dashboard sam wysyłał zapytania i stylizował odpowiedź we własnym interfejsie:

```http
POST https://europe-west1-discoveryengine.googleapis.com/v1/projects/falazycia-os/locations/europe-west1/collections/default_collection/engines/TWOJE_APP_ID/sessions/-:converse
Authorization: Bearer YOUR_GCP_ACCESS_TOKEN
Content-Type: application/json

{
  "query": {
    "input": "Znajdź mi lot w klasie biznes z Warszawy (WAW) do BKK na listopad za Avios."
  }
}
```

Odpowiedź zawierać będzie:
1. Przeszukany i skonsolidowany kontekst z notatek Piotra Łotowskiego.
2. Zintegrowane wyniki na żywo ze skanera Seats.aero API.
3. Gotowy link rezerwacyjny i instrukcję przelewu punktów step-by-step.
