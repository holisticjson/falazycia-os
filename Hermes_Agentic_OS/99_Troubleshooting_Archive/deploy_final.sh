#!/bin/bash
set -e

echo "=== [1/3] Wdrożenie finalnej konfiguracji ==="
cp /tmp/litellm_config_final.yaml /home/holisticjson/litellm_config.yaml
echo "[OK] litellm_config.yaml zaktualizowany"
echo "Zawartość:"
cat /home/holisticjson/litellm_config.yaml

echo ""
echo "=== [2/3] Restart LiteLLM ==="
pkill -f "litellm --config" || true
sleep 3

nohup uvx --python 3.12 --from litellm litellm \
    --config /home/holisticjson/litellm_config.yaml \
    --port 4000 \
    > /home/holisticjson/litellm.log 2>&1 &

echo "[OK] LiteLLM uruchomiony PID=$!"
sleep 10

echo ""
echo "=== [3/3] Test końcowy: hermes-fast (gemini-2.5-flash) ==="
RESULT=$(curl -sf http://127.0.0.1:4000/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-hermes-local" \
  -d '{"model":"hermes-fast","messages":[{"role":"user","content":"Say only the word: WORKS"}],"max_tokens":10}' 2>&1)

echo "$RESULT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    if 'choices' in d:
        answer = d['choices'][0]['message']['content'].strip()
        model = d.get('model', '?')
        print(f'[SUCCESS] Model: {model} | Odpowiedź: {answer}')
    else:
        print('[ERROR]', json.dumps(d, indent=2)[:300])
except Exception as e:
    raw = open('/dev/stdin').read() if False else ''
    print('[PARSE ERROR]:', e)
    print('Raw:', sys.argv)
" 2>/dev/null || echo "[WARN] Odpowiedź: $RESULT" | head -c 300

echo ""
echo "=== HEALTH CHECK ==="
curl -sf http://127.0.0.1:4000/health 2>&1 | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(f'Healthy: {d.get(\"healthy_count\",\"?\")} | Unhealthy: {d.get(\"unhealthy_count\",\"?\")}')
    for m in d.get('healthy_endpoints',[]):
        print(f'  ✅ {m.get(\"model\",\"?\")}')
except:
    pass
" 2>/dev/null || true

echo ""
echo "=== GOTOWE ==="
