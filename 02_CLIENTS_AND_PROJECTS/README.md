# 📁 SILOS B: CLIENTS AND PROJECTS
> **Przeznaczenie:** Scentralizowany obszar obsługi klientów zewnętrznych agencji Jaison.

## 🚫 Czego NIE wolno robić pod-agentom w tym folderze:
1. **ZAKAZ wycieków danych (Kategoryczna Izolacja):** Pliki, logi i kody klienta A pod żadnym pozorem nie mogą być linkowane ani kopiowane do folderu klienta B. Dane są hermetycznie odizolowane.
2. **ZAKAZ wprowadzania zmian w infrastrukturze agencji:** Żaden skrypt deweloperski klienta nie może mieć uprawnień do edycji lub odczytu Silosu A (`01_JAISON_AGENCY_OS`).
3. **Zasada szablonu:** Każdy nowy klient projektowy musi być inicjowany wyłącznie poprzez skopiowanie struktury z katalogu `Szablon_Projektu/`.
