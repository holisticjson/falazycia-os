#!/bin/bash
echo "=== HEALTH z API KEY ==="
curl -s http://127.0.0.1:4000/health \
  -H "Authorization: Bearer sk-hermes-local" | python3 -m json.tool 2>/dev/null | grep -E "healthy|model|status" | head -20

echo ""
echo "=== TEST QUERY: gemini-2.5-flash ==="
RESP=$(curl -s http://127.0.0.1:4000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-hermes-local" \
  -d '{"model":"hermes-fast","messages":[{"role":"user","content":"Powiedz tylko: DZIALA"}],"max_tokens":20}')

echo "$RESP" | python3 -c "
import sys, json
d = json.load(sys.stdin)
if 'choices' in d:
    txt = d['choices'][0]['message']['content']
    model = d.get('model','?')
    print(f'[SUCCESS] Model={model} | Odp={txt}')
else:
    err = d.get('error', d)
    print(f'[ERROR] {err}')
"

echo ""
echo "=== OSTATNIE LOGI ==="
tail -n 5 /home/holisticjson/litellm.log | grep -v InsecureRequest
