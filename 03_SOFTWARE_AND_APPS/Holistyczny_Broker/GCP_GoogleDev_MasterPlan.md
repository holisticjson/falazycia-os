# Master Plan GCP & Google Developers: Holistyczny Broker

Ten dokument stanowi techniczną specyfikację infrastruktury chmurowej oraz procedury weryfikacyjnej w Google Developers dla projektu **Holistyczny Broker**. Został opracowany w celu wdrożenia architektury dwukontowej (Dual-Account), optymalizacji kosztowej (Low-Cost) oraz ułatwienia procesu weryfikacji aplikacji.

---

## 🏛️ 1. Architektura Dwukontowa GCP (Dual-Account)

Aby oddzielić prywatne projekty i zapobiec mieszaniu się danych (np. tematów ADHD i marketingu Holistic Jason z wrażliwymi danymi deweloperskimi i off-market), wdrażamy pełną separację:

| Filar | Konto Właściciela | Rola w Ekosystemie | Środki i Kredyty |
| :--- | :--- | :--- | :--- |
| **Holistic Jason** | `holisticjson@gmail.com` | Maszyna wirtualna VM (Hermes), prywatne repozytoria, integracje n8n. | $300 Free Trial na GCP |
| **Holistic Broker** | `brokerholistic@gmail.com` | Organizacja B2B, Google Vertex AI (Llama, Gemini), systemy generatywne (Veo, Imagen). | $1000 App Builder Credit |

### 🚀 Korzyści z separacji baz RAG:
1. **Czystość Danych (Data Isolation):** Zapytania o nieruchomości i deweloperów nie będą mieszać się z notatkami o ADHD i marketingu, co drastycznie zwiększa precyzję RAG.
2. **Podwójny Grant (Double Credits):** Wykorzystując dwa oddzielne konta GCP, na obu możesz aktywować darmowe środki, co daje łącznie **$2000 na same bazy RAG (Vertex AI Search)**.

---

## ☁️ 2. Instrukcja Aktywacji Grantu $1000 (Vertex AI Search)

Na nowym koncie organizacji (`brokerholistic@gmail.com`) środki "Trial credit for GenAI App Builder" uaktywniają się automatycznie przy pierwszej inicjalizacji usługi. 

### 🛠️ Kroki do wyklikania w Konsoli Google Cloud:
1. Zaloguj się do **Google Cloud Console** jako użytkownik `brokerholistic@gmail.com`.
2. Upewnij się, że w lewym gargnym rogu konsoli masz wybrany projekt: **`holistic-broker`**.
3. W pasku wyszukiwania na samej górze wpisz i kliknij: **`AI Applications`** *(usługa ta to dawna nazwa Vertex AI Search and Conversation)*.
4. Kliknij przycisk **Enable API** (Aktywuj API) i poczekaj na zakończenie procesu.
5. Utwórz pierwszą, testową aplikację:
   - Kliknij **Create App** -> Wybierz typ **Search**.
   - Nazwij aplikację np. `HolistycznyBroker-RAG`.
   - Utwórz nowy **Data Store** (np. wybierając opcję importu ze strony internetowej i podając link `https://holistycznybroker.pl` lub wrzucając dowolny próbny dokument PDF).
6. Po przejściu tej procedury, w ciągu kilkunastu minut w zakładce **Billing -> Credits** na Twoim koncie powinno pojawić się nowe zasilenie na kwotę **$1000**.

---

## 🔑 3. Konfiguracja LiteLLM i Routing Modelu (Region: us-central1)

Zgodnie z audytem limitów w regionie `us-central1` na koncie `holistic-broker`, LiteLLM (działający na porcie `4000`) powinien kierować zapytania do najnowszych i najbardziej efektywnych kosztowo modeli Google:

```yaml
# Lokalizacja: /home/holisticjson/litellm_config.yaml (na maszynie VM)
model_list:
  - model_name: hermes-fast
    litellm_params:
      model: vertex_ai/gemini-2.0-flash-001             # Szybkie i tanie wnioskowanie B2B/B2C
      vertex_project: holistic-broker
      vertex_location: us-central1
      vertex_credentials: /home/holisticjson/gcp-sa-key.json
      rpm: 2000 
  - model_name: hermes-think
    litellm_params:
      model: vertex_ai/gemini-2.5-pro-preview-06-05     # Trudne zadania logiczne, analizy prawne
      vertex_project: holistic-broker
      vertex_location: us-central1
      vertex_credentials: /home/holisticjson/gcp-sa-key.json
      rpm: 60
  - model_name: hermes-image
    litellm_params:
      model: vertex_ai/imagegeneration@006             # Zoptymalizowany model Imagen 3 (Fast)
      vertex_project: holistic-broker
      vertex_location: us-central1
      vertex_credentials: /home/holisticjson/gcp-sa-key.json
      rpm: 20                                            # Ominięcie limitu 1 RPM wersji "Standard"
```

---

## 📝 4. Wniosek do Google for Developers (Weryfikacja OAuth)

Gdy Hermes (AntiGravity System) będzie potrzebował zintegrować się z **Gmail API** lub **Google Sheets API** na koncie organizacji, Google poprosi o podanie uzasadnienia bezpieczeństwa. Wklej poniższy angielski tekst w formularzu zgody (OAuth Consent Screen Verification):

### 📋 Gotowy Tekst Uzasadnienia (App Justification):
```text
Holistic Broker (AntiGravity System) is an internal CRM and workflow automation tool designed specifically for our elite real estate agency. Our application requests access to the Gmail API and Google Sheets API to automate internal B2B lead processing, synchronize NDA agreements for off-market properties, and manage our internal client portfolio. 

The application does not expose user data to third parties. We are automating our own agency's email communications (sending initial NDAs to verified investors) and storing analytical data securely in our own Google Sheets. This integration is crucial for maintaining our 'Quiet Luxury' standard of rapid, secure, and discrete client communication.
```

### 🔒 Wymogi dotyczące domeny i zgodności prawnej:
Przed wysłaniem wniosku do weryfikacji w konsoli Google Cloud, upewnij się, że na stronie `holistycznybroker.pl` wdrożono:
1. **Politykę Prywatności oraz Regulamin:** Muszą być łatwo dostępne (np. w stopce strony).
2. **Dane rejestrowe firmy:** W sekcji "Administrator Danych" w Polityce Prywatności lub na końcu regulaminu należy twardo wpisać:
   - Pełną nazwę firmy
   - Numer NIP i REGON
   - Adres siedziby
3. **Zgodność z RODO:** Google ręcznie weryfikuje czy strona posiada te elementy. Bez nich wniosek o weryfikację OAuth zostanie odrzucony.
