import http.server
import socketserver
import time
import threading
import sys
import json
import logging
from google.oauth2 import service_account
import google.auth.transport.requests
import urllib.request
import urllib.error

class UrllibResponse:
    def __init__(self, status_code, content, headers, text):
        self.status_code = status_code
        self.content = content
        self.headers = headers
        self.text = text

def http_post(url, json_data, headers, timeout=60.0):
    data_bytes = json.dumps(json_data).encode("utf-8")
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
    try:
        import ssl
        ctx = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
            status_code = response.getcode()
            response_content = response.read()
            resp_headers = {}
            for k, v in response.info().items():
                resp_headers[k] = v
            try:
                response_text = response_content.decode("utf-8")
            except:
                response_text = ""
            return UrllibResponse(status_code, response_content, resp_headers, response_text)
    except urllib.error.HTTPError as e:
        status_code = e.code
        try:
            response_content = e.read()
            response_text = response_content.decode("utf-8")
        except:
            response_content = str(e).encode("utf-8")
            response_text = str(e)
        resp_headers = {}
        for k, v in e.headers.items():
            resp_headers[k] = v
        return UrllibResponse(status_code, response_content, resp_headers, response_text)
    except Exception as e:
        err_msg = str(e).encode("utf-8")
        return UrllibResponse(500, err_msg, {}, str(e))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("gcp_vertex_proxy")

import os
import ssl
import urllib3
import requests

# Monkey patch urllib3 HTTPSConnectionPool to disable SSL checks globally
orig_new_conn = urllib3.connectionpool.HTTPSConnectionPool._new_conn
def patch_new_conn(self):
    conn = orig_new_conn(self)
    if hasattr(conn, 'ssl_context') and conn.ssl_context:
        conn.ssl_context.check_hostname = False
        conn.ssl_context.verify_mode = ssl.CERT_NONE
    return conn
urllib3.connectionpool.HTTPSConnectionPool._new_conn = patch_new_conn
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PORT = 8089

# Resolve GCP Service Account key
import os
possible_paths = [
    os.path.expanduser('~/.hermes/keys/coolfon-project-sa.json'),
    '/home/holisticjson/.hermes/keys/coolfon-project-sa.json',
    "coolfon-project-sa.json",
    os.path.expanduser('~/.hermes/keys/holistic-jaison-sa.json'),
    '/home/holisticjson/.hermes/keys/holistic-jaison-sa.json',
    "holistic-jaison-sa.json",
    os.path.expanduser('~/.hermes/keys/holistic-broker-sa.json'),
    '/home/holisticjson/.hermes/keys/holistic-broker-sa.json',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "holistic-broker-sa.json"),
    "holistic-broker-sa.json",
    "holistic-dashboard-dev-dea2c872139e.json",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "holistic-dashboard-dev-dea2c872139e.json")
]
SA_KEY_PATH = None
for p in possible_paths:
    if os.path.exists(p):
        SA_KEY_PATH = p
        break

PROJECT_ID = os.getenv("VERTEX_PROJECT", "coolfon-project")
if SA_KEY_PATH:
    try:
        with open(SA_KEY_PATH, "r") as f:
            sa_data = json.load(f)
            PROJECT_ID = sa_data.get("project_id", PROJECT_ID)
    except Exception as e:
        logger.error(f"Error reading project_id from SA key: {e}")

LOCATION = os.getenv("VERTEX_LOCATION", "us-central1")
TARGET_URL = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/openapi/chat/completions"

token_lock = threading.Lock()
creds = None
active_token = None
token_expiry = 0

def get_token():
    global active_token, token_expiry, creds
    with token_lock:
        now = time.time()
        if not active_token or now >= token_expiry - 60:
            logger.info(f"GCP OAuth token is missing or near expiry. Key path: {SA_KEY_PATH}")
            if creds is None:
                creds = service_account.Credentials.from_service_account_file(
                    SA_KEY_PATH,
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
            
            # Use non-verifying session for oauth token refresh
            session = requests.Session()
            session.verify = False
            request = google.auth.transport.requests.Request(session=session)
            creds.refresh(request)
            active_token = creds.token
            token_expiry = now + 3500
            logger.info("GCP OAuth token refreshed successfully.")
        return active_token

class VertexProxyHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Override to log via standard logger instead of stderr
        logger.info("%s - - %s" % (self.address_string(), format % args))

    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "service": "GCP Vertex Proxy"}).encode())
        elif self.path in ["/v1/models", "/models"]:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            models_data = {
                "object": "list",
                "data": [
                    {
                        "id": "google/gemini-2.0-flash",
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "google"
                    },
                    {
                        "id": "google/gemini-2.5-flash",
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "google"
                    },
                    {
                        "id": "google/gemini-2.5-pro",
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "google"
                    },
                    {
                        "id": "google/imagen-3.0-generate-001",
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "google"
                    },
                    {
                        "id": "google/gemini-1.5-pro",
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "google"
                    },
                    {
                        "id": "google/gemini-1.5-flash",
                        "object": "model",
                        "created": int(time.time()),
                        "owned_by": "google"
                    }
                ]
            }
            self.wfile.write(json.dumps(models_data).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path in ["/v1/chat/completions", "/chat/completions"]:
            # 1. Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                data = json.loads(body)
                # Map model names to expected publisher format if they don't have google/ prefix
                model_name = data.get("model", "")
                if model_name and not model_name.startswith("google/"):
                    data["model"] = f"google/{model_name}"
                logger.info(f"Proxying request for model: {data['model']}")
            except Exception as e:
                logger.error(f"Error parsing request payload: {e}")
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid JSON body")
                return

            # 2. Get GCP Token
            try:
                token = get_token()
            except Exception as e:
                logger.error(f"Failed to obtain GCP OAuth token: {e}")
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"Failed to authenticate with Google Cloud")
                return

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            # 3. Try multiple regions with fallback on HTTP 429 / RESOURCE_EXHAUSTED
            regions = ["us-central1", "us-east4", "europe-west1", "europe-west9", "us-west1"]
            response = None
            
            for idx, rgn in enumerate(regions):
                target_url = f"https://{rgn}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{rgn}/endpoints/openapi/chat/completions"
                logger.info(f"Attempt {idx+1}/{len(regions)}: Sending request to Vertex AI in region: {rgn}")
                logger.info(f"Request Payload: {json.dumps(data)}")
                try:
                    response = http_post(target_url, json_data=data, headers=headers, timeout=180.0)
                    logger.info(f"Vertex AI region {rgn} response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        break
                    elif response.status_code == 429:
                        logger.warning(f"Rate limit / Resource exhausted in region {rgn} (429). Response: {response.text[:250]}")
                        if idx < len(regions) - 1:
                            logger.info(f"Falling back to next region after a brief rate-limiting sleep (2.0s)...")
                            time.sleep(2.0)
                            continue
                        else:
                            logger.error("All regions exhausted with 429 Rate Limits.")
                    else:
                        logger.error(f"Non-retryable error {response.status_code} in region {rgn}: {response.text[:250]}")
                        break
                except Exception as e:
                    logger.error(f"Network / connection error in region {rgn}: {e}")
                    if idx < len(regions) - 1:
                        logger.info("Attempting fallback to next region...")
                        continue
                    else:
                        break
            
            if response is not None:
                self.send_response(response.status_code)
                for k, v in response.headers.items():
                    if k.lower() in ['content-type', 'cache-control']:
                        self.send_header(k, v)
                self.end_headers()
                self.wfile.write(response.content)
            else:
                self.send_response(502)
                self.end_headers()
                self.wfile.write(b"GCP Vertex AI Gateway Error")
        else:
            self.send_response(404)
            self.end_headers()

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

if __name__ == "__main__":
    logger.info(f"Starting GCP Vertex Proxy on port {PORT}...")
    server = ThreadedHTTPServer(("127.0.0.1", PORT), VertexProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down GCP Vertex Proxy...")
        server.server_close()
