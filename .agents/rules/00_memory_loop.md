# **Protokół Pętli Pamięci: Closed-Loop State [Always On]**

Ten dokument definiuje żelazny mechanizm ciągłości pracy i pamięci w ekosystemie Jaison. Każdy agent przed przystąpieniem do pracy oraz bezpośrednio po jej zakończeniu ma obowiązek wykonać kroki pętli pamięci.

---

## **Protokół "Closed-Loop State"**

### **1. Zawsze przed startem: Czytaj STATE.md**
*   **Wymóg:** Zanim napiszesz choćby linijkę kodu, uruchomisz komendę lub zaproponujesz rozwiązanie, **musisz wczytać plik `STATE.md`** (oraz `WORKSPACE_MEMORY.md` lub `profil.txt` jeśli istnieją w danym module).
*   **Cel:** Uniknięcie błądzenia po omacku. Musisz wiedzieć, na czym stanęły prace, jaki jest aktualny status wdrożenia i co jest obecnie wąskim gardłem. Zero zgadywania.

### **2. Zawsze po pracy: Aktualizuj STATE.md**
*   **Wymóg:** Natychmiast po zakończeniu sesji, wykonaniu zadania lub naprawieniu błędu, **zaktualizuj plik `STATE.md`**.
*   **Co wpisać (krótko, zwięźle, w punktach):**
    *   **Logi i status:** Co realnie zostało zrobione i jaki jest obecny stan systemu.
    *   **Infrastruktura:** Wszelkie zmiany w zasobach chmurowych (GCP, Cloud Run, GCS, bazy danych) oraz zmiennych środowiskowych `.env`.
    *   **Next Action (ADHD-Optimal):** Jeden, maksymalnie dwa konkretne i mierzalne kroki, które należy wykonać w następnej kolejności.

### **3. Pętla Utrwalania Wiedzy (SOP Loop)**
*   **Logika:** Jeśli podczas pracy zderzyłeś się z błędem technicznym (np. problem z uwierzytelnieniem w GCP, błąd bibliotek Streamlit, wysypany kontener, limity API) i go naprawiłeś — **nie zostawiaj tego tylko dla siebie**.
*   **Działanie:** Przełóż rozwiązanie na łopatologiczną, prostą instrukcję krok po kroku i dopisz ją do pliku SOP (Standard Operating Procedure) w odpowiednim katalogu `.agents/skills/` lub `.agents/rules/`.
*   **Zasada:** *Raz popełniony i naprawiony błąd nigdy więcej nie ma prawa się powtórzyć.*

---

## **Szybka Checklista Końca Sesji**
- [ ] Czy zaktualizowałem `STATE.md` o zmiany i logi?
- [ ] Czy określiłem jasny `Next Action` dla Tomasza lub kolejnego agenta?
- [ ] Czy spisałem instrukcję naprawy błędu (SOP), jeśli na jakiś natrafiłem?
- [ ] Czy usunąłem pliki tymczasowe i śmieci (zgodnie z zasadą sprzątania)?

*Działaj spójnie z tym protokołem. Czysta pamięć to czysty zysk i zero marnowania czasu.*
