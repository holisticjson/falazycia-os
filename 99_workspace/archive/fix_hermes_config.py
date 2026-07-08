import re

config_path = "/home/holisticjson/hermes_server_config.yaml"
with open(config_path, "r") as f:
    content = f.read()

# 1. REMOVE notebooklm from mcp_servers block
# Replace the notebooklm SSE entry with empty comment
content = re.sub(
    r'\s+notebooklm:\n\s+transport: sse\n\s+url: http://localhost:8089/mcp/notebooklm/sse',
    '',
    content
)

# 2. REMOVE notebooklm from platform_toolsets (all occurrences)
content = re.sub(r'\s+- notebooklm', '', content)

# 3. Set AWS Bedrock keys in the provider/model section
# Update provider to bedrock
if "provider: google" in content:
    content = content.replace("provider: google", "provider: bedrock")

# 4. Add AWS env vars as custom_providers section or in env
# Check if AWS keys already there
if "AWS_ACCESS_KEY_ID" not in content:
    # Add before the last line
    content = content.rstrip() + "\n\naws:\n  access_key_id: AKIAXCEIPZ5HZKP5TCL6\n  secret_access_key: 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\n  region: us-east-1\n"

with open(config_path, "w") as f:
    f.write(content)

print("Done! Config updated:")
print("- NotebookLM MCP removed from mcp_servers")
print("- notebooklm removed from all platform_toolsets")
print("- AWS Bedrock credentials added")
