import yaml
with open("/home/holisticjson/litellm/config.yaml", "r") as f:
    c = yaml.safe_load(f)
if "general_settings" in c:
    c["litellm_settings"] = c.pop("general_settings")
with open("/home/holisticjson/litellm/config.yaml", "w") as f:
    yaml.dump(c, f, default_flow_style=False)
