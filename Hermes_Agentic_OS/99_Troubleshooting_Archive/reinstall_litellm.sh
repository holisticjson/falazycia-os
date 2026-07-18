#!/bin/bash
set -e

echo "=== Reinstalacja LiteLLM z pelna zaleznoscia google ==="

# 1. Zatrzymaj stary litellm
echo "[1/4] Zatrzymanie LiteLLM..."
pkill -f "litellm --config" || true
sleep 2

# 2. Wyczysc stare archiwum uv tool
echo "[2/4] Odinstalowanie starego litellm..."
uv tool uninstall litellm 2>/dev/null || true
sleep 1

# 3. Reinstaluj litellm[proxy] z google-cloud-aiplatform jako extra dep
echo "[3/4] Instalacja litellm[proxy,vertex] z google-cloud-aiplatform..."
uv tool install \
    "litellm[proxy]" \
    --python 3.12 \
    --with google-cloud-aiplatform \
    --with google-auth \
    --with google-cloud-storage \
    --force

echo "[VERIFY] Sprawdzam czy google dostepne..."
# Znajdz nowe archiwum
NEW_PYTHON=$(uv tool run --python 3.12 --from litellm python -c "import sys; print(sys.executable)" 2>/dev/null || find /home/holisticjson/.cache/uv/archive-v0 -name "python" -path "*/litellm*" 2>/dev/null | head -1)

if [ -n "$NEW_PYTHON" ]; then
    $NEW_PYTHON -c "import google.auth; print('[SUCCESS] google.auth OK')" || echo "[WARN] google.auth nadal brak"
fi

# 4. Uruchom ponownie litellm
echo "[4/4] Uruchamiam LiteLLM..."
nohup uvx --python 3.12 --from litellm litellm \
    --config /home/holisticjson/litellm_config.yaml \
    --port 4000 \
    > /home/holisticjson/litellm.log 2>&1 &

echo "[OK] LiteLLM uruchomiony PID=$!"
sleep 8

echo "=== Health check ==="
curl -sf http://127.0.0.1:4000/health 2>&1 | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    hc = d.get('healthy_count', '?')
    uc = d.get('unhealthy_count', '?')
    print(f'Healthy: {hc} | Unhealthy: {uc}')
    for m in d.get('healthy_endpoints', []):
        print(f'  [OK] {m.get(\"model\", \"?\")}')
    for m in d.get('unhealthy_endpoints', []):
        print(f'  [FAIL] {m.get(\"model\", \"?\")} -> {m.get(\"error\", \"?\")}')
except:
    print(sys.stdin.read()[:200])
" 2>/dev/null || echo "[WARN] Health check nie odpowiada"

echo "=== DONE ==="
