import subprocess
import os

# Upload run_gateway.sh
gateway_script = """#!/bin/bash
cd /home/holisticjson/hermes-agent
export PATH=/home/holisticjson/.hermes/node/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
source .venv/bin/activate
set -a
source .env
set +a
python3.11 hermes gateway
"""

# Write it directly on the remote
cmd = f"cat > /home/holisticjson/hermes-agent/run_gateway.sh << 'HEREDOC'\n{gateway_script}\nHEREDOC"
result = subprocess.run(
    ["ssh", "HermesGCP", cmd],
    capture_output=True, text=True, timeout=15
)
print("Write result:", result.returncode, result.stdout, result.stderr)

# Set executable
result2 = subprocess.run(
    ["ssh", "HermesGCP", "chmod +x /home/holisticjson/hermes-agent/run_gateway.sh && ls -la /home/holisticjson/hermes-agent/run_gateway.sh"],
    capture_output=True, text=True, timeout=15
)
print("Chmod result:", result2.returncode, result2.stdout, result2.stderr)
