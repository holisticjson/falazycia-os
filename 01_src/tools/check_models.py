import os
from google import genai

SA_KEY_PATH = r"c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_KEY_PATH

client = genai.Client(
    vertexai=True,
    project="holistic-dashboard-dev",
    location="us-central1"
)

print("Listing models in us-central1:")
try:
    for model in client.models.list():
        print(f"Model: {model.name}")
except Exception as e:
    print(f"Error in us-central1: {e}")

client_east = genai.Client(
    vertexai=True,
    project="holistic-dashboard-dev",
    location="us-east-1"
)

print("\nListing models in us-east-1:")
try:
    for model in client_east.models.list():
        print(f"Model: {model.name}")
except Exception as e:
    print(f"Error in us-east-1: {e}")
