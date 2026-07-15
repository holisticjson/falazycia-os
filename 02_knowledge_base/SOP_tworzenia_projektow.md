# 🚀 SOP: Automatyczne Tworzenie i Integracja Projektów (J(AI)SON OS)

Niniejszy dokument definiuje standard operacyjny (SOP) oraz automatyzację tworzenia nowych projektów klienckich oraz aplikacji w środowisku **AntiGravity / J(AI)SON OS** przy użyciu architektury hybrydowej (fizyczne pliki konfiguracyjne + centralne symlinki do sztabu dyrektorów).

---

## 🛠️ 1. Narzędzie Automatyzacji: `create_project.ps1`

W roocie systemu (`C:\Aplikacje MVP\`) znajduje się skrypt **`create_project.ps1`**, który wykonuje całą pracę przygotowawczą w 1 sekundę.

### Co robi skrypt pod maską?
1. **Tworzy folder projektu** we właściwym miejscu:
   - Dla klientów (`-Type client`) ➡️ `C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\<Nazwa>`
   - Dla aplikacji (`-Type app`) ➡️ `C:\Aplikacje MVP\03_SOFTWARE_AND_APPS\<Nazwa>`
2. **Tworzy fizyczny plik `.agents/AGENTS.md`** z unikalnym szablonem do opisania specyfiki klienta (technologia, cele, stack).
3. **Tworzy fizyczny plik `.agents/00_memory_loop.md`** (Pętla Pamięci), inicjalizując go z poprawną datą i pierwszą decyzją.
4. **Tworzy Link Symboliczny (Symlink)** z lokalnego `.agents/skills` do centralnej bazy wiedzy `C:\Aplikacje MVP\.agents\skills`. 
   > Dzięki temu wszyscy Twoi Dyrektorzy (CEO, CTO, CMO, CFO itd.) oraz tożsamość Ghost są zawsze automatycznie aktualne i dostępne w każdym projekcie!

---

## 💻 2. Jak utworzyć nowy projekt? (Instrukcja dla Ciebie)

Gdy pozyskasz nowego klienta lub startujesz z nową aplikacją:

1. Otwórz **PowerShell jako Administrator** (wymagane do stworzenia symlinku systemowego).
2. Uruchom skrypt, podając nazwę projektu i jego typ:

#### Przykład 1: Nowy klient agencji (np. "Lombard Oranżada")
```powershell
Set-Location -Path "C:\Aplikacje MVP"
.\create_project.ps1 -Name "Lombard_Oranzada" -Type client
```

#### Przykład 2: Nowa własna aplikacja (np. "LiveWave")
```powershell
Set-Location -Path "C:\Aplikacje MVP"
.\create_project.ps1 -Name "LiveWave" -Type app
```

---

## 🔄 3. Synchronizacja Laptop 🔁 Stacjonarny

Dzięki temu, że reguły są spięte w gicie, po wykonaniu `git sync` (który teraz na obu komputerach działa automatycznie co 15 minut!):

1. **Nowy projekt (kod i lokalne ustawienia) automatycznie pojawi się na drugiej maszynie.**
2. Jedyne, co musisz zrobić na drugiej maszynie, to jednorazowo wywołać komendę PowerShell (jako Administrator), która odtworzy lokalny link symboliczny (Symlink) dla tego konkretnego projektu (gdyż Git nie przenosi fizycznie symlinków na Windowsie).
3. Aby ułatwić sobie życie, jeśli przenosisz projekt na laptopa, po prostu uruchom PowerShell jako Administrator i wklej tę komendę:
   ```powershell
   New-Item -ItemType SymbolicLink -Path "C:\Aplikacje MVP\<ŚCIEŻKA_PROJEKTU>\.agents\skills" -Target "C:\Aplikacje MVP\.agents\skills" -Force
   ```

---

## 🤖 4. Jak wprowadzić Agenta w AntiGravity do nowego projektu?

Gdy po raz pierwszy uruchamiasz czat w nowo utworzonym projekcie (np. przez "New Worktree"), wklej agentowi tę powitalną instrukcję startową:

> *"Cześć! Rozpoczynamy pracę nad nowym projektem. Wszystkie wytyczne, technologia i cele tego projektu znajdują się w pliku roboczym `.agents/AGENTS.md`.*
> 
> *Twoje zadania na start:*
> 1. *Przeanalizuj plik `.agents/AGENTS.md` oraz pętlę pamięci w `.agents/00_memory_loop.md`.*
> 2. *Zwróć uwagę, że masz pełen dostęp do centralnego sztabu Dyrektorów (SOP-ów) w `.agents/skills/` (w tym dyrektorów CMO, CFO, CTO oraz tożsamości Ghost).*
> 3. *Wprowadź się w kontekst, potwierdź zrozumienie założeń i zaproponuj pierwszy, konkretny krok techniczny w realizacji tego projektu."*

Dzięki temu agent od pierwszej sekundy działa na najwyższych obrotach, zachowując Twój elitarny standard jakości! 💪🔥🚀
