# 🛡️ ZASADA IZOLACJI ŚRODOWISK (SOP DLA AGENTÓW AI)
*Standard Bezpieczeństwa i Eliminacji Halucynacji — Jaison OS v9.0*

---

## 👨‍💻 BEZWZGLĘDNA REGUŁA PRACY (DLA KAŻDEGO AGENTA):
Każdy agent AI przydzielony do pracy nad konkretnym projektem klienta (np. <strong>Coolfon</strong>, <strong>Kurczak u Jasia</strong>, <strong>VIPTransporter</strong>) lub projektem pobocznym (np. <strong>LifeWave MLM</strong>) ma <strong>kategoryczny zakaz</strong> odpytywania, czytania lub modyfikowania centralnego pliku `.env` agencji (znajdującego się w `/01_JAISON_AGENCY_OS/.env`).

Wszystkie operacje, zmienne środowiskowe, dostępy FTP oraz klucze API <strong>muszą</strong> być pobierane wyłącznie z lokalnego pliku `.env` znajdującego się bezpośrednio w folderze danego projektu.

---

## 🎯 Uniwersalny Prompt do Wklejenia Agentowi (System Guidelines)

Jeśli zlecasz zadanie agentowi (np. Antigravity, Claude lub innemu sub-agentowi) w projekcie klienta, wklej mu ten prompt na samym początku konwersacji:

```markdown
Pracujesz teraz w odizolowanym środowisku projektu klienta. 
Twoim katalogiem roboczym (CWD) jest folder projektu (np. /02_CLIENTS_AND_PROJECTS/[nazwa_klienta]/).

Złote zasady bezpieczeństwa, których musisz bezwzględnie przestrzegać:
1. Wszystkie zmienne środowiskowe (klucze API, hasła do WordPress, dane FTP, połączenia bazy danych) wczytuj WYŁĄCZNIE z lokalnego pliku `.env` w Twoim folderze roboczym.
2. Pod żadnym pozorem nie szukaj kluczy w folderze `/01_JAISON_AGENCY_OS/.env` ani wyżej. Jeżeli lokalny plik `.env` nie istnieje lub brakuje w nim kluczy, stwórz go na bazie szablonu `.env.example` i wyświetl użytkownikowi czytelny komunikat, o jakie klucze musi go uzupełnić.
3. Kategorycznie zabrania się wykonywania operacji na zasobach agencji (np. robienia deployu na główne serwery Jaison, modyfikowania bazy danych brokera). Twój zasięg działania jest ograniczony wyłącznie do zasobów i serwerów zdefiniowanych w Twoim lokalnym `.env`.
4. Przed wywołaniem jakiegokolwiek połączenia (FTP, REST API) zweryfikuj poprawność lokalnych danych autoryzacyjnych. W razie błędów autoryzacji (np. błędne hasło aplikacji WP) wyświetl czytelną, maszynowo sprawną instrukcję w UI, co Tomasz musi poprawić.
```

---

## 📋 Szablon `.env.example` dla Projektów Klientów

W folderze każdego klienta (np. `/02_CLIENTS_AND_PROJECTS/coolfon/`, `/02_CLIENTS_AND_PROJECTS/kurczakujasia/` itp.) tworzymy standardowy szablon `.env.example`, który wskazuje agentowi, jakie parametry są mu dozwolone:

```env
# ==============================================================================
# LOKALNA KONFIGURACJA PROJEKTU KLIENTA
# Skopiuj ten plik do .env i uzupełnij prawdziwymi danymi.
# Agent AI ma prawo korzystać WYŁĄCZNIE z poniższych zmiennych.
# ==============================================================================

# Autoryzacja WordPress REST API
WP_URL=https://nazwa-klienta.pl
WP_USER=Holistic OS Agent
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx

# Dostęp FTP do serwera produkcyjnego klienta (np. Hostido/DirectAdmin)
FTP_HOST=ftp.nazwa-klienta.pl
FTP_USER=ftp_username
FTP_PASS=ftp_secure_password
FTP_PORT=21
FTP_REMOTE_DIR=/public_html

# Lokalne specyficzne klucze (np. asystent zamówień, bot WhatsApp)
LOCAL_BOT_TOKEN=your_telegram_or_whatsapp_token
LOCAL_DATABASE_URL=sqlite:///local_data.db
```

---

## 🔧 Jak sprawdzić i wyczyścić obecne pliki `.env`?

1. <strong>Przejrzyj lokalny `.env`</strong>: Otwórz dany plik `.env` (np. w folderze Coolfona).
2. <strong>Usuń zbędne klucze</strong>: Jeśli w lokalnym `.env` klienta znajdziesz klucze agencji (np. `GEMINI_API_KEY` Twojego głównego konta, hasła FTP do `jaison.pl` itp.), <strong>natychmiast je usuń</strong>. Agent klienta ma używać lokalnego WordPress REST API i lokalnego FTP klienta.
3. <strong>Zastąp je zmiennymi klienta</strong>: Wpisz tam dane dedykowane dla tej konkretnej strony.

Dzięki temu eliminujemy jakiekolwiek ryzyko halucynacji i gwarantujemy 100% szczelność danych agencji!
