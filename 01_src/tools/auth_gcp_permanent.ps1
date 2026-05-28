# ======================================================================
# 🔑 Stała Autoryzacja Google Cloud SDK za pomocą Service Account
# ======================================================================
# Ten skrypt loguje gcloud CLI jako Service Account. Poświadczenia te
# NIE WYGASAJĄ co godzinę/12 godzin, co rozwiązuje problem uciekających tokenów.
# ======================================================================

$ErrorActionPreference = "Stop"
$PROJECT = "holistic-dashboard-dev"
$SA_JSON = "c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"

Write-Host "🧠 Holistic Operator — Permanent GCP Auth" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

if (Test-Path $SA_JSON) {
    Write-Host "📌 Krok 1: Weryfikacja pliku poświadczeń..." -ForegroundColor Yellow
    Write-Host "   Znaleziono: $SA_JSON" -ForegroundColor Gray
    
    Write-Host "`n📌 Krok 2: Aktywacja Service Account w gcloud CLI..." -ForegroundColor Yellow
    gcloud auth activate-service-account --key-file=$SA_JSON
    
    Write-Host "`n📌 Krok 3: Ustawianie projektu domyślnego na '$PROJECT'..." -ForegroundColor Yellow
    gcloud config set project $PROJECT
    
    Write-Host "`n📌 Krok 4: Weryfikacja aktywnego konta..." -ForegroundColor Yellow
    gcloud auth list
    
    Write-Host "`n✅ Sukces! gcloud CLI zostało pomyślnie autoryzowane za pomocą Service Account." -ForegroundColor Green
    Write-Host "💡 Twoje tokeny są teraz stałe i NIE wygasną samoczynnie (brak limitu 12:00)." -ForegroundColor Cyan
} else {
    Write-Host "`n❌ Błąd: Nie znaleziono pliku Service Account w lokalizacji: $SA_JSON" -ForegroundColor Red
    Write-Host "⚠️ Upewnij się, że plik JSON z kluczem konta usługowego znajduje się w katalogu projektu." -ForegroundColor Yellow
}
