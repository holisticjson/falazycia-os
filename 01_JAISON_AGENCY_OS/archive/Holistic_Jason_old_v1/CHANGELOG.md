# 📝 Dziennik Postępów i Zmian (CHANGELOG) — Holistic OS

Ten dokument służy do profesjonalnego rejestrowania kamieni milowych, postępów wdrożeń oraz historii modyfikacji kodu w systemie. Stanowi on historyczne źródło prawdy dla architektów i deweloperów AI.

---

## 📅 Ostatnie Zmiany: 27.06.2026

### 🟢 Uruchomienie lokalnego Streamlita
*   **Zmiana:** Uruchomiono lokalny serwer Streamlit na porcie `8501`.
*   **Weryfikacja:** Proces działa poprawnie w tle z logiem `Uvicorn server started on 0.0.0.0:8501`. Dostępny pod adresem [http://localhost:8501](http://localhost:8501).

### 📚 Integracja bazy wiedzy Akademia.pl w UI
*   **Zmiana:** Dodano zakładkę `"📚 Akademia & Skarbiec Prompty"` w sekcji `📻 NotebookLM Sync & Obsidian Vault` aplikacji Streamlit.
*   **Opis:** Użytkownik może teraz dynamicznie przeglądać i czytać wszystkie 136 plików markdown z checklistami, promptami i strategiami biznesowymi bezpośrednio z poziomu interfejsu Streamlit.
*   **Kod:** Zmodyfikowano sekcję tabów w [app.py](file:///c:/Aplikacje%20MVP/Holistic%20Jason/app.py#L2057) w celu dynamicznego wczytywania plików z `./deploy/knowledge`.

### 🛡️ Korekta podziału kont GCP w SOP
*   **Zmiana:** Poprawiono wymagane narzędzia we wszystkich plikach SOP Wirtualnych Dyrektorów (w katalogu lokalnym `skills/` oraz globalnym wtyczek `.gemini/config/plugins/holistic-virtual-board/skills/`).
*   **Opis:** Rozgraniczono konto organizacji GCP `brokerholistic@gmail.com` (Holistic Broker, zasilanie LiteLLM) od konta osobistego `holisticjson@gmail.com` (J(a)SON ADHD, integracja CRM i Gmail/Sheets).

### 📄 Utworzenie dokumentacji PRD
*   **Zmiana:** Stworzono oficjalny plik [PRD.md](file:///c:/Aplikacje%20MVP/Holistic%20Jason/PRD.md) z opisem ról wirtualnych doradców MLM (Eric Worre i Jeff Altgilbers).

---

## 📋 Lista Zadań (TODO List)

### 🚀 Priorytety na dzisiaj:
*   [ ] **Wrzucenie zdjęć Tomasza:** Oczekiwanie na wgranie przez Tomasza 5-10 zdjęć referencyjnych do folderu [assets/tomasz_reference_photos/](file:///c:/Aplikacje%20MVP/Holistic%20Jason/assets/tomasz_reference_photos/).
*   [ ] **Testy integracji Stripe & Systeme.io:** Uruchomienie próbnego zapisu na landing page'u i weryfikacja webhooków.

### 📅 Planowane na kolejny etap:
*   [ ] **Wdrożenie skryptu Habit Engine (COO):** Napisanie cron-joba weryfikującego nawyki i integrującego go ze Slackiem.
*   [ ] **Wdrożenie MLM RAG:** Spięcie Vertex AI Search z folderem plików o produktach i praktykach MLM.
