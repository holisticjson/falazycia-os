import json, glob, requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/business.manage']
tokens = glob.glob('tokens/gbp/*.json')
print(f'Znaleziono {len(tokens)} tokenow')

for tf in tokens:
    print(f'\n--- Token: {tf} ---')
    creds = Credentials.from_authorized_user_file(tf, SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    
    # 1. Sprawdz konta
    url = 'https://mybusinessaccountmanagement.googleapis.com/v1/accounts'
    headers = {'Authorization': f'Bearer {creds.token}'}
    r = requests.get(url, headers=headers)
    print(f'Accounts status: {r.status_code}')
    print(f'Accounts response: {r.text[:800]}')
    
    if r.status_code == 200:
        accounts = r.json().get('accounts', [])
        print(f'Liczba kont: {len(accounts)}')
        for acc in accounts:
            acc_name = acc.get("name", "?")
            acc_account_name = acc.get("accountName", "?")
            acc_type = acc.get("type", "?")
            print(f'  Konto: {acc_name} | {acc_account_name} | type={acc_type}')
            
            # 2. Sprawdz lokalizacje
            loc_url = f'https://mybusinessbusinessinformation.googleapis.com/v1/{acc_name}/locations'
            params = {'readMask': 'name,title,storefrontAddress'}
            lr = requests.get(loc_url, headers=headers, params=params)
            print(f'  Locations status: {lr.status_code}')
            print(f'  Locations response: {lr.text[:800]}')
