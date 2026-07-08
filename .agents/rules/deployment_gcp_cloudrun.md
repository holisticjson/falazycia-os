# Deployment na GCP Cloud Run (Streamlit) [Manual Workflow]

## Cel
Ten dokument to sekwencyjny workflow (przepływ pracy), wywoływany ręcznie na żądanie. Instrukcje te zapewniają ustandaryzowany, bezpieczny, powtarzalny proces konteneryzacji i wdrażania lokalnego *Holistic CEO Dashboard* (zbudowanego w Python/Streamlit) na architekturze Serverless w Google Cloud Run z uwzględnieniem wykorzystania darmowego budżetu $300 GCP.

## KROK 1: Konteneryzacja (Zarządzanie Zależnościami i Dockerfile)
Aplikacja wymaga zablokowanego środowiska poprzez poprawny obraz Dockerowy.

1.  Upewnij się, że plik `requirements.txt` zawiera wszystkie potrzebne biblioteki (m.in. `streamlit`, `google-genai`, `boto3`, `google-cloud-storage`, itp.).
2.  Twój `Dockerfile` powinien opierać się na lekkim obrazie `python:3.10-slim` (lub podobnym) w celu minimalizacji wagi.
3.  Zasady Dockerfile dla Streamlit:
    *   Wystaw i ujawnij port `8080` (`EXPOSE 8080`).
    *   Ustaw odpowiednią komendę startową z argumentami, np.:
        `CMD ["streamlit", "run", "holistic_ceo.py", "--server.port=8080", "--server.address=0.0.0.0"]`

## KROK 2: Przygotowanie Zmiennych Środowiskowych
Aplikacja opiera się na wielu zewnętrznych API (Gemini, Anthropic/Bedrock, Make webhooki).
1.  Nie umieszczaj sekretów w kodzie źródłowym ani w Dockerfile (zignoruj w `.dockerignore`).
2.  Wykorzystaj system Google Cloud Secret Manager lub po prostu przekaż bezpieczne `Environment Variables` podczas komendy wdrażania Cloud Run.
3.  Baza Wiedzy: Ścieżki lokalne (np. `Baza_Wiedzy/`) muszą być zapisywane do Google Cloud Storage, lub, jeśli baza nie jest duża i nie ewoluuje asynchronicznie, zamrożona wewnątrz obrazu przy każdym buidzie.

## KROK 3: Operacje Terminala GCP CLI (Deployment)
Zakładając, że masz zainstalowany lokalnie `gcloud cli` i jesteś uwierzytelniony:

1. **Ustawienie projektu:**
   `gcloud config set project [ID_TWOJEGO_PROJEKTU_GCP]`

2. **Zbudowanie i Wysłanie obrazu (Google Artifact Registry lub Container Registry):**
   Użyj polecenia Cloud Build dla uproszczenia (pozwala na budowę na serwerach Google, bez lokalnego dockera!):
   `gcloud builds submit --tag gcr.io/[ID_TWOJEGO_PROJEKTU_GCP]/holistic-ceo-dashboard`

3. **Deploy usługi na Cloud Run:**
   `gcloud run deploy holistic-ceo-dashboard --image gcr.io/[ID_TWOJEGO_PROJEKTU_GCP]/holistic-ceo-dashboard --platform managed --region europe-central2 --allow-unauthenticated --port 8080 --memory 1Gi`
   *(Parametr memory może zostać zwiększony w razie potrzeb modeli/Streamlit)*

## KROK 4: Weryfikacja Po Wdrożeniu
1.  Pobierz URL wygenerowany przez polecenie deploy.
2.  Upewnij się, że routing URL (`?modul=...`) poprawnie współgra z reverse proxy Google.
3.  Przetestuj zrzut pamięci w Ingestion Hub. Zauważ, że standardowy Cloud Run jest "Stateless". Pliki zapisywane na dysku kontenera (np. zmiany w `inspirations.json`) znikną, gdy kontener zostanie uśpiony. Jeśli potrzebujesz trwałości danych (persistance) poza GCS, upewnij się, że agent zsynchronizował je przed usunięciem kontenera!

## Kiedy wywołać ten Workflow?
Komenda aktywacyjna dla Agenta (Ty jako CEO/Architekt):
*   *"Wykonaj workflow @deployment_gcp_cloudrun. Zbuduj instrukcję wdrożeniową krok-po-kroku z aktualnym kodem dla Cloud Run."*
