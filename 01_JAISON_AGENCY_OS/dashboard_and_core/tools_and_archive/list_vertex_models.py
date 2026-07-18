import requests
import json
from google.oauth2 import service_account
import google.auth.transport.requests

sa_path = '/home/holisticjson/.hermes/keys/holistic-broker-sa.json'
project_id = 'holistic-broker'

creds = service_account.Credentials.from_service_account_file(
    sa_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

session = requests.Session()
request = google.auth.transport.requests.Request(session=session)
creds.refresh(request)

headers = {
    'Authorization': f'Bearer {creds.token}',
    'Content-Type': 'application/json'
}

# 1. Query the list of models in us-central1
regions = ['us-central1', 'us-east4', 'europe-west4', 'europe-west1']
for region in regions:
    print(f"\n=== Listing models in region {region} ===")
    url = f"https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/models"
    try:
        res = requests.get(url, headers=headers)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            models_data = res.json()
            if 'models' in models_data:
                for m in models_data['models']:
                    print(f"  - {m['displayName']} ({m['name']})")
            else:
                print("  No models found in this project's deployments.")
        else:
            print(f"  Failed: {res.text}")
    except Exception as e:
        print(f"  Error: {e}")
