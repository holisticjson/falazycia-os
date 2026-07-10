# Standard Bezpiecznej Migracji i Refaktoryzacji (Safe Migration & Refactoring Standard)

Podczas przenoszenia plików, zmiany struktury katalogów oraz aktualizowania kodu źródłowego, agenci AI muszą przestrzegać rygorystycznych procedur bezpieczeństwa, aby uniknąć uszkodzenia działających integracji, utraty danych lub przerwania działania środowisk produkcyjnych.

## Procedura Krok po Kroku (Migration Protocol)
1. **Analiza Zależności (Dependency Discovery):** Przed jakąkolwiek zmianą lokalizacji pliku, należy wykonać pełne wyszukiwanie tekstowe (grep) w całym obszarze roboczym, aby zidentyfikować wszystkie skrypty i konfiguracje, które odwołują się do tego pliku/folderu.
2. **Kompilacja i Testy (Verification):** Każdy zmodyfikowany skrypt Python musi zostać skompilowany testowo za pomocą polecenia `python -m py_compile <sciezka_pliku>`, aby upewnić się, że nie zawiera błędów składniowych wywołanych refaktoryzacją.
3. **Zasada Nienaruszalności Nazw:**
   - Folder `.agents/` (liczba mnoga) **NIGDY** nie może zostać przemianowany na `.agent/` (liczba pojedyncza), ponieważ spowoduje to trwałą utratę dostępu asystentów AI do ich umiejętności systemowych.
   - Folder `11_digital_product/` **MUSI** pozostać bezpośrednio w roocie repozytorium ze względu na zewnętrzne zależności systemowe.
4. **Strategia Rollback i Backupów:**
   - W przypadku nadpisywania istniejących plików konfiguracyjnych, system musi automatycznie wygenerować kopię zapasową o nazwie `<nazwa_pliku>_backup.<rozszerzenie>`.
   - Wszelkie destrukcyjne operacje (usuwanie nienależących do nas danych lub usuwanie dużych folderów) wymagają jednoznacznej, tekstowej zgody użytkownika.
5. **Autoryzacja (Zero-Guessing):** Przed uruchomieniem jakichkolwiek skryptów chmurowych (GCP, Firebase), skrypt lub agent musi sprawdzić istnienie i poprawność kluczy autoryzacyjnych w `.env` lub domyślnych poświadczeń GCP Application Default Credentials, zamiast rzucać surowymi wyjątkami w runtime.
