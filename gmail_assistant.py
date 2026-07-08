import os
import pickle
import base64
import json
import re
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import requests

# Zgodnie z wytycznymi Juliana Goldi - organizacja cold maili, wyciąganie leadów i analizowanie szans SEO.
# Ten skrypt będzie pobierał najnowsze maile i kategoryzował je przy użyciu Llama/Gemini poprzez LiteLLM.

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
LITELLM_URL = "http://localhost:4000/v1/chat/completions"

def get_all_gmail_services():
    services = []
    # Znajdź wszystkie pliki zaczynające się od 'token_' (np. token_tom.pickle, token_info.pickle)
    token_files = [f for f in os.listdir('.') if f.startswith('token_') and f.endswith('.pickle')]
    
    if not token_files:
        print("\n[BŁĄD] Nie znaleziono żadnych plików 'token_*.pickle'.")
        print("Aby podłączyć 3 lub więcej kont zgodnie z metodologią Juliana Goldi:")
        print("1. Pobierz credentials.json z Google Cloud.")
        print("2. Uruchom skrypt uwierzytelniający (auth.py) dla każdego konta, by wygenerować token_konto1.pickle, token_konto2.pickle itd.")
        print("Obecny skrypt będzie obsługiwał wszystkie odnalezione pliki tokenów.")
        return services

    for token_file in token_files:
        creds = None
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)
            
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    with open(token_file, 'wb') as token:
                        pickle.dump(creds, token)
                except Exception as e:
                    print(f"Nie udało się odświeżyć tokena {token_file}: {e}")
                    continue
            else:
                print(f"Token {token_file} jest niepoprawny i nie można go odświeżyć.")
                continue
                
        try:
            service = build('gmail', 'v1', credentials=creds)
            services.append({"name": token_file.replace('token_', '').replace('.pickle', ''), "service": service})
        except Exception as e:
            print(f"Błąd inicjalizacji serwisu dla {token_file}: {e}")
            
    return services

def extract_email_body(payload):
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    body += base64.urlsafe_b64decode(data).decode('utf-8')
            elif part['mimeType'] == 'text/html':
                continue # Pomiń HTML jeśli mamy plain text, albo dodaj logikę parsowania HTML (np. BeautifulSoup)
            elif 'parts' in part:
                body += extract_email_body(part)
    else:
        data = payload['body'].get('data')
        if data:
            body = base64.urlsafe_b64decode(data).decode('utf-8')
    return body

def analyze_with_llm(subject, sender, body):
    prompt = f"""
Jesteś zaawansowanym Asystentem Skrzynki Pocztowej opartym na strategiach Juliana Goldi.
Masz do przeanalizowania poniższego maila. Twoim zadaniem jest skategoryzowanie go do jednego z 4 tagów:
1. LEAD - Potencjalny klient, odpowiedź na cold mail, zainteresowanie usługą.
2. SEO_OPPORTUNITY - Propozycja guest posta, link buildingu, wymiany linków.
3. INVOICE - Faktura, płatność, koszty operacyjne (do wpięcia w KSeF/Finanse).
4. NEWSLETTER - Inspiracje, branżowe newsy, spam (do modułu Brain Dump).

Zwróć wynik jako JSON w formacie:
{{"kategoria": "LEAD", "podsumowanie": "krótkie podsumowanie 1 zdanie", "waznosc": 1-5}}

Mail:
Od: {sender}
Temat: {subject}
Treść:
{body[:2000]} # Ograniczamy do 2000 znaków
"""
    try:
        response = requests.post(LITELLM_URL, json={
            "model": "google/gemini-2.5-flash", # lub Llama-3 przez LiteLLM
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1
        })
        content = response.json()['choices'][0]['message']['content']
        # Wyciągamy JSON
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        return {"kategoria": "NIEZNANA", "podsumowanie": "Błąd parsowania LLM", "waznosc": 1}
    except Exception as e:
        print(f"Błąd LLM: {e}")
        return {"kategoria": "BŁĄD", "podsumowanie": str(e), "waznosc": 1}

def create_or_get_label(service, user_id, label_name):
    try:
        results = service.users().labels().list(userId=user_id).execute()
        labels = results.get('labels', [])
        for label in labels:
            if label['name'].upper() == label_name.upper():
                return label['id']
        
        # Stwórz jeśli nie istnieje
        label = {'name': label_name, 'labelListVisibility': 'labelShow', 'messageListVisibility': 'show'}
        created_label = service.users().labels().create(userId=user_id, body=label).execute()
        return created_label['id']
    except Exception as e:
        print(f"Błąd podczas zarządzania etykietami: {e}")
        return None



def process_inbox():
    print("Uruchamianie Multi-Inbox Gmail Assistant (Metodologia Juliana Goldi)...")
    accounts = get_all_gmail_services()
    if not accounts:
        print("Nie znaleziono autoryzowanych kont. Przerywam.")
        return

    print(f"Podłączono kont Google: {len(accounts)}")
    
    for account in accounts:
        service = account['service']
        account_name = account['name']
        print(f"\n[{account_name}] Sprawdzanie skrzynki...")
        
        try:
            results = service.users().messages().list(userId='me', q='is:unread', maxResults=10).execute()
            messages = results.get('messages', [])

            if not messages:
                print(f"[{account_name}] Brak nowych wiadomości w Inboxie.")
                continue

            print(f"[{account_name}] Znaleziono {len(messages)} nowych wiadomości. Analizowanie...")
            
            for msg in messages:
                try:
                    msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
                    payload = msg_data['payload']
                    headers = payload['headers']
                    
                    subject = next((h['value'] for h in headers if h['name'].lower() == 'subject'), "Brak Tematu")
                    sender = next((h['value'] for h in headers if h['name'].lower() == 'from'), "Nieznany")
                    
                    print(f"\nAnaliza: [{sender}] - {subject}")
                    body = extract_email_body(payload)
                    
                    analysis = analyze_with_llm(subject, sender, body)
                    kategoria = analysis.get("kategoria", "NIEZNANA")
                    waznosc = analysis.get("waznosc", 1)
                    podsumowanie = analysis.get("podsumowanie", "")
                    
                    print(f" => Wynik: {kategoria} (Ważność: {waznosc}/5) - {podsumowanie}")
                    
                    label_id = create_or_get_label(service, 'me', f"HolisticAI/{kategoria}")
                    if label_id:
                        service.users().messages().modify(
                            userId='me', id=msg['id'],
                            body={'addLabelIds': [label_id], 'removeLabelIds': ['UNREAD']}
                        ).execute()
                        print(f" => Oznaczono etykietą HolisticAI/{kategoria} i usunięto z nieprzeczytanych.")
                        
                except Exception as e:
                    print(f"[{account_name}] Błąd podczas przetwarzania wiadomości {msg['id']}: {e}")
        except Exception as e:
            print(f"[{account_name}] Błąd połączenia z API: {e}")

if __name__ == '__main__':
    process_inbox()
