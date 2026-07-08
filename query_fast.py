import urllib.request
import json

req = urllib.request.Request(
    'http://127.0.0.1:4000/v1/chat/completions',
    data=json.dumps({
        'model': 'hermes-fast',
        'messages': [{'role': 'user', 'content': 'Say hello'}]
    }).encode(),
    headers={
        'Authorization': 'Bearer sk-hermes-local',
        'Content-Type': 'application/json'
    }
)
try:
    with urllib.request.urlopen(req) as response:
        print(response.read().decode())
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, 'read'):
        print(e.read().decode())
