import requests
import json

api_key = 'AQ.Ab8RN6Icx0WTaJPGqSVUpcHqrLoGL8X_b9RPtV7uq1xwiNOPAg'

models = ['gemini-3.5-flash', 'gemini-3.1-pro', 'gemini-2.5-flash', 'gemini-1.5-flash']

# 1. Test Gemini Developer API endpoint (generativelanguage)
print("=== Testing Google AI Studio / Gemini API endpoint ===")
for model in models:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": "Say hello in one word."}]
        }]
    }
    print(f"Testing model {model}...")
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        print(f"  Status code: {res.status_code}")
        if res.status_code == 200:
            print(f"  SUCCESS: {res.json()['candidates'][0]['content']['parts'][0]['text'].strip()}")
        else:
            print(f"  FAILED: {res.text[:300]}")
    except Exception as e:
        print(f"  Error: {e}")

# 2. Test Agent Platform API / Vertex API key endpoint
print("\n=== Testing Agent Platform API (Vertex) with API Key ===")
# Agent Platform API endpoint for API Key typically routes through Vertex AI
# We will check if it can be accessed
for model in models:
    # Example Vertex endpoint with API Key
    # https://us-central1-aiplatform.googleapis.com/v1/projects/holistic-broker/locations/us-central1/publishers/google/models/gemini-2.5-flash:generateContent?key=...
    url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/holistic-broker/locations/us-central1/publishers/google/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": "Say hello in one word."}]
        }]
    }
    print(f"Testing Vertex model {model}...")
    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        print(f"  Status code: {res.status_code}")
        if res.status_code == 200:
            print(f"  SUCCESS: {res.json()['candidates'][0]['content']['parts'][0]['text'].strip()}")
        else:
            print(f"  FAILED: {res.text[:300]}")
    except Exception as e:
        print(f"  Error: {e}")
