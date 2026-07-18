# ======================================================================
# Deploy Jaison MLM Portal na Google Cloud Run (PowerShell)
# ======================================================================
# Wymagania: 
#   1. Zainstalowany gcloud CLI (https://cloud.google.com/sdk/docs/install)
# ======================================================================

$ErrorActionPreference = "Stop"
$PROJECT = "holistic-dashboard-dev"
$REGION = "europe-central2"  # Warszawa — najnizsze opoznienie dla Polski
$SERVICE = "jaison-mlm-portal"
$IMAGE = "gcr.io/$PROJECT/$SERVICE"

Write-Host "Jaison MLM Portal - Deploy na Cloud Run" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Krok 0: Autoryzacja - Korzystamy z domyslnej sesji uzytkownika, poniewaz projekt docelowy
# to 'holistic-dashboard-dev' na koncie GCP uzytkownika, a nie stare konto serwisowe.
Write-Host "Krok 0: Autoryzacja - Uzywam aktywnej sesji gcloud dewelopera..." -ForegroundColor Yellow

# Krok 1: Ustaw projekt
Write-Host "Krok 1: Ustawiam projekt GCP na $PROJECT..." -ForegroundColor Yellow
gcloud config set project $PROJECT

# Krok 2: Wlacz wymagane API (pomijamy, poniewaz sa juz aktywne w projekcie holistic-dashboard-dev,
# co zapobiega bledom uprawnien Service Usage).
Write-Host "Krok 2: Pomijam reczne wlaczanie API (sa juz aktywne w projekcie docelowym)..." -ForegroundColor Yellow

# Krok 3: Zbuduj i wypchnij obraz Docker w chmurze
Write-Host "Krok 3: Buduje kontener w Google Cloud Build..." -ForegroundColor Yellow
Write-Host "Trwa kompilacja i pakowanie w chmurze (pomijajac pliki z .dockerignore)..." -ForegroundColor DarkGray
gcloud builds submit --tag $IMAGE .

# Krok 4: Deploy na Cloud Run
Write-Host "Krok 4: Deploying uslugi na Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $SERVICE --image $IMAGE --platform managed --region $REGION --allow-unauthenticated --memory 512Mi --cpu 1 --min-instances 0 --max-instances 2 --timeout 300

# Krok 5: Pobierz URL i podsumuj
Write-Host "Deploy zakonczony sukcesem!" -ForegroundColor Green
$URL = gcloud run services describe $SERVICE --region $REGION --format "value(status.url)"
Write-Host "Portal Jaison MLM dostepny pod adresem Cloud Run:" -ForegroundColor Cyan
Write-Host "URL: $URL" -ForegroundColor Green
Write-Host "Aby podpiac domene mlm.jaison.pl, uzyj mapowania domen Cloud Run lub Nginx." -ForegroundColor DarkGray
