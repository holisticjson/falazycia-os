# -*- coding: utf-8 -*-
import os
import zipfile
import shutil
import sys

print("=== JAISON AI - ZIP HISTORY RESTORER ===")

USER_HOME = os.path.expanduser("~")
LAPTOP_AG_DIR = os.path.join(USER_HOME, ".gemini", "antigravity")

script_dir = os.path.dirname(os.path.abspath(__file__))
zip_src = os.path.join(script_dir, "jaison_history_backup.zip")

if not os.path.exists(zip_src):
    # Try looking in root USB directory or current directory
    zip_src = "jaison_history_backup.zip"
    if not os.path.exists(zip_src):
        print("[!] Error: jaison_history_backup.zip not found in current folder.")
        sys.exit(1)

print(f"Unpacking history backup from: {zip_src}")
print(f"Destination: {LAPTOP_AG_DIR}")

os.makedirs(LAPTOP_AG_DIR, exist_ok=True)

try:
    with zipfile.ZipFile(zip_src, 'r') as zip_ref:
        # Extract everything
        zip_ref.extractall(LAPTOP_AG_DIR)
    print("\n=== RESTORE COMPLETE ===")
    print("Your full conversation history is now successfully restored on the laptop!")
    print("Restart your AntiGravity IDE, and you will see all your past conversations!")
except Exception as e:
    print(f"\n[!] Error during extraction: {e}")
