import re

def find_bounds(text_pattern):
    try:
        with open('view.xml', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Regex to find bounds for a node with specific text
        pattern = f'text="{text_pattern}".*?bounds="\\[(\\d+),(\\d+)\\]\\[(\\d+),(\\d+)\\]"'
        match = re.search(pattern, content, re.IGNORECASE)
        
        if match:
            x1, y1, x2, y2 = map(int, match.groups())
            # Center of the bounds
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            print(f"FOUND: {cx} {cy}")
        else:
            print("NOT_FOUND")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    import sys
    search_text = sys.argv[1] if len(sys.argv) > 1 else "Zobacz swój raport"
    find_bounds(search_text)
