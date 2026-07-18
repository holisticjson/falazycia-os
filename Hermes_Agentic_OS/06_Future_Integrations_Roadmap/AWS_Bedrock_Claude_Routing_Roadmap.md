# Roadmapa Routing: AWS Bedrock (Anthropic Claude)

Obecnie Hermes jest spięty bezpiecznie (w sposób Low-Friction) z Google Cloud Vertex AI poprzez serwer LiteLLM. W niedalekiej przyszłości chcemy włączyć do tego inteligentnego routingu ("Smart Routing") modele Anthropic Claude hostowane na AWS Bedrock, dla których mamy już podniesione limity (Quotas).

## 1. Filozofia Rozbudowy (Zero-Breakage)
Rozbudowa *nie może* uszkodzić działającej magistrali do Google Vertex AI. Musimy wykorzystać istniejące już Proxy (LiteLLM), które idealnie radzi sobie z obsługą multicloud.

## 2. Roadmapa Wdrożenia:
1. **Wygenerowanie Poświadczeń AWS:** Utworzenie profilu w AWS IAM z dostępem `AmazonBedrockFullAccess`. Zapisanie Access Key oraz Secret Key.
2. **Aktualizacja LiteLLM Env:** Wstrzyknięcie zmiennych `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` oraz `AWS_REGION_NAME` w sposób bezpieczny (z pliku .env) na maszynie wirtualnej Hermesa.
3. **Modyfikacja `litellm_config.yaml`:**
   Dopisanie nowych bloków do routera:
   ```yaml
   - model_name: hermes-claude-fast
     litellm_params:
       model: bedrock/anthropic.claude-3-haiku-20240307-v1:0
       rpm: 1000

   - model_name: hermes-claude-think
     litellm_params:
       model: bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0
       rpm: 60
   ```
4. **Smart Routing i Fallbacki (Fail-over):**
   Ustawienie Claude 3.5 Sonnet jako głownego mózgu deweloperskiego, z płynnym fallbackiem na Gemini 2.5 Pro w przypadku błędu rate-limitingu (429):
   ```yaml
   router_settings:
     fallbacks:
       - hermes-claude-think: [hermes-think]
   ```
5. **Edukacja Bota:** Dodanie do `Hermes Model Routing Instructions` wiedzy o tym, do czego służą nowo wpięte modele Claude (np. wyjątkowe umiejętności w kodowaniu, analizie tekstu literackiego), by wewnętrzny koordynator Hermes wywoływał je bezbłędnie.
