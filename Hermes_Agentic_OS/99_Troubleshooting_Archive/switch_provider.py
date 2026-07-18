#!/usr/bin/env python3
import yaml

config_path = "/home/holisticjson/.hermes/config.yaml"

with open(config_path, "r") as f:
    data = yaml.safe_load(f)

# Wymuś uzycie OpenAI jako providera (kierujacego do LiteLLM)
data["provider"] = "openai"
data["model"] = "hermes-fast"

if "providers" not in data or not data["providers"]:
    data["providers"] = {}

data["providers"]["openai"] = {
    "api_key": "sk-hermes-local",
    "base_url": "http://127.0.0.1:4000"
}

# Usuwamy custom, zeby nie psul
if "custom" in data["providers"]:
    del data["providers"]["custom"]

with open(config_path, "w") as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

print("[OK] Zmieniono config na provider=openai (LiteLLM proxy na porcie 4000)")
