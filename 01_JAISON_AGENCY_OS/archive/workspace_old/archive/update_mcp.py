import yaml
import os

config_path = '/home/holisticjson/.hermes/config.yaml'
env_path = '/home/holisticjson/.hermes/.env'

token = None
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('GITHUB_TOKEN='):
                token = line.strip().split('=', 1)[1]
                break

if not token:
    # fallback hardcoded token if needed, but let's check both
    with open(env_path, 'r') as f:
        for line in f:
            if line.startswith('GITHUB_PERSONAL_ACCESS_TOKEN='):
                token = line.strip().split('=', 1)[1]
                break

if not token:
    token = "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"

print(f"Using token: {token[:8]}...")

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

if 'mcp_servers' not in config:
    config['mcp_servers'] = {}

config['mcp_servers']['github'] = {
    'command': 'npx',
    'args': ['-y', '@modelcontextprotocol/server-github'],
    'env': {
        'GITHUB_PERSONAL_ACCESS_TOKEN': token
    }
}

with open(config_path, 'w') as f:
    yaml.safe_dump(config, f, default_flow_style=False)

print("Updated config.yaml with github mcp server.")
