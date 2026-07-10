# 🧠 Architektura Agentów Autonomicznych: Holistic CEO

Dokument ten to "Zapis Stanu Gry" oraz docelowy plan zbrojenia naszych Agentów w zewnętrzne umiejętności (Skille / Function Calling), aby system był w pełni autonomiczny.

---

## 1. STRUKTURA PROFILOWANIA (Rozdział ról)

Zgodnie z ustaleniami z wiadomości głosowej, rozdzielamy proces profilowania na dwa tory:

### A. Własny Profil (Holistic Jason) - *Prywatny*
*   **Cel:** Zbudowanie bazy pod Prompt 2 (Asystent), Prompt 3 (Analiza Konkurencji) i Prompt 4 (Strategia).
*   **Narzędzie:** Aktualny "Głęboki Czat Profilujący" w Dashboardzie. Używamy go jednorazowo (wklejając wytyczne Mirka), przechodzimy punkt po punkcie, aż system wypluje ostateczny plik `Holistic_Jason_Profil_AIBiznesLab.md`. Ten plik staje się sercem całego ekosystemu.

### B. Profilowanie Klienta (B2B / B2C) - *Lekkie*
*   **Cel:** Szybka ocena, czy lead ma pieniądze i problem (Cost of Chaos).
*   **Narzędzie:** Zwykły, szybki skaner oparty na Twojej metodologii S-C-A-R, wbudowany w `Client Intake Scanner`.

---

## 2. ZBROJOWNIA AGENTÓW (Tool Calling / Skille)

Aby agenci przestali tylko "gadać", a zaczęli "robić", wdrażamy im konkretne skille za pomocą Gemini Function Calling oraz MCP (Model Context Protocol). Oto plan przypisania ról i skilli:

### 📡 1. Holistic-Researcher (Agent Badawczy i Lead-Gen)
**Aktualny Skill:** Google Search Grounding (wyszukiwanie ogólne).
**Skille do zaimplementowania (Deep Research & Scraping):**
1.  **`LinkedIn_Scraper_Skill` / `Apollo_API_Skill`**: Narzędzie pozwalające agentowi pobrać imię, nazwisko, nazwę firmy oraz adres e-mail decydenta na podstawie nazwy firmy znalezionej w Google.
2.  **`Fetch_URL_Skill`**: Zamiast polegać na ogólnym Google, agent dostaje URL strony firmy i pobiera jej dokładny tekst do analizy, szukając "bólu" do zaczepienia w Cold Emailu.

### 🔌 2. GHL Agent (Agent Operacyjny i Sprzedażowy - CSO)
**Skille do zaimplementowania:**
1.  **`GHL_Create_Contact_Skill`**: Po znalezieniu kontaktu przez Researchera, GHL Agent samoczynnie wypycha go do GoHighLevel przez API.
2.  **`GHL_Send_Email_Skill`**: Agent samodzielnie wysyła Cold Email oparty na stylu z pliku *Ghost v2*.

### 🧠 3. Ghost Operator (Twórca Treści i Social Media)
**Skille do zaimplementowania:**
1.  **`Read_Knowledge_Base_Skill`**: Dostęp do nowo utworzonych plików `.md` z kursów i newsletterów. Agent sam szuka w nich "hooków" i wiedzy do postów.
2.  **`YouTube_Transcriber_Skill` (Twój priorytet!):** Moduł/Skill podpięty pod Ghosta, który przyjmuje link do niepublicznego wideo na YouTube, pobiera transkrypcję, robi z niej notatkę wizualną (MD) i zapisuje w Bazie Wiedzy.

---

## 3. NASTĘPNY KROK (ACTION PLAN)

Zgodnie z prośbą o "Zapisanie stanu gry i przyspieszenie", oto plan działania na nasze najbliższe ruchy:

1.  **Zadanie Domowe dla Ciebie:** Odpalasz na spokojnie lokalnie Dashboard (`localhost:8080`), używasz "Czatu Profilującego", przechodzisz z nim wywiad i generujesz swój **Prywatny Profil (Holistic Jason)**. Następnie dodajemy go do Bazy jako core!
2.  **Zadanie dla mnie (Krok 1 - YouTube):** Zbuduję potężny skrypt `youtube_transcriber.py`, który obsłuży niepubliczne linki z "Umiejętności Jutra", wyciągnie transkrypcję (używając omijania API) i zrobi z tego super-streszczenie do bazy wiedzy, żebyś nadgonił kursy.
3.  **Zadanie dla mnie (Krok 2 - Skille Lead-Gen):** Zakoduję pierwszą integrację z bazą kontaktów (Scraper lub API do leadów), by Twój Researcher przyniósł Ci tabelę z prawdziwymi mailami.

**Status gry zapisany!** Architektura zaakceptowana, Baza Wiedzy (Setki plików z Dysku G) skompresowana i czysta. Jesteśmy gotowi na instalowanie cyber-skilli naszym agentom.
