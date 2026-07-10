import boto3
import os
import json

# Load .env variables
env_vars = {}
with open('/home/holisticjson/litellm/.env', 'r') as f:
    for line in f:
        if '=' in line and not line.strip().startswith('#'):
            k, v = line.strip().split('=', 1)
            env_vars[k.strip()] = v.strip().strip('"').strip("'")

aws_id = env_vars.get('AWS_ACCESS_KEY_ID', '')
aws_secret = env_vars.get('AWS_SECRET_ACCESS_KEY', '')

def test_region_models(region, models):
    print(f"\n=== Testing region: {region} ===")
    session = boto3.Session(
        aws_access_key_id=aws_id,
        aws_secret_access_key=aws_secret,
        region_name=region
    )
    client = session.client('bedrock-runtime')
    for model in models:
        print(f"Testing model: {model}...")
        body = json.dumps({
            'anthropic_version': 'bedrock-2023-05-31',
            'max_tokens': 10,
            'messages': [{'role': 'user', 'content': 'Say OK'}]
        })
        try:
            res = client.invoke_model(
                modelId=model,
                body=body
            )
            res_body = json.loads(res['body'].read().decode())
            print(f"  SUCCESS: {res_body['content'][0]['text'].strip()}")
        except Exception as e:
            print(f"  FAILED: {str(e)[:200]}")

# Test EU models in eu-central-1
test_region_models('eu-central-1', [
    'eu.anthropic.claude-sonnet-4-6',
    'eu.anthropic.claude-3-haiku-20240307-v1:0',
    'anthropic.claude-sonnet-4-6',
    'anthropic.claude-3-haiku-20240307-v1:0'
])

# Test US models in us-east-1
test_region_models('us-east-1', [
    'us.anthropic.claude-sonnet-4-6',
    'us.anthropic.claude-3-haiku-20240307-v1:0',
    'anthropic.claude-sonnet-4-6',
    'anthropic.claude-3-haiku-20240307-v1:0'
])
