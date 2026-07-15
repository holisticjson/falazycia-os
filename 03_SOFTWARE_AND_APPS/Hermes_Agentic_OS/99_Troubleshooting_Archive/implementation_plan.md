# 🏗️ Architektoniczny Pivot: Ze Streamlit do natywnego silnika Hermes OS

Dokument ten służy jako **baza wiedzy i oficjalny plan transformacji (Master Plan)**. Podsumowuje on rezygnację z ciężkiego i ograniczonego frameworka Streamlit na rzecz wydajnego, asynchronicznego silnika **Hermes Agent** z autorską nakładką frontendową **Holistic OS AI/DHD Architect System**.

Dokument jest przeznaczony do konsultacji z Dyrektorem Operacyjnym (Hermesem), aby miał pełny obraz tego, co porzucamy i jak nowa struktura przejmuje stare obowiązki.

---

## 1. Dlaczego porzuciliśmy Streamlit (Twardy Pivot)?

Poprzedni system (zbudowany w Streamlit) posiadał 13 zakładek w bocznym pasku i 9 oddzielnych agentów. Doprowadziło to do:
- **Paraliżu decyzyjnego (ADHD overload)** – zbyt wiele opcji na jednym ekranie.
- **Topornych integracji** – np. GoHighLevel (GHL) był przeładowany funkcjami, co kłóci się z ideą uproszczeń dla neuro-różnorodnych.
- **Powielania kodu** – 3 różne moduły do generowania wideo, 2 do shadow operatora.
- **Braków w pamięci** – agenci nie mieli wspólnego, permanentnego mózgu.

Nasz nowy cel: **Low Friction, High Dopamine, Omni-Channel**.

---

## 2. Nowa Architektura: Holistic OS na silniku Hermes

Zamiast budować logikę w UI, cała "inteligencja" jest po stronie Hermesa. Nowy frontend (Holistic OS) to lekka, asynchroniczna "skóra" w technologii Glassmorphism (HTML/CSS/JS).

### Mapowanie Starych Modułów na Nową Strukturę (Z 13 do 8)

Poniżej przedstawiam, w jaki sposób 13 starych zakładek i systemów zostało wchłoniętych przez 8 czystych modułów w nowym Holistic OS.

#### ⚡ 1. Centrum Dowodzenia (Orkiestracja i Chat)
*Zastępuje: Centrum Dowodzenia, Client Intake Scanner, Kreator Profilu.*
- Główny ekran komunikacji z Hermesem. Piszesz lub mówisz (np. "Przyjmij nowego klienta"). Hermes sam decyduje, jakich skilli użyć.

#### 📋 2. Tablica Kanban & Dopamine Tracker
*Zastępuje: ADHD Command Center (Zen, Kanban, Flow, SOS, Dopamine Journal).*
- Główne narzędzie pracy z obsługą Drag & Drop (przeciągnij i upuść). 
- System grywalizacji: każde zadanie przeciągnięte do "Done" dodaje punkty dopaminowe na pasku postępu (wizualna nagroda dla mózgu ADHD).

#### 🧠 3. Mnemosyne (Pamięć i Baza Wiedzy)
*Zastępuje: Centrum Wiedzy (Kombajn & Mapy), Scratchpad, Katalog Procedur (Wiki).*
- Moduł podłączony bezpośrednio do wtyczki `Mnemosyne` (wektorowa baza SQLite Hermesa). Przechowuje procedury i notatki.

#### 📡 4. Prospecting & Radar
*Zastępuje: Market Holistic Radar, Shadow & Ghost Operator.*
- Wykorzystuje wbudowaną w Hermesa kontrolę przeglądarki (Web Control) do skanowania LinkedIn, Reddita (r/ADHD, r/business) oraz platformy X i generowania "Gorących leadów".

#### 💻 5. Anti-Gravity IDE (Kodowanie)
*Zastępuje: Ręczne przełączanie się do zewnętrznych edytorów kodu.*
- Sub-agent Anti-Gravity posiada własną konsolę wewnątrz Dashboardu do budowania oprogramowania.

#### 🎨 6. Agency Pipeline (Fabryka Treści)
*Zastępuje: AI Influencer, Viral Generator, Content Lab, Social Planner.*
- Generator Kampanii (Copywriting, wymyślanie skryptów wideo).
- Galeria Mediów (Integracja z Imagen 3 / DALL-E oraz Veo 3.1 / Runway). 

#### 🌪️ 7. Holistic Funnel Builder (Nowość!)
*Zastępuje: GHL Agent, Funnel Hacker.*
- **Całkowita rezygnacja z GoHighLevel.** Zamiast przytłaczającego kombajnu budujemy własny, dedykowany moduł Funnel Builder.
- Zaprojektowany w duchu *Low Friction* – maksymalnie uproszczony, chroniący przed paraliżem decyzyjnym u osób z ADHD.
- Integracja wielokanałowa (Omni-channel) w jednym prostym widoku: automatyzacja emaili, SMS, komunikatorów.

#### ⚖️ 8. Finanse & Prawo (Nowość!)
*Nowe założenie, którego brakowało w Streamlit.*
- **Dział Prawny**: Generowanie umów NDA, kontraktów dla twórców i klientów agencyjnych (Ghost/Shadow Operator).
- **Dział Finansowy**: Wystawianie faktur, śledzenie płatności. Wszystko zintegrowane z orkiestratorem (np. "Hermes, wystaw fakturę na 5000 zł dla Dentysta sp. z o.o. za Landing Page").

---

## 3. Ekosystem Umiejętności Hermesa (Skills)

Cała wiedza domenowa zostaje przeniesiona do otwartego formatu Hermesa (`SKILL.md`). Zbudujemy "paczki wiedzy" dla każdego modułu:
- `web_researcher.md` (Prospecting)
- `landing_page_builder.md` (Anti-Gravity IDE)
- `campaign_generator.md` (Agency Pipeline)
- **Nowe**: `funnel_architect.md` (obsługa lejków *Low Friction*)
- **Nowe**: `legal_and_finance_admin.md` (faktury, umowy)

---

## 4. Etap Wdrożenia (Status "Wstrzymany na konsultacje")

**Co już zostało zrobione:**
- Makietowanie HTML/CSS nowego Dashboardu Holistic OS na lokalnym dysku (z wdrożonym systemem okien dla IDE, Prospectingu, Kanban i Agency Pipeline).
- Zbudowanie formatu Markdown dla bazowych skilli Hermesa.

**Kroki do wykonania PO konsultacji z Hermesem:**
1. Wysłanie plików UI przez WinSCP na serwer GCP i podpięcie pod serwer WWW Hermesa.
2. Uruchomienie `install_plugins.sh` na serwerze GCP (zainstaluje Mnemosyne, Kanban).
3. Podłączenie backendowego kanału komunikacji (SSE / WebSocket).
4. Zaprogramowanie logiki biznesowej dla nowego **Holistic Funnel Builder** oraz modułu **Finanse & Prawo** po stronie skilli Hermesa.

---

## Open Questions dla Hermesa (Do konsultacji)
1. W jaki sposób domyślnie serwujesz swój interfejs WWW (czy używasz do tego wbudowanego modułu Pythona, np. FastAPI, czy oddzielnego serwera typu Nginx/Caddy)? Pozwoli nam to bezproblemowo wrzucić stworzony przez Antigravity folder `ui/`.
2. Czy preferujesz autoryzację do tego lokalnego Dashboardu przez hasło/token, aby z zewnątrz nikt nie miał dostępu do bazy leadów i IDE na serwerze?
3. Jak najlepiej zintegrować bibliotekę generowania PDF (np. do faktur i umów) z Twoim systemem `SKILL.md`?
