import re

env_path = "/home/holisticjson/.hermes/.env"
with open(env_path, "r") as f:
    content = f.read()

# Append GCP Credentials if not exists
if "GOOGLE_APPLICATION_CREDENTIALS" not in content:
    content += "\nGOOGLE_APPLICATION_CREDENTIALS=/home/holisticjson/.hermes/keys/holistic-broker-sa.json\n"
else:
    content = re.sub(r"GOOGLE_APPLICATION_CREDENTIALS=.*", "GOOGLE_APPLICATION_CREDENTIALS=/home/holisticjson/.hermes/keys/holistic-broker-sa.json", content)

if "VERTEX_PROJECT" not in content:
    content += "VERTEX_PROJECT=holistic-broker\n"
else:
    content = re.sub(r"VERTEX_PROJECT=.*", "VERTEX_PROJECT=holistic-broker", content)
    
if "VERTEX_LOCATION" not in content:
    content += "VERTEX_LOCATION=us-central1\n"
else:
    content = re.sub(r"VERTEX_LOCATION=.*", "VERTEX_LOCATION=us-central1", content)

with open(env_path, "w") as f:
    f.write(content)

print("Updated .env with GCP credentials")
