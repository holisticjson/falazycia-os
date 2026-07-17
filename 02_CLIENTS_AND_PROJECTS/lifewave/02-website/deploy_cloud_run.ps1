# ======================================================================
# 🚀 Deploy Jaison X2O Portal na Google Cloud Run (PowerShell)
# ======================================================================
# Wymagania: 
#   1. Zainstalowany gcloud CLI (https://cloud.google.com/sdk/docs/install)
#   2. Klucz Service Account JSON w podfolderze php/key.json (automatycznie autoryzowany)
# ======================================================================

$ErrorActionPreference = "Stop"
$PROJECT = "jaison-x2o-portal"
$REGION = "europe-central2"  # Warszawa — najniższe opóźnienie dla Polski
$SERVICE = "jaison-x2o-portal"
$IMAGE = "gcr.io/$PROJECT/$SERVICE"

Write-Host "🧠 Jaison X2O Portal — Deploy na Cloud Run" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Krok 0: Stała autoryzacja przez Service Account
Write-Host "`n📌 Krok 0: Autoryzacja za pomocą Service Account..." -ForegroundColor Yellow
$SA_JSON = "c:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\lifewave\02-website\php\key.json"
if (Test-Path $SA_JSON) {
    gcloud auth activate-service-account --key-file=$SA_JSON
    Write-Host "✅ Autoryzacja ukończona pomyślnie przy użyciu: $SA_JSON" -ForegroundColor Green
} else {
    Write-Host "⚠️ Brak pliku Service Account w $SA_JSON. Używam domyślnej sesji gcloud (może wygasnąć)." -ForegroundColor DarkYellow
}

# Krok 1: Ustaw projekt
Write-Host "`n📌 Krok 1: Ustawiam projekt GCP..." -ForegroundColor Yellow
gcloud config set project $PROJECT

# Krok 2: Włącz wymagane API
Write-Host "`n📌 Krok 2: Włączam API w projekcie..." -ForegroundColor Yellow
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Krok 3: Zbuduj i wypchnij obraz Docker w chmurze
Write-Host "`n📌 Krok 3: Buduję kontener w Google Cloud Build..." -ForegroundColor Yellow
Write-Host "⏳ Trwa kompilacja i pakowanie w chmurze (pomijając pliki z .dockerignore)..." -ForegroundColor DarkGray
gcloud builds submit --tag $IMAGE .

# Krok 4: Deploy na Cloud Run
Write-Host "`n📌 Krok 4: Deploying usługi na Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $SERVICE --image $IMAGE --platform managed --region $REGION --allow-unauthenticated --memory 512Mi --cpu 1 --min-instances 0 --max-instances 2 --timeout 300

# Krok 5: Pobierz URL i podsumuj
Write-Host "`n✅ Deploy zakończony sukcesem!" -ForegroundColor Green
$URL = gcloud run services describe $SERVICE --region $REGION --format "value(status.url)"
Write-Host "🌐 Portal Jaison X2O dostępny pod adresem Cloud Run:" -ForegroundColor Cyan
Write-Host "👉 $URL" -ForegroundColor Green
Write-Host "`n💡 Aby podpiąć domenę x2o.jaison.pl, użyj gotowego szablonu Nginx (nginx_x2o_jaison.conf)" -ForegroundColor DarkGray
