# Hermes Agent UI & Customization Ecosystem (SOP)

Zestawienie repozytoriów, narzędzi i opcji personalizacji dla Hermes Agent (aktualne od wersji v0.16.0). 
Wiedza zebrana na potrzeby przyszłych modyfikacji wizualnych i funkcjonalnych systemu.

## 🖥️ Gotowe repozytoria do Dashboardu (Web UI)
W ekosystemie Hermes Agent dostępnych jest kilka alternatywnych i oficjalnych interfejsów graficznych:

1. **Oficjalny wbudowany dashboard**: 
   - Od wersji v0.16.0 pełny panel webowy jest wbudowany bezpośrednio w rdzeń projektu. 
   - Możesz go uruchomić lokalnie komendą `hermes dashboard` w przeglądarce.
2. **EKKOLearnAI/hermes-web-ui**: 
   - Rozbudowany i bardzo popularny interfejs webowy oferujący zaawansowany Web Terminal, menedżer poświadczeń, logi oraz integrację z Docker Compose.
   - 🔗 [GitHub Repository](https://github.com/EKKOLearnAI/hermes-web-ui)
3. **nesquena/hermes-webui**: 
   - Kolejna popularna i często aktualizowana alternatywa ułatwiająca zarządzanie agentem z poziomu przeglądarki i telefonu.
   - 🔗 [GitHub Repository](https://github.com/nesquena/hermes-webui)
4. **Daniel-Parke/hermes-control-hub**: 
   - Centrum dowodzenia (Control Hub) do zarządzania zadaniami cron, sesjami i konfiguracją agentów bez używania CLI.

## 🎨 Skiny i motywy (Themes)
Zgodnie z dokumentacją systemu rozszerzeń *Extending the Dashboard*, Hermes wspiera dwa niezależne systemy personalizacji wizualnej:

1. **Dashboard Themes (Web UI)**: 
   - Są to pliki konfiguracji YAML zmieniające paletę kolorów, typografię oraz układ graficzny panelu webowego. 
   - **Instalacja**: Wystarczy umieścić pobrany/stworzony plik `.yaml` w katalogu `~/.hermes/dashboard-themes/`.
2. **CLI Skins**: 
   - System modyfikacji wyglądu interfejsu terminalowego (TUI), całkowicie odrębny od motywów przeglądarkowych.

🔗 **Dokumentacja**: [Extending the Dashboard](https://hermes-agent.nousresearch.com/docs/user-guide/features/extending-the-dashboard)

## 🔌 Pluginy i rozszerzenia
System wtyczek w Hermesie dzieli się na warstwę wizualną (UI) oraz logiczną (Backend oparty na FastAPI):

1. **outsourc-e/hermesworld**: 
   - Przykładowy i gotowy plugin do zainstalowania bezpośrednio przez zakładkę *Plugins* w dashboardzie.
2. **joeynyc/hermes-hud**: 
   - Terminalowy system monitorowania stanu "świadomości" agenta, analizujący jego pamięć i historię popełnianych błędów w czasie rzeczywistym.
3. **Rozszerzenia MCP (Model Context Protocol)**: 
   - Hermes v0.16.0 wspiera oficjalny katalog Nous-approved MCP catalog. Pozwala to na dynamiczne podpinanie zewnętrznych serwerów narzędziowych (np. integracja z bazami danych czy zewnętrznymi API) bezpośrednio z poziomu interfejsu Web UI.
