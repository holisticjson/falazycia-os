import os
import sys

# Reconfigure stdout/stderr to utf-8 to prevent UnicodeEncodeError on Windows terminal
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

import pickle
import uvicorn
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request as FastAPIRequest
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from googleapiclient.discovery import build
from google.auth.transport.requests import Request as GoogleAuthRequest
from dotenv import load_dotenv

# Wczytujemy zmienne środowiskowe, m.in. GOOGLE_SHEET_ID_CRM
load_dotenv()

app = FastAPI(title="Holistic CRM Webhook API")

# Dodajemy CORS, aby strony HTML mogły bezpiecznie wysyłać zapytania POST z przeglądarki
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Docelowo w produkcji zamienimy na ["https://holistycznybroker.pl"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID_CRM")
TOKEN_PATH = "token_brokerholistic.pickle"

# Definiujemy strukturę danych, której spodziewamy się od Agenta frontendowego
class LeadPayload(BaseModel):
    project: str # Wartość: "broker" lub "jason"
    name: str
    contact: str
    budget: str = ""
    investment_type: str = ""
    industry: str = ""
    problem: str = ""
    source: str = "Website Form"

def get_sheets_service():
    if not os.path.exists(TOKEN_PATH):
        raise Exception("Brak pliku autoryzacji (token_brokerholistic.pickle)")
    with open(TOKEN_PATH, 'rb') as token:
        creds = pickle.load(token)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(GoogleAuthRequest())
    return build('sheets', 'v4', credentials=creds)

def forward_to_systeme_io(payload: LeadPayload):
    import requests
    import json
    systeme_webhook_url = os.getenv("SYSTEME_IO_WEBHOOK_URL")
    systeme_api_key = os.getenv("SYSTEME_IO_API_KEY")
    
    if not systeme_webhook_url and not systeme_api_key:
        print("Systeme.io not configured (missing SYSTEME_IO_WEBHOOK_URL or SYSTEME_IO_API_KEY). Skipping forwarding.")
        return
        
    success = False
    
    # 1. Forward via Webhook
    if systeme_webhook_url:
        try:
            data = {
                "name": payload.name,
                "email": payload.contact,
                "project": payload.project,
                "budget": payload.budget,
                "source": payload.source
            }
            res = requests.post(systeme_webhook_url, json=data, timeout=5)
            if res.status_code in [200, 201]:
                print(f"Forwarded lead to Systeme.io Webhook. Response: {res.status_code}")
                success = True
            else:
                print(f"Systeme.io Webhook returned status code: {res.status_code}")
        except Exception as e:
            print(f"Error forwarding to Systeme.io Webhook: {e}")
            
    # 2. Forward via API v2 (Bearer Auth)
    if systeme_api_key:
        try:
            url = "https://api.systeme.io/api/v2/contacts"
            headers = {
                "Authorization": f"Bearer {systeme_api_key}",
                "Content-Type": "application/json"
            }
            email = payload.contact if "@" in payload.contact else f"{payload.name.lower().replace(' ', '')}@example.com"
            data = {
                "email": email,
                "fields": [
                    {"slug": "first_name", "value": payload.name}
                ]
            }
            res = requests.post(url, headers=headers, json=data, timeout=5)
            if res.status_code in [200, 201, 409]: # 409 means contact already exists, which is acceptable
                print(f"Forwarded lead to Systeme.io API v2. Status: {res.status_code}")
                success = True
            else:
                print(f"Systeme.io API v2 error. Status: {res.status_code}, Body: {res.text}")
        except Exception as e:
            print(f"Error forwarding to Systeme.io API v2: {e}")
            
    # 3. Fallback Mechanism (RODO / Guardrails)
    if not success:
        fallback_path = r"c:\Aplikacje MVP\Holistic Jason\clients\leads_fallback.json"
        print(f"⚠️ Zapisywanie leadu do pliku fallback: {fallback_path}")
        lead_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": payload.name,
            "contact": payload.contact,
            "project": payload.project,
            "budget": payload.budget,
            "industry": payload.industry,
            "problem": payload.problem,
            "source": payload.source
        }
        try:
            existing = []
            if os.path.exists(fallback_path):
                with open(fallback_path, "r", encoding="utf-8") as f:
                    existing = json.load(f)
            existing.append(lead_data)
            with open(fallback_path, "w", encoding="utf-8") as f:
                json.dump(existing, f, indent=4, ensure_ascii=False)
        except Exception as ex:
            print(f"Blad zapisu pliku fallback: {ex}")


def add_to_streamlit_crm(payload: LeadPayload):
    import json
    crm_file = r"c:\Aplikacje MVP\Holistic Jason\dashboard\crm.json"
    
    # Upewniamy się, że katalog dashboard istnieje (uniknięcie FileNotFoundError)
    os.makedirs(os.path.dirname(crm_file), exist_ok=True)
    
    lead_id = f"lead_{int(datetime.now().timestamp())}"
    
    new_lead = {
        "id": lead_id,
        "name": payload.name,
        "stage": "conversation",
        "notes": f"Kontakt: {payload.contact} | Źródło: {payload.source}. " + (f"Problem: {payload.problem}" if payload.problem else "Zapis na e-book Bezpieczny Telefon."),
        "last_contact": datetime.now().strftime("%Y-%m-%d"),
        "next_action": "Skontaktować się lub sprawdzić status wysyłki Systeme.io",
        "draft_reply": f"Cześć {payload.name}, dziękuję za pobranie e-booka 'Prywatna Twierdza'. Jak oceniasz zawarte tam wskazówki dotyczące prywatności?"
    }
    
    try:
        crm_data = {"leads": []}
        if os.path.exists(crm_file):
            try:
                with open(crm_file, "r", encoding="utf-8") as f:
                    crm_data = json.load(f)
            except Exception as read_ex:
                print(f"⚠️ Błąd odczytu crm.json: {read_ex}. Tworzę nowy słownik.")
        
        if "leads" not in crm_data:
            crm_data["leads"] = []
            
        exists = False
        for lead in crm_data["leads"]:
            if payload.contact in lead.get("notes", "") or lead.get("name") == payload.name:
                lead["notes"] += f" | Ponowny zapis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                exists = True
                break
        
        if not exists:
            crm_data["leads"].append(new_lead)
            
        with open(crm_file, "w", encoding="utf-8") as f:
            json.dump(crm_data, f, indent=4, ensure_ascii=False)
            
        print(f"✅ Pomyślnie zsynchronizowano lead {payload.name} z CRM w Streamlicie (crm.json)")
    except Exception as e:
        print(f"⚠️ Błąd zapisu do Streamlit CRM (crm.json): {e}")


def send_custom_ebook_email(payload: LeadPayload):
    import json
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    email_to = payload.contact
    name = payload.name
    
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port_str = os.getenv("SMTP_PORT", "587")
    smtp_username = os.getenv("SMTP_USERNAME", "holisticjson@gmail.com")
    smtp_password = os.getenv("SMTP_PASSWORD", "").strip()
    smtp_from_name = os.getenv("SMTP_FROM_NAME", "Tomasz Duda | Holistic Jason")
    smtp_from_email = os.getenv("SMTP_FROM_EMAIL", "holisticjson@gmail.com")
    
    try:
        smtp_port = int(smtp_port_str)
    except:
        smtp_port = 587
        
    subject = "Twoja pancerna twierdza czeka — E-book: Bezpieczny Telefon 📱"
    
    # Text Body (Ghost v2 Style)
    text_content = f"""Siemanko {name}, tutaj Tomasz (Holistic Jason).

To jest nasze bezpośrednie, niezagłuszone przez algorytmy połączenie. Dzięki za zaufanie.

Zgodnie z obietnicą, Twój przewodnik "Prywatna Twierdza: Jak zabezpieczyć i odciążyć Androida w 15 minut" jest gotowy do czytania.

Otwórz e-booka bezpośrednio w przeglądarce pod poniższym linkiem (możesz go też wydrukować/zapisać jako PDF):
👉 https://mercury.holisticjson.pl/ebook_prywatna_twierdza.html

Co robimy teraz? Twój telefon potrzebuje oddechu. Wykonaj te 3 proste, szybkie kroki:

1. PRZENIEŚ TEGO MAILA do zakładki Główne (Primary), jeśli wpadł do Ofert lub Spamu. Dzięki temu nie ominą Cię kolejne bezpłatne poradniki i asynchroniczne triki.
2. POBIERZ DARMOWY KOMUNIKATOR MERKURY bezpośrednio z naszej strony (https://mercury.holisticjson.pl). To w pełni bezpieczna, szyfrowana lokalnie aplikacja bez centralnego serwera.
3. ODCIĄŻ SWÓJ TELEFON. Jeśli chcesz, żebym profesjonalnie usunął preinstalowane śmieci systemowe i fabryczne trackery z Twojego modelu (debloating systemowy, uwalniający baterię i RAM bez rootowania), po prostu odpisz bezpośrednio na tę wiadomość.

Bądź bezpieczny,
Tomasz Duda — Holistic Jason
"""

    # HTML Body (Luxury Dark Theme matching the website)
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bezpieczny Telefon: Prywatna Twierdza</title>
</head>
<body style="margin: 0; padding: 0; background-color: #0c0f14; font-family: 'Helvetica Neue', Arial, sans-serif; color: #f1f3f5; -webkit-font-smoothing: antialiased;">
    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #0c0f14; padding: 40px 10px;">
        <tr>
            <td align="center">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: rgba(30, 38, 50, 0.4); border: 1px solid rgba(130, 177, 255, 0.15); border-radius: 24px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.3);">
                    <!-- Header -->
                    <tr>
                        <td align="center" style="padding: 40px 40px 20px 40px; border-bottom: 1px solid rgba(255,255,255,0.05);">
                            <span style="font-size: 13px; font-weight: 700; color: #82b1ff; letter-spacing: 2px; text-transform: uppercase; display: block; margin-bottom: 12px;">BEZPOŚREDNIE POŁĄCZENIE</span>
                            <h1 style="color: #ffffff; font-size: 28px; font-weight: 700; margin: 0; line-height: 1.2;">Twoja pancerna twierdza czeka</h1>
                        </td>
                    </tr>
                    
                    <!-- Content -->
                    <tr>
                        <td style="padding: 40px; font-size: 15px; line-height: 1.6; color: #e1e4e6;">
                            <p style="margin-top: 0; margin-bottom: 24px;">Siemanko <strong>{name}</strong>, tutaj Tomasz (Holistic Jason).</p>
                            
                            <p style="margin-bottom: 24px;">To jest nasze bezpośrednie, niezagłuszone przez algorytmy połączenie. Dzięki za zaufanie.</p>
                            
                            <p style="margin-bottom: 32px;">Zgodnie z obietnicą, Twój przewodnik <strong>"Prywatna Twierdza: Jak zabezpieczyć i odciążyć Androida w 15 minut"</strong> jest już gotowy do czytania.</p>
                            
                            <!-- Button CTA -->
                            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 36px;">
                                <tr>
                                    <td align="center">
                                        <a href="https://mercury.holisticjson.pl/ebook_prywatna_twierdza.html" target="_blank" style="display: inline-block; padding: 16px 36px; background-color: #82b1ff; color: #002f6c; font-size: 16px; font-weight: bold; text-decoration: none; border-radius: 12px; box-shadow: 0 8px 30px rgba(130, 177, 255, 0.25); text-align: center;">
                                            Otwórz E-book (PDF / HTML)
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            
                            <!-- Steps List -->
                            <div style="background-color: rgba(12, 15, 20, 0.6); border: 1px solid rgba(130, 177, 255, 0.05); border-radius: 16px; padding: 24px; margin-bottom: 32px;">
                                <h3 style="color: #82b1ff; font-size: 14px; font-weight: 700; margin-top: 0; margin-bottom: 16px; text-transform: uppercase; letter-spacing: 0.5px;">📋 Co robimy teraz? Wykonaj 3 szybkie kroki:</h3>
                                <ul style="list-style: none; padding-left: 0; margin: 0;">
                                    <li style="margin-bottom: 16px; display: flex; align-items: flex-start;">
                                        <span style="background-color: rgba(130,177,255,0.12); color: #82b1ff; font-weight: bold; width: 22px; height: 22px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; margin-right: 12px; flex-shrink: 0; margin-top: 2px;">1</span>
                                        <span style="font-size: 14px; line-height: 1.5;"><strong>Przenieś tego maila do skrzynki głównej (Primary)</strong>, jeśli wpadł do Ofert lub Spamu. Dzięki temu nie ominą Cię kolejne bezpłatne poradniki i asynchroniczne triki.</span>
                                    </li>
                                    <li style="margin-bottom: 16px; display: flex; align-items: flex-start;">
                                        <span style="background-color: rgba(130,177,255,0.12); color: #82b1ff; font-weight: bold; width: 22px; height: 22px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; margin-right: 12px; flex-shrink: 0; margin-top: 2px;">2</span>
                                        <span style="font-size: 14px; line-height: 1.5;"><strong>Pobierz darmowy komunikator Merkury</strong> bezpośrednio z naszej strony <a href="https://mercury.holisticjson.pl" target="_blank" style="color: #82b1ff; text-decoration: underline;">mercury.holisticjson.pl</a>. To w pełni bezpieczna, szyfrowana lokalnie aplikacja bez centralnego serwera.</span>
                                    </li>
                                    <li style="margin-bottom: 0; display: flex; align-items: flex-start;">
                                        <span style="background-color: rgba(130,177,255,0.12); color: #82b1ff; font-weight: bold; width: 22px; height: 22px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 12px; margin-right: 12px; flex-shrink: 0; margin-top: 2px;">3</span>
                                        <span style="font-size: 14px; line-height: 1.5;"><strong>Odciąż swój telefon.</strong> Jeśli chcesz, żebym profesjonalnie usunął preinstalowane śmieci systemowe i fabryczne trackery z Twojego modelu (debloating uwalniający baterię i RAM bez rootowania), po prostu <strong>odpisz bezpośrednio na tę wiadomość</strong>.</span>
                                    </li>
                                </ul>
                            </div>
                            
                            <p style="margin-top: 0; margin-bottom: 0; font-size: 14px; color: #90a4ae;">
                                Trzymaj się bezpiecznie,<br>
                                <strong style="color: #ffffff;">Tomasz Duda — Holistic Jason</strong>
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding: 24px; background-color: rgba(12, 15, 20, 0.8); border-top: 1px solid rgba(255,255,255,0.05); font-size: 11px; color: #90a4ae; line-height: 1.4;">
                            Dbamy o Twoją prywatność. Ta wiadomość została wysłana automatycznie po Twoim zapisie na stronie mercury.holisticjson.pl.<br>
                            Zgodę na newsletter możesz wycofać w każdej chwili pisząc na kontakt@holisticjson.pl.<br>
                            &copy; 2026 Holistic Jason. Wszelkie prawa zastrzeżone.
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""

    # Check if SMTP_PASSWORD is set.
    if not smtp_password:
        fallback_path = r"c:\Aplikacje MVP\Holistic Jason\clients\emails_outbox_offline.json"
        print("\n" + "="*80)
        print("⚠️  ZASADA PROAKTYWNEJ WERYFIKACJI: BRAK HASŁA SMTP_PASSWORD W PLIKU .ENV!")
        print("="*80)
        print("Nie możemy w tej chwili fizycznie wysłać maila powitalnego do klienta.")
        print(f"E-mail został pomyślnie zakolejkowany w trybie fail-safe (Offline Queue) w:")
        print(f"👉 {fallback_path}")
        print("\nINSTRUKTYWNA CHECKLISTA JAK TO ROZWIĄZAĆ:")
        print("1. Otwórz plik .env znajdujący się w folderze: c:\\Aplikacje MVP\\Holistic Jason\\.env")
        print("2. Znajdź sekcję SMTP i ustaw zmienną:")
        print("   SMTP_PASSWORD=twoje_haslo_aplikacji_gmail")
        print("   (Wskazówka: Użyj hasła aplikacji Google z konta holisticjson@gmail.com)")
        print("3. Zapisz plik .env. Następne zapisy na e-booka zostaną wysłane automatycznie!")
        print("="*80 + "\n")
        
        # Save to offline outbox file
        queue_item = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "email_to": email_to,
            "name": name,
            "subject": subject,
            "body_text": text_content,
            "status": "queued_offline_no_smtp_password"
        }
        try:
            os.makedirs(os.path.dirname(fallback_path), exist_ok=True)
            existing_queue = []
            if os.path.exists(fallback_path):
                with open(fallback_path, "r", encoding="utf-8") as f:
                    try:
                        existing_queue = json.load(f)
                    except:
                        pass
            existing_queue.append(queue_item)
            with open(fallback_path, "w", encoding="utf-8") as f:
                json.dump(existing_queue, f, indent=4, ensure_ascii=False)
        except Exception as queue_ex:
            print(f"⚠️ Błąd zapisu do kolejki offline: {queue_ex}")
        return False

    # Send the email via SMTP
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{smtp_from_name} <{smtp_from_email}>"
        msg['To'] = email_to
        
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        
        msg.attach(part1)
        msg.attach(part2)
        
        print(f"📨 Próba fizycznej wysyłki e-booka przez SMTP ({smtp_host}:{smtp_port}) do: {email_to}...")
        
        # Connect to SMTP
        server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
        server.ehlo()
        server.starttls() # Secure connection with TLS
        server.ehlo()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_from_email, email_to, msg.as_string())
        server.quit()
        
        print(f"✅ E-mail powitalny z E-bookiem został pomyślnie wysłany przez SMTP do: {email_to}")
        return True
        
    except Exception as smtp_err:
        print(f"❌ Błąd wysyłki SMTP do {email_to}: {smtp_err}")
        
        # Save to offline queue as fallback
        fallback_path = r"c:\Aplikacje MVP\Holistic Jason\clients\emails_outbox_offline.json"
        queue_item = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "email_to": email_to,
            "name": name,
            "subject": subject,
            "body_text": text_content,
            "error": str(smtp_err),
            "status": "queued_offline_smtp_error"
        }
        try:
            os.makedirs(os.path.dirname(fallback_path), exist_ok=True)
            existing_queue = []
            if os.path.exists(fallback_path):
                with open(fallback_path, "r", encoding="utf-8") as f:
                    try:
                        existing_queue = json.load(f)
                    except:
                        pass
            existing_queue.append(queue_item)
            with open(fallback_path, "w", encoding="utf-8") as f:
                json.dump(existing_queue, f, indent=4, ensure_ascii=False)
            print(f"⚠️ E-mail został zapisany do kolejki offline z powodu błędu SMTP.")
        except Exception as q_ex:
            print(f"Błąd zapisu kolejki fallback: {q_ex}")
        return False


@app.post("/api/lead")
async def receive_lead(payload: LeadPayload):
    try:
        service = get_sheets_service()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Logika wyboru odpowiedniej zakładki w Arkuszu na podstawie payloadu
        if payload.project.lower() == "broker":
            range_name = "Leady_Broker!A:G"
            values = [[
                current_time,
                payload.name,
                payload.contact,
                payload.budget,
                payload.investment_type,
                "NOWY",
                payload.source
            ]]
        else:
            range_name = "Leady_Jason_B2B!A:G"
            values = [[
                current_time,
                payload.name,
                payload.contact,
                payload.industry,
                payload.problem,
                "NOWY",
                payload.source
            ]]
            
        body = {'values': values}
        
        # Fizyczny zapis do Google Sheets
        result = service.spreadsheets().values().append(
            spreadsheetId=GOOGLE_SHEET_ID,
            range=range_name,
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        
        print(f"✅ Zapisano nowy lead: {payload.name} do projektu {payload.project}")
        
        # Synchronizacja z CRM w Streamlicie (crm.json)
        add_to_streamlit_crm(payload)
        
        # Forward to Systeme.io or handle custom transactional email for Mercury Ebook
        if payload.source == "Mercury Ebook":
            # For Mercury E-book, we use our own custom, free SMTP transactional mailer
            send_custom_ebook_email(payload)
        else:
            # For other lead sources (like Ebook #2), forward to Systeme.io
            forward_to_systeme_io(payload)
        
        return {"status": "success", "message": "Lead zapisany poprawnie", "updatedCells": result.get("updates", {}).get("updatedCells")}
        
    except Exception as e:
        print(f"❌ Błąd zapisu: {e}")
        raise HTTPException(status_code=500, detail=str(e))

import sqlite3
import uuid
import tempfile
import subprocess

def get_db_connection():
    conn = sqlite3.connect("local_crm.db", timeout=5.0)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=5000;")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS systeme_events (
            id TEXT PRIMARY KEY,
            contact_email TEXT,
            event_type TEXT,
            utm_source TEXT,
            utm_campaign TEXT,
            amount REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def upload_to_gcs_silos(report_content: str, filename: str):
    try:
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.md') as f:
            f.write(report_content)
            temp_path = f.name
        
        print(f"Raport {filename} gotowy. Próba uploadu do gs://holistic_kubelek/silos-cmo/raporty/")
        subprocess.run(['gsutil', 'cp', temp_path, f"gs://holistic_kubelek/silos-cmo/raporty/{filename}"], capture_output=True, check=False)
        os.unlink(temp_path)
    except Exception as e:
        print(f"Error uploading to GCS: {e}")

@app.post("/webhook/systeme-io")
async def systeme_io_webhook(request: FastAPIRequest):
    try:
        payload = await request.json()
        event_type = payload.get("type", "unknown")
        
        # Struktura payloadu Systeme.io zazwyczaj opakowuje kontakt i dane zamówienia
        data = payload.get("data", payload)
        contact = data.get("contact", {})
        email = contact.get("email", "unknown")
        
        utm_source = contact.get("utm_source", data.get("utm_source", "unknown"))
        utm_campaign = contact.get("utm_campaign", data.get("utm_campaign", "unknown"))
        
        amount = 0.0
        if "sale" in event_type.lower():
            amount = float(data.get("transaction", {}).get("amount", 0.0))
            
        event_id = str(uuid.uuid4())
        
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO systeme_events (id, contact_email, event_type, utm_source, utm_campaign, amount) VALUES (?, ?, ?, ?, ?, ?)",
            (event_id, email, event_type, utm_source, utm_campaign, amount)
        )
        conn.commit()
        conn.close()
        
        report_md = f"""# Raport Zdarzenia Systeme.io: {event_type}
- **ID Zdarzenia:** {event_id}
- **Data:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **Email Klienta:** {email}
- **UTM Source:** {utm_source}
- **UTM Campaign:** {utm_campaign}
- **Przychód (Cash Collected):** {amount} PLN

Wniosek systemowy: Zdarzenie '{event_type}' poprawnie zarejestrowane dla {email}. 
"""
        filename = f"report_{event_id}.md"
        upload_to_gcs_silos(report_md, filename)
        
        return {"status": "success", "event_id": event_id}
    except Exception as e:
        print(f"Webhook processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🌍 Nasłuchiwanie na przychodzące Leady pod adresem: http://localhost:8000/api/lead")
    uvicorn.run("webhook_api:app", host="0.0.0.0", port=8000, reload=False)
