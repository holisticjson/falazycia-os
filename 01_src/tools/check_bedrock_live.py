"""
Diagnostyka AWS Bedrock - pobiera liste dostepnych modeli
oraz PROFILI WNIOSKOWANIA z regionow EU i US.
Uruchom: python check_bedrock_live.py
"""
import boto3
import sys

# Fix encoding for Windows terminal
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REGIONS = ["eu-central-1", "us-east-1"]

def check_region(region):
    print(f"\n{'='*60}")
    print(f"  REGION: {region}")
    print(f"{'='*60}")

    try:
        session = boto3.Session(profile_name="default")
        client = session.client("bedrock", region_name=region)

        # 1. Lista modeli bazowych (Foundation Models - ON_DEMAND)
        print("\n--- Modele bazowe Claude (ON_DEMAND): ---")
        try:
            resp = client.list_foundation_models(
                byProvider="Anthropic",
                byInferenceType="ON_DEMAND"
            )
            models = resp.get("modelSummaries", [])
            if models:
                for m in models:
                    status = m.get("modelLifecycle", {}).get("status", "-")
                    print(f"  [OK] ID: {m['modelId']}")
                    print(f"       Nazwa: {m.get('modelName', '-')}")
                    print(f"       Status: {status}")
                    print()
            else:
                print("  [--] Brak aktywnych modeli ON_DEMAND w tym regionie.")
        except Exception as e:
            print(f"  [ERR] Blad pobierania modeli: {e}")

        # 2. Lista profili wnioskowania (Inference Profiles)
        print("\n--- Profile Wnioskowania (Cross-Region Inference Profiles): ---")
        try:
            resp2 = client.list_inference_profiles()
            profiles = resp2.get("inferenceProfileSummaries", [])
            claude_profiles = [p for p in profiles if "claude" in p.get("inferenceProfileId", "").lower()]
            if claude_profiles:
                for p in claude_profiles:
                    print(f"  [PROFILE] ID: {p['inferenceProfileId']}")
                    print(f"            ARN: {p.get('inferenceProfileArn', '-')}")
                    print(f"            Typ: {p.get('type', '-')}")
                    print()
            else:
                print("  [--] Brak profili Claude w tym regionie.")
        except Exception as e:
            print(f"  [ERR] Blad pobierania profili: {e}")

    except Exception as e:
        print(f"  [ERR] Nie mozna polaczyc z regionem {region}: {e}")

if __name__ == "__main__":
    print("[START] Diagnostyka AWS Bedrock - Szukam aktywnych modeli i profili Claude...\n")
    for region in REGIONS:
        check_region(region)
    print(f"\n{'='*60}")
    print("  Gotowe! Powyzsze Profile ID wklej do Cline -> Model ID.")
    print(f"{'='*60}\n")
