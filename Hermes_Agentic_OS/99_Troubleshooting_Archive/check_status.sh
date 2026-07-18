#!/bin/bash
echo "=== PROCESY ==="
ps aux | grep -E "hermes_cli|litellm" | grep -v grep

echo ""
echo "=== LITELLM HEALTH (port 4000) ==="
curl -sf http://127.0.0.1:4000/health 2>&1 | head -10 || echo "[WARN] Brak odpowiedzi"

echo ""
echo "=== OSTATNIE 15 LINII gateway.log ==="
tail -n 15 /home/holisticjson/.hermes/logs/gateway.log 2>/dev/null || echo "Brak pliku"

echo ""
echo "=== OSTATNIE 5 LINII BLEDOW ==="
tail -n 5 /home/holisticjson/.hermes/logs/errors.log 2>/dev/null || echo "Brak plik"
