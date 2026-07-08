import sys
import os
import ssl
# Bypass SSL verification globally for local testing behind proxy/firewall
ssl._create_default_https_context = ssl._create_unverified_context

from google.oauth2 import service_account
import google.auth.transport.requests
import httpx
import json

print("Starting Vertex AI API multi-region and multi-model auth check...")
try:
    # 1. Load service account credentials with fallback paths
    import os
    sa_path = '/home/holisticjson/.hermes/gcp-sa-key.json'
    if not os.path.exists(sa_path):
        sa_path = os.path.join(os.getcwd(), 'holistic-dashboard-dev-dea2c872139e.json')
    if not os.path.exists(sa_path):
        sa_path = os.path.expanduser('~/.hermes/gcp-sa-key.json')
    print(f"Loading service account credentials from: {sa_path}")
    creds = service_account.Credentials.from_service_account_file(
        sa_path,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    import requests
    # Disable warnings for unverified requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    session = requests.Session()
    session.verify = False
    request = google.auth.transport.requests.Request(session=session)
    print("Refreshing Google OAuth token...")
    creds.refresh(request)
    print("Token refreshed successfully!")

    project_id = "holistic-dashboard-dev"

    regions = ["us-central1", "europe-west3", "europe-west9", "us-east4", "europe-west1"]
    models = [
        "google/gemini-1.5-flash-002",
        "google/gemini-1.5-flash-001",
        "google/gemini-1.5-pro-002",
        "google/gemini-1.5-pro-001",
        "google/gemini-2.0-flash-exp",
    ]

    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }

    success = False
    for region in regions:
        url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/endpoints/openapi/chat/completions"
        print(f"\n--- Testing region: {region} at {url} ---")
        for model in models:
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": "Say 'ok' in one word."}]
            }
            print(f"  Testing model: {model} ...")
            try:
                # Use verify=False in httpx post
                response = httpx.post(url, json=payload, headers=headers, timeout=10.0, verify=False)
                print(f"    Result code: {response.status_code}")
                if response.status_code == 200:
                    print(f"    SUCCESS for {model} in {region}!")
                    print(response.json())
                    success = True
                    break
                else:
                    print(f"    Failed: {response.text[:200]}")
            except Exception as e:
                print(f"    Network error for {model} in {region}: {e}")
        if success:
            break

except Exception as e:
    print(f"Error occurred: {e}", file=sys.stderr)
    sys.exit(1)
