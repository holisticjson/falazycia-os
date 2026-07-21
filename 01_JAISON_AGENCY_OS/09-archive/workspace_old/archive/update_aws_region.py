import re, yaml, os

# 1. Update AWS region in .env
env_path = "/home/holisticjson/.hermes/.env"
with open(env_path, "r") as f:
    content = f.read()

if "AWS_REGION_NAME" in content:
    content = re.sub(r"AWS_REGION_NAME=.*", "AWS_REGION_NAME=eu-central-1", content)
else:
    content = re.sub(r"AWS_REGION=.*", "AWS_REGION=eu-central-1", content) if "AWS_REGION" in content else content + "\nAWS_REGION_NAME=eu-central-1"

with open(env_path, "w") as f:
    f.write(content)

# 2. Update aws_bedrock_coder profile config
profile_config = "/home/holisticjson/.hermes/profiles/aws_bedrock_coder/config.yaml"
if os.path.exists(profile_config):
    with open(profile_config, "r") as f:
        cfg = yaml.safe_load(f) or {}
else:
    cfg = {}

cfg["delegation"] = cfg.get("delegation", {})
cfg["delegation"]["model"] = "bedrock/anthropic.claude-sonnet-4-6"

with open(profile_config, "w") as f:
    yaml.dump(cfg, f)

# 3. Update global config default model
global_config = "/home/holisticjson/hermes_server_config.yaml"
with open(global_config, "r") as f:
    gcontent = f.read()

# Set aws region in global config  
if "AWS_REGION" not in gcontent:
    gcontent = gcontent.rstrip() + "\naws_region: eu-central-1\n"

with open(global_config, "w") as f:
    f.write(gcontent)

print("=== DONE ===")
print(f"Region:  eu-central-1 (Frankfurt)")
print(f"Model:   anthropic.claude-sonnet-4-6")
print(f".env:    AWS_REGION_NAME=eu-central-1")
print(f"Profile: aws_bedrock_coder → bedrock/anthropic.claude-sonnet-4-6")
