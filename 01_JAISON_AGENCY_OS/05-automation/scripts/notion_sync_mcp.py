import os
import requests
import json
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def sync_to_database(api_url, auth_token, data_payload, db_type="generic"):
    """
    Skrypt zastępczy MCP (Low-Cost) używany przez C-Level Agentów do wypychania danych
    do zewnętrznych baz (Supabase, Notion, Airtable) za darmo, poprzez bezpośrednie REST API.
    """
    logging.info(f"Rozpoczynanie synchronizacji danych dla bazy typu: {db_type}")
    
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
    
    # Przykładowe nagłówki dla Notion
    if db_type == "notion":
        headers["Notion-Version"] = "2022-06-28"
        
    try:
        response = requests.post(api_url, headers=headers, json=data_payload)
        response.raise_for_status()
        logging.info("Synchronizacja zakończona sukcesem! 🚀")
        return True
    except requests.exceptions.HTTPError as err:
        logging.error(f"HTTP Error podczas synchronizacji: {err}")
        logging.error(f"Response: {response.text}")
        return False
    except Exception as e:
        logging.error(f"Błąd krytyczny: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AntiGravity Generic DB Sync Tool (MCP Alternative)")
    parser.add_argument("--url", required=True, help="API Endpoint URL")
    parser.add_argument("--data-file", required=True, help="Ścieżka do pliku JSON z danymi do wgrania")
    parser.add_argument("--type", default="generic", help="Typ bazy (notion, supabase, generic)")
    
    args = parser.parse_args()
    
    AUTH_TOKEN = os.environ.get("DB_SYNC_TOKEN")
    
    if not AUTH_TOKEN:
        logging.error("Brak poświadczeń (DB_SYNC_TOKEN)! Upewnij się, że .env jest załadowany.")
        exit(1)
        
    try:
        with open(args.data_file, 'r', encoding='utf-8') as f:
            payload = json.load(f)
    except Exception as e:
        logging.error(f"Nie można wczytać pliku payloadu: {str(e)}")
        exit(1)
        
    success = sync_to_database(args.url, AUTH_TOKEN, payload, args.type)
    if not success:
        exit(1)
