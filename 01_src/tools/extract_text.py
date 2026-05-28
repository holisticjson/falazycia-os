import re

def extract_text(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        texts = re.findall(r'text="(.*?)"', content)
        clean_texts = [t for t in texts if t.strip()]
        
        with open('extracted_report.md', 'a', encoding='utf-8') as out:
            out.write("\n\n--- Kolejna Sekcja ---\n\n")
            out.write('\n\n'.join(clean_texts))
        
        print("SUCCESS: Text saved to extracted_report.md")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    import sys
    fname = sys.argv[1] if len(sys.argv) > 1 else 'report.xml'
    extract_text(fname)
