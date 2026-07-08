import sys
sys.path.insert(0, "/home/holisticjson/hermes-agent")
sys.path.insert(0, "/home/holisticjson/hermes-agent/.venv/lib/python3.11/site-packages")
import os
os.chdir("/home/holisticjson/hermes-agent")

try:
    from hermes_cli.config import load_config, cfg_get
    cfg = load_config()
    print("Full config:", cfg)
    print("model.default:", cfg_get("model.default") if cfg else "N/A")
    print("model.base_url:", cfg_get("model.base_url") if cfg else "N/A")
    print("provider:", cfg_get("model.provider") if cfg else "N/A")
except Exception as e:
    print("Error:", e)
    import traceback; traceback.print_exc()
