import yaml

config_path = "/home/holisticjson/.hermes/profiles/aws_bedrock_coder/config.yaml"

try:
    with open(config_path, "r") as f:
        config = yaml.safe_load(f) or {}
except FileNotFoundError:
    config = {}

# In Hermes, we can override the delegation model or default model in the profile config
if "delegation" not in config:
    config["delegation"] = {}
config["delegation"]["model"] = "bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0"

# Also try setting fallback_model to enforce bedrock
config["fallback_model"] = {
    "provider": "bedrock",
    "model": "anthropic.claude-3-5-sonnet-20241022-v2:0"
}

with open(config_path, "w") as f:
    yaml.dump(config, f)

soul_path = "/home/holisticjson/.hermes/profiles/aws_bedrock_coder/SOUL.md"
soul_text = """Jesteś elitarnym Architektem Oprogramowania (Coding Agent) zasilanym przez AWS Bedrock.
Twoim głównym celem jest kodowanie (HTML, CSS, JS) Landing Page'y i aplikacji.
Zero lania wody. Same gotowe bloki kodu. Konkretne działania. Masz dostęp do powłoki i plików."""

with open(soul_path, "w") as f:
    f.write(soul_text)
