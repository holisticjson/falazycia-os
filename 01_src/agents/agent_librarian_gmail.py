import os
import base64
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import google.generativeai as genai

# KONFIGURACJA
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
KNOWLEDGE_BASE_DIR = r"c:\Aplikacje MVP\Holistic Jason\Baza_Wiedzy\Syntetyczna"
GEMINI_API_KEY = "AIzaSyBfcG1lyqbXh8jVbjONWLgwbt6vyQg4dGk" # Twój klucz

# Inicjalizacja Gemini (Aktualizacja do wersji 3.1 GA)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-3.1-flash-lite')

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def distill_email_content(subject, body):
    prompt = f"""
    Działaj jako Agent Bibliotekarz dla Holistic Jason. 
    Otrzymałeś newsletter o tytule: {subject}
    Treść: {body}
    
    ZADANIE: 
    1. Wyciągnij z tego newslettera tylko konkretne, techniczne porady lub trendy dotyczące AI i automatyzacji.
    2. Pomiń marketingowy "szum" i autopromocję.
    3. Stwórz z tego notatkę w formacie Markdown.
    4. Na początku dodaj sekcję 'ŹRÓDŁO: Newsletter - {subject}'.
    """
    response = model.generate_content(prompt)
    return response.text

def process_emails():
    service = get_gmail_service()
    # Szukamy maili z etykietą 'AI-NEWS' (możesz ją zmienić w Gmailu)
    results = service.users().messages().list(userId='me', q='label:AI-NEWS').execute()
    messages = results.get('messages', [])

    if not messages:
        print("Brak nowych newsletterów do przetworzenia.")
        return

    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        payload = txt['payload']
        headers = payload['headers']
        subject = ""
        for d in headers:
            if d['name'] == 'Subject':
                subject = d['value']
        
        # Wyciąganie treści (uproszczone dla plain text)
        body = ""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode()
        
        print(f"Przetwarzam: {subject}...")
        distilled_data = distill_email_content(subject, body)
        
        # Zapis do bazy wiedzy
        safe_subject = "".join([c for c in subject if c.isalnum() or c==' ']).rstrip()
        file_path = os.path.join(KNOWLEDGE_BASE_DIR, f"NEWSLETTER_{safe_subject}.md")
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(distilled_data)
        
        # Oznacz jako przetworzone (usuń etykietę AI-NEWS)
        service.users().messages().batchModify(userId='me', body={
            'ids': [msg['id']],
            'removeLabelIds': ['Label_ID_Zmienna'] # Tu trzeba będzie wpisać ID etykiety
        }).execute()
        print(f"Zapisano notatkę: {file_path}")

if __name__ == "__main__":
    process_emails()
