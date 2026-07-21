import os
import pickle
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def create_crm_database():
    print("Inicjalizacja Bazy Danych CRM w Google Sheets...")
    
    # Ładujemy token, który wygenerowaliśmy dla Brokera
    token_path = 'token_brokerholistic.pickle'
    
    if not os.path.exists(token_path):
        print(f"❌ Nie znaleziono pliku {token_path}. Najpierw uruchom auth.py!")
        return

    with open(token_path, 'rb') as token:
        creds = pickle.load(token)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    try:
        # Podłączamy się do Google Sheets API
        service = build('sheets', 'v4', credentials=creds)
        
        # Definicja nowego pliku (Arkusz Kalkulacyjny)
        spreadsheet = {
            'properties': {
                'title': 'Holistic_CRM_DB'
            },
            'sheets': [
                {
                    'properties': {
                        'title': 'Leady_Broker',
                        'gridProperties': {'frozenRowCount': 1}
                    }
                },
                {
                    'properties': {
                        'title': 'Leady_Jason_B2B',
                        'gridProperties': {'frozenRowCount': 1}
                    }
                }
            ]
        }
        
        spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId,spreadsheetUrl').execute()
        sheet_id = spreadsheet.get('spreadsheetId')
        sheet_url = spreadsheet.get('spreadsheetUrl')
        
        print(f"✅ Baza danych utworzona pomyślnie!")
        print(f"🔗 Link do bazy: {sheet_url}")
        print(f"🔑 ID Arkusza: {sheet_id}")
        
        # Wypełniamy nagłówki dla Brokera
        values_broker = [['Data', 'Imię i Nazwisko', 'Kontakt (Email/Tel)', 'Budżet', 'Rodzaj Inwestycji', 'Status', 'Źródło']]
        body_broker = {'values': values_broker}
        service.spreadsheets().values().update(
            spreadsheetId=sheet_id, range='Leady_Broker!A1:G1',
            valueInputOption='USER_ENTERED', body=body_broker).execute()
            
        # Wypełniamy nagłówki dla Jasona
        values_jason = [['Data', 'Imię i Nazwisko', 'Kontakt (Email/Tel)', 'Branża', 'Problem Biznesowy', 'Status', 'Źródło']]
        body_jason = {'values': values_jason}
        service.spreadsheets().values().update(
            spreadsheetId=sheet_id, range='Leady_Jason_B2B!A1:G1',
            valueInputOption='USER_ENTERED', body=body_jason).execute()

        print("✅ Nagłówki tabel (Broker i Jason) zostały zapisane.")
        print("\nSkopiuj 'ID Arkusza' do pliku .env jako GOOGLE_SHEET_ID_CRM")

    except Exception as e:
        print(f"❌ Wystąpił błąd podczas tworzenia bazy: {e}")
        print("Pamiętaj, aby włączyć 'Google Sheets API' i 'Google Drive API' w panelu Google Cloud!")

if __name__ == '__main__':
    create_crm_database()
