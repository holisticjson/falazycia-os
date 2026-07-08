import urllib.request, json

# Check OpenRouter free models
req = urllib.request.Request(
    "https://openrouter.ai/api/v1/models",
    headers={"Authorization": "Bearer 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"}
)
with urllib.request.urlopen(req, timeout=10) as r:
    models = json.loads(r.read()).get("data", [])

free = [m for m in models if str(m.get("pricing", {}).get("prompt", "1")) == "0"]
print(f"\n=== FREE MODELS ON OPENROUTER ({len(free)} total) ===")
interesting = [m for m in free if any(k in m["id"].lower() for k in ["claude", "gemini", "llama-3", "gpt-4", "qwen", "deepseek", "mistral"])]
for m in sorted(interesting, key=lambda x: x["id"]):
    ctx = m.get("context_length", 0)
    print(f"  - {m['id']} (ctx: {ctx:,})")

# Check current balance
req2 = urllib.request.Request(
    "https://openrouter.ai/api/v1/auth/key",
    headers={"Authorization": "Bearer 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"}
)
with urllib.request.urlopen(req2, timeout=10) as r:
    key_info = json.loads(r.read()).get("data", {})
print(f"\n=== OPENROUTER ACCOUNT ===")
print(f"  Label: {key_info.get('label', 'N/A')}")
print(f"  Usage: ${key_info.get('usage', 0):.4f}")
print(f"  Limit: ${key_info.get('limit', 'unlimited')}")
print(f"  Free tier: {key_info.get('is_free_tier', False)}")
