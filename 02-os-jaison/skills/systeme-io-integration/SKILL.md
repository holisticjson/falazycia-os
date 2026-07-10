---
name: ckm:systeme-io-integration
description: Standardy operacyjne (SOP) i blueprints do zarządzania lejkami, e-mail marketingiem oraz tagami w darmowym planie Systeme.io.
author: Tomasz Duda & Antigravity
version: 1.0.0
---

# 📧 ckm:systeme-io-integration — Systeme.io Automation & CRM SOP

Zgodnie z **Projektową Biblią (AGENTS.md)**, kategorycznie zabrania się tworzenia własnego systemu mailingowego lub lejków od zera. Ten skill definiuje rygorystyczne standardy integracji i orkiestracji procesów marketingowych za pomocą darmowego planu **Systeme.io** (limit do 2000 kontaktów).

---

## 🎯 Główne Cele Integracji
1. **Dostarczalność (Deliverability):** Wykorzystanie infrastruktury mailowej Systeme.io w celu uniknięcia filtrów antyspamowych i banów domen.
2. **Niskie Koszty (Low-Cost First):** Maksymalne wykorzystanie darmowych funkcji (1 lejek, 3 kroki, 1 reguła automatyzacji, 1 tag w darmowym planie).
3. **Automatyczna Synchronizacja:** Połączenie ankiet kwalifikacyjnych (np. Client Intake Scanner z Streamlit) z listami kontaktów.

---

## 🗺️ Architektura Reguł Automatyzacji i Tagów
Darmowy plan Systeme.io pozwala na **1 Tag** i **1 Regułę Automatyzacji**. Musimy podejść do tego strategicznie!

### Strategia "Jednego Taga" dla MVP:
*   Zamiast tworzyć dziesiątki tagów (co zmusiłoby Tomasza do przejścia na płatny pakiet), używamy jednego, uniwersalnego taga głównego: `holistic-contact`.
*   Rozróżnienie statusu kontaktu (np. lead, klient, subskrybent) przechowujemy w **polach niestandardowych (Custom Fields)** lub sterujemy tym za pomocą workflow w zewnętrznym n8n / webhooku.

---

## 🔌 API Quick Reference (Python Client Helper)
Do pobierania, tworzenia i tagowania kontaktów w Systeme.io używamy oficjalnego API v2.

### Konfiguracja połączenia w Pythonie (`systeme_agent.py`):
```python
import os
import requests

class SystemeIOClient:
    def __init__(self):
        self.api_key = os.environ.get("SYSTEME_IO_API_KEY")
        self.base_url = "https://api.systeme.io/api/v2"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def add_contact(self, email, first_name, custom_fields=None):
        """
        Dodaje kontakt do Systeme.io.
        Zgodnie z zasadą 'Zero Zagadek' - walidujemy dane wejściowe.
        """
        if not self.api_key:
            return {"status": "error", "message": "Brak SYSTEME_IO_API_KEY w pliku .env"}
            
        url = f"{self.base_url}/contacts"
        payload = {
            "email": email,
            "fields": [
                {"slug": "first_name", "value": first_name}
            ]
        }
        
        if custom_fields:
            for slug, val in custom_fields.items():
                payload["fields"].append({"slug": slug, "value": val})
                
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            if response.status_code in [200, 201]:
                return {"status": "success", "data": response.json()}
            elif response.status_code == 409:
                return {"status": "exists", "message": "Kontakt już istnieje w systemie."}
            else:
                return {"status": "error", "message": f"Błąd {response.status_code}: {response.text}"}
        except Exception as e:
            return {"status": "error", "message": f"Wyjątek sieciowy: {e}"}

    def subscribe_to_campaign(self, contact_id, campaign_id):
        """
        Zapisuje kontakt do gotowej kampanii e-mailowej (Autoresponder).
        """
        url = f"{self.base_url}/campaigns/{campaign_id}/subscriptions"
        payload = {"contactId": contact_id}
        response = requests.post(url, json=payload, headers=self.headers, timeout=10)
        return response.status_code in [200, 201]
```

---

## 🛠️ Wzorzec Kampanii (Copywriting Blueprint)
Dla darmowego planu projektujemy kampanię powitalną (Nurturing) opartą na psychologii sprzedaży High-Ticket:

1.  **Dzień 1 (Natychmiast po zapisie):** *Dostarczenie obiecanej wartości (Lead Magnet).*
    *   **Temat:** Twoje narzędzie jest gotowe (Pobierz) 🎁
    *   **Cel:** Budowanie zaufania. Szybki zastrzyk dopaminy dla odbiorcy.
2.  **Dzień 2 (+24h):** *Przedstawienie Tomasza & Historii ADHD4life (Problem/Rozwiązanie).*
    *   **Temat:** Jak z ADHD zbudowałem agencję AI... 🧠
    *   **Cel:** Połączenie emocjonalne (Thought Leadership).
3.  **Dzień 3 (+48h):** *Oferta High-Ticket & Wyzwanie (Call To Action).*
    *   **Temat:** Czy masz 15 minut na audyt Twojej automatyzacji? ⚡
    *   **Cel:** Umówienie asynchronicznej kwalifikacji (przez Client Intake Scanner).

---

## 🛡️ Reguły Bezpieczeństwa (Guardrails)
*   **NIGDY** nie przekraczaj limitu 2000 kontaktów bez pisemnej zgody Tomasza. Systematycznie czyść nieaktywne adresy e-mail (odbicia, brak otwarć przez 30 dni).
*   **Double Opt-in:** Zawsze upewnij się, że Twoje formularze mają klauzulę RODO/GDPR, aby chronić markę.
*   **Fallback:** Jeśli API Systeme.io zwróci błąd, zapisz dane leada lokalnie do pliku `clients/leads_fallback.json` w workspace, wyślij alert na Telegram i wyświetl czysty komunikat w UI.
