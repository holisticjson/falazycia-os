# ======================================================================
# 🚀 Deploy Holistic CEO na Google Cloud Run
# ======================================================================
# Wymagania: 
#   1. Zainstalowany gcloud CLI (https://cloud.google.com/sdk/docs/install)
#   2. Klucz Service Account JSON w katalogu głównym (automatycznie autoryzowany)
# ======================================================================

$ErrorActionPreference = "Stop"
$PROJECT = "holistic-dashboard-dev"
$REGION = "europe-central2"  # Warszawa — najniższe opóźnienie
$SERVICE = "holistic-ceo"
$IMAGE = "gcr.io/$PROJECT/$SERVICE"

Write-Host "🧠 Holistic CEO — Deploy na Cloud Run" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Krok 0: Stała autoryzacja przez Service Account
Write-Host "`n📌 Krok 0: Autoryzacja za pomocą Service Account..." -ForegroundColor Yellow
$SA_JSON = "c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"
if (Test-Path $SA_JSON) {
    gcloud auth activate-service-account --key-file=$SA_JSON
    Write-Host "✅ Autoryzacja ukończona pomyślnie!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Brak pliku Service Account. Używam domyślnej sesji gcloud (może wygasnąć)." -ForegroundColor DarkYellow
}

# Krok 1: Ustaw projekt
Write-Host "`n📌 Krok 1: Ustawiam projekt GCP..." -ForegroundColor Yellow
gcloud config set project $PROJECT

# Krok 2: Włącz wymagane API
Write-Host "`n📌 Krok 2: Włączam API..." -ForegroundColor Yellow
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable aiplatform.googleapis.com

# Krok 3: Zbuduj i wypchnij obraz Docker
Write-Host "`n📌 Krok 3: Buduję kontener..." -ForegroundColor Yellow
gcloud builds submit --tag $IMAGE .

# Krok 4: Deploy na Cloud Run
Write-Host "`n📌 Krok 4: Deploying na Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $SERVICE `
    --image $IMAGE `
    --platform managed `
    --region $REGION `
    --allow-unauthenticated `
    --memory 1Gi `
    --cpu 1 `
    --min-instances 0 `
    --max-instances 2 `
    --timeout 300 `
    --set-env-vars "APP_PASSWORD=holistic2026,GCP_PROJECT=$PROJECT,GCP_LOCATION=us-central1" `
    --service-account "holistic-dashboard@$PROJECT.iam.gserviceaccount.com"

# Krok 5: Pobierz URL
Write-Host "`n✅ Deploy zakończony!" -ForegroundColor Green
$URL = gcloud run services describe $SERVICE --region $REGION --format "value(status.url)"
Write-Host "🌐 Dashboard dostępny pod: $URL" -ForegroundColor Cyan
Write-Host "🔑 Hasło: holistic2026" -ForegroundColor Yellow
Write-Host "`n💡 Zmień hasło w Cloud Run → Variables → APP_PASSWORD" -ForegroundColor DarkGray
