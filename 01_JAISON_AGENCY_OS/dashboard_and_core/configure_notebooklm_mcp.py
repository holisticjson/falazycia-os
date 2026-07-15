import yaml
import os

config_path = '/home/holisticjson/.hermes/config.yaml'

def update_hermes_config():
    if not os.path.exists(config_path):
        print(f"Error: {config_path} not found.")
        return

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        
    if 'mcp_servers' not in config:
        config['mcp_servers'] = {}
        
    # Remove old stdio definition if it exists
    if 'notebooklm' in config['mcp_servers']:
        print("Usuwanie starej konfiguracji stdio dla notebooklm...")
        del config['mcp_servers']['notebooklm']
        
    # Add SSE configuration (connecting to GCP Vertex Proxy)
    # The exact syntax depends on Hermes framework. 
    # Usually 'url' and 'transport': 'sse' works for standard MCP clients.
    config['mcp_servers']['notebooklm'] = {
        'transport': 'sse',
        'url': 'http://localhost:8089/mcp/notebooklm/sse'
    }
    
    with open(config_path, 'w') as f:
        yaml.safe_dump(config, f, default_flow_style=False)
        
    print("Zaktualizowano config.yaml Hermesa! NotebookLM działa teraz przez proxy Antigravity (SSE).")

if __name__ == "__main__":
    update_hermes_config()
