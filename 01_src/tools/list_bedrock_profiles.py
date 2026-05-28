import requests
import json

def list_profiles():
    api_key = "ABSKQmVkcm9ja0FQSUtleS1jYTF0KzEtYXQtNDg1NjE3NTUzMjMxOjA2RjVFOXZucEpuL2hFWHdoSFdHODlGdmhmNWRvWjVMQW52bzBMcTFkb2Z6SkhiVUZ6emFCcVVQdzBZPQ=="
    region = "eu-central-1"
    
    url = f"https://bedrock.{region}.amazonaws.com/inference-profiles"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    print(f"--- Pobieram liste profilów w regionie {region} ---")
    try:
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            profiles = response.json().get("inferenceProfileSummaries", [])
            print(f"--- Znaleziono {len(profiles)} profilów ---")
            for p in profiles:
                print(f"Profile: {p['inferenceProfileName']} | ID: {p['inferenceProfileId']}")
        else:
            print(f"--- Blad {response.status_code} ---")
            print(response.text)
    except Exception as e:
        print(f"--- Wyjatek: {str(e)}")

if __name__ == "__main__":
    list_profiles()
