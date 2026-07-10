import os
import sys

# Add path so we can import tools
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tools import search_pixabay_broll

# Ensure env var is set
os.environ["PIXABAY_API_KEY"] = "56349573-73a4ac749b5ba589dc9562db8"

args = {"query": "yellow flowers"}
print("Running search_pixabay_broll with args:", args)

results = search_pixabay_broll(args)

print("\n--- RESULTS ---")
import json
print(json.dumps(results, indent=2))
