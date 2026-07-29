# ======================================================================
# Deploy Klubu Fala Życia na Google Cloud Run (Dashboard & Web Portal)
# ======================================================================

$ErrorActionPreference = "Stop"
$PROJECT = "falazycia-os"
$REGION = "europe-central2"

Write-Host "🌊 Klubu Fala Życia - Continuous Deployment na Cloud Run" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

# Krok 1: Ustaw projekt GCP
gcloud config set project $PROJECT

# Krok 2: Deploy Aplikacji Dashboardu (Streamlit Python App)
Write-Host "🚀 Buduję i wdrażam usługet fala-zycia-dashboard (Streamlit App)..." -ForegroundColor Yellow
gcloud builds submit --tag "gcr.io/$PROJECT/fala-zycia-dashboard" -f Dockerfile .
gcloud run deploy fala-zycia-dashboard --image "gcr.io/$PROJECT/fala-zycia-dashboard" --platform managed --region $REGION --allow-unauthenticated --memory 1Gi --cpu 1 --min-instances 0 --max-instances 3

# Krok 3: Deploy Portalu Statycznego (Nginx Web Portal)
Write-Host "🌐 Buduję i wdrażam usługę fala-zycia-web (Nginx Web Portal)..." -ForegroundColor Yellow
gcloud builds submit --tag "gcr.io/$PROJECT/fala-zycia-web" -f Dockerfile.web .
gcloud run deploy fala-zycia-web --image "gcr.io/$PROJECT/fala-zycia-web" --platform managed --region $REGION --allow-unauthenticated --memory 512Mi --cpu 1 --min-instances 0 --max-instances 3

Write-Host "✅ DEPLOY ZAKOŃCZONY SUKCESEM!" -ForegroundColor Green
Write-Host "Dashboard: https://fala-zycia-dashboard-194182220831.europe-central2.run.app" -ForegroundColor Cyan
Write-Host "Portal Web: https://fala-zycia.pl" -ForegroundColor Cyan
