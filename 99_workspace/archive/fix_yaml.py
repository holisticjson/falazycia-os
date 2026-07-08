import yaml
import os

config_path = "/home/holisticjson/litellm/config.yaml"
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    if "router_settings" in config and "fallbacks" in config["router_settings"]:
        for idx, fallback_dict in enumerate(config["router_settings"]["fallbacks"]):
            if "free-fast" in fallback_dict:
                # Remove self-referencing fallback
                fallback_dict["free-fast"] = [x for x in fallback_dict["free-fast"] if x != "free-fast"]
                if not fallback_dict["free-fast"]:
                    fallback_dict["free-fast"] = ["smart-logic"] # Safe fallback
                    
    with open(config_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
