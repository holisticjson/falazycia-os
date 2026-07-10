import os
import shutil

DIRS = [
    "kurczakujasia_html",
    "kurczakujasia_html/assets",
    "kurczakujasia_html/assets/css",
    "kurczakujasia_html/assets/js",
    "kurczakujasia_html/assets/img"
]

for d in DIRS:
    os.makedirs(d, exist_ok=True)
    print(f"Created {d}")
