import os
import requests
from dotenv import load_dotenv

# Preload environment
load_dotenv()

def get_env_var(var_name):
    """Pobiera zmienną środowiskową z .env lub systemu w sposób odporny."""
    load_dotenv()
    return os.environ.get(var_name) or os.getenv(var_name)

def search_tavily(query):
    """Wyszukuje informacje za pomocą Tavily API."""
    key = get_env_var("TAVILY_API_KEY")
    if not key:
        return {"success": False, "error": "Missing TAVILY_API_KEY in .env"}
        
    try:
        if any(x in key.lower() for x in ["simulated", "mock", "test", "your_"]):
            return {
                "success": True, 
                "data": {
                    "answer": f"Zoptymalizowana podsumowująca odpowiedź Tavily dla zapytania: '{query}'",
                    "results": [
                        {"title": f"Wynik 1 dla {query}", "url": "https://example.com/tavily-1", "content": "To jest przykładowa treść zwrócona przez Tavily."},
                        {"title": f"Wynik 2 dla {query}", "url": "https://example.com/tavily-2", "content": "Kolejny zintegrowany fragment wiedzy z sieci."}
                    ]
                }
            }
            
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": key,
            "query": query,
            "include_answer": True
        }
        res = requests.post(url, json=payload, timeout=15)
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        else:
            return {"success": False, "error": f"Tavily API returned status code {res.status_code}: {res.text}"}
    except Exception as e:
        return {"success": False, "error": f"Tavily API request failed: {str(e)}"}

def search_serper(query):
    """Wyszukuje informacje w Google za pomocą Serper.dev API."""
    key = get_env_var("SERPER_API_KEY")
    if not key:
        return {"success": False, "error": "Missing SERPER_API_KEY in .env"}
        
    try:
        if any(x in key.lower() for x in ["simulated", "mock", "test", "your_"]):
            return {
                "success": True,
                "data": {
                    "organic": [
                        {"title": f"Wynik Google: {query}", "link": "https://example.com/serper-1", "snippet": "To jest zasymulowany opis snippetu z Google za pośrednictwem serwisu Serper.dev."}
                    ]
                }
            }
            
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": key,
            "Content-Type": "application/json"
        }
        payload = {"q": query}
        res = requests.post(url, headers=headers, json=payload, timeout=15)
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        else:
            return {"success": False, "error": f"Serper API returned status code {res.status_code}: {res.text}"}
    except Exception as e:
        return {"success": False, "error": f"Serper API request failed: {str(e)}"}

def search_google_cse(query):
    """Wyszukuje informacje za pomocą Google Custom Search Engine (CSE)."""
    cx = get_env_var("GOOGLE_CSE_ID")
    key = get_env_var("GOOGLE_API_KEY")
    if not cx or not key:
        return {"success": False, "error": "Missing GOOGLE_CSE_ID or GOOGLE_API_KEY in .env"}
        
    try:
        if any(x in key.lower() for x in ["simulated", "mock", "test", "your_"]) or any(x in cx.lower() for x in ["simulated", "mock", "test", "your_"]):
            return {
                "success": True,
                "data": {
                    "items": [
                        {"title": f"Google CSE: {query}", "link": "https://example.com/cse-1", "snippet": "Zasymulowana informacja z Google CSE."}
                    ]
                }
            }
            
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": key,
            "cx": cx,
            "q": query
        }
        res = requests.get(url, params=params, timeout=15)
        if res.status_code == 200:
            return {"success": True, "data": res.json()}
        else:
            return {"success": False, "error": f"Google CSE API returned status code {res.status_code}: {res.text}"}
    except Exception as e:
        return {"success": False, "error": f"Google CSE request failed: {str(e)}"}
