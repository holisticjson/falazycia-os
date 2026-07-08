import os
import sys
import ssl

# Monkey patch urllib3 HTTPSConnectionPool to disable SSL checks globally
import urllib3
import ssl
orig_new_conn = urllib3.connectionpool.HTTPSConnectionPool._new_conn
def patch_new_conn(self):
    conn = orig_new_conn(self)
    if hasattr(conn, 'ssl_context') and conn.ssl_context:
        conn.ssl_context.check_hostname = False
        conn.ssl_context.verify_mode = ssl.CERT_NONE
    return conn
urllib3.connectionpool.HTTPSConnectionPool._new_conn = patch_new_conn
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set credentials path
sa_path = os.path.join(os.getcwd(), 'holistic-dashboard-dev-dea2c872139e.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_path

print(f"Setting GOOGLE_APPLICATION_CREDENTIALS to: {sa_path}")

try:
    from google import genai
    from google.genai import types
    
    print("Initializing GenAI Client with Vertex AI...")
    client = genai.Client(
        vertexai=True,
        project="holistic-dashboard-dev",
        location="us-central1"
    )
    
    # Try gemini-1.5-flash
    print("Generating content with gemini-1.5-flash...")
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents='Say "Hello, Holistic AI is working!"',
    )
    print("Success!")
    print(f"Response: {response.text}")

except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
