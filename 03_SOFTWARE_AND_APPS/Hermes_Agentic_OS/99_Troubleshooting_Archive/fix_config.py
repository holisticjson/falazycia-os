import yaml

config_path = '/home/holisticjson/.hermes/config.yaml'

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

config['model'] = 'hermes-fast'
config['provider'] = 'custom'

if 'providers' in config and 'google' in config['providers']:
    config['providers']['google']['api_key'] = '/home/holisticjson/gcp-sa-key.json'

with open(config_path, 'w') as f:
    yaml.safe_dump(config, f)

print("Config updated successfully.")
