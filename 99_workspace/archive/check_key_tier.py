import sys
import httpx
import json

api_key = "AQ.Ab8RN6Kdoy2zR8bE6YY1FdkCjlp95N_Zt_W-KI0GBKeWqyaGuQ"
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
payload = {
    "contents": [{"role": "user", "parts": [{"text": "Say 'Key test success' in exactly three words."}]}]
}

print(f"Testing API key {api_key[:10]}... with generateContent...")
try:
    resp = httpx.post(
        url,
        params={"key": api_key},
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=10.0
    )
    print(f"Response status: {resp.status_code}")
    if resp.status_code == 200:
        print("SUCCESS! Response JSON:")
        print(json.dumps(resp.json(), indent=2))
        
        # Check rate limit headers
        headers_lower = {k.lower(): v for k, v in resp.headers.items()}
        rpd_header = headers_lower.get("x-ratelimit-limit-requests-per-day")
        print(f"Daily limit header (x-ratelimit-limit-requests-per-day): {rpd_header}")
        if rpd_header:
            try:
                rpd_val = int(rpd_header)
                if rpd_val <= 1000:
                    print("--> WARNING: Key appears to be on FREE TIER.")
                else:
                    print("--> SUCCESS: Key is on PAID TIER!")
            except:
                pass
        else:
            print("--> SUCCESS: No free-tier rate limit header found. Key is likely on PAID TIER!")
    else:
        print(f"Failed with code {resp.status_code}:")
        print(resp.text)

except Exception as e:
    print(f"Error: {e}")
