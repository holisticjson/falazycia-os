# 🤖 Prompt dla Asystenta Przeglądarkowego COMED (Opcja B - Hosting)

Skopiuj poniższy prompt i wklej go do swojego asystenta przeglądarkowego COMED (np. Claude/Gemini z wtyczką przeglądarkową lub dedykowanego agenta E2E), aby zautomatyzować setup kont.

---

### PROMPT DO SKOPIOWANIA:

```markdown
Jesteś zaawansowanym asystentem automatyzacji przeglądarkowej (E2E Browser Agent). Twoim zadaniem jest zalogowanie się do panelu hostingu Hostido oraz automatyczne utworzenie kont pocztowych i haseł aplikacji WordPress dla 4 domen klienckich.

#### 🔐 DANE LOGOWANIA DO HOSTINGU (Użyj tych danych do wejścia do panelu):
- **Panel Hostido URL:** https://panel.hostido.pl (lub bezpośredni URL do DirectAdmin/cPanel podany przez użytkownika)
- **Login/E-mail:** [UŻYJ DANYCH Z PLIKU .env LUB WPISZ RĘCZNIE] (Hostido FTP User: deploy@holistycznybroker.pl)
- **Hasło:** [UŻYJ DANYCH Z PLIKU .env LUB WPISZ RĘCZNIE] (Hostido FTP Pass: Qwerty!!@@1234)

#### 🌐 DOMENY DOCELOWE:
1. coolfon.pl
2. viptransporter.pl
3. smartrade.pl
4. kurczakujasia.pl

---

### 🛠️ KROKI DO WYKONANIA DLA KAŻDEJ Z 4 DOMEN:

#### KROK 1: Tworzenie Konta E-mail
1. Przejdź do zakładki **Konta E-mail / Konta Pocztowe** (Email Accounts) w panelu Hostido dla wybranej domeny.
2. Kliknij **Utwórz / Dodaj konto pocztowe**.
3. Ustaw parametry:
   - **Nazwa użytkownika (Email):** `agent` (pełny e-mail to: `agent@nazwa_domeny.pl`)
   - **Hasło:** Wygeneruj silne, losowe hasło (np. 16 znaków, litery, cyfry, znaki specjalne). Zapisz je!
   - **Limit pojemności (Quota):** Nielimitowany lub 2GB.
4. Kliknij **Utwórz / Zapisz**.

#### KROK 2: Logowanie do WordPress i Generowanie Hasła Aplikacji
1. Znajdź w panelu hostingu sekcję **WordPress** (np. WordPress Toolkit / Softaculous / WordPress Manager) i użyj opcji **Zaloguj automatycznie** (One-click Login) jako Administrator do panelu `/wp-admin` danej domeny.
   *Alternatywnie:* Jeśli automatyczne logowanie nie jest dostępne, przejdź na `https://[nazwa_domeny.pl]/wp-admin` i użyj danych administratora podanych przez użytkownika.
2. W panelu WordPress przejdź do: **Użytkownicy -> Profil** (Users -> Profile) lub **Użytkownicy -> Dodaj nowego** (jeśli chcesz stworzyć dedykowanego użytkownika):
   - Stwórz nowego użytkownika (jeśli nie istnieje):
     - **Nazwa użytkownika:** `Holistic OS Agent`
     - **E-mail:** `agent@[nazwa_domeny.pl]`
     - **Rola:** Administrator
3. Edytuj profil użytkownika `Holistic OS Agent` (lub profil aktualnego administratora) i zjedź na sam dół do sekcji **Hasła aplikacji** (Application Passwords).
4. Wpisz nazwę nowego hasła: `Holistic OS Agent Key`.
5. Kliknij przycisk **Dodaj nowe hasło aplikacji** (Add New Application Password).
6. **SKOPIUJ I ZAPISZ** wygenerowany 24-znakowy klucz (ma format `xxxx xxxx xxxx xxxx`).

---

### 📊 RAPORT KOŃCOWY:
Po zakończeniu operacji dla wszystkich 4 domen, wygeneruj tabelę podsumowującą w formacie Markdown zawierającą:

| Domena | Utworzony E-mail | Hasło E-mail | WordPress Login | Hasło Aplikacji (WP Application Password) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| coolfon.pl | `agent@coolfon.pl` | `[Hasło]` | `Holistic OS Agent` | `xxxx xxxx xxxx xxxx` | Sukces / Błąd |
| viptransporter.pl | `agent@viptransporter.pl`| `[Hasło]` | `Holistic OS Agent` | `xxxx xxxx xxxx xxxx` | Sukces / Błąd |
| smartrade.pl | `agent@smartrade.pl` | `[Hasło]` | `Holistic OS Agent` | `xxxx xxxx xxxx xxxx` | Sukces / Błąd |
| kurczakujasia.pl| `agent@kurczakujasia.pl` | `[Hasło]` | `Holistic OS Agent` | `xxxx xxxx xxxx xxxx` | Sukces / Błąd |

Rozpocznij automatyzację od zalogowania się na panel Hostido. Raportuj postęp po każdej domenie.
```
