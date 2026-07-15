import yaml
import re

# ===== 1. FIX ~/.hermes/config.yaml =====
# Problem: custom_providers wskazuje na port 8089, a LiteLLM dziala na 4000
config_path = "/home/holisticjson/.hermes/config.yaml"

with open(config_path, "r") as f:
    cfg = f.read()

before = cfg
cfg = cfg.replace("http://127.0.0.1:8089/v1", "http://127.0.0.1:4000")

if cfg != before:
    with open(config_path, "w") as f:
        f.write(cfg)
    print("[OK] config.yaml: port naprawiony 8089 -> 4000")
else:
    print("[INFO] config.yaml: port juz poprawny lub nie znaleziono '8089'")

# Pokaz aktualna wartosc custom_providers
for line in cfg.splitlines():
    if "8089" in line or "4000" in line or "base_url" in line:
        print(" >>", line.strip())

# ===== 2. FIX /home/holisticjson/litellm_config.yaml =====
# Problem: gemini-3.5-flash / gemini-3.1-pro NIE ISTNIEJA w Vertex AI
# Poprawne nazwy: gemini-2.0-flash-001, gemini-2.5-pro-preview-06-05
litellm_path = "/home/holisticjson/litellm_config.yaml"

litellm_config = {
    "model_list": [
        {
            "model_name": "hermes-fast",
            "litellm_params": {
                "model": "vertex_ai/gemini-2.0-flash-001",
                "vertex_project": "holistic-broker",
                "vertex_location": "us-central1",
                "vertex_credentials": "/home/holisticjson/gcp-sa-key.json",
                "rpm": 2000
            }
        },
        {
            "model_name": "hermes-think",
            "litellm_params": {
                "model": "vertex_ai/gemini-2.5-pro-preview-06-05",
                "vertex_project": "holistic-broker",
                "vertex_location": "us-central1",
                "vertex_credentials": "/home/holisticjson/gcp-sa-key.json",
                "rpm": 60
            }
        },
        {
            "model_name": "hermes-image",
            "litellm_params": {
                "model": "vertex_ai/imagegeneration@006",
                "vertex_project": "holistic-broker",
                "vertex_location": "us-central1",
                "vertex_credentials": "/home/holisticjson/gcp-sa-key.json"
            }
        }
    ],
    "router_settings": {
        "fallbacks": [{"hermes-fast": ["hermes-think"]}]
    },
    "general_settings": {
        "disable_database": True
    }
}

with open(litellm_path, "w") as f:
    yaml.dump(litellm_config, f, default_flow_style=False, allow_unicode=True)

print("[OK] litellm_config.yaml: modele Vertex AI zaktualizowane")
print("   hermes-fast  -> vertex_ai/gemini-2.0-flash-001")
print("   hermes-think -> vertex_ai/gemini-2.5-pro-preview-06-05")
print("   hermes-image -> vertex_ai/imagegeneration@006")
