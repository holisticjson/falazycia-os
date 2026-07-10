# 📑 BRIEF DLA AGENTA ANDROID: Rebranding J(AI)SON & Architektura API (Aktualizacja po migracji GCP)

Cześć! Wdrożyliśmy globalną migrację infrastruktury oraz rebranding z marki **Holistic Jason** na **J(AI)SON**. Zmienia to naszą architekturę sieciową, adresy IP maszyn oraz mapowanie domen. 

Jako agent odpowiedzialny za aplikację mobilną Android oraz jej backend, musisz dostosować konfigurację sieciową aplikacji i poznać nowe punkty wejścia (endpoints) dla systemu **Hermes Agentic OS** oraz backendu komunikatora.

---

## 🌐 1. Nowa Infrastruktura GCP i IP Maszyny

Cała infrastruktura została przeniesiona z USA (`us-central1-a`) do Europy (**`europe-west1-b` - Belgia**).
* **Nowy zewnętrzny adres IP VPS (maszyna `hermes-jaison-core`):** `35.210.44.117`
* **Stary adres IP (`34.55.82.86`) oraz stara maszyna (`hermes-os`) w USA są nieaktywne i przeznaczone do usunięcia.**

---

## 🌐 2. Nowy Podział Domenowy w Cloudflare

Domeny są zarządzane przez Cloudflare. Ze względu na decyzje biznesowe wprowadzamy następujący podział subdomen:

1. **`jaison.pl`** (oraz `www.jaison.pl`) ➔ **Landing Page Główny (Agencja AI)**
   * **Host:** Google Cloud Run (`holisticjson-website`)
2. **`app.jaison.pl`** ➔ **Landing Page dla bezpiecznej aplikacji mobilnej J(AI)SON**
   * **Przeznaczenie:** Docelowo strona pobierania i prezentacji autorskiej, bezpiecznej aplikacji Jaison.
3. **`api.jaison.pl`** (lub alternatywnie `messenger.jaison.pl`) ➔ **Backend API komunikatora**
   * **Host:** VPS `35.210.44.117` na porcie `8080` (Docker: `hermes-messenger-server`).
   * *Nginx proxy config:* Przekazuje ruch z HTTPS do kontenera na porcie `8080`.
4. **`os.jaison.pl`** ➔ **Hermes Agentic OS (Streamlit Dashboard & System APIs)**
   * **Host:** VPS `35.210.44.117` na porcie `9119` (usługa systemd `hermes-dashboard.service` bindowana do `127.0.0.2:9119`).
   * *Nginx proxy config:* Rozwiązano błąd 502 Bad Gateway. Streamlit działa poprawnie i jest w pełni zintegrowany.

---

## 🔌 3. Jak aplikacja mobilna komunikuje się z serwerem? (Endpoints)

Gdy aplikacja Android wykonuje połączenia do API, używa następujących punktów wejścia na nowym VPS:

| Zewnętrzny Endpoint (HTTPS) | Wewnętrzny Cel na VPS | Opis / Przeznaczenie |
| :--- | :--- | :--- |
| `https://api.jaison.pl/` | `http://127.0.0.1:8080` | **Backend API komunikatora** (kontener Docker) |
| `https://os.jaison.pl/` | `http://127.0.0.2:9119` | **Hermes Dashboard** (Streamlit UI) |
| `https://os.jaison.pl/api/lead` | `http://127.0.0.1:8000/api/lead` | **Lead Collector API** (FastAPI) |
| `https://os.jaison.pl/hermes-api/` | `http://127.0.0.1:8642/` | **Główne API Hermes OS** (n8n / workflow core) |
| `https://os.jaison.pl/v1/` | `http://127.0.0.1:8642/v1/` | **API kompatybilne z OpenAI** (dla chatbotów) |

---

## 🛠️ 4. Zadania dla Agenta Android

1. **Aktualizacja Adresów IP i URL API:** Zmień wszystkie twardo zakodowane adresy lub wartości w plikach konfiguracyjnych backendu i aplikacji mobilnej ze starych domen/IP USA na nowe:
   * Backend API komunikatora: `https://api.jaison.pl`
   * Hermes Integration API: `https://os.jaison.pl`
2. **Certyfikaty SSL (Cloudflare):** Całość ruchu szyfrowana jest przez SSL. Nginx na serwerze posługuje się certyfikatami Let's Encrypt i proxy Cloudflare. Upewnij się, że biblioteki sieciowe w Androidzie (OkHttp, Retrofit) nie napotykają problemów z zaufaniem certyfikatów.
3. **Pliki konfiguracyjne (.env):** Zaktualizuj pliki konfiguracyjne w folderze `c:\Aplikacje MVP\Android\server\.env` na podstawie `.env.example` wprowadzając nowe wartości domen.

W razie potrzeby dodania nowych reguł routingu w Nginx lub modyfikacji kontenerów Docker na serwerze, daj znać agentowi Hermes Cloud Architect / CTO (opiekunowi serwera VPS) - wszystko skonfigurujemy w locie!
