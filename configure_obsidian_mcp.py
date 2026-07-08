import yaml
import os

# To uruchom na serwerze (WSL/VPS) gdzie działa Hermes
config_path = '/home/holisticjson/.hermes/config.yaml'

def configure_obsidian_mcp():
    print("Konfiguracja MCP dla Obsidian Vault...")
    if not os.path.exists(config_path):
        print(f"Brak pliku {config_path}. Utwórz go przed uruchomieniem.")
        return

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f) or {}

    if 'mcp_servers' not in config:
        config['mcp_servers'] = {}

    config['mcp_servers']['obsidian_vault'] = {
        'command': 'npx',
        'args': ['-y', '@modelcontextprotocol/server-filesystem', '/home/holisticjson/Baza_Wiedzy']
    }

    with open(config_path, 'w') as f:
        yaml.safe_dump(config, f, default_flow_style=False)

    print("Zaktualizowano config.yaml o serwer MCP 'obsidian_vault' (dostęp do plików Baza_Wiedzy).")

if __name__ == "__main__":
    configure_obsidian_mcp()
