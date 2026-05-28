import re
import sys

def find_clickable_parent(text_pattern):
    try:
        with open('view_today.xml', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the node with the text
        nodes = re.findall(r'<node (.*?)>', content)
        target_node_idx = -1
        for i, node in enumerate(nodes):
            if text_pattern in node:
                target_node_idx = i
                break
        
        if target_node_idx == -1:
            print("TEXT_NOT_FOUND")
            return

        # Look backwards for the first clickable="true" node
        for i in range(target_node_idx, -1, -1):
            if 'clickable="true"' in nodes[i]:
                bounds_match = re.search(r'bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', nodes[i])
                if bounds_match:
                    x1, y1, x2, y2 = map(int, bounds_match.groups())
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    print(f"CLICKABLE_FOUND: {cx} {cy}")
                    return
        
        print("NO_CLICKABLE_PARENT")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    find_clickable_parent("Zobacz swój raport")
