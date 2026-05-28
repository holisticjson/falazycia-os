import boto3
import json
import time
import random
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

# Ładujemy klucze z pliku .env
load_dotenv()

def call_bedrock_robust(prompt, model_id="anthropic.claude-opus-4-7", max_retries=10):
    """
    Pancerny Agent Bedrock - obsługuje Throttling (429) z wykładniczym backoffem.
    Używa oficjalnego SDK boto3 i kluczy IAM.
    """
    
    # Inicjalizacja klienta Bedrock Runtime
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1"
    )
    
    client = session.client("bedrock-runtime")

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    })

    for attempt in range(max_retries):
        try:
            response = client.invoke_model(
                modelId=model_id,
                body=body
            )
            
            response_body = json.loads(response.get("body").read())
            return response_body.get("content", [{}])[0].get("text", "")

        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            
            # Jeśli przekroczono limity (429)
            if error_code in ["ThrottlingException", "429"]:
                wait_time = (2 ** attempt) + (random.uniform(0, 1))
                print(f"--- [!] Limit Bedrock przekroczony ({error_code}). Próba {attempt+1}/{max_retries}. Czekam {wait_time:.2f}s... ---")
                time.sleep(wait_time)
                continue
            else:
                # Inne błędy (np. brak dostępu do modelu)
                print(f"--- [X] Błąd AWS: {e} ---")
                break
                
        except Exception as e:
            print(f"--- [X] Nieoczekiwany błąd: {str(e)} ---")
            break
            
    return None

if __name__ == "__main__":
    # Test działania
    test_prompt = "Wymień 3 kluczowe zasady pracy głębokiej (Deep Work) dla osoby z ADHD."
    print("--- [START] Zapytanie do Pancernego Agenta ---")
    
    start_time = time.time()
    response = call_bedrock_robust(test_prompt)
    end_time = time.time()

    if response:
        print(f"\n[SUKCES] Odpowiedź Claude (czas: {end_time - start_time:.2f}s):\n")
        print(response)
    else:
        print("\n[PORAŻKA] Nie udało się uzyskać odpowiedzi po wszystkich próbach.")
