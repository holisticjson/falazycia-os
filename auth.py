import os
import pickle
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def authenticate(credentials_file, token_name):
    """
    Uwierzytelnia konto na podstawie pliku credentials i zapisuje token.
    """
    creds = None
    token_file = f'token_{token_name}.pickle'

    # Sprawdź czy plik credentials istnieje
    if not os.path.exists(credentials_file):
        print(f"[BŁĄD] Nie znaleziono pliku: {credentials_file}")
        return

    print(f"Rozpoczynam uwierzytelnianie na podstawie {credentials_file}...")
    
    # Inicjalizuj proces logowania (wymaga przeglądarki)
    try:
        flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
        creds = flow.run_local_server(port=0)
    except Exception as e:
        print(f"[BŁĄD] Błąd podczas autoryzacji: {e}")
        return

    # Zapisz token, by nie trzeba było logować się ponownie
    with open(token_file, 'wb') as token:
        pickle.dump(creds, token)
        
    print(f"[SUKCES] Pomyślnie utworzono {token_file}! Konto zostało podłączone do asystenta.")

if __name__ == '__main__':
    print("=== Generator Kluczy Dostępów (Dual-GCP) ===")
    
    # Domyślne wartości
    cred_file = "credentials_broker.json"
    t_name = "brokerholistic"

    if len(sys.argv) == 3:
        cred_file = sys.argv[1]
        t_name = sys.argv[2]
    else:
        print("Uruchamianie z domyślnymi parametrami dla Holistic Broker.")
        print("Aby uruchomić dla innego konta użyj: python auth.py <plik_credentials.json> <nazwa_konta>")
        
    authenticate(cred_file, t_name)
