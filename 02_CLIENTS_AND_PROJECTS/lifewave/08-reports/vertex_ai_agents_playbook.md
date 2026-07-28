# 🤖 Vertex AI Agents Playbook - Jaison MLM OS (Fala Życia)

Ten dokument to zarys architektoniczny (Blueprint) wdrożenia Agentów konwersacyjnych AI na infrastrukturze Google Cloud. Projekt jest w pełni zgodny z wytycznymi Jaison (Zero Halucynacji, Low-Cost First) i wykorzystuje limit `$1000 GenAI App Builder credit` oraz konto bilingowe `gcpholisticjson`.

## 🏗️ Architektura Działania (Data Stores w Vertex AI)

Aby zminimalizować ryzyko mieszania kontekstów (np. podawania gościom na portalu tajnych skryptów rekrutacyjnych), wdrożymy **dwóch odrębnych Agentów**, podpiętych pod dwa oddzielne magazyny danych (Data Stores).

---

### 🟢 AGENT 1: "Przewodnik po Fali Życia" (Publiczny B2C)
* **Gdzie zostanie wdrożony:** Główna strona `fala-zycia.pl` (zintegrowany widget).
* **Cel:** Edukacja gości, odpowiedzi na pytania o technologię, zachęcanie do kontaktu/zostawienia leada.
* **Grupa Docelowa:** Osoby poszukujące rozwiązań na chroniczne zmęczenie, wsparcie w chorobach autoimmunologicznych (komunikacja delikatna, RODO/GIS compliant).
* **Data Store (Źródła Wiedzy):**
    * `X2O_HYDRATION_MASTER.md` (Działanie Stacji X2O, biofotonowa matryca)
    * `PHOTOBIOMODULATION_X39_MASTER.md` (Nauka o X39, miedź GHK-Cu, brak obietnic medycznych)
    * (Planowane) `CELERGIZE_MASTER.md`
* **Instrukcja Modelu (System Prompt - Ghost v2):**
  > "Jesteś przewodnikiem Klubu Fala Życia. Odpowiadasz na pytania w oparciu TYLKO o podaną bazę wiedzy. Masz budować autorytet i wzbudzać ciekawość. Twoim głównym celem jest zaproponowanie użytkownikowi umówienia się na bezpłatną konsultację lub degustację ustrukturyzowanej wody w Świątyni Harmonii."
* **Zabezpieczenie przed halucynacjami:** Agent ma zablokowaną możliwość doradzania medycznego (zawsze kieruje do lekarza prowadzącego) i bazuje wyłącznie na RAG.

---

### 🔵 AGENT 2: "Biznes Klasa Advisor & MLM Mentor" (Zamknięty dla Liderów)
* **Gdzie zostanie wdrożony:** Aplikacja wewnętrzna `dashboard.py` (Strefa Partnera).
* **Cel:** Wsparcie partnerów w codziennej pracy: asystowanie przy rezerwacji biletów za mile, podpowiadanie argumentów do rozmów z nowymi klientami.
* **Grupa Docelowa:** Aktywni dystrybutorzy i liderzy struktury LifeWave.
* **Data Store (Źródła Wiedzy):**
    * Cała wiedza Agenta 1 (Produkty) PLUS:
    * `MLM_DUPLICATION_MASTER.md` (Skrypty sprzedaży, obiekcje, lejki, lewarowanie linkami polecającymi)
    * `FLIGHT_HACKING_MASTER.md` (Poradnik Piotra Lotniczego, transfer mil, użycie Seats.aero)
    * `QUANTUM_PROSPERITY_MASTER.md` (Metodyka rozwoju lidera)
* **Instrukcja Modelu (System Prompt):**
  > "Jesteś wirtualnym Dyrektorem Operacyjnym (COO AI) dla partnera LifeWave w ekosystemie Jaison MLM OS. Pomagasz mu domykać sprzedaż używając technik NLP (VAK), doradzasz jak tanio latać po świecie używając Flight Hacking, i wspierasz go w duplikacji zespołu. Jesteś konkretny, motywujący i nastawiony na wyniki."

---

## 🛠️ Proces Wdrożenia na GCP (Instrukcja Krok po Kroku)

1. **Uruchomienie Środowiska:**
   * Zalogowanie na konsolę GCP (`gcpholisticjson`).
   * Wejście do sekcji **Vertex AI Agent Builder**.
   * Wybranie opcji *Create App -> Chat App*.

2. **Kreacja Data Stores:**
   * **Data Store A (Produkty):** Import plików Markdown z GCS bucketu dla publicznego Agenta.
   * **Data Store B (Biznes):** Import wszystkich plików Markdown (w tym Flight Hacking i Skrypty MLM) dla Agenta wewnętrznego.

3. **Budowa i Testy Agentów:**
   * Ustawienie Agentów na model **Gemini 2.5 Flash** (szybkość i niski koszt inference).
   * Konfiguracja parametrów RAG (Strictness) na poziomie uziemiającym (Groundedness = High), aby uniemożliwić wymyślanie własnych stawek milowych.
   * Przetestowanie Agenta Biznesowego: *"Znajdź mi lot do USA za mile"* -> Weryfikacja, czy agent odpowie: *"Sprawdź Seats.aero i poluj na 55k mil w Meilenschnäppchen"*.

4. **Integracja (Frontend):**
   * Agent Publiczny: Eksport kodu `<iframe>` Dialogflow CX i wklejenie do `index.html` portalu `fala-zycia.pl`.
   * Agent Partnerski: Podpięcie przez bibliotekę `google-cloud-dialogflow-cx` (Python) bezpośrednio do Streamlita w `modules/advisor.py`.

---
*Status: Oczekuje na realizację przez zespół wdrożeniowy.*
