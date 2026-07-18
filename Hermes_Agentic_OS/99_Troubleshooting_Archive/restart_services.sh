#!/bin/bash
set -e

echo "=== [1/3] Zatrzymanie LiteLLM ==="
pkill -f "litellm --config" || true
sleep 2

echo "=== [2/3] Restart LiteLLM na porcie 4000 ==="
nohup uvx --python 3.12 --from "litellm[proxy]" litellm \
    --config /home/holisticjson/litellm_config.yaml \
    --port 4000 \
    > /home/holisticjson/litellm.log 2>&1 &

LITELLM_PID=$!
echo "[OK] LiteLLM uruchomiony PID=$LITELLM_PID"
sleep 5

echo "=== [3/3] Restart Hermes Gateway ==="
hermes gateway restart || true
sleep 3

echo "=== STATUS ==="
ps aux | grep -E "litellm|hermes" | grep -v grep | head -10

echo "=== KONIEC - test portu 4000 ==="
curl -s http://127.0.0.1:4000/health || echo "[WARN] LiteLLM health check nie odpowiada jeszcze"
