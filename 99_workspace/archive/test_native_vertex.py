import sys
import os
import ssl
import requests
import json
from google.oauth2 import service_account
import google.auth.transport.requests

# Disable SSL verification for local environment behind proxy/firewall
ssl._create_default_https_context = ssl._create_unverified_context
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("Starting native Vertex AI check...")

try:
    # 1. Load service account credentials with fallbacks
    sa_path = os.path.join(os.getcwd(), 'holistic-dashboard-dev-dea2c872139e.json')
    if not os.path.exists(sa_path):
        sa_path = '/home/holisticjson/.hermes/gcp-sa-key.json'
    if not os.path.exists(sa_path):
        sa_path = os.path.expanduser('~/.hermes/gcp-sa-key.json')
        
    print(f"Loading service account credentials from: {sa_path}")
    creds = service_account.Credentials.from_service_account_file(
        sa_path,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    
    session = requests.Session()
    session.verify = False
    request = google.auth.transport.requests.Request(session=session)
    print("Refreshing Google OAuth token...")
    creds.refresh(request)
    print("Token refreshed successfully!")

    project_id = "holistic-dashboard-dev"
    region = "us-central1"
    
    models = [
        "gemini-1.5-flash-002",
        "gemini-1.5-flash-001",
        "gemini-1.5-pro-002",
        "gemini-1.5-pro-001",
        "gemini-1.0-pro-002",
        "gemini-1.0-pro-001",
        "gemini-2.0-flash-001",
        "gemini-2.5-flash",
    ]
    
    success = False
    for model in models:
        # Native Vertex AI URL
        url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/publishers/google/models/{model}:generateContent"
        print(f"\nTesting model: {model} at URL: {url}")
        
        headers = {
            "Authorization": f"Bearer {creds.token}",
            "Content-Type": "application/json"
        }
        
        # Native Gemini payload
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {"text": "Say 'OK' in one word."}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 10
            }
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, verify=False, timeout=10.0)
            print(f"Result code: {response.status_code}")
            if response.status_code == 200:
                print(f"SUCCESS for {model}!")
                print(response.json())
                success = True
                break
            else:
                print(f"Failed for {model}: {response.text[:250]}")
        except Exception as conn_err:
            print(f"Connection error for {model}: {conn_err}")
            
    if not success:
        print("\nAll tested models failed.")
    
    if response.status_code == 200:
        print("SUCCESS!")
        res_json = response.json()
        print("Response JSON:")
        print(json.dumps(res_json, indent=2, ensure_ascii=False))
        try:
            text = res_json['candidates'][0]['content']['parts'][0]['text']
            print(f"Extracted Text: {text}")
        except Exception as parse_err:
            print(f"Parse error: {parse_err}")
    else:
        print(f"Failed: {response.text}")

except Exception as e:
    print(f"Error occurred: {e}", file=sys.stderr)
    sys.exit(1)
