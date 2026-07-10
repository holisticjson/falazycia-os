import httpx
import json
import sys

url = "http://127.0.0.1:8089/v1/chat/completions"
payload = {
    "model": "gemini-2.5-flash",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is this image? Reply in exactly one word."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
                    }
                }
            ]
        }
    ]
}

print("Testing local proxy vision request at http://127.0.0.1:8089...")
try:
    response = httpx.post(url, json=payload, timeout=20.0)
    print(f"Proxy response code: {response.status_code}")
    if response.status_code == 200:
        print("SUCCESS! Proxy vision works!")
        print(response.json())
    else:
        print(f"Failed with code {response.status_code}:")
        print(response.text)
except Exception as e:
    print(f"Error calling proxy: {e}", file=sys.stderr)
    sys.exit(1)
