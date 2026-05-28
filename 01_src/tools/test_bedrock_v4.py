import requests
import json

def test_bedrock_v4():
    api_key = "ABSKQmVkcm9ja0FQSUtleS1jYTF0KzEtYXQtNDg1NjE3NTUzMjMxOjA2RjVFOXZucEpuL2hFWHdoSFdHODlGdmhmNWRvWjVMQW52bzBMcTFkb2Z6SkhiVUZ6emFCcVVQdzBZPQ=="
    region = "eu-central-1"
    model_id = "anthropic.claude-sonnet-4-20250514-v1:0"
    url = f"https://bedrock-runtime.{region}.amazonaws.com/model/{model_id}/invoke"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 100,
        "messages": [
            {
                "role": "user",
                "content": "Czesc, potwierdz prosze swoje dzialanie: 'System Bedrock Claude 4 aktywny!'"
            }
        ]
    }

    print(f"--- Wysylam zapytanie do {model_id} ---")
    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)
        if response.status_code == 200:
            result = response.json()
            answer = result.get("content", [{}])[0].get("text", "Brak tekstu")
            print(f"--- Sukces! Odpowiedz: {answer}")
        else:
            print(f"--- Blad {response.status_code} ---")
            print(response.text)
    except Exception as e:
        print(f"--- Wyjatek: {str(e)}")

if __name__ == "__main__":
    test_bedrock_v4()
