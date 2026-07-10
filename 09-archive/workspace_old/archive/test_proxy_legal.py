import urllib.request, json, sys

payload = {"model": "gemini-2.5-flash", "messages": [{"role": "user", "content": "Odpowiedz po polsku jednym zdaniem: TEST PROXY DZIALA"}]}
data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(
    "http://127.0.0.1:8089/v1/chat/completions",
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read().decode())
        content = resp["choices"][0]["message"]["content"]
        print("PROXY_OK:", content[:150])
except Exception as e:
    print("PROXY_FAIL:", type(e).__name__, str(e)[:200])

# Test Pro model
payload2 = {"model": "gemini-2.5-pro", "messages": [{"role": "user", "content": "Say WORKS in one word"}]}
data2 = json.dumps(payload2).encode("utf-8")
req2 = urllib.request.Request(
    "http://127.0.0.1:8089/v1/chat/completions",
    data=data2,
    headers={"Content-Type": "application/json"},
    method="POST"
)
try:
    with urllib.request.urlopen(req2, timeout=60) as r:
        resp2 = json.loads(r.read().decode())
        content2 = resp2["choices"][0]["message"]["content"]
        print("PRO_OK:", content2[:150])
except Exception as e:
    print("PRO_FAIL:", type(e).__name__, str(e)[:300])
