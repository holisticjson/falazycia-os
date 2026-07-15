#!/bin/bash
set -e

echo "=== Restart Hermes Gateway ==="

# Zatrzymaj stary gateway
pkill -f "hermes_cli.main gateway" || true
sleep 3

# Uruchom nowy gateway z poprawionym configiem
nohup /home/holisticjson/hermes-agent/.venv/bin/python \
    -m hermes_cli.main gateway run --replace \
    >> /home/holisticjson/.hermes/logs/gateway.log 2>&1 &

echo "[OK] Hermes Gateway restarted PID=$!"
sleep 5

echo "=== Sprawdzenie health LiteLLM (port 4000) ==="
curl -sf http://127.0.0.1:4000/health && echo "[OK] LiteLLM odpowiada!" || echo "[WARN] LiteLLM jeszcze nie gotowy"

echo "=== Procesy kluczowe ==="
ps aux | grep -E "(hermes_cli|litellm)" | grep -v grep

echo "=== Ostatnie 10 linii logow ==="
tail -n 10 /home/holisticjson/.hermes/logs/gateway.log 2>/dev/null || true
