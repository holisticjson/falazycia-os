import os
import requests
import google.auth.transport.requests
from google.oauth2 import service_account

sa_path = '/home/holisticjson/.hermes/keys/holistic-broker-sa.json'
project_id = 'holistic-broker'
region = 'us-central1'

print(f'Loading service account credentials from: {sa_path}')
creds = service_account.Credentials.from_service_account_file(
    sa_path,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

session = requests.Session()
request = google.auth.transport.requests.Request(session=session)
creds.refresh(request)
print('Token refreshed successfully!')

headers = {
    'Authorization': f'Bearer {creds.token}',
    'Content-Type': 'application/json'
}

models = [
    'gemini-3.5-flash',
    'gemini-3.5-flash-preview',
    'gemini-3.5-flash-001',
    'gemini-3.1-pro',
    'gemini-3.1-pro-preview',
    'gemini-3.1-pro-preview-0217',
    'gemini-2.5-flash',
    'gemini-2.5-pro',
    'gemini-2.5-flash-001',
    'gemini-2.5-pro-001'
]

for model in models:
    url = f'https://{region}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{region}/publishers/google/models/{model}:generateContent'
    payload = {
        'contents': [{
            'role': 'user',
            'parts': [{'text': 'Say hello'}]
        }]
    }
    print(f'Testing {model}...')
    res = requests.post(url, json=payload, headers=headers)
    print(f'  Status code: {res.status_code}')
    if res.status_code == 200:
        print(f'  SUCCESS: {res.json()["candidates"][0]["content"]["parts"][0]["text"].strip()}')
    else:
        print(f'  FAILED: {res.text[:200]}')
