import re
import sys

env_file = "/home/holisticjson/.hermes/.env"
with open(env_file, "r") as f:
    content = f.read()

# Replace or add keys
keys = {
    "AWS_ACCESS_KEY_ID": "AKIAXCEIPZ5HZKP5TCL6",
    "AWS_SECRET_ACCESS_KEY": "QfcaV5xhOKVOP1SGJNwl19YWHEKjahKDBX8CbQd7",
    "AWS_REGION_NAME": "us-east-1"
}

for k, v in keys.items():
    if re.search(f"^{k}=.*$", content, flags=re.MULTILINE):
        content = re.sub(f"^{k}=.*$", f"{k}={v}", content, flags=re.MULTILINE)
    else:
        content += f"\n{k}={v}"

with open(env_file, "w") as f:
    f.write(content)
