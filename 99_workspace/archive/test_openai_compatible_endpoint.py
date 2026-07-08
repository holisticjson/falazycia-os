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

print("Starting OpenAI-compatible Vertex AI check...")

try:
    sa_path = os.path.join(os.getcwd(), 'holistic-dashboard-dev-dea2c872139e.json')
    if not os.path.exists(sa_path):
        sa_path = '/home/holisticjson/.hermes/gcp-sa-key.json'
        
    creds = service_account.Credentials.from_service_account_file(
        sa_path,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    
    session = requests.Session()
    session.verify = False
    request = google.auth.transport.requests.Request(session=session)
    creds.refresh(request)
    print("Token refreshed successfully!")

    project_id = "holistic-dashboard-dev"
    region = "us-central1"
    
    models = ["google/gemini-2.5-flash", "google/gemini-2.5-pro"]
    
    for model in models:
        url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/endpoints/openapi/chat/completions"
        print(f"\nTesting OpenAI-compat for {model} at {url}...")
        
        headers = {
            "Authorization": f"Bearer {creds.token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Say 'OK' in one word."}]
        }
        
        response = requests.post(url, json=payload, headers=headers, verify=False, timeout=15.0)
        print(f"Result code: {response.status_code}")
        if response.status_code == 200:
            print(f"SUCCESS for {model}!")
            print(response.json())
        else:
            print(f"Failed for {model}: {response.text[:300]}")

except Exception as e:
    print(f"Error occurred: {e}", file=sys.stderr)
    sys.exit(1)
