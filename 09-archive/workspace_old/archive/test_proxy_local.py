import httpx
import json
import sys

url = "http://127.0.0.1:8089/v1/chat/completions"
payload = {
    "model": "gemini-2.5-flash",
    "messages": [{"role": "user", "content": "Say 'proxy works' in exactly two words."}]
}

print("Testing local proxy at http://127.0.0.1:8089...")
try:
    response = httpx.post(url, json=payload, timeout=20.0)
    print(f"Proxy response code: {response.status_code}")
    if response.status_code == 200:
        print("SUCCESS! Proxy works!")
        print(response.json())
    else:
        print(f"Failed with code {response.status_code}:")
        print(response.text)
except Exception as e:
    print(f"Error calling proxy: {e}", file=sys.stderr)
    sys.exit(1)
