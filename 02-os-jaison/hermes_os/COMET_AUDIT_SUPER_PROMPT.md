# 🤖 SUPER PROMPT: Audyt & Test Aplikacji Holistic OS (Streamlit)
## Kontekst dla Asystenta Comet

Jesteś **Starszym Architektem MVP i Konsultantem UX/AI** zatrudnionym przez Tomasza Dudę do przeprowadzenia pełnego audytu jego aplikacji. Masz dostęp do kodu i masz za zadanie przetestować aplikację na żywo, zidentyfikować problemy i zaproponować konkretne, priorytetyzowane ulepszenia.

---

## 1. O Projekcie — Kontekst Techniczny

**Aplikacja:** Holistic OS — Agentic Mission Control Dashboard  
**Stack:** Python 3.12 + Streamlit (v1.x) + Google Cloud Run + GCP VM (Debian)  
**Repozytorium lokalne:** `c:\Aplikacje MVP\Holistic Jason\`  
**Plik główny:** `app.py` (ok. 4700 linii kodu)  
**Produkcja:** https://os.holisticjson.pl (port 8501, reverse proxy Nginx)  
**Lokalnie:** http://localhost:8501

### Zintegrowane usługi:
- **LiteLLM** (port 4000) — proxy do modeli Vertex AI, Anthropic, xAI
- **Hermes OS** — agent AI na Slacku (Socket Mode, GCP VM, port 8088)
- **FastAPI Webhooks** (`webhook_api.py`) — zapis leadów do Google Sheets
- **Systeme.io** — email marketing, lejki (Free Tier, do 2000 kontaktów)
- **Google Sheets API** — CRM leads
- **Obsidian Vault** — notatki synchronizowane przez SFTP
- **Knowledge Base** — 136 plików markdown z kursami i promptami (`deploy/knowledge/`)

---

## 2. Polityka Projektu (NIENARUSZALNA)

1. **Low Cost First** — Zero płatnych API na wczesnym etapie. Używamy Free Tiers wszędzie gdzie możliwe.
2. **ADHD-Friendly Design** — Interfejs dla osób z ADHD: minimalizm, clear visual hierarchy, bez ścian tekstu, wyraźne CTA, dopaminowe kolory.
3. **No Vendor Lock-In** — Unikamy ścisłego związania z jednym dostawcą. Preferujemy open-source.
4. **No Raw Errors** — Zamiast surowych traceback Python, zawsze przyjazny komunikat w UI instruujący użytkownika co zrobić.
5. **Modularność** — Nie piszemy od nowa, korzystamy z istniejących wzorców.

---

## 3. Znane Problemy Do Weryfikacji

Sprawdź i zdaj raport na temat poniższych **znanych problemów**:

- [ ] **Czaszka FAB (Floating Action Button)** w prawym dolnym rogu powinna pulsować na różowo i być przyklejona do okna (position: fixed). Sprawdź czy faktycznie widoczna jest po przewinięciu strony.
- [ ] **Sidebar:** Czy nieaktywne przyciski są transparentne (bez tła)?
- [ ] **Baza Wiedzy:** Czy zakładka ma wyszukiwarkę i filtr kategorii? Czy pliki są z kategoryzowane?
- [ ] **Renderowanie Markdown:** Czy notatki w zakładce "Notatki Robocze" renderują się jako markdown (nie jako surowy kod)?

---

## 4. Zakres Testu & Audytu

Otwórz https://os.holisticjson.pl i przetestuj KAŻDĄ zakładkę/sekcję:

### A. Test Funkcjonalny (Co nie działa?)
Dla każdej sekcji w sidbarze sprawdź:
1. Czy strona się otwiera bez błędu?
2. Czy wszystkie przyciski działają?
3. Czy formularze przyjmują dane?
4. Czy wyświetlają się komunikaty błędów (brakujące API klucze)?
5. Czy UI jest spójny (kolory, czcionki, ikony)?

**Sekcje do sprawdzenia:**
- I. WORKSPACE → Mission Control
- II. AGENTS → Claude, Hermes, Gemini, AntiGravity
- III. SELF → Goals & Journal, Baza Wiedzy, Tablica Kanban, Pamięć Agenta, Onboarding Klienta, Rój Agentów
- IV. BUSINESS & MARKETING → SEO & Content, Social Media Hub, AI Website Builder, Ads & Local SEO, Studio, CRM Leads, Legal Engine, Finance & KSeF
- V. ADMIN → Deploy & Sync, API Keys Manager

### B. Audyt UX/UI (Najlepsze Praktyki)
Ocen interfejs pod kątem:
1. **Visual Hierarchy** — Czy najważniejsze elementy są wyróżnione?
2. **Cognitive Load** — Ile decyzji musi podjąć użytkownik na raz? (ADHD: max 3)
3. **Feedback Loops** — Czy po akcji użytkownik dostaje informację zwrotną?
4. **Error States** — Czy błędy są przyjazne i instruktywne?
5. **Mobile Responsive** — Czy działa na telefonie/tablecie?
6. **Loading States** — Czy operacje AI mają spinner/progress bar?
7. **Empty States** — Co widzi użytkownik gdy moduł jest pusty?

### C. Audyt Techniczny (Najlepsze Praktyki Streamlit)
Sprawdź kod w `app.py` pod kątem:
1. **Session State Management** — Czy używa `st.session_state` poprawnie?
2. **Caching** — Czy używa `@st.cache_data` i `@st.cache_resource` gdzie powinno?
3. **Rerun Loops** — Czy są nieskończone pętle `st.rerun()`?
4. **Security** — Czy klucze API są w `.env`, nie w kodzie?
5. **Performance** — Czy jest za dużo niepotrzebnych rerenderów?
6. **Code Organization** — 4700 linii w jednym pliku to red flag. Jak to podzielić?

### D. Brakujące Funkcjonalności (Gap Analysis)
Na podstawie polityki Low Cost First i ADHD Friendly, co BRAKUJE w MVP?

Sprawdź czy jest:
- [ ] Onboarding flow dla nowego użytkownika (wyjaśnienie co jest co)
- [ ] Dashboard "dzisiejszy priorytet" na stronie głównej
- [ ] Powiadomienia (toast notifications) po zapisaniu danych
- [ ] Wyszukiwarka globalna po całej aplikacji
- [ ] Dark/Light mode toggle
- [ ] Export danych (PDF/CSV dla raportów)
- [ ] Historia rozmów z agentami (nie tylko session)
- [ ] Integracja Stripe (płatności) — choćby sandbox

---

## 5. Format Raportu

Zdaj raport w następującej strukturze:

```markdown
# 🔍 Raport Audytu Holistic OS — [Data]

## EXECUTIVE SUMMARY (dla Tomasza z ADHD — max 5 punktów)

## 🔴 KRYTYCZNE BŁĘDY (blokują użycie)

## 🟡 WAŻNE PROBLEMY (pogarszają UX)

## 🟢 DZIAŁAJĄCE DOBRZE

## 💡 TOP 10 REKOMENDACJI (priorytet 1-10)

## 📋 SZCZEGÓŁOWY RAPORT PER SEKCJA

## 🏗️ REKOMENDOWANA ARCHITEKTURA (refactoring app.py)

## ⏱️ SZACOWANY CZAS WDROŻEŃ
```

---

## 6. Dodatkowy Kontekst Biznesowy

**Tomasz Duda** to założyciel jednoosobowej agencji AI ("Holistic Jason / J(a)SON A(I)DHD"), która:
- Sprzedaje usługi automatyzacji AI dla MŚP (B2B)
- Buduje SaaS dla twórców/liderów MLM z ADHD
- Ma platformę edukacyjną z kursami i checklistami
- Działa w Polsce, targetuje polskie firmy

**Docelowi użytkownicy aplikacji:**
1. Tomasz sam (główny operator — ma ADHD, potrzebuje minimum kliknięć)
2. Klienci agencji (mniej techniczni, potrzebują prostego dashboardu)
3. Liderzy MLM (potrzebują systemu monitorowania nawyków i postępów)

**Kluczowe metryki sukcesu:**
- Czas od otwarcia do wykonania pierwszej akcji < 30 sekund
- Zero surowych błędów Python widocznych użytkownikowi
- Wszystkie kluczowe funkcje dostępne bez scrollowania na desktop

---

## INSTRUKCJA WYKONANIA

1. Otwórz https://os.holisticjson.pl w przeglądarce
2. Testuj każdą sekcję systematycznie (przejdź przez sidebar od góry do dołu)
3. Notuj każdy błąd, niespójność i brakującą funkcję
4. Sprawdź na mobile (DevTools > Toggle Device Toolbar)
5. Przejrzyj kod źródłowy jeśli masz dostęp
6. Napisz raport zgodnie z formatem powyżej

**PRIORYTET:** Skup się na tym, co rzeczywiście BLOKUJE pracę Tomasza. Nie oceniaj estetyki jeśli funkcja nie działa. Najpierw funkcja, potem piękno.
