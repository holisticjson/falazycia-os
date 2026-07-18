import glob
import re

for filepath in glob.glob("*.html"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    forms = re.findall(r'(<form.*?</form>)', content, re.DOTALL | re.IGNORECASE)
    if forms:
        print(f"File: {filepath} has {len(forms)} form(s)")
        for idx, form in enumerate(forms):
            print(f"--- Form {idx} snippet (first 300 chars):")
            print(form[:300])
            print("...")
            print("---")
