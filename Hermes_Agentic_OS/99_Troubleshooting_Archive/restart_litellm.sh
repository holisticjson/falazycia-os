#!/bin/bash
# Restart LiteLLM with new config pointing to holistic-dashboard-dev
echo "=== Stopping old LiteLLM ==="
pkill -9 -f "litellm" 2>/dev/null || true
sleep 3
echo "=== Verifying config ==="
grep vertex_project /home/holisticjson/litellm_config.yaml | head -3
echo "=== Starting LiteLLM ==="
su -s /bin/bash holisticjson -c "nohup /home/holisticjson/.local/bin/uv tool uvx --python 3.12 --from litellm litellm --config /home/holisticjson/litellm_config.yaml --port 4000 > /tmp/litellm_new.log 2>&1 &"
sleep 8
echo "=== Health check ==="
curl -s -H "Authorization: Bearer sk-hermes-local" http://127.0.0.1:4000/health | python3 -c "import sys,json; d=json.load(sys.stdin); print('Healthy:', d.get('healthy_count',0), 'Unhealthy:', d.get('unhealthy_count',0))" 2>/dev/null || curl -s http://127.0.0.1:4000/health | head -c 200
echo "=== Models ==="
curl -s -H "Authorization: Bearer sk-hermes-local" http://127.0.0.1:4000/models | python3 -c "import sys,json; d=json.load(sys.stdin); print([m['id'] for m in d.get('data',[])])" 2>/dev/null
