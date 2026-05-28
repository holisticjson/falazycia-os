import requests
import json
import os

def test_bedrock():
    api_key = "ABSKQmVkcm9ja0FQSUtleS1jYTF0KzEtYXQtNDg1NjE3NTUzMjMxOjA2RjVFOXZucEpuL2hFWHdoSFdHODlGdmhmNWRvWjVMQW52bzBMcTFkb2Z6SkhiVUZ6emFCcVVQdzBZPQ=="
    region = "eu-central-1"
    model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
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
                "content": "Cześć, jeśli mnie słyszysz, odpowiedz krótko: 'System Bedrock aktywny!'"
            }
        ]
    }

    print(f"--- Wysylam zapytanie do {model_id} w regionie {region} ---")

    try:
        response = requests.post(url, headers=headers, json=payload, verify=False) # verify=False bypasses the SSL issue for testing
        if response.status_code == 200:
            result = response.json()
            answer = result.get("content", [{}])[0].get("text", "Brak tekstu w odpowiedzi")
            print(f"--- Sukces! Odpowiedz Claude: {answer}")
        else:
            print(f"--- Blad: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"--- Wyjatek: {str(e)}")

if __name__ == "__main__":
    test_bedrock()
