import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def list_inference_profiles():
    session = boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "eu-central-1")
    )
    client = session.client("bedrock")
    
    try:
        response = client.list_inference_profiles()
        profiles = response.get("inferenceProfileSummaries", [])
        print(f"Znaleziono {len(profiles)} profilów:")
        for p in profiles:
            if "sonnet-4" in p['inferenceProfileId'].lower():
                print(f"Name: {p['inferenceProfileName']} | ID: {p['inferenceProfileId']}")
    except Exception as e:
        print(f"Błąd: {e}")

if __name__ == "__main__":
    list_inference_profiles()
