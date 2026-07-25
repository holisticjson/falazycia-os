# ==============================================================================
# J(AI)SON OS — AUTOMATED BACKGROUND GIT SYNCHRONIZER (git_sync.ps1)
# ==============================================================================
# Skrypt do bezobsługowej, automatycznej synchronizacji kodu i bazy wiedzy 
# pomiędzy komputerem stacjonarnym a laptopem przez GitHub w tle.
# Zapobiega konfliktom, automatycznie tworzy commity i dba o spójność.
# ==============================================================================

# Konfiguracja ścieżek
$RepoPath = "C:\Aplikacje MVP"
$LogPath = "$RepoPath\git_sync.log"

# Funkcja do zapisu logów
function Write-Log {
    param([string]$message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMsg = "[$timestamp] $message"
    Write-Host $logMsg
    Add-Content -Path $LogPath -Value $logMsg
}

Write-Log "=== Rozpoczecie automatycznej synchronizacji J(AI)SON ==="

# 1. Sprawdzenie połączenia z internetem (GitHub)
$ping = Test-Connection -ComputerName github.com -Count 1 -Quiet
if (-not $ping) {
    Write-Log "[INFO] Brak polaczenia z github.com. Urzadzenie offline lub brak internetu. Przerywam."
    exit
}

# 2. Przejście do folderu projektu
Set-Location -Path $RepoPath

# Włączenie obsługi długich ścieżek plików w Windows Git
git config core.longpaths true

# 3. Sprawdzenie lokalnych zmian w kodzie
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Log "[INFO] Wykryto lokalne modyfikacje plikow. Przygotowuje automatyczny zapis..."
    
    # Dodanie wszystkich dozwolonych plików (wykluczając sekrety i logi z .gitignore)
    git add -A
    
    # Utworzenie automatycznego commita z nazwą komputera i czasem
    $computerName = $env:COMPUTERNAME
    $dateStr = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $commitMsg = "auto: update from $computerName [$dateStr]"
    git commit -m "$commitMsg"
    
    Write-Log "[OK] Zmiany zatwierdzone lokalnie: $commitMsg"
} else {
    Write-Log "[OK] Brak lokalnych zmian do zapisu."
}

# 4. Pobranie najnowszego stanu z repozytorium GitHub (Fetch)
Write-Log "[INFO] Pobieranie stanu z GitHub (git fetch)..."
git fetch origin main

# 5. Bezpieczny Pull za pomocą Rebase (utrzymuje liniową historię bez merge commitów)
Write-Log "[INFO] Pobieranie i scalanie zmian (git pull --rebase)..."
$pullResult = git pull --rebase origin main 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Log "[ERR] Wykryto konflikt podczas scalania (Pull Rebase)! Bezpiecznie anuluje operacje..."
    git rebase --abort
    Write-Log "[WARN] Synchronizacja wstrzymana. Rozwiaz konflikty recznie."
    exit
} else {
    Write-Log "[OK] Scalanie zakonczone sukcesem!"
}

# 6. Wypchnięcie lokalnych zmian do chmury (Push), jeśli istnieją commity przed origin/main
$aheadBehind = git rev-list --left-right --count origin/main...main
$ahead = ($aheadBehind -split '\s+')[1]

if ([int]$ahead -gt 0) {
    Write-Log "[INFO] Wykryto $ahead lokalnych zatwierdzen. Wysylam do GitHub..."
    git push origin main 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Log "[OK] Dane zostaly pomyslnie wyslane do chmury!"
    } else {
        Write-Log "[ERR] Blad podczas wysylania danych (git push)."
    }
} else {
    Write-Log "[OK] Brak nowych lokalnych zatwierdzen do wyslania."
}

Write-Log "=== Koniec automatycznej synchronizacji ==="
