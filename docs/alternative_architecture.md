# 🏗️ Architektura Alternatywna (Low-Cost / Low-Friction) — Holistic Jason

## 🎯 Status quo & Cel
Uproszczenie infrastruktury. Eliminacja kosztów i skomplikowania (tarcia).

---

## ❌ Dlaczego JAMStack i AWS Bedrock to błąd w tym projekcie?

1. **AWS Bedrock — Konflikt i Koszty:**
   * Masz już skonfigurowany projekt Google Cloud (`holistic-broker`) z aktywnym kontem Vertex AI (darmowe 300 USD).
   * Dodawanie AWS Bedrock wprowadza drugiego dostawcę chmurowego, dodatkowe IAM, klucze i rozliczenia.
   * LiteLLM na VM już doskonale obsługuje Vertex AI i OpenRouter. Nie potrzebujemy kolejnego punktu awarii.

2. **JAMStack (np. Next.js/Vercel) — Przeintegrowanie (Over-engineering):**
   * Chcemy generować i wdrażać proste strony lądowania (landing pages) w locie.
   * JAMStack wymaga procesu budowania (build pipeline), repozytorium GitHub dla każdej strony, konfiguracji domen i hostingu na Vercel/Netlify.
   * Generowanie statycznego HTML + Tailwind CDN i bezpośredni deploy przez FTP na Hostido zajmuje **3 sekundy** i kosztuje **0 PLN** (w ramach istniejącego hostingu).

---

## 🚀 Zwycięski Schemat (Zamiennik): Holistic Low-Friction Stack

### 1. Panel Sterowania (Dashboard): Streamlit
* Działa na maszynie VM w Google Cloud Platform.
* Służy jako interfejs użytkownika do orkiestracji agentów, bazy wiedzy, CRM oraz Local SEO.

### 2. API LLM: Vertex AI + OpenRouter + LiteLLM
* Wszystkie zapytania przechodzą przez LiteLLM na serwerze GCP.
* Używamy darmowych modeli z Vertex AI (Gemini 1.5 Pro / Flash) jako głównego silnika.
* OpenRouter służy jako natychmiastowy fallback.

### 3. Hosting & Domeny: Hostido + FTP Deploy
* Wszystkie landing page są czystym plikiem HTML/CSS/JS.
* Zapisujemy je lokalnie, a następnie agent przesyła je bezpośrednio przez FTP do odpowiednich katalogów na Hostido.
* Zerowe koszty serwerowe za ruch, natychmiastowe wyświetlanie strony pod subdomenami.

### 4. Integracja WordPress: REST API + Hasła Aplikacji
* Strony klienckie (`coolfon.pl`, `kurczakujasia.pl`, etc.) zostają na WordPressie.
* Agenci łączą się z nimi bezpośrednio przez WordPress REST API (Basic Auth z Application Passwords).
* Pozwala to na pobieranie treści, audyt SEO i publikację wpisów bez migracji baz danych ani przepisywania szablonów.

---

## 📈 Korzyści biznesowe
* **Czas wdrożenia (Time to market):** Zamiast dni konfiguracji — minuty.
* **Koszty (Run Cost):** Bliskie zeru. Wszystko w ramach darmowych kredytów GCP i taniego hostingu Hostido.
* **Prostota (Simplicity):** Kod w Streamlicie i prosty skrypt FTP w Pythonie. Każdy deweloper (i agent) to zrozumie.
