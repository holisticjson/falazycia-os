import requests
from skills.gbp_auth import get_all_gbp_credentials

def list_all_gbp_accounts():
    """Listuje konta ze WSZYSTKICH podłączonych kont Google."""
    all_accounts = []
    creds_list = get_all_gbp_credentials()
    
    for creds in creds_list:
        url = "https://mybusinessaccountmanagement.googleapis.com/v1/accounts"
        headers = {"Authorization": f"Bearer {creds.token}"}
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            accounts = response.json().get('accounts', [])
            # Dodajemy informację, do których credsów należy konto (opcjonalnie)
            for acc in accounts:
                acc['_creds'] = creds # Zachowujemy credsy do dalszych zapytań
                all_accounts.append(acc)
    
    return all_accounts

def list_gbp_locations(account):
    """Listuje lokalizacje dla konkretnego konta, używając przypisanych mu poświadczeń."""
    creds = account.get('_creds')
    if not creds:
        return {"error": "Brak poświadczeń dla konta"}
        
    url = f"https://mybusinessbusinessinformation.googleapis.com/v1/{account['name']}/locations"
    params = {
        "readMask": "name,title,storeCode,storefrontAddress,categories,metadata"
    }
    headers = {"Authorization": f"Bearer {creds.token}"}
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get('locations', [])
    else:
        return {"error": response.status_code, "detail": response.text}

def create_gbp_post(location_name, creds, text, media_url=None):
    """Tworzy post na wizytówce używając konkretnych poświadczeń."""
    url = f"https://mybusiness.googleapis.com/v4/{location_name}/localPosts"
    headers = {"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"}
    
    data = {
        "languageCode": "pl-PL",
        "summary": text,
        "callToAction": {
            "actionType": "LEARN_MORE",
            "url": "https://holisticjson.pl"
        }
    }
    
    if media_url:
        data["media"] = [{"mediaFormat": "PHOTO", "sourceUrl": media_url}]
        
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "detail": response.text}
