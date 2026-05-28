import requests
import json

def list_models():
    api_key = "ABSKQmVkcm9ja0FQSUtleS1jYTF0KzEtYXQtNDg1NjE3NTUzMjMxOjA2RjVFOXZucEpuL2hFWHdoSFdHODlGdmhmNWRvWjVMQW52bzBMcTFkb2Z6SkhiVUZ6emFCcVVQdzBZPQ=="
    region = "eu-central-1"
    
    # Try listing foundation models
    url = f"https://bedrock.{region}.amazonaws.com/foundation-models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print(f"--- Pobieram liste modeli w regionie {region} ---")
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            models = response.json().get("modelSummaries", [])
            print(f"--- Znaleziono {len(models)} modeli ---")
            for m in models:
                if "claude" in m['modelId'].lower():
                    print(f"ID: {m['modelId']} ({m.get('modelName')})")
        else:
            print(f"--- Blad {response.status_code} ---")
            print(response.text)
    except Exception as e:
        print(f"--- Wyjatek: {str(e)}")

if __name__ == "__main__":
    list_models()
