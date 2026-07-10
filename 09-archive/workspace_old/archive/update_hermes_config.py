import yaml
import sys

config_path = '/home/holisticjson/.hermes/config.yaml'

print("Reading Hermes config.yaml...")
try:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    print("Modifying model configuration...")
    # Update default model and provider
    if 'model' not in config:
        config['model'] = {}
    config['model']['default'] = 'gemini-2.5-flash'
    config['model']['provider'] = 'custom:gcp-vertex-ai'
    config['model']['base_url'] = ''
    config['model']['api_mode'] = 'chat_completions'
    
    # Add custom provider
    print("Adding GCP Vertex AI custom provider...")
    custom_providers = config.get('custom_providers', [])
    # Check if already exists
    exists = False
    for p in custom_providers:
        if p.get('name') == 'GCP Vertex AI':
            p['base_url'] = 'http://127.0.0.1:8089/v1'
            exists = True
            break
    if not exists:
        custom_providers.append({
            'name': 'GCP Vertex AI',
            'base_url': 'http://127.0.0.1:8089/v1'
        })
    config['custom_providers'] = custom_providers
    
    print("Writing modified config.yaml...")
    with open(config_path, 'w') as f:
        yaml.safe_dump(config, f, default_flow_style=False)
    print("Configuration updated successfully!")

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
