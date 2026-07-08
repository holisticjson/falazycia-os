import urllib.request
import json
import sys

def test_model(model_id):
    print(f"Testing model: {model_id}...")
    req = urllib.request.Request(
        'http://127.0.0.1:4000/v1/chat/completions',
        data=json.dumps({
            'model': model_id,
            'messages': [{'role': 'user', 'content': 'Hello, respond with exactly "OK" if you can read this.'}],
            'max_tokens': 100
        }).encode(),
        headers={
            'Authorization': 'Bearer sk-hermes-local',
            'Content-Type': 'application/json'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res = json.loads(response.read().decode())
            text = res['choices'][0]['message']['content'].strip()
            print(f"  -> SUCCESS! Response: {text}")
            return True
    except Exception as e:
        print(f"  -> FAILED: {e}")
        if hasattr(e, 'read'):
            print(f"     Details: {e.read().decode()}")
        return False

# Run tests
fast_ok = test_model('hermes-fast')
bedrock_ok = test_model('bedrock/anthropic.claude-sonnet-4-6')

if fast_ok and bedrock_ok:
    print("\n=== ALL TESTS PASSED! Both Vertex AI and AWS Bedrock are working! ===")
    sys.exit(0)
else:
    print("\n=== SOME TESTS FAILED! ===")
    sys.exit(1)
