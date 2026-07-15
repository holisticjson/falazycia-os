import os
import requests
from dotenv import load_dotenv

# Preload environment
load_dotenv()

def get_env_var(var_name):
    """Pobiera zmienną środowiskową z .env lub systemu w sposób odporny."""
    load_dotenv()
    return os.environ.get(var_name) or os.getenv(var_name)

def hunter_domain_search(domain):
    """Wyszukuje publiczne adresy e-mail dla danej domeny przez Hunter.io API."""
    key = get_env_var("HUNTER_API_KEY")
    if not key:
        return {"success": False, "error": "Missing HUNTER_API_KEY in .env"}
        
    try:
        if any(x in key.lower() for x in ["simulated", "mock", "test", "your_"]):
            return {
                "success": True,
                "data": {
                    "pattern": "{first}.{last}",
                    "emails": [
                        {
                            "value": f"office@{domain}",
                            "first_name": "Office",
                            "last_name": "Team",
                            "position": "Support"
                        },
                        {
                            "value": f"tomasz@{domain}",
                            "first_name": "Tomasz",
                            "last_name": "Kowalski",
                            "position": "CEO"
                        }
                    ]
                }
            }
            
        url = "https://api.hunter.io/v2/domain-search"
        params = {
            "domain": domain,
            "api_key": key
        }
        res = requests.get(url, params=params, timeout=15)
        if res.status_code == 200:
            return {"success": True, "data": res.json().get("data", {})}
        else:
            return {"success": False, "error": f"Hunter.io API returned status code {res.status_code}: {res.text}"}
    except Exception as e:
        return {"success": False, "error": f"Hunter.io request failed: {str(e)}"}

def hunter_verify_email(email):
    """Weryfikuje dostarczalność adresu e-mail przez Hunter.io API."""
    key = get_env_var("HUNTER_API_KEY")
    if not key:
        return {"success": False, "error": "Missing HUNTER_API_KEY in .env"}
        
    try:
        if any(x in key.lower() for x in ["simulated", "mock", "test", "your_"]):
            return {
                "success": True,
                "data": {
                    "status": "deliverable",
                    "result": "deliverable",
                    "score": 98,
                    "regexp": True,
                    "mx_records": True
                }
            }
            
        url = "https://api.hunter.io/v2/email-verifier"
        params = {
            "email": email,
            "api_key": key
        }
        res = requests.get(url, params=params, timeout=15)
        if res.status_code == 200:
            data = res.json().get("data", {})
            # Zagwarantowanie obecności klucza status (czasami w API jest tylko 'result')
            if "status" not in data and "result" in data:
                data["status"] = data["result"]
            return {"success": True, "data": data}
        else:
            return {"success": False, "error": f"Hunter.io API returned status code {res.status_code}: {res.text}"}
    except Exception as e:
        return {"success": False, "error": f"Hunter.io request failed: {str(e)}"}
