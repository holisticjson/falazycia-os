import os
import json
import glob
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes dla Google Business Profile
SCOPES = ['https://www.googleapis.com/auth/business.manage']

TOKENS_DIR = 'tokens/gbp'
CLIENT_SECRET_PATH = 'client_secret_gbp.json'

def get_all_gbp_credentials():
    """Pobiera wszystkie zapisane poświadczenia z folderu tokens/gbp."""
    creds_list = []
    token_files = glob.glob(os.path.join(TOKENS_DIR, "*.json"))
    
    for token_file in token_files:
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(token_file, 'w') as f:
                    f.write(creds.to_json())
            except Exception as e:
                print(f"Błąd odświeżania tokena {token_file}: {e}")
                continue
        if creds and creds.valid:
            creds_list.append(creds)
            
    return creds_list

def add_new_gbp_account():
    """Uruchamia proces OAuth2 dla nowego konta."""
    if not os.path.exists(CLIENT_SECRET_PATH):
        raise FileNotFoundError(f"Nie znaleziono pliku {CLIENT_SECRET_PATH}")
    
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
    creds = flow.run_local_server(port=0)
    
    # Używamy e-maila lub unikalnego ID jako nazwy pliku
    # W v2 Credentials nie ma bezpośrednio e-maila, ale możemy go pobrać lub użyć timestampa
    # Dla uproszczenia na razie używamy timestampa, docelowo pobierzemy info o koncie
    from datetime import datetime
    filename = f"token_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    token_path = os.path.join(TOKENS_DIR, filename)
    
    with open(token_path, 'w') as token:
        token.write(creds.to_json())
        
    return creds

if __name__ == "__main__":
    print("Dodawanie nowego konta Google Business Profile...")
    try:
        credentials = add_new_gbp_account()
        print(f"✅ Nowe konto dodane pomyślnie!")
    except Exception as e:
        print(f"❌ Błąd: {e}")
