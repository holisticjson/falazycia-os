import urllib.request
import json
req = urllib.request.Request("http://127.0.0.1:4000/v1/models", headers={"Authorization": "Bearer sk-hermes-local"})
try:
    with urllib.request.urlopen(req) as response:
        print("SUCCESS:", response.read().decode())
except Exception as e:
    print("Error:", e)
