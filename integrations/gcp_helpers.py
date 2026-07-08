import os
import urllib3
import requests
from google.oauth2 import service_account
import google.auth.transport.requests

def get_gcp_sa_path():
    """Wyszukuje ścieżkę do pliku klucza Service Account dla GCP."""
    # Definiujemy ścieżki względne i bezwzględne
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sa_paths = [
        os.path.expanduser("~/.hermes/gcp-sa-key.json"),
        os.path.join(current_dir, "holistic-dashboard-dev-dea2c872139e.json"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "holistic-dashboard-dev-dea2c872139e.json"),
        "holistic-dashboard-dev-dea2c872139e.json"
    ]
    for p in sa_paths:
        if os.path.exists(p):
            return p
    return None

def get_gcp_sa_credentials(scopes=['https://www.googleapis.com/auth/cloud-platform']):
    """
    Pobiera i odświeża poświadczenia Service Account GCP.
    Zwraca tuple (creds, token, error_message).
    """
    sa_path = get_gcp_sa_path()
    if not sa_path:
        return None, None, "Brak klucza GCP Service Account (szukano w ~/.hermes/gcp-sa-key.json oraz holistic-dashboard-dev-dea2c872139e.json)."
    
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        creds = service_account.Credentials.from_service_account_file(
            sa_path,
            scopes=scopes
        )
        session = requests.Session()
        session.verify = False
        request = google.auth.transport.requests.Request(session=session)
        creds.refresh(request)
        return creds, creds.token, None
    except Exception as e:
        return None, None, f"Błąd odświeżania poświadczeń GCP: {str(e)}"
