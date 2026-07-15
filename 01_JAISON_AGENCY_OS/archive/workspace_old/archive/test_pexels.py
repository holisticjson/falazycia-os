import os
import sys

os.environ["PEXELS_API_KEY"] = "hrpSqvbfg4qQ7Ibk9ZhfNkcLVHxLVuIgm6uOrLIQr8DPvwJXmJGCQCVY"
sys.path.append("/home/holisticjson/.hermes/plugins/video_editor")
from tools import search_pexels_broll

print("Results 1:", search_pexels_broll({"query": "futuristic AI interface"}))
print("Results 2:", search_pexels_broll({"query": "flashing computer code"}))
