# Modyfikacja UI & Hermes Studio (v0.16.0+)

Wersja **Hermes v0.16.0** wprowadza potężne zmiany: Desktop GUI, nowy Dashboard oraz wbudowany Leaner Skillset. W związku z tym, podejście do customizacji "Agencji Marketingowej" na side-barze musi być nowoczesne i **Low-Friction**.

## 1. Strategia Modyfikacji (Zamiast Brutalnego Forka)
Zamiast "twardego" forkowania i ręcznej modyfikacji kodu (co niszczy ścieżkę łatwych aktualizacji), naszą główną procedurą jest **Deep Research** i wykorzystanie natywnych rozwiązań platformy Hermes:
1.  **Analiza API / Pluginów**: Sprawdzamy na oficjalnym GitHubie, dokumentacji i materiałach społeczności (np. Nose Portal Agent Search), czy Hermes v0.16.0 udostępnia punkty zaczepienia (Hooks / Plugins) do wstrzykiwania własnych zakładek (np. iframe lub dedykowanych Web-Views).
2.  **Dashboard Extensions**: Jeżeli Hermes pozwala definiować "Custom Views" w konfiguracji, nasz moduł agencji powstanie jako niezależna mini-aplikacja, linkowana z poziomu nawigacji Hermesa.

## 2. Architektura Subdomen (Proxy & Bezpieczeństwo)
*   Nowe warstwy bezpieczeństwa z v0.16.0 dla GUI mogą wymagać odpowiedniego routingu w Nginx.
*   Zawsze używamy rewersyjnego proxy (Nginx / Caddy), aby wystawić interfejs na dedykowanej subdomenie klienta: `os.holisticjson.pl` lub `os.[domenaklienta].pl`.
*   Aplikujemy dodatkowe zabezpieczenia (OAuth, HTTP Basic Auth na ścieżki krytyczne, restrykcje IP), jeśli wbudowane w Hermesa nie są wystarczające dla danego planu usługowego B2B.

## 3. Integracja "Julian Goldie Style" (Claude Code, Gemini)
*   Darmowe instancje kodu Claude (lub Claude App Code) spinamy z Hermesem jako dedykowane narzędzia.
*   Moduł agencji może wywoływać CLI Claude w tle, a statusy przepychać do GUI Hermesa.
*   Hermes ma być tu "Mózgiem" rozdzielającym taski pomiędzy dostępne terminale (np. okienko Claude, kodowanie w oknie głównym) poprzez wewnętrzne Skills.
