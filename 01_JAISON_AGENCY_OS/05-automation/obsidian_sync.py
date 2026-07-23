#!/usr/bin/env python3
"""
Obsidian Second Brain Synchronizer - Jaison OS
Automatyczna synchronizacja notatek, decyzji, profilu Ghost v2 i briefów klientów z Obsidian Vault.
"""

import os
import sys
import shutil
import glob
from datetime import datetime

# Reconfigure stdout for utf-8 emoji support on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Ścieżki źródłowe i domyślna ścieżka do Obsidian Vault
BASE_DIR = r"C:\Aplikacje MVP\01_JAISON_AGENCY_OS"
CLIENTS_DIR = r"C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS"
DEFAULT_OBSIDIAN_VAULT = os.environ.get(
    "OBSIDIAN_VAULT_PATH",
    r"C:\Users\tomas_yq1b9su\Documents\Obsidian Vault\Jaison_OS_Brain"
)

def sync_to_obsidian(vault_path=None):
    if not vault_path:
        vault_path = DEFAULT_OBSIDIAN_VAULT
        
    os.makedirs(vault_path, exist_ok=True)
    notes_synced = 0
    
    print(f"🧠 Synchronizacja Jaison OS Second Brain do Obsidian Vault: {vault_path}")
    
    # 1. Synchronizacja Profilu Tomasza i Głównego Paszportu
    memory_file = os.path.join(BASE_DIR, "WORKSPACE_MEMORY.md")
    if os.path.exists(memory_file):
        dest = os.path.join(vault_path, "00_WORKSPACE_MEMORY.md")
        shutil.copy2(memory_file, dest)
        notes_synced += 1
        print("  ✅ Zsynchronizowano WORKSPACE_MEMORY.md")
        
    # 2. Synchronizacja Produktów Cyfrowych z 11_digital_product
    dp_dir = os.path.join(BASE_DIR, "11_digital_product")
    if os.path.exists(dp_dir):
        obsidian_dp = os.path.join(vault_path, "11_Digital_Products")
        os.makedirs(obsidian_dp, exist_ok=True)
        for md_file in glob.glob(os.path.join(dp_dir, "*.md")):
            shutil.copy2(md_file, os.path.join(obsidian_dp, os.path.basename(md_file)))
            notes_synced += 1
        print("  ✅ Zsynchronizowano produkty cyfrowe z 11_digital_product")
        
    # 3. Synchronizacja Profilu Klientów z 02_CLIENTS_AND_PROJECTS
    if os.path.exists(CLIENTS_DIR):
        obsidian_clients = os.path.join(vault_path, "02_Clients")
        os.makedirs(obsidian_clients, exist_ok=True)
        for client_name in os.listdir(CLIENTS_DIR):
            client_path = os.path.join(CLIENTS_DIR, client_name)
            if os.path.isdir(client_path):
                client_target = os.path.join(obsidian_clients, client_name)
                os.makedirs(client_target, exist_ok=True)
                for root, _, files in os.walk(client_path):
                    for file in files:
                        if file.endswith(".md"):
                            src_file = os.path.join(root, file)
                            rel_dir = os.path.relpath(root, client_path)
                            dest_dir = os.path.join(client_target, rel_dir)
                            os.makedirs(dest_dir, exist_ok=True)
                            shutil.copy2(src_file, os.path.join(dest_dir, file))
                            notes_synced += 1
        print("  ✅ Zsynchronizowano profile i strategie klientów")
        
    print(f"✨ Synchronizacja zakończona pomyślnie! Zsynchronizowano {notes_synced} plików .md do Obsidian Vault.")

if __name__ == "__main__":
    vault_override = sys.argv[1] if len(sys.argv) > 1 else None
    sync_to_obsidian(vault_override)
