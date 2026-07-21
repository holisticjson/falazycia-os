import os
import json
import re

# Central paths
BASE_DIR = r"C:\Aplikacje MVP"
CLIENTS_DIR = os.path.join(BASE_DIR, "02_CLIENTS_AND_PROJECTS")
VISUALIZER_PATH = os.path.join(BASE_DIR, "01_JAISON_AGENCY_OS", "02-website", "mindmap_visualizer.html")

def scan_clients_and_projects():
    """
    Scans the 02_CLIENTS_AND_PROJECTS folder for clients and parses their AGENTS.md metadata.
    """
    clients_nodes = []
    clients_edges = []
    
    if not os.path.exists(CLIENTS_DIR):
        return clients_nodes, clients_edges
        
    start_id = 100  # Dynamic clients start at ID 100
    
    for folder_name in os.listdir(CLIENTS_DIR):
        folder_path = os.path.join(CLIENTS_DIR, folder_name)
        if os.path.isdir(folder_path) and not folder_name.startswith(".") and folder_name != "raw" and folder_name != "technical_and_excluded":
            client_id = start_id
            start_id += 1
            
            # Default values
            label = folder_name.replace("_", " ").title()
            title = f"Projekt Klienta: {label}"
            desc = "Aktywny projekt wdrożeniowy J(AI)SON OS. Trwa zbieranie danych i automatyzacja procesów."
            tech = ["n8n", "Systeme.io", "Jaison OS"]
            status = "planned"
            
            # Check for local AGENTS.md to extract rich metadata
            agents_md_path = os.path.join(folder_path, ".agents", "AGENTS.md")
            if os.path.exists(agents_md_path):
                status = "live"
                try:
                    with open(agents_md_path, "r", encoding="utf-8") as f:
                        md_content = f.read()
                        # Simple regex to extract tech stacks or specific keywords if needed
                        tech_found = re.findall(r"stack:\s*\[(.*?)\]", md_content, re.IGNORECASE)
                        if tech_found:
                            tech = [t.strip().replace("'", "").replace('"', '') for t in tech_found[0].split(",")]
                except Exception:
                    pass
            
            # Append generated node
            clients_nodes.append({
                "id": client_id,
                "label": f"🏢 {label}",
                "group": "client",
                "title": title,
                "desc": desc,
                "tech": tech,
                "status": status
            })
            
            # Connect this client to the Core Jaison Agency (ID: 1)
            clients_edges.append({
                "from": 1,
                "to": client_id,
                "label": "Obsługa",
                "arrows": "to"
            })
            
    return clients_nodes, clients_edges

def generate_dynamic_html():
    """
    Reads the base mindmap_visualizer.html, injects the static core nodes + dynamically scanned client nodes,
    and returns the updated HTML content.
    """
    if not os.path.exists(VISUALIZER_PATH):
        return "Error: mindmap_visualizer.html not found."
        
    with open(VISUALIZER_PATH, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # Scan dynamic clients
    client_nodes, client_edges = scan_clients_and_projects()
    
    # Locate NODES and EDGES declarations in HTML and modify them
    # Note: We keep the original static system nodes (core, agents, tools) 
    # and append our new dynamic client nodes to the lists.
    
    # 1. Parse original NODES array string
    nodes_match = re.search(r"const NODES = \[(.*?)\];", html_content, re.DOTALL)
    if nodes_match:
        original_nodes_str = nodes_match.group(1).strip().rstrip(",")
        # Add dynamic client nodes sformatowane jako JS obiekty
        dynamic_nodes_js = []
        for cn in client_nodes:
            node_str = (
                f"  {{ id: {cn['id']}, label: '{cn['label']}', group: '{cn['group']}', "
                f"title: '{cn['title']}', desc: '{cn['desc']}', tech: {json.dumps(cn['tech'])}, status: '{cn['status']}' }}"
            )
            dynamic_nodes_js.append(node_str)
            
        separator = ",\n" if original_nodes_str else ""
        new_nodes_str = original_nodes_str + separator + ",\n".join(dynamic_nodes_js)
        html_content = html_content.replace(nodes_match.group(0), f"const NODES = [\n{new_nodes_str}\n];")
        
    # 2. Parse original EDGES array string
    edges_match = re.search(r"const EDGES = \[(.*?)\];", html_content, re.DOTALL)
    if edges_match:
        original_edges_str = edges_match.group(1).strip().rstrip(",")
        dynamic_edges_js = []
        for ce in client_edges:
            edge_str = f"  {{ from: {ce['from']}, to: {ce['to']}, label: '{ce['label']}', arrows: '{ce['arrows']}' }}"
            dynamic_edges_js.append(edge_str)
            
        separator = ",\n" if original_edges_str else ""
        new_edges_str = original_edges_str + separator + ",\n".join(dynamic_edges_js)
        html_content = html_content.replace(edges_match.group(0), f"const EDGES = [\n{new_edges_str}\n];")
        
    return html_content

if __name__ == "__main__":
    # Test script locally and write a temp generated HTML
    output_html = generate_dynamic_html()
    print(f"Pomyślnie przetworzono mapę sieci. Wykryto {len(scan_clients_and_projects()[0])} dynamicznych klientów!")
