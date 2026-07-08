# Instrukcja Konfiguracji Integracji Hermes OS ze Slackiem (Od A do Z)

Ten dokument opisuje kompletny i sprawdzony proces konfiguracji integracji Hermes OS ze Slackiem. Instrukcja opiera się w 100% na realnym procesie debugowania i uruchamiania bramki komunikacyjnej w środowisku produkcyjnym GCP.

---

## Spis Treści
1. [KROK 1: Konfiguracja Aplikacji na api.slack.com](#krok-1-konfiguracja-aplikacji-na-apislackcom)
2. [KROK 2: Konfiguracja Środowiska i Plików na Serwerze GCP](#krok-2-konfiguracja-srodowiska-i-plikow-na-serwerze-gcp)
3. [KROK 3: Zarządzanie i Restart Bramki Hermes Gateway](#krok-3-zarzadzanie-i-restart-bramki-hermes-gateway)
4. [KROK 4: Testowanie i Weryfikacja Połączenia](#krok-4-testowanie-i-weryfikacja-polaczenia)

---

## KROK 1: Konfiguracja Aplikacji na api.slack.com

Konfiguracja odbywa się w oficjalnym panelu deweloperskim Slacka dla wybranej aplikacji (np. **Hermes OS**).

### A. Włączenie trybu Socket Mode (WebSocket)
Tradycyjne webhooki wymagają publicznego, certyfikowanego adresu HTTPS (Request URL). Hermes OS korzysta z **Socket Mode**, co pozwala na stabilne połączenie dwukierunkowe przez WebSockets bez wystawiania portów na świat.

1. Przejdź do zakładki **Settings** -> **Socket Mode** w lewym menu.
2. Przełącz opcję **Enable Socket Mode** na **ON** (zielony przełącznik).
3. Jeśli konfigurujesz to po raz premierowy, Slack poprosi Cię o wygenerowanie **App-Level Token** (zaczynającego się od `xapp-`).
   * Nadaj mu nazwę (np. `hermes-socket-mode`).
   * Dodaj wymagany zakres uprawnień: `connections:write`.
   * Zapisz ten token — to będzie Twój `SLACK_APP_TOKEN`.

### B. Konfiguracja Uprawnień Bot Token Scopes
W lewym menu wejdź w **Features** -> **OAuth & Permissions**. Zjedź na dół do sekcji **Scopes** -> **Bot Token Scopes** i upewnij się, że posiadasz dokładnie te uprawnienia:

| Uprawnienie (Scope) | Przeznaczenie |
| :--- | :--- |
| `app_mentions:read` | Reagowanie na wzmianki o bocie w kanałach (np. `@Hermes OS`) |
| `chat:write` | Wysyłanie wiadomości na kanały i w DMs |
| `im:read` | Odczytywanie wiadomości bezpośrednich (DMs) od użytkownika |
| `im:write` | Odpowiadanie użytkownikowi w wiadomościach bezpośrednich (DMs) |
| `channels:read` | Odczytywanie listy publicznych kanałów |
| `channels:manage` | Tworzenie/zarządzanie kanałami publicznymi |
| `groups:read` | **KLUCZOWE:** Odczytywanie listy prywatnych grup i kanałów (bez tego bramka zgłasza błąd `missing_scope` przy starcie) |
| `groups:write` | Odpowiadanie w prywatnych grupach |
| `files:write` | Wysyłanie plików (np. wygenerowanych raportów czy obrazów) |

> [!IMPORTANT]
> Token bota (`SLACK_BOT_TOKEN`, zaczynający się od `xoxb-`) znajdziesz na samej górze tej strony pod etykietą **Bot User OAuth Token**.

### C. Włączenie i Konfiguracja Event Subscriptions (Subskrypcji Zdarzeń)
Bez tego kroku Socket Mode połączy się poprawnie, ale Slack **nie będzie przesyłał żadnych wiadomości ani zdarzeń** do Twojego serwera.

1. Przejdź do **Features** -> **Event Subscriptions** w lewym menu.
2. Przełącz opcję **Enable Events** na **ON** (suwak zmieni kolor na zielony).
3. Zauważysz komunikat informujący, że Socket Mode jest aktywny:
   > *Socket Mode is enabled. You won't need to specify a Request URL.* (Pole Request URL pozostaje puste i jest nieaktywne).
4. Kliknij i rozwiń sekcję **Subscribe to bot events**.
5. Kliknij **Add Bot User Event** i dodaj dokładnie te 5 zdarzeń:
   * `app_mention` — reagowanie na oznaczenia bota na kanałach.
   * `message.im` — reagowanie na wiadomości bezpośrednie (Direct Messages).
   * `message.channels` — słuchanie wiadomości na kanałach publicznych.
   * `message.groups` — słuchanie wiadomości na kanałach prywatnych.
   * `message.mpim` — reagowanie na wieloosobowe wiadomości bezpośrednie.
6. Kliknij zielony przycisk **Save Changes** na samym dole ekranu.

### D. Reinstalacja Aplikacji w Workspace
Po zmianie uprawnień i subskrypcji zdarzeń Slack wymaga przeładowania konfiguracji:
1. U góry ekranu kliknij żółty pasek z linkiem **"reinstall your app"** (lub przejdź do **Settings** -> **Install App** i kliknij **Reinstall to Workspace**).
2. Zaakceptuj nowe uprawnienia na ekranie autoryzacji.
3. **Uwaga:** Tokens (`SLACK_BOT_TOKEN` oraz `SLACK_APP_TOKEN`) **NIE zmieniają się** przy reinstalacji. Nic nie musisz podmieniać na serwerze!

---

## KROK 2: Konfiguracja Środowiska i Plików na Serwerze GCP

Wszystkie zmienne logowania muszą zostać zapisane w plikach konfiguracyjnych na serwerze wirtualnym GCP (`hermes-os`).

### A. Zmienne Środowiskowe w plikach `.env`
Na serwerze te trzy zmienne muszą być identycznie skonfigurowane w plikach:
* `/home/holisticjson/.env`
* `/home/holisticjson/hermes-agent/.env`

Dodaj lub zaktualizuj poniższe klucze:
```env
SLACK_BOT_TOKEN=xoxb-1144461594...-twoj-pelny-token-bota
SLACK_APP_TOKEN=xapp-1-A0BCXFM2...-twoj-pelny-token-aplikacji
SLACK_SIGNING_SECRET=bee2b93f2c8f...-twoj-signing-secret
```

### B. Konfiguracja w `.hermes/config.yaml`
Główny plik konfiguracyjny agenta `/home/holisticjson/.hermes/config.yaml` automatycznie aktywuje platformę Slack, jeśli wykryje ustawioną zmienną środowiskową `SLACK_BOT_TOKEN`. Aby upewnić się, że zestaw narzędzi dla platformy Slack jest dostępny, w sekcji `platform_toolsets` pliku konfiguracyjnego musi istnieć wpis:

```yaml
platform_toolsets:
  slack:
    - hermes-slack
```

---

## KROK 3: Zarządzanie i Restart Bramki Hermes Gateway

Bramka Hermes Gateway uruchamiana jest jako niezależna usługa systemd w przestrzeni użytkownika. Po każdej zmianie konfiguracji uprawnień Slacka lub plików `.env` należy ją zrestartować.

### Komendy Konsoli (SSH):

#### 🔄 Restart bramki:
```bash
systemctl --user restart hermes-gateway
```

#### 🟢 Sprawdzenie statusu usługi:
```bash
systemctl --user status hermes-gateway
```

#### 📋 Podgląd logów na żywo (monitoring błędów):
```bash
journalctl --user -u hermes-gateway -f --no-pager
```

#### 🛑 Zatrzymanie bramki:
```bash
systemctl --user stop hermes-gateway
```

#### 🎬 Start bramki:
```bash
systemctl --user start hermes-gateway
```

---

## KROK 4: Testowanie i Weryfikacja Połączenia

Po restarcie bramki, w logach `journalctl` nie powinny pojawiać się żadne błędy ani ostrzeżenia typu `missing_scope` czy `failed to list Slack channels`.

### Jak przetestować działanie?
1. **Wiadomość Bezpośrednia (DM):** Wejdź w Slacku w zakładkę wiadomości bezpośrednich z **Hermes OS** i napisz cokolwiek, np. `Cześć Hermes, czy jesteś już gotowy?`.
2. **Wzmianka na Kanale (Mention):** Dodaj bota do dowolnego kanału (np. `#all-holistic-json`), wpisując `/invite @Hermes OS`, a następnie napisz: `@Hermes OS jaki jest nasz status?`.

W logach serwera zobaczysz błyskawicznie przepływ zdarzeń, a bot odpisze bezpośrednio na Twoim czacie!
