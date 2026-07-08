#!/usr/bin/env python3
"""
Fix all services on GCP:
1. Kill old hermes-agent (run_agent.py)  
2. Restart LiteLLM with correct config
3. Start hermes as proper gateway
"""
import subprocess, os, time

NODE_BIN = "/home/holisticjson/.hermes/node/bin"
PM2 = f"{NODE_BIN}/pm2"
HERMES_DIR = "/home/holisticjson/hermes-agent"
VENV_PY = f"{HERMES_DIR}/.venv/bin/python3.11"
HERMES_BIN = f"{HERMES_DIR}/hermes"
LITELLM_DIR = "/home/holisticjson/litellm"
env = {**os.environ, "PATH": f"{NODE_BIN}:/usr/local/bin:/usr/bin:/bin"}

def run(cmd, **kw):
    print(f"CMD: {cmd}")
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env, **kw)
    if r.stdout: print("OUT:", r.stdout[:500])
    if r.stderr: print("ERR:", r.stderr[:500])
    return r.returncode == 0

# 1. Stop old hermes-agent (run_agent.py that keeps hitting LiteLLM with empty model)
print("\n=== 1. Stop old hermes-agent ===")
run(f"{PM2} delete hermes-agent")

# 2. Restart LiteLLM 
print("\n=== 2. Restart LiteLLM ===")
run(f"{PM2} restart litellm")
time.sleep(8)  # Give LiteLLM time to start

# 3. Check if LiteLLM is up
print("\n=== 3. Check LiteLLM health ===")
import urllib.request
try:
    with urllib.request.urlopen("http://127.0.0.1:4000/health", timeout=5) as r:
        print("LiteLLM HEALTH:", r.read().decode()[:200])
except Exception as e:
    print("LiteLLM health error:", e)
    # Try models endpoint
    try:
        with urllib.request.urlopen("http://127.0.0.1:4000/v1/models", timeout=5) as r:
            print("LiteLLM MODELS:", r.read().decode()[:200])
    except Exception as e2:
        print("LiteLLM models error:", e2)

# 4. Create proper gateway startup script
print("\n=== 4. Create gateway startup script ===")
gateway_script = f"""#!/bin/bash
cd {HERMES_DIR}
export PATH={NODE_BIN}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
source .venv/bin/activate
set -a
source .env
set +a
exec {VENV_PY} {HERMES_BIN} gateway
"""
with open(f"{HERMES_DIR}/run_gateway.sh", "w") as f:
    f.write(gateway_script)
run(f"chmod +x {HERMES_DIR}/run_gateway.sh")
print("Gateway script created.")

# 5. Start hermes gateway in PM2
print("\n=== 5. Start hermes gateway ===")
run(f"{PM2} start {HERMES_DIR}/run_gateway.sh --name hermes-agent")
run(f"{PM2} save")

# 6. Final status
print("\n=== 6. Final PM2 status ===")
run(f"{PM2} status")

print("\n=== DONE ===")
