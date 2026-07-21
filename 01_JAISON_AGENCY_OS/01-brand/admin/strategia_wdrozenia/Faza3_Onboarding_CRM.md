# **Raport Architektoniczny: Faza 3 – Kreator Onboardingu Klienta i CRM Pipeline**

Jako Twój Główny Architekt Biznesowy AI, przeanalizowałem dostarczone materiały szkoleniowe, checklisty oraz strukturę "Holistic Agentic OS". Dla systemu dedykowanego twórcom i przedsiębiorcom z ADHD, kluczem jest bezwzględna eliminacja szumu informacyjnego (Minimalizm Poznawczy) oraz automatyzacja przejścia od surowych danych do gotowej oferty.

Poniżej znajduje się projekt zaawansowanego systemu onboardingu, ustrukturyzowana baza kontekstu klienta oraz techniczny workflow dla Streamlit i Hermes OS.

---

### 1. Zaawansowany Audyt Diagnostyczny (Holistic Onboarding Wizard)

Aby Wirtualny Zarząd AI (CEO, CMO, CTO) mógł natychmiast wygenerować celny lejek i ofertę, musimy porzucić płaską listę pytań na rzecz 5-etapowego, kognitywnego wywiadu. Będzie on łączył psychologię zakupową B2B, strategię wyceny Alexa Hormoziego oraz profilowanie "Ghost".

**Struktura Audytu i Niestandardowe Pytania:**

#### Sekcja A: Fundamenty & Transformacja (Dla CEO AI & Product Managera AI)
Zamiast pytać "co sprzedajesz?", diagnozujemy unikalne dźwignie i blokady.
*   **Supermoce:** Jakie są Twoje 3 supermoce (rzeczy, które robisz w TOP 10%)? (Pomaga to AI zaprojektować unikalny mechanizm oferty).
*   **Czerwone Linie (Red Flags):** Czego absolutnie NIE CHCESZ robić w biznesie (np. zimne telefony, pokazywanie twarzy, MLM)? (Kluczowe dla klientów z ADHD, by chronić ich przed wypaleniem).
*   **Wizja Transformacji:** Jaki jest wymarzony, końcowy rezultat Twojego klienta, ignorując sam proces dostarczania usługi?

#### Sekcja B: Psychologia Klienta B2B (Dla CSO AI)
Odkrywamy głęboki ból i budujemy "Akwizycję Finansowaną przez Klienta".
*   **Koszt Status Quo:** Co się stanie i ile straci Twój klient, jeśli NIE ROZWIĄŻE tego problemu w ciągu najbliższych 6-12 miesięcy? (Zmusza to klienta do kwantyfikacji bólu).
*   **BANT / CHAMP:** Kto ostatecznie decyduje o zakupie i w jakich ramach czasowych chcą to wdrożyć?

#### Sekcja C: Analiza Finansowa i Pakiety (Dla CFO AI)
Wykorzystujemy strategię 3 pakietów (Good-Better-Best) oraz psychologię kotwiczenia cen (Anchoring).
*   **Model Big Head, Long Tail:** Jaka jest jednorazowa wartość transformacji (opłata za wdrożenie), a jaka wartość utrzymania (abonament)?
*   **Konstrukcja Pakietów:** Jaka jest minimalna wersja Twojej usługi ("Starter"), wersja docelowa 2x droższa ("Recommended") oraz wersja ekskluzywna z osobistym dostępem 3x droższa ("VIP")?

#### Sekcja D: Wybór Lejka (Dla CMO AI i CTO AI)
Dopasowujemy architekturę sprzedażową do ceny i zasobów.
*   **Mechanizm Pozyskiwania:** Czy sprzedajesz usługę masową (np. *Lejek Quizowy* / *Lejek Webinarowy*), czy usługę Premium za +10 000 PLN (wymagającą *Lejka Aplikacyjnego* lub *Lejka Audytu/Diagnozy*)?

#### Sekcja E: Profil Komunikacji - Ghost (Dla CCO AI & GHOST)
Kalibrujemy styl pisania, aby komunikaty generowane przez AI brzmiały autentycznie.
*   **Emocje i Formaty:** Jak reagujesz na dobre wiadomości (np. "Super!", "Zajebiście!")? Czy w komunikacji używasz list numerowanych czy bullet pointów?

---

### 2. Struktura Pliku `client_context.json`

Poniższy JSON jest "paliwem" dla Twoich agentów. Gdy CEO AI lub CMO AI otrzyma to do kontekstu, natychmiast wygeneruje gotowe kopie i strony, ponieważ format ten jest zoptymalizowany pod "Chain of Thought" (ciąg myślowy) modeli LLM.

```json
{
  "client_id": "holistic_broker_01",
  "client_name": "Holistic Broker Nieruchomości",
  "onboarding_status": "Diagnoza",
  "fundamental_profile": {
    "superpowers": ["Tłumaczenie skomplikowanych umów", "Szybki networking", "Selekcja ofert premium"],
    "red_lines": ["Zimne telefony (Cold Calling)", "Praca po 18:00"],
    "dream_outcome": "Kupno apartamentu inwestycyjnego bez stresu i formalności."
  },
  "b2b_psychology": {
    "cost_of_inaction": "Utrata do 15% zysku przez inflację i nietrafione inwestycje w ciągu 12 miesięcy.",
    "bant_decision_maker": "Przedsiębiorca (CEO) lub inwestor prywatny."
  },
  "financial_and_pricing": {
    "roi_parameters": {
      "target_ltv_to_cac_ratio": "10:1",
      "client_financed_acquisition": true
    },
    "pricing_tiers": {
      "good_starter": {
        "name": "Konsultacja i Raport Rynkowy",
        "price_pln": 997,
        "features": ["Raport 10 nieruchomości", "Godzina konsultacji wideo"]
      },
      "better_recommended": {
        "name": "Pakiet Inwestor (Najpopularniejszy)",
        "price_pln": 4997,
        "features": ["Wszystko ze Starter", "Negocjacje ceny", "Weryfikacja prawna"]
      },
      "best_vip": {
        "name": "VIP Concierge (DFY)",
        "price_pln": 14997,
        "features": ["Wszystko z Inwestor", "Osobisty odbiór kluczy", "Wykończenie pod klucz"]
      }
    }
  },
  "funnel_strategy": {
    "recommended_funnel": "high_ticket_application",
    "lead_magnet": "Kalkulator ROI z Nieruchomości Premium (Web App)",
    "sales_mechanism": "Diagnoza -> Audyt -> Prezentacja Oferty (Zoom)"
  },
  "ghost_profile": {
    "tone_of_voice": "Bezpośredni, pewny siebie, lekko ironiczny, bazujący na liczbach.",
    "forbidden_ai_words": ["kompleksowy", "innowacyjny", "synergia", "w dzisiejszych czasach"],
    "formatting": "Krótkie akapity (max 2 zdania), częste używanie bullet-pointów."
  }
}
```

---

### 3. Techniczny Workflow w Streamlit i Hermes OS

Projektując aplikację pod kątem ADHD, musimy uniknąć przeładowania stron (reloads) i zadbać o natychmiastowe powiadomienia (Dopamine Hits). Workflow będzie asynchroniczny i podzielony na 5 kroków integracyjnych.

#### Krok 1: Obsługa formularza w Streamlit (`st.session_state`)
Aby formularz nie przeładowywał aplikacji po każdym kliknięciu, korzystamy z natywnego `st.form` i callbacks, wymuszających płynne przechodzenie przez etapy bez utraty danych.
```python
import streamlit as st
import json
import os

# Zapisanie stanu etapów kreatora (Wizard)
if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = 1

def next_step():
    st.session_state.onboarding_step += 1

with st.form("onboarding_form"):
    st.subheader("Faza 1: Supermoce i Ograniczenia")
    superpowers = st.text_input("Jakie są Twoje 3 supermoce?")
    red_lines = st.text_input("Czego absolutnie NIE CHCESZ robić w firmie?")
    # Pozostałe pola...
    
    submitted = st.form_submit_button("Dalej ->", on_click=next_step)
```

#### Krok 2: Synteza do JSON (Wywołanie Gemini 1.5 Pro)
Gdy użytkownik skończy, przechwytujemy zmienne i wysyłamy ustrukturyzowany prompt (Structured Outputs) do modelu Vertex AI / Gemini. Nakazujemy modelowi zwrócenie **wyłącznie surowego obiektu JSON**, który mapuje luźne notatki z formularza na nasz schemat.
```python
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel

# Gemini Syntetyzator (Super-analityk)
def synthesize_client_data(raw_answers):
    model = GenerativeModel("gemini-1.5-pro")
    prompt = f"""Przeanalizuj poniższe odpowiedzi klienta. 
    Wygeneruj z nich ustrukturyzowany plik JSON zgodnie ze ścisłym schematem (client_context.json). 
    Zwróć TYLKO kod JSON bez żadnego znacznika markdown.
    Dane wejściowe: {raw_answers}"""
    
    response = model.generate_content(prompt)
    return json.loads(response.text)
```

#### Krok 3: Automatyczny Zapis do Silosów Pamięci (GCS & Lokalnie)
Po wygenerowaniu JSON, zapisujemy go lokalnie do `/opt/holistic_os/04_clients/nazwa_klienta/` oraz opcjonalnie wysyłamy do Google Cloud Storage (`gs://holistic_kubelek/silos-ceo/`). Plik ten staje się z miejsca aktywnym RAG'iem dla Wirtualnego Zarządu.

```python
client_folder = f"04_clients/{client_name}/"
os.makedirs(client_folder, exist_ok=True)
with open(f"{client_folder}/client_context.json", "w", encoding="utf-8") as f:
    json.dump(client_json, f, indent=4, ensure_ascii=False)
```

#### Krok 4: Dynamiczny CRM (Streamlit State Management)
Zmiana statusu w lekkiej, wbudowanej pamięci (lub bazie SQLite Mnemosyne, jeśli połączona) na bieżąco zmienia widoki dla konkretnego klienta w lewym pasku bocznym (Sidebar).
```python
# Zmiana flagi statusu CRM po udanej generacji JSON
st.session_state.crm_status[client_name] = "Diagnoza" # Przejście z Nowy Lead
```

#### Krok 5: Powiadomienie Asynchroniczne na Telegramie przez Hermes OS
Gdy plik JSON ląduje na dysku, wywołujemy lokalne API bramki Hermesa (które nasłuchuje na porcie 8642). Bramka Hermes przetworzy powiadomienie i wyśle je bezpośrednio na Twój telefon przez połączonego z nim Bota na Telegramie.

```python
import requests

def notify_ceo_telegram(client_name, funnel_type):
    # Endpoint zintegrowany z Hermes Agent API (Port 8642)
    url = "http://localhost:8642/v1/chat/completions"
    
    payload = {
        "model": "hermes-agent", # lub nazwa Twojego modelu alertującego
        "messages": [
            {"role": "system", "content": "Jesteś asystentem notyfikacyjnym. Przekaż tę wiadomość bezpośrednio na Telegram szefa."},
            {"role": "user", "content": f"🚀 UWAGA: Zakończono diagnozę dla klienta {client_name}. Wygenerowano architekturę lejka: {funnel_type}. Profil JSON czeka w katalogu. Czy mam obudzić CMO AI, by napisał Landing Page?"}
        ]
    }
    
    # Wywołanie bez blokowania interfejsu (asynchronicznie)
    requests.post(url, json=payload)
```
