import os
import json
import time
import requests

class SystemeIOClient:
    def __init__(self):
        # Pobieranie klucza API z zmiennych środowiskowych
        self.api_key = os.environ.get("SYSTEME_IO_API_KEY")
        self.base_url = "https://api.systeme.io/api"
        self.headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }


    def _save_fallback_lead(self, email, first_name, custom_fields=None, error_msg=""):
        """Zapisuje dane leada lokalnie w przypadku awarii API Systeme.io."""
        fallback_file = os.path.join("clients", "leads_fallback.json")
        os.makedirs("clients", exist_ok=True)
        
        lead_data = {
            "email": email,
            "first_name": first_name,
            "custom_fields": custom_fields or {},
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "error": error_msg
        }
        
        leads = []
        if os.path.exists(fallback_file):
            try:
                with open(fallback_file, "r", encoding="utf-8") as f:
                    leads = json.load(f)
            except Exception:
                leads = []
                
        leads.append(lead_data)
        
        try:
            with open(fallback_file, "w", encoding="utf-8") as f:
                json.dump(leads, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False

    def add_contact(self, email, first_name, custom_fields=None):
        """
        Dodaje kontakt do Systeme.io.
        W przypadku błędu API, automatycznie zapisuje leada do pliku awaryjnego.
        """
        if not self.api_key:
            err_msg = "Brak klucza SYSTEME_IO_API_KEY w pliku .env"
            self._save_fallback_lead(email, first_name, custom_fields, err_msg)
            return {"status": "error", "message": err_msg, "fallback": True}
            
        url = f"{self.base_url}/contacts"
        payload = {
            "email": email,
            "fields": [
                {"slug": "first_name", "value": first_name}
            ]
        }
        
        if custom_fields:
            for slug, val in custom_fields.items():
                payload["fields"].append({"slug": slug, "value": val})
                
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            if response.status_code in [200, 201]:
                return {"status": "success", "data": response.json(), "fallback": False}
            elif response.status_code == 409:
                return {"status": "exists", "message": "Kontakt już istnieje w systemie.", "fallback": False}
            else:
                err_msg = f"API Error {response.status_code}: {response.text}"
                self._save_fallback_lead(email, first_name, custom_fields, err_msg)
                return {"status": "error", "message": err_msg, "fallback": True}
        except Exception as e:
            err_msg = f"Wyjątek sieciowy: {str(e)}"
            self._save_fallback_lead(email, first_name, custom_fields, err_msg)
            return {"status": "error", "message": err_msg, "fallback": True}

    def subscribe_to_campaign(self, contact_id, campaign_id):
        """
        Subskrybuje kontakt do określonej kampanii (autoresponder).
        """
        if not self.api_key:
            return {"status": "error", "message": "Brak klucza API"}
            
        url = f"{self.base_url}/campaigns/{campaign_id}/subscriptions"
        payload = {"contactId": contact_id}
        
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            if response.status_code in [200, 201]:
                return {"status": "success", "data": response.json()}
            else:
                return {"status": "error", "message": f"Błąd {response.status_code}: {response.text}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def add_tag_to_contact(self, contact_id, tag_id):
        """
        Dodaje tag do kontaktu (ograniczenie darmowego planu: 1 tag).
        """
        if not self.api_key:
            return {"status": "error", "message": "Brak klucza API"}
            
        url = f"{self.base_url}/tags/{tag_id}/subscriptions"
        payload = {"contactId": contact_id}
        
        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            if response.status_code in [200, 201]:
                return {"status": "success", "data": response.json()}
            else:
                return {"status": "error", "message": f"Błąd {response.status_code}: {response.text}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_contacts(self):
        """
        Pobiera listę kontaktów z Systeme.io.
        """
        if not self.api_key:
            return {"status": "error", "message": "Brak klucza API"}
            
        url = f"{self.base_url}/contacts"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return {"status": "success", "data": response.json()}
            else:
                return {"status": "error", "message": f"Błąd {response.status_code}: {response.text}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
