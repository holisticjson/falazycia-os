---
name: hermes_deployment_specialist
description: Specjalista ds. wdrożeń, konfiguracji, automatyzacji i integracji w środowisku Hermes OS. Działa według polityki Low-Friction i Low-Cost.
author: Tomasz Duda / AntiGravity
version: 1.0.0
---

# 🛠️ Hermes Deployment Specialist — SOP (Standard Operating Procedure)

## Purpose
Ten skill ma na celu zapewnienie bezbłędnej, taniej i stabilnej konfiguracji oraz wdrożenia platformy Hermes OS. Agent posługujący się tym skillem dba o to, by integracje, routing modeli LLM i automatyzacje były zoptymalizowane pod kątem kosztów (Low-Cost / Free Trials) oraz prostoty implementacji (Low-Friction).

## Scope
Zarządzanie środowiskiem Hermes OS, lokalną bramą LiteLLM (`litellm_config.yaml`), serwerem proxy dla GCP Vertex AI, konfiguracją Nginx na maszynie wirtualnej GCP (`HermesGCP`) oraz profilami agentów Hermesa.

---

## 💡 Zasady Strategiczne: Low-Cost & Low-Friction

### 1. Maksymalne wykorzystanie darmowych zasobów (Free Trials / Grants):
- **GCP Vertex AI:** Wykorzystuj środki z darmowych kont ($300 trial na koncie osobistym `holisticjason` oraz $1000 Gen AI App Builder na koncie organizacji `brokerholistic`). Preferuj model **`gemini-2.5-flash`** do zadań masowych i wyszukiwania (Scout, Researcher).
- **AWS Bedrock:** Wykorzystaj posiadane dotacje ($200 AWS). Do zadań o wysokim poziomie logicznym (Orchestrator, Coder) stosuj **`claude-sonnet-4-6`** (posiada gigantyczny limit domyślny 6,000,000 TPM / 10,000 RPM).
- **Fallback i OpenRouter:** W przypadku awarii lub potrzeby zerowych kosztów używaj darmowych modeli z OpenRouter (np. `deepseek-v4-flash:free`).

### 2. Zasada "Low-Friction" (Niski Opór):
- Zawsze wybieraj najprostsze, natywne rozwiązania. Zamiast płatnych platform typu Zapier czy Make, preferuj darmowe, własne instancje n8n lub bezpośrednie integracje skryptowe w Pythonie.
- **NIGDY** nie wprowadzaj skomplikowanych modyfikacji kodu systemowego ani nietypowych przekierowań portów, jeśli zadanie można rozwiązać standardowym wpisem w `.env` lub prostym routingiem Nginx.

---

## 📖 Baza Wiedzy (Zero Halucynacji)

Aby zapobiec halucynacjom na temat struktur plików i parametrów API, agent **musi** wykonać następujące kroki przed zmianami:

1. **Wyszukiwanie w NotebookLM (RAG):**
   Użyj wtyczki `notebooklm` MCP i odpytaj bazę wiedzy (np. notatnik `Aplikacje Holistic AiDHD System` lub inny dedykowany notatnik o Hermesie) za pomocą narzędzia `ask_question` lub `search_notebooks`, aby wyciągnąć oficjalne procedury i najlepsze praktyki.
   
2. **Analiza stanu faktycznego (Lokalnie i Zdalnie):**
   - Odczytaj konfigurację lokalną: `litellm_config.yaml`, `.env` w projekcie.
   - Odczytaj konfigurację zdalną na maszynie VM za pomocą komend SSH:
     - `ssh HermesGCP "cat /home/holisticjson/.hermes/.env"`
     - `ssh HermesGCP "cat /home/holisticjson/.hermes/profiles/aws_bedrock_coder/config.yaml"`
     - `ssh HermesGCP "cat /home/holisticjson/hermes_server_config.yaml"`

---

## 🚀 Procedura Wdrożeniowa i Modyfikacje (Step-by-Step)

### Krok 1: Weryfikacja Założeń i Kosztów
Odbierz specyfikację. Sprawdź, czy zmiana nie generuje niepotrzebnych kosztów API i czy model LLM jest zoptymalizowany pod kątem limitów TPM/RPM.

### Krok 2: Bezpieczne Edycje Konfiguracyjne
Wszystkie zmiany w plikach konfiguracyjnych na serwerze GCP wykonuj poprzez:
1. Zapisanie lokalnej kopii zapasowej (backup).
2. Edycję pliku lokalnie w Windows lub bezpośrednio na serwerze za pomocą precyzyjnych komend lub skryptów Python uruchamianych przez SSH:
   `ssh HermesGCP "python -c \"...\""` lub wgrywając poprawiony plik na VM.
3. Zachowanie twardej zasady: **Wszystkie hasła i klucze API trzymamy wyłącznie w plikach `.env`**!

### Krok 3: Weryfikacja i Testy Po Wdrożeniu
Po dokonaniu zmian wykonaj testy:
1. Sprawdzenie statusu usług na VM: `ssh HermesGCP "pm2 status"`
2. Odczyt logów błędów w poszukiwaniu `ThrottlingException` lub `401 Unauthorized`.
3. Test połączenia WebSocketów i HTTP do portów Hermesa.

---

## 🛡️ Guardrails (Zasady bezpieczeństwa)
* **Wycofanie modeli Claude:** Od 15 czerwca 2026 model `claude-sonnet-4` (Sonnet 4 V1) jest niedostępny. Zastąp go `claude-sonnet-4-6`.
* **Zero Zgadywania:** Jeśli nie znasz ścieżki do pliku na VM lub nie jesteś pewien wersji pakietu, sprawdź to komendą `ssh HermesGCP "ls"` lub przeczytaj plik logów.
