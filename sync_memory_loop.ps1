# sync_memory_loop.ps1 - Memory Loop and Gitkeep Engine (ASCII ONLY to avoid PowerShell parser bugs)
# 1. Creates/updates WORKSPACE_MEMORY.md files (Memory Loop).
# 2. Creates .gitkeep in empty subfolders to force Git sync.

$ErrorActionPreference = "SilentlyContinue"
$DateNow = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

Write-Host "=====================================================" -ForegroundColor Purple
Write-Host "INICJALIZACJA PETLI PAMIECI I SYNCHRONIZACJI STRUKTUR" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Purple

# Definicje katalogow
$BaseDir = "C:\Aplikacje MVP"
$ClientsDir = Join-Path $BaseDir "02_CLIENTS_AND_PROJECTS"
$AgencyDir = Join-Path $BaseDir "01_JAISON_AGENCY_OS"

# Funkcja generujaca szablon
function Get-MemoryTemplate($ProjectName) {
    $Lines = @(
        "# MEMORY - $ProjectName",
        "",
        "---",
        "",
        "## STATUS PROJEKTU",
        "- **Status:** Planowanie (Inicjalizacja petli)",
        "- **Ostatnia aktualizacja:** ${DateNow} przez Memory Loop Engine",
        "- **Biezacy cel glowny:** Zdefiniuj glowny cel biznesowy dla projektu $ProjectName.",
        "",
        "---",
        "",
        "## ARCHITEKTURA I STACK TECHNICZNY",
        "- **Frontend:** HTML/CSS/JS (Low-Friction) lub Streamlit",
        "- **Automatyzacja:** n8n Webhooks and Systeme.io (Marketing)",
        "- **Sztuczna Inteligencja (AI):** Gemini 2.5 Flash / Vertex AI Agent Builder",
        "- **Baza Danych and Storage:** Google Cloud Storage / SQLite / Local files",
        "",
        "---",
        "",
        "## NAJBLIZSZE KAMIE MILE I STATUS TODO",
        "- [ ] **Kamien Milowy 1:** Inicjalizacja bazy wiedzy (.md) i audyt struktury folderow.",
        "- [ ] **Kamien Milowy 2:** Podpiecie lejkow w Systeme.io i integracja webhookow n8n.",
        "- [ ] **Kamien Milowy 3:** Testy e2e suwerennego agenta i przekazanie dostepu.",
        "",
        "---",
        "",
        "## LOG AKTYWNOSCI",
        "- **${DateNow}**: Automatyczna inicjalizacja pliku pamieci WORKSPACE_MEMORY.md przez systemowa petle."
    )
    return $Lines -join "`r`n"
}

$FoldersToScan = @()

# 1. Folder agencji
if (Test-Path $AgencyDir) {
    $FoldersToScan += [PSCustomObject]@{
        Name = "Jaison Agency"
        Path = $AgencyDir
    }
}

# 2. Foldery klientow
if (Test-Path $ClientsDir) {
    $SubDirs = Get-ChildItem -Path $ClientsDir -Directory
    foreach ($d in $SubDirs) {
        if (!$d.Name.StartsWith(".")) {
            $FoldersToScan += [PSCustomObject]@{
                Name = $d.Name
                Path = $d.FullName
            }
        }
    }
}

Write-Host "Wykryto $($FoldersToScan.Count) folderow..." -ForegroundColor Yellow

foreach ($f in $FoldersToScan) {
    # --- CZESC 1: MEMORY LOOP ---
    if ($f.Name -ne "Szablon_Projektu") {
        $MemoryPath = Join-Path $f.Path "WORKSPACE_MEMORY.md"
        
        if (Test-Path $MemoryPath) {
            Write-Host "[PAMIEC] [Istnieje] $($f.Name) -> Aktualizuje timestamp..." -ForegroundColor Green
            $Content = Get-Content -Path $MemoryPath -Raw -Encoding UTF8
            $Pattern = "- \*\*Ostatnia aktualizacja:\*\* .*? przez (.*)"
            if ($Content -match $Pattern) {
                $Replacement = "- **Ostatnia aktualizacja:** ${DateNow} przez Jaison Agent OS"
                $Content = [regex]::Replace($Content, $Pattern, $Replacement)
                Set-Content -Path $MemoryPath -Value $Content -Encoding UTF8
            }
        } else {
            Write-Host "[PAMIEC] [Nowy] $($f.Name) -> Tworze plik WORKSPACE_MEMORY.md..." -ForegroundColor Yellow
            $TemplateContent = Get-MemoryTemplate -ProjectName $f.Name
            Set-Content -Path $MemoryPath -Value $TemplateContent -Encoding UTF8
        }
    }

    # --- CZESC 2: GITKEEP FOR EMPTY DIRECTORIES ---
    $SubFolders = Get-ChildItem -Path $f.Path -Recurse -Directory
    
    foreach ($sf in $SubFolders) {
        if ($sf.FullName -match "\\\.(git|venv|agents|vscode|roo|pnpm)" -or $sf.FullName -match "node_modules|__pycache__") {
            continue
        }

        $Elements = Get-ChildItem -Path $sf.FullName
        
        if ($Elements.Count -eq 0) {
            $GitKeepPath = Join-Path $sf.FullName ".gitkeep"
            Write-Host "[STABILIZACJA] Tworze .gitkeep w: $($sf.FullName.Replace($BaseDir, ''))" -ForegroundColor Cyan
            Set-Content -Path $GitKeepPath -Value "# Gitkeep" -Encoding ASCII
        }
    }
}

Write-Host "=====================================================" -ForegroundColor Purple
Write-Host "SYNCHRONIZACJA ZAKONCZONA SUKCESEM!" -ForegroundColor Cyan
Write-Host "=====================================================" -ForegroundColor Purple
