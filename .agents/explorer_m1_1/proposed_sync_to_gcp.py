import os
import zipfile
import subprocess
import time

# Configurations
SSH_KEY = r"C:\Users\tomas_yq1b9su\.ssh\id_rsa_gcp"
VM_USER = "holisticjson"
VM_IP = "34.55.82.86"

WORKSPACE_LOCAL = r"c:\Aplikacje MVP\Holistic Jason"
WORKSPACE_REMOTE = "/home/holisticjson/Agentic_OS/holistic-aidhd-os"

# Specific paths inside .gemini to sync
CONFIG_LOCAL = r"C:\Users\tomas_yq1b9su\.gemini\config"
BRAIN_LOCAL = r"C:\Users\tomas_yq1b9su\.gemini\antigravity\brain\8870d516-bbf7-4a9b-b540-34938cc9c42f"

WORKSPACE_ZIP = "holistic_jason.zip"
GEMINI_ZIP = "gemini_config.zip"

EXCLUDED_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", 
    "dist", "build", "generated_media"
}

def create_workspace_zip():
    print(f"[ZIP] Packaging workspace {WORKSPACE_LOCAL} into {WORKSPACE_ZIP}...")
    zip_count = 0
    with zipfile.ZipFile(WORKSPACE_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(WORKSPACE_LOCAL):
            dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
            for file in files:
                if file.endswith('.zip') or file.endswith('.tmp'):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, WORKSPACE_LOCAL)
                zipf.write(full_path, rel_path)
                zip_count += 1
    print(f"[ZIP] Packaged {zip_count} workspace files.")

def create_gemini_config_zip():
    print(f"[ZIP] Packaging config and active brain into {GEMINI_ZIP}...")
    zip_count = 0
    with zipfile.ZipFile(GEMINI_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 1. Add global config folder
        if os.path.exists(CONFIG_LOCAL):
            for root, dirs, files in os.walk(CONFIG_LOCAL):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, CONFIG_LOCAL)
                    archive_name = os.path.join("config", rel_path)
                    zipf.write(full_path, archive_name)
                    zip_count += 1
                    
        # 2. Add current conversation brain folder
        if os.path.exists(BRAIN_LOCAL):
            for root, dirs, files in os.walk(BRAIN_LOCAL):
                for file in files:
                    if file.endswith('.zip') or file.endswith('.tmp'):
                        continue
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, BRAIN_LOCAL)
                    archive_name = os.path.join("antigravity", "brain", "8870d516-bbf7-4a9b-b540-34938cc9c42f", rel_path)
                    zipf.write(full_path, archive_name)
                    zip_count += 1
                    
    print(f"[ZIP] Packaged {zip_count} config/brain files.")

def run_command_proc(cmd):
    print(f"[CMD] Executing: {cmd}")
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"[ERROR] Command failed: {res.stderr}")
        return False
    print(res.stdout)
    return True

def main():
    start_time = time.time()
    
    # 1. Zip files
    create_workspace_zip()
    create_gemini_config_zip()
    
    # 2. Upload zip files
    scp_cmd_ws = f'scp -i "{SSH_KEY}" -o StrictHostKeyChecking=no {WORKSPACE_ZIP} {VM_USER}@{VM_IP}:/home/holisticjson/'
    scp_cmd_gem = f'scp -i "{SSH_KEY}" -o StrictHostKeyChecking=no {GEMINI_ZIP} {VM_USER}@{VM_IP}:/home/holisticjson/'
    
    print("[DEPLOY] Uploading workspace ZIP to GCP VM...")
    if not run_command_proc(scp_cmd_ws):
        print("[ERROR] Failed to upload workspace ZIP.")
        return
        
    print("[DEPLOY] Uploading .gemini configurations ZIP to GCP VM...")
    if not run_command_proc(scp_cmd_gem):
        print("[ERROR] Failed to upload .gemini ZIP.")
        return

    # 3. Extract and restart remote services
    print("[DEPLOY] Extracting archives on VM, linking skills, and restarting Streamlit...")
    
    # Remote execution block
    remote_cmds = [
        # Create directories if not exist
        f"mkdir -p {WORKSPACE_REMOTE}",
        "mkdir -p /home/holisticjson/.gemini",
        "mkdir -p /home/holisticjson/.hermes/skills",
        "mkdir -p /home/holisticjson/.hermes/profiles",
        
        # Unzip workspace (overwrite existing)
        f"unzip -o /home/holisticjson/{WORKSPACE_ZIP} -d {WORKSPACE_REMOTE} > /dev/null",
        
        # Unzip .gemini config
        f"unzip -o /home/holisticjson/{GEMINI_ZIP} -d /home/holisticjson/.gemini/ > /dev/null",
        
        # Link workspace skills to ~/.hermes/skills/ and ~/.hermes/profiles/
        f'for d in {WORKSPACE_REMOTE}/skills/*; do [ -d "$d" ] && name=$(basename "$d") && rm -rf "/home/holisticjson/.hermes/skills/$name" && ln -sf "$d" "/home/holisticjson/.hermes/skills/$name" && rm -rf "/home/holisticjson/.hermes/profiles/$name" && ln -sf "$d" "/home/holisticjson/.hermes/profiles/$name"; done || true',
        
        # Clean up remote ZIP files
        f"rm -f /home/holisticjson/{WORKSPACE_ZIP}",
        f"rm -f /home/holisticjson/{GEMINI_ZIP}",
        
        # Copy .env to workspace directory on VM for API keys
        f"cp -f {WORKSPACE_REMOTE}/.env {WORKSPACE_REMOTE}/.env 2>/dev/null || true",
        
        # Restart Streamlit process
        "pkill -u holisticjson -f 'streamlit run' 2>/dev/null || true",
        "sleep 2",
        f"nohup /home/holisticjson/.local/bin/streamlit run {WORKSPACE_REMOTE}/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true > ~/streamlit.log 2>&1 & sleep 3",
        "ss -tlnp | grep 8501"
    ]
    
    combined_remote_cmd = " && ".join(remote_cmds)
    ssh_cmd = f'ssh -i "{SSH_KEY}" -o StrictHostKeyChecking=no {VM_USER}@{VM_IP} "{combined_remote_cmd}"'
    
    if run_command_proc(ssh_cmd):
        print("[SUCCESS] Migration and symlinking completed successfully!")
    else:
        print("[ERROR] Failed to complete remote extraction/restart.")
        
    # 4. Clean up local ZIPs
    print("[CLEAN] Cleaning up local temporary archives...")
    if os.path.exists(WORKSPACE_ZIP):
        os.remove(WORKSPACE_ZIP)
    if os.path.exists(GEMINI_ZIP):
        os.remove(GEMINI_ZIP)
        
    print(f"[TIME] Total migration time: {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    main()
