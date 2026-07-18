#!/bin/bash
echo "=== TEST: LiteLLM -> Vertex AI ==="

# Sprawdz czy LiteLLM odpowiada na health
HEALTH=$(curl -sf http://127.0.0.1:4000/health 2>&1)
echo "Health: $HEALTH"

echo ""
echo "=== TEST QUERY: hermes-fast (gemini-2.0-flash-001) ==="
curl -sf http://127.0.0.1:4000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-hermes-local" \
  -d '{
    "model": "hermes-fast",
    "messages": [{"role": "user", "content": "Say OK in one word"}],
    "max_tokens": 10
  }' 2>&1 | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    if 'choices' in data:
        print('[SUCCESS] Model odpowiedzial:', data['choices'][0]['message']['content'])
    else:
        print('[ERROR] Odpowiedz bez choices:', json.dumps(data, indent=2))
except Exception as e:
    raw = sys.stdin.read() if hasattr(sys.stdin, 'read') else ''
    print('[PARSE ERROR]:', e)
"

echo ""
echo "=== LITELLM LOG (ostatnie 10 linii) ==="
tail -n 10 /home/holisticjson/litellm.log 2>/dev/null || echo "Brak pliku"
