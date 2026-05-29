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
        with urllib.request.urlopen(req, timeout=timeout) as response:
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

PORT = 8089
SA_KEY_PATH = '/home/holisticjson/.hermes/gcp-sa-key.json'
PROJECT_ID = "holistic-dashboard-dev"
LOCATION = "us-central1"
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
            logger.info("GCP OAuth token is missing or near expiry. Refreshing...")
            if creds is None:
                creds = service_account.Credentials.from_service_account_file(
                    SA_KEY_PATH,
                    scopes=['https://www.googleapis.com/auth/cloud-platform']
                )
            request = google.auth.transport.requests.Request()
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

            # 3. Stream request/response from/to client
            try:
                # We do a standard post first if we want to log errors easily, or just read the first chunk of stream if it fails.
                # Actually, let's just make a standard request, read response, and stream it if successful, or log if error.
                # Since we don't have extremely large payloads, a standard request (non-stream) is simpler and much easier to debug!
                # Let's change the proxy to use standard non-streaming POST for reliability and ease of logging, then we can add streaming if needed.
                logger.info(f"Sending request to Vertex AI: {TARGET_URL}")
                logger.info(f"Request Headers: {json.dumps({k: v for k, v in headers.items() if k != 'Authorization'})} (Auth Token Length: {len(headers.get('Authorization', ''))})")
                logger.info(f"Request Payload: {json.dumps(data)}")
                response = http_post(TARGET_URL, json_data=data, headers=headers, timeout=60.0)
                logger.info(f"Vertex AI response status: {response.status_code}")
                
                if response.status_code == 200:
                    self.send_response(200)
                    for k, v in response.headers.items():
                        if k.lower() in ['content-type', 'cache-control']:
                            self.send_header(k, v)
                    self.end_headers()
                    self.wfile.write(response.content)
                else:
                    logger.error(f"Vertex AI returned error {response.status_code}: {response.text}")
                    self.send_response(response.status_code)
                    self.end_headers()
                    self.wfile.write(response.content)
            except Exception as e:
                logger.error(f"Error during proxying to GCP: {e}")
                try:
                    self.send_response(502)
                    self.end_headers()
                    self.wfile.write(b"GCP Vertex AI Gateway Error")
                except Exception:
                    pass
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
