param(
    [Parameter(Mandatory=$true)]
    [string]$Name,
    
    [Parameter(Mandatory=$true)]
    [ValidateSet("client", "app")]
    [string]$Type
)

# Ścieżka bazowa
$BaseDir = "C:\Aplikacje MVP"
$TargetParent = if ($Type -eq "client") { "$BaseDir\02_CLIENTS_AND_PROJECTS" } else { "$BaseDir\03_SOFTWARE_AND_APPS" }
$ProjectDir = "$TargetParent\$Name"
$AgentsDir = "$ProjectDir\.agents"

Write-Host "=== Tworzenie nowego projektu J(AI)SON OS: $Name ($Type) ===" -ForegroundColor Cyan

# 1. Tworzenie katalogu projektu
if (Test-Path $ProjectDir) {
    Write-Warning "Katalog projektu już istnieje! $ProjectDir"
    exit
}

New-Item -ItemType Directory -Path $ProjectDir -Force | Out-Null
New-Item -ItemType Directory -Path $AgentsDir -Force | Out-Null

# 2. Tworzenie fizycznego pliku AGENTS.md z szablonu
$AgentsContent = @"
# Reguly Projektu: $Name

## Opis Projektu
- **Nazwa:** $Name
- **Typ:** $Type
- **Technologia:** [np. Python, Next.js, HTML/CSS]
- **Cel:** [Krotki opis celu projektu]

## Instrukcje dla Agentow
1. Zawsze przestrzegaj petli pamieci w pliku \`.agents/00_memory_loop.md\`.
2. Do konfiguracji LLM i API uzywaj wylacznie pliku \`.env\` w glownym folderze tego projektu.
3. Zachowaj pelna tozsamosc marki Ghost Tomasz (szczegoly w \`.agents/skills/ghost/SKILL.md\`).
"@

Set-Content -Path "$AgentsDir\AGENTS.md" -Value $AgentsContent -Encoding UTF8

# 3. Tworzenie fizycznego pliku 00_memory_loop.md (Petla Pamieci)
$MemoryContent = @"
# Petla Pamieci Projektu: $Name

## Stan Aktualny
- **Cel Glowny:** Inicjalizacja projektu i okreslenie wymagan
- **Krok Obecny:** Konfiguracja struktury roboczej i asystentow AI
- **Kolejny Krok:** Pierwsza rozmowa z agentem w AntiGravity

## Historia Wdrozen i Decyzji
- **$((Get-Date).ToString("yyyy-MM-dd HH:mm")):** Inicjalizacja projektu za pomoca skryptu automatyzacji create_project.ps1. Podlaczenie centralnego sztabu Dyrektorow (SOP-ow) przez link symboliczny.
"@

Set-Content -Path "$AgentsDir\00_memory_loop.md" -Value $MemoryContent -Encoding UTF8

# 4. Tworzenie Symlinku do folderu centralnych umiejetnosci (skills)
$SkillsTarget = "$BaseDir\.agents\skills"
$SkillsLink = "$AgentsDir\skills"

Write-Host "Tworzenie linku symbolicznego do centralnych SOP-ow..." -ForegroundColor Yellow
New-Item -ItemType SymbolicLink -Path $SkillsLink -Target $SkillsTarget -Force | Out-Null

Write-Host "[OK] Projekt $Name zostal pomyslnie utworzony i zintegrowany z J(AI)SON OS!" -ForegroundColor Green
Write-Host "Lokalizacja: $ProjectDir" -ForegroundColor Green
