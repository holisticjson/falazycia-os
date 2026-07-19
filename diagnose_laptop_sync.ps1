# ==============================================================================
# J(AI)SON OS — LAPTOP SYNC DOCTOR & DIAGNOSTICIAN (diagnose_laptop_sync.ps1)
# ==============================================================================
# Skrypt uruchamiany na laptopie (lub komputerze stacjonarnym) do wykrywania,
# diagnozowania i automatycznego naprawiania problemów z dwukierunkową synchronizacją.
# ==============================================================================

$RepoPath = "C:\Aplikacje MVP"
$LogPath = "$RepoPath\git_sync.log"

Clear-Host
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "         J(AI)SON OS — LAPTOP SYNC DOCTOR (v2.1)" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "Skrypt rozpoczyna diagnoze i automatyczna naprawe synchronizacji..." -ForegroundColor Yellow
Write-Host ""

# Funkcja pomocnicza do sprawdzania uprawnień administratora
function Test-IsAdmin {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

if (-not (Test-IsAdmin)) {
    Write-Host "[UWAGA] Skrypt nie zostal uruchomiony jako Administrator." -ForegroundColor Magenta
    Write-Host "Niektore operacje (np. naprawa Harmonogramu Zadan) moga sie nie powiesc." -ForegroundColor Magenta
    Write-Host "Zalecane: Uruchom PowerShell jako Administrator!" -ForegroundColor Magenta
    Write-Host ""
}

# 1. Sprawdzenie katalogu projektu
if (-not (Test-Path -Path $RepoPath)) {
    Write-Host "[ERR] Katalog $RepoPath nie istnieje!" -ForegroundColor Red
    Write-Host "Upewnij sie, ze projekt znajduje sie w domyslnej sciezce na tym urzadzeniu." -ForegroundColor Red
    exit
}
Write-Host "[OK] Wykryto katalog projektu: $RepoPath" -ForegroundColor Green

Set-Location -Path $RepoPath

# 2. Sprawdzenie logu ostatnich synchronizacji
if (Test-Path -Path $LogPath) {
    Write-Host "[INFO] Analiza ostatnich 10 wpisow z logu synchronizacji ($LogPath):" -ForegroundColor Cyan
    Write-Host "------------------------------------------------------------------" -ForegroundColor Gray
    Get-Content -Path $LogPath -Tail 10 | ForEach-Object {
        if ($_ -like "*[ERR]*") {
            Write-Host $_ -ForegroundColor Red
        } elseif ($_ -like "*[WARN]*") {
            Write-Host $_ -ForegroundColor Yellow
        } else {
            Write-Host $_ -ForegroundColor Gray
        }
    }
    Write-Host "------------------------------------------------------------------" -ForegroundColor Gray
} else {
    Write-Host "[WARN] Plik logu $LogPath nie istnieje. Synchronizacja mogla nigdy nie ruszyc na tym urzadzeniu." -ForegroundColor Yellow
}

# 3. Analiza stanu Gita i odblokowywanie ewentualnych procesów
Write-Host ""
Write-Host "Checking: Stan repozytorium Git..." -ForegroundColor Yellow

# Czy trwa proces rebase?
$rebaseMerge = Test-Path -Path "$RepoPath\.git\rebase-merge"
$rebaseApply = Test-Path -Path "$RepoPath\.git\rebase-apply"
if ($rebaseMerge -or $rebaseApply) {
    Write-Host "[ERR] Wykryto zawieszony/uszkodzony proces REBASE (konflikt z chmura)!" -ForegroundColor Red
    Write-Host "Automatycznie oczyszczam i cofam zablokowany rebase..." -ForegroundColor Yellow
    git rebase --abort 2>&1 | Out-Null
    Write-Host "[OK] Rebase zostal bezpiecznie anulowany. Repozytorium odblokowane." -ForegroundColor Green
} else {
    Write-Host "[OK] Brak aktywnego/zawieszonego procesu rebase." -ForegroundColor Green
}

# 4. Automatyczne usuwanie zagnieżdżonych .git (najważniejszy powód gubienia plików)
Write-Host ""
Write-Host "Checking: Poszukiwanie zagniezzdzonych repozytoriow .git..." -ForegroundColor Yellow
$nestedGitDirs = Get-ChildItem -Path $RepoPath -Recurse -Directory -Filter ".git" -Force -ErrorAction SilentlyContinue | Where-Object {$_.FullName -ne "$RepoPath\.git"}

if ($nestedGitDirs) {
    Write-Host "[WARN] Znaleziono zagniezdzone foldery .git, ktore blokuja synchronizacje plików!" -ForegroundColor Yellow
    foreach ($dir in $nestedGitDirs) {
        Write-Host " -> Usuwanie blokady w: $($dir.Parent.FullName)" -ForegroundColor DarkYellow
        # Usuń z pamięci cache Gita, jeśli było śledzone jako submoduł/gitlink
        git rm --cached $($dir.Parent.Name) 2>&1 | Out-Null
        # Usuń fizyczny folder .git z dysku
        Remove-Item -Path $dir.FullName -Recurse -Force -ErrorAction SilentlyContinue
    }
    Write-Host "[OK] Wszystkie zagniezdzone repozytoria .git zostaly trwale usuniete!" -ForegroundColor Green
} else {
    Write-Host "[OK] Brak zagniezzdzonych folderow .git. Struktura jest czysta." -ForegroundColor Green
}

# 5. Sprawdzenie połączenia i poświadczeń GitHub
Write-Host ""
Write-Host "Checking: Polaczenie i autoryzacja z GitHub..." -ForegroundColor Yellow
$ping = Test-Connection -ComputerName github.com -Count 1 -Quiet
if (-not $ping) {
    Write-Host "[ERR] Brak polaczenia z internetem lub github.com. Urzadzenie jest offline!" -ForegroundColor Red
    exit
}

Write-Host "Pobieranie najnowszego stanu z chmury (git fetch origin)..." -ForegroundColor Gray
$fetchResult = git fetch origin main 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERR] Blad uwierzytelniania lub polaczenia z GitHub!" -ForegroundColor Red
    Write-Host "Git zwrocil blad:" -ForegroundColor DarkRed
    Write-Host $fetchResult -ForegroundColor DarkRed
    Write-Host "Rekomendacja: Sprawdz, czy masz zalogowanego gita na tym urzadzeniu (np. sprawdz Personal Access Token)." -ForegroundColor Yellow
    exit
}
Write-Host "[OK] Polaczenie i autoryzacja z GitHub przebiegla pomyślnie." -ForegroundColor Green

# 6. Synchronizacja i ujednolicenie stanu (Pull & Rebase)
Write-Host ""
Write-Host "Action: Synchronizowanie stanu lokalnego z chmura..." -ForegroundColor Yellow

# Zabezpiecz lokalne zmiany przed pobraniem (stash)
$status = git status --porcelain
if ($status) {
    Write-Host "[INFO] Wykryto lokalne modyfikacje plikow na tym urzadzeniu." -ForegroundColor Cyan
    Write-Host "Zabezpieczam Twoje lokalne zmiany (git stash)..." -ForegroundColor Gray
    git stash -u 2>&1 | Out-Null
    $stashed = $true
}

Write-Host "Pobieranie i nakladanie zmian z chmury (git pull --rebase)..." -ForegroundColor Gray
$pullResult = git pull --rebase origin main 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERR] Blad podczas automatycznego pobierania zmian z chmury!" -ForegroundColor Red
    Write-Host $pullResult -ForegroundColor DarkRed
    if ($stashed) {
        Write-Host "Przywracam Twoje lokalne zmiany z pamieci podrecznej (git stash pop)..." -ForegroundColor Gray
        git stash pop 2>&1 | Out-Null
    }
    exit
}
Write-Host "[OK] Zmiany zostaly pomyslnie dociagniete z chmury na to urzadzenie!" -ForegroundColor Green

# Przywróć zmiany, jeśli były schowane
if ($stashed) {
    Write-Host "Przywracam Twoje lokalne zmiany (git stash pop)..." -ForegroundColor Gray
    $stashPopResult = git stash pop 2>&1
    Write-Host "[OK] Lokalne zmiany zostaly przywrocone i polaczone ze stanem z chmury." -ForegroundColor Green
}

# 7. Audyt i naprawa Harmonogramu Zadan (Windows Task Scheduler)
Write-Host ""
Write-Host "Checking: Audyt Harmonogramu Zadan (JaisonWorkspaceAutoSync)..." -ForegroundColor Yellow

$taskName = "JaisonWorkspaceAutoSync"
$taskExists = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

if ($taskExists) {
    $taskUser = $taskExists.Principal.UserId
    Write-Host "[OK] Wykryto zarejestrowane zadanie w tle: $taskName" -ForegroundColor Green
    Write-Host " Zadanie uruchamia sie jako uzytkownik: $taskUser" -ForegroundColor Gray
    Write-Host " Aktualnie zalogowany uzytkownik to : $currentUser" -ForegroundColor Gray
    
    # Sprawdzenie czy użytkownik w zadaniu pokrywa się z zalogowanym (ważne przy migracji laptopa!)
    # Często na laptopie nazwa użytkownika jest inna niż na stacjonarnym (np. 'tomasz' zamiast 'tomas_yq1b9su')
    if ($taskUser -ne $env:USERNAME -and $taskUser -ne $currentUser) {
        Write-Host "[WARN] Uzytkownik w zadaniu ($taskUser) rozni sie od aktualnego ($currentUser)!" -ForegroundColor Yellow
        Write-Host "Moze to blokowac automatyczne uruchamianie skryptu na tym urzadzeniu!" -ForegroundColor Yellow
        $recreateTask = $true
    }
} else {
    Write-Host "[WARN] Brak zadania '$taskName' w Harmonogramie Zadan na tym urzadzeniu!" -ForegroundColor Yellow
    $recreateTask = $true
}

if ($recreateTask -and (Test-IsAdmin)) {
    Write-Host "Automatycznie rejestruje zadanie w tle dla uzytkownika $currentUser..." -ForegroundColor Yellow
    
    # Usuń stare zadanie jeśli istniało
    if ($taskExists) {
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    }
    
    # Parametry nowego zadania
    $action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -WindowStyle Hidden -File ""$RepoPath\git_sync.ps1"""
    # Uruchamiaj co 15 minut, bez końca
    $trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 15)
    $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
    
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -User $currentUser -RunLevel Limited -ErrorAction SilentlyContinue | Out-Null
    
    if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
        Write-Host "[OK] Zadanie w tle zostalo pomyslnie zarejestrowane i zoptymalizowane!" -ForegroundColor Green
    } else {
        Write-Host "[ERR] Nie udalo sie zarejestrowac zadania w Harmonogramie." -ForegroundColor Red
    }
} elseif ($recreateTask) {
    Write-Host "[REKOMENDACJA] Aby naprawic/zarejestrowac zadanie w tle, musisz uruchomic ten skrypt jako Administrator!" -ForegroundColor Yellow
}

# 8. Testowy manualny sync na zakonczenie deweloperskie
Write-Host ""
Write-Host "Action: Uruchamianie pierwszego pelnego testu synchronizacji (git_sync.ps1)..." -ForegroundColor Yellow
& "$RepoPath\git_sync.ps1"

Write-Host ""
Write-Host "==================================================================" -ForegroundColor Green
Write-Host "           DIAGNOZA I NAPRAWA ZAKONCZONA POMYSLNIE!" -ForegroundColor Green
Write-Host "==================================================================" -ForegroundColor Green
Write-Host "Twoje urzadzenie jest teraz w pelni zsynchronizowane z chmura." -ForegroundColor White
Write-Host "Zadanie w tle bedzie automatycznie odpytywac i wysylac zmiany co 15 min." -ForegroundColor White
Write-Host "==================================================================" -ForegroundColor Green
Write-Host "Nacisnij dowolny klawisz, aby zakonczyc..." -ForegroundColor Gray
Read-Host | Out-Null
