#!/usr/bin/env python3
"""
Naprawia providers.custom w ~/.hermes/config.yaml
Ustawia base_url na http://127.0.0.1:4000
i usuwa CustomProviders ktore wskazuja na openrouter
"""
import yaml
import re

config_path = "/home/holisticjson/.hermes/config.yaml"

with open(config_path, "r") as f:
    cfg = f.read()

# Parsuj YAML
data = yaml.safe_load(cfg)

print("=== PRZED ZMIANA ===")
print("provider:", data.get("provider"))
print("model:", data.get("model"))
print("providers.custom:", data.get("providers", {}).get("custom"))
print("custom_providers:", data.get("custom_providers"))

# 1. Upewnij sie ze provider = custom
data["provider"] = "custom"

# 2. Ustaw providers.custom z poprawnym base_url (localhost:4000)
if "providers" not in data:
    data["providers"] = {}
data["providers"]["custom"] = {
    "api_key": "sk-hermes-local",
    "base_url": "http://127.0.0.1:4000"
}

# 3. Zaktualizuj custom_providers - usun stary wpis openrouter/8089, dodaj lokalny
data["custom_providers"] = [
    {
        "name": "LiteLLM-Vertex",
        "base_url": "http://127.0.0.1:4000"
    }
]

# 4. Model domyslny
data["model"] = "hermes-fast"

# Zapisz
with open(config_path, "w") as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

print("\n=== PO ZMIANIE ===")
with open(config_path, "r") as f:
    saved = yaml.safe_load(f)
print("provider:", saved.get("provider"))
print("model:", saved.get("model"))
print("providers.custom:", saved.get("providers", {}).get("custom"))
print("custom_providers:", saved.get("custom_providers"))
print("\n[OK] config.yaml zaktualizowany")
