# 🤖 Przewodnik Integracji z Viktor.com (Twój Nowy AI Coworker)

Ten dokument zawiera instrukcję krok po kroku, jak założyć konto, aktywować **$100 darmowych kredytów na start** i zintegrować autonomicznego agenta **Viktor.com** z Twoim Wirtualnym Zarządem (**Holistic OS**) oraz komunikatorami biznesowymi (Slack / MS Teams).

---

## 💡 Co to jest Viktor.com?
**Viktor.com** to nie zwykły chatbot (jak ChatGPT). To **autonomiczny pracownik cyfrowy (AI Coworker)**, który:
1. Posiada **własny komputer w chmurze**, na którym pisze i uruchamia kod w Pythonie, aby wykonywać Twoje polecenia.
2. Integruje się z ponad **3200 narzędziami** (Stripe, HubSpot, Notion, Google Workspace, GitHub, Meta Ads, PostHog, Google Analytics).
3. Samodzielnie generuje realne pliki robocze: **raporty PDF, arkusze Excel (.xlsx), prezentacje, a nawet proste aplikacje webowe**.
4. Działa asynchronicznie w tle i raportuje postępy bezpośrednio wewnątrz kanałów **Slack** lub **Microsoft Teams**.

---

## 💸 Jak Wykorzystać $100 Darmowych Kredytów na Start?

Viktor oferuje doskonały darmowy pakiet próbny dla nowych twórców i agencji AI. **Karta kredytowa NIE jest wymagana do rejestracji!**

### Krok 1: Rejestracja bez ryzyka
1. Przejdź na stronę: **[viktor.com](https://viktor.com)**.
2. Kliknij przycisk **"Try for Free"** lub **"Sign Up"**.
3. Załóż konto za pomocą swojego adresu e-mail powiązanego z agencją AI (np. `holisticjson@gmail.com`).
4. Po rejestracji i potwierdzeniu e-maila, na Twoim koncie zostanie automatycznie aktywowany darmowy budżet **$100 w kredytach/tokenach platformy**.
5. *Ważna zaleta:* W przeciwieństwie do miesięcznych pakietów, te kredyty próbne **nie wygasają** po 30 dniach — możesz z nich korzystać we własnym tempie.

### Krok 2: Instalacja w Twojej Przestrzeni Pracy
1. Zaloguj się do swojego panelu Viktor.com.
2. Wybierz komunikator, którego używasz do zarządzania agencją (rekomendujemy darmowy workspace **Slack**).
3. Kliknij **"Add to Slack"** i przejdź autoryzację, aby dodać aplikację Viktor do swojego workspace.
4. Od tej pory Viktor jest aktywnym użytkownikiem na Twoim Slacku — możesz wywołać go za pomocą `@Viktor` w dowolnym kanale lub pisać do niego bezpośrednio w wiadomości prywatnej (Direct Message).

---

## 🚀 Scenariusze Wykorzystania dla Agencji Holistic Jason (Low-Cost Master Plan)

Zamiast marnować kredyty na proste pogawędki (do których służy nasz lokalny Streamlit/LiteLLM), wykorzystaj Viktora do **ciężkich, asynchronicznych zadań biurowych**:

### 📊 Scenariusz A: Automatyczny Raport Finansowy z Stripe (Dla CFO AI)
*   **Jak to działa:** Zamiast samodzielnie logować się do Stripe i liczyć wskaźniki, poproś Viktora:
    > *"@Viktor, pobierz dane o płatnościach z mojego konta Stripe z ostatnich 30 dni, wylicz MRR (Miesięczny Powtarzalny Przychód), wskaźnik churnu i przygotuj mi piękny, sformatowany raport w pliku Excel (.xlsx), a wykresy zapisz w formacie PDF."*
*   **Efekt:** Viktor uruchomi swój komputer w chmurze, wykona bezpieczne zapytania API do Stripe, napisze skrypt w Pythonie (używając biblioteki Pandas i ReportLab), wygeneruje pliki Excel oraz PDF i wyśle Ci je jako gotowe załączniki na Slacku.

### 📈 Scenariusz B: Synchronizacja Leadów z HubSpot do Systeme.io (Dla CSO AI)
*   **Jak to działa:** Viktor może działać jako inteligentny "klej" monitorujący Twój CRM w czasie rzeczywistym.
    > *"@Viktor, monitoruj nowe kontakty w HubSpot. Jeśli pojawi się nowy lead z tagiem 'High-Ticket', prześlij go natychmiast do Systeme.io, nadaj mu tag 'Hot Lead' i wyślij mi powiadomienie na Slacku z krótkim streszczeniem profilu tej osoby na LinkedIn."*
*   **Efekt:** Pełna asynchroniczna automatyzacja bez konieczności płacenia za drogie plany Zapier czy Make!

### 🎥 Scenariusz C: Generowanie Kampanii i Kontentu (Dla CMO/CCO AI)
*   **Jak to działa:** Poproś Viktora o zrobienie researchu konkurencji i przygotowanie harmonogramu publikacji:
    > *"@Viktor, przeanalizuj aktualne trendy AI i ADHD na TikToku z ostatnich 7 dni, stwórz tabelę z 10 pomysłami na rolki (haki, scenariusz, wezwanie do działania) i zapisz to w Notion w mojej bazie kontentu."*

---

## 🛡️ Praktyczne Zasady Oszczędzania Tokenów (Maksymalizacja Wydajności)

Aby darmowe $100 starczyło Ci na kilka miesięcy intensywnej pracy i testów:

1.  **Unikaj pętli (Infinite Loops):** Nigdy nie uruchamiaj cyklicznych zadań, które odpytują API co 1 minutę. Używaj wyzwalaczy opartych o zdarzenia (Webhooks).
2.  **Duże zadania zlecaj precyzyjnie:** Viktor zużywa kredyty na czas działania swojego komputera chmurowego. Im bardziej precyzyjne dasz mu instrukcje (system prompt, pożądany format wyjściowy), tym szybciej napisze poprawny kod w pierwszej próbie i zużyje mniej mocy obliczeniowej.
3.  **Lokalne testowanie promptów:** Zanim wyślesz skomplikowane zapytanie do Viktora, przetestuj strukturę i logikę zapytania na darmowych modelach Gemini w swoim panelu **Holistic OS** (zakładka Workspace / Laboratorium). Kiedy upewnisz się, czego dokładnie potrzebujesz, zleć Viktorowi ostateczne wykonanie pracy i wygenerowanie plików.

---

*Ten plik został trwale zapisany w Twojej bazie wiedzy pod ścieżką `docs/viktor_integration_guide.md` i będzie wykorzystywany przez wszystkich Agentów Wirtualnego Zarządu do asynchronicznej współpracy z Viktorem.*
