# Skrypt wdrozeniowy backendu Holistyczny Broker na Google Cloud Run
# Uruchom w terminalu PowerShell: .\deploy_backend.ps1

param(
    [switch]$AutoDeploy
)

Write-Host "==========================================================" -ForegroundColor Yellow
Write-Host "   HOLISTYCZNY BROKER - DEPLOY BACKENDU NA GOOGLE CLOUD   " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Yellow

# 1. Definicja stalych parametrow
$PROJECT_ID = "holistic-broker"
$REGION = "europe-west1"  # Belgia (zgodnie ze starym kontem i spójnością infrastruktury)
$REPO_NAME = "broker-repo"
$SERVICE_NAME = "broker-backend"
$IMAGE_TAG = "$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/backend:latest"

# Sprawdzenie czy gcloud jest zainstalowany
if (!(Get-Command gcloud -ErrorAction SilentlyContinue)) {
    Write-Host "[BLAD] Google Cloud SDK (gcloud) nie jest zainstalowany na tym komputerze." -ForegroundColor Red
    Write-Host "Zainstaluj go z: https://cloud.google.com/sdk/docs/install" -ForegroundColor Yellow
    Exit
}

# 2. Ustawienie aktywnego projektu w gcloud
Write-Host "`n[1/5] Ustawianie aktywnego projektu GCP na: $PROJECT_ID..." -ForegroundColor Cyan
gcloud config set project $PROJECT_ID

# 3. Wlaczenie niezbednych uslug API na GCP
Write-Host "`n[2/5] Wlaczenie niezbednych uslug API (Cloud Build, Artifact Registry, Cloud Run)..." -ForegroundColor Cyan
gcloud services enable cloudbuild.googleapis.com artifactregistry.googleapis.com run.googleapis.com

# 4. Tworzenie repozytorium w Artifact Registry (jesli nie istnieje)
Write-Host "`n[3/5] Sprawdzanie / tworzenie bezpiecznego repozytorium Artifact Registry w Belgii ($REGION)..." -ForegroundColor Cyan
$repoExists = gcloud artifacts repositories describe $REPO_NAME --location=$REGION --quiet 2>$null
if (!$repoExists) {
    Write-Host "Repozytorium nie istnieje. Tworzenie nowej strefy '$REPO_NAME'..." -ForegroundColor Yellow
    gcloud artifacts repositories create $REPO_NAME --repository-format=docker --location=$REGION --description="Repozytorium backendu Holistyczny Broker"
} else {
    Write-Host "Repozytorium '$REPO_NAME' juz istnieje w regionie $REGION." -ForegroundColor Green
}

# 4.5. Przygotowanie folderu na pliki statyczne (Konsolidacja Frontendu + Backendu)
Write-Host "`n[4.5] Kopiowanie najnowszego frontendu z .\strona www do .\backend\static..." -ForegroundColor Cyan
$STATIC_DIR = ".\backend\static"

if (Test-Path $STATIC_DIR) {
    Remove-Item -Path "$STATIC_DIR\*" -Recurse -Force -ErrorAction SilentlyContinue
} else {
    New-Item -ItemType Directory -Path $STATIC_DIR -Force | Out-Null
}

# Kopiujemy tylko pliki produkcyjne (HTML, CSS, JS, PNG, robots.txt, sitemap.xml), pomijajac pliki pomocnicze .py i .md
Copy-Item -Path ".\strona www\*.html" -Destination $STATIC_DIR -ErrorAction SilentlyContinue
Copy-Item -Path ".\strona www\*.css" -Destination $STATIC_DIR -ErrorAction SilentlyContinue
Copy-Item -Path ".\strona www\*.js" -Destination $STATIC_DIR -ErrorAction SilentlyContinue
Copy-Item -Path ".\strona www\*.png" -Destination $STATIC_DIR -ErrorAction SilentlyContinue
Copy-Item -Path ".\strona www\robots.txt" -Destination $STATIC_DIR -ErrorAction SilentlyContinue
Copy-Item -Path ".\strona www\sitemap.xml" -Destination $STATIC_DIR -ErrorAction SilentlyContinue

Write-Host "Kopiowanie frontendu zakonczone sukcesem!" -ForegroundColor Green

# 5. Budowanie obrazu kontenera w chmurze (Google Cloud Build)
Write-Host "`n[4/5] Budowanie kontenera bezposrednio w chmurze przy uzyciu Google Cloud Build..." -ForegroundColor Cyan
Write-Host "Wysylanie zrodel z katalogu .\backend..." -ForegroundColor Yellow
gcloud builds submit .\backend --tag $IMAGE_TAG

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n[BLAD] Budowanie kontenera w chmurze nie powiodlo sie." -ForegroundColor Red
    Exit
}

Write-Host "`n[SUKCES] Kontener zostal poprawnie zbudowany i zapisany w Artifact Registry!" -ForegroundColor Green
Write-Host "Sciezka obrazu: $IMAGE_TAG" -ForegroundColor White

# 6. Opcjonalne automatyczne wdrozenie na Google Cloud Run
Write-Host "`n[5/5] Czy chcesz automatycznie wdrozyc ten kontener do uslugi Google Cloud Run w Belgii ($REGION)?" -ForegroundColor Yellow
if ($AutoDeploy) {
    Write-Host "Wykryto parametr -AutoDeploy. Automatyczne potwierdzenie wdrozenia." -ForegroundColor Green
    $confirmation = 'T'
} else {
    $confirmation = Read-Host "Wpisz [T] aby wdrozyc, lub [N] aby zakonczyc i wybrac obraz recznie w panelu (T/N)"
}

if ($confirmation -ne 'T' -and $confirmation -ne 't') {
    Write-Host "`nWdrozenie anulowane. Obraz kontenera czeka w Artifact Registry." -ForegroundColor Yellow
    Write-Host "Mozesz teraz odswiezyc strone w przegladarce i wybrac go recznie w panelu tworzenia uslugi!" -ForegroundColor Green
    Exit
}

Write-Host "`nWdrazanie kontenera na Google Cloud Run z dostepem publicznym..." -ForegroundColor Cyan

# Klasyczne, w 100% odporne i jednolinijkowe wywolanie gcloud bez zadnych tablic parametrow i backtickow
gcloud run deploy $SERVICE_NAME --image=$IMAGE_TAG --region=$REGION --platform=managed --allow-unauthenticated --min-instances=1 --max-instances=5 --port=8080

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n==========================================================" -ForegroundColor Green
    Write-Host "   WDROZENIE ZAKONCZONE SUKCESEM! BACKEND JEST ONLINE!     " -ForegroundColor Green
    Write-Host "==========================================================" -ForegroundColor Green
    Write-Host "Twoj produkcyjny, bezpieczny endpoint dla leadow to:" -ForegroundColor White
    Write-Host "https://[ZWROCONY-ADRES-URL-Z-KONSOLI]/api/lead" -ForegroundColor Yellow -NoNewline
    Write-Host " (Sprawdz powyzszy komunikat gcloud Service URL)" -ForegroundColor Gray
    Write-Host "Skopiuj ten adres i podmien go w plikach HTML/JS lub w Make/n8n!" -ForegroundColor Yellow
} else {
    Write-Host "`n[BLAD] Wdrozenie na Cloud Run nie powiodlo sie." -ForegroundColor Red
}
