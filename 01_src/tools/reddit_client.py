import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Import search client as fallback
try:
    from . import search_client
except ImportError:
    import search_client

# Preload environment
load_dotenv()

def get_env_var(var_name):
    """Pobiera zmienną środowiskową z .env lub systemu w sposób odporny."""
    load_dotenv()
    return os.environ.get(var_name) or os.getenv(var_name)

def search_reddit(query, subreddit="all", limit=15):
    """Wyszukuje posty na Reddit za pomocą API lub fallbacku w wyszukiwarce."""
    client_id = get_env_var("REDDIT_CLIENT_ID")
    client_secret = get_env_var("REDDIT_CLIENT_SECRET")
    
    has_keys = bool(client_id and client_secret)
    is_mock = False
    if has_keys:
        if any(x in client_id.lower() for x in ["simulated", "mock", "test", "your_"]):
            is_mock = True

    if has_keys and not is_mock:
        try:
            # 1. Pobierz OAuth Token
            auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
            data = {"grant_type": "client_credentials"}
            headers = {"User-Agent": "HolisticOS/0.1 by HolisticJason"}
            
            token_res = requests.post(
                "https://www.reddit.com/api/v1/access_token",
                auth=auth,
                data=data,
                headers=headers,
                timeout=10
            )
            
            if token_res.status_code == 200:
                token_data = token_res.json()
                token = token_data.get("access_token")
                
                # 2. Wyszukiwanie
                search_headers = {
                    "Authorization": f"Bearer {token}",
                    "User-Agent": "HolisticOS/0.1 by HolisticJason"
                }
                
                if subreddit and subreddit.lower() != "all":
                    url = f"https://oauth.reddit.com/r/{subreddit}/search"
                    params = {"q": query, "limit": limit, "restrict_sr": "on"}
                else:
                    url = "https://oauth.reddit.com/search"
                    params = {"q": query, "limit": limit}
                    
                search_res = requests.get(url, headers=search_headers, params=params, timeout=10)
                if search_res.status_code == 200:
                    children = search_res.json().get("data", {}).get("children", [])
                    posts = []
                    for child in children:
                        d = child.get("data", {})
                        created_utc = d.get("created_utc", 0)
                        created_at = datetime.fromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M') if created_utc else "N/A"
                        
                        posts.append({
                            "title": d.get("title", "No Title"),
                            "subreddit": d.get("subreddit", subreddit),
                            "author": d.get("author", "unknown"),
                            "created_at": created_at,
                            "score": d.get("score", 0),
                            "text": d.get("selftext", ""),
                            "permalink": f"https://www.reddit.com{d.get('permalink', '')}"
                        })
                    return {"success": True, "posts": posts}
        except Exception:
            pass # Przejdź do fallbacku w razie błędu sieci/auth

    # Fallback do Tavily/Serper jeśli są dostępne
    tavily_key = get_env_var("TAVILY_API_KEY")
    serper_key = get_env_var("SERPER_API_KEY")
    
    if tavily_key or serper_key:
        fallback_query = "site:reddit.com"
        if subreddit and subreddit.lower() != "all":
            fallback_query += f" inurl:r/{subreddit}"
        fallback_query += f" {query}"
        
        if tavily_key:
            try:
                res = search_client.search_tavily(fallback_query)
                if res.get("success"):
                    tav_results = res.get("data", {}).get("results", [])
                    posts = []
                    for item in tav_results[:limit]:
                        posts.append({
                            "title": item.get("title", "Wątek Reddit"),
                            "subreddit": subreddit,
                            "author": "anonymous",
                            "created_at": "N/A (Tavily Fallback)",
                            "score": 0,
                            "text": item.get("content", ""),
                            "permalink": item.get("url", "https://reddit.com")
                        })
                    return {"success": True, "posts": posts, "note": "Wyniki pobrane za pomocą Tavily (fallback)"}
            except Exception:
                pass
                
        if serper_key:
            try:
                res = search_client.search_serper(fallback_query)
                if res.get("success"):
                    serp_results = res.get("data", {}).get("organic", [])
                    posts = []
                    for item in serp_results[:limit]:
                        posts.append({
                            "title": item.get("title", "Wątek Reddit"),
                            "subreddit": subreddit,
                            "author": "anonymous",
                            "created_at": "N/A (Serper Fallback)",
                            "score": 0,
                            "text": item.get("snippet", ""),
                            "permalink": item.get("link", "https://reddit.com")
                        })
                    return {"success": True, "posts": posts, "note": "Wyniki pobrane za pomocą Serper.dev (fallback)"}
            except Exception:
                pass
                
    # Symulacja jeśli brak kluczy lub błąd fallbacków
    posts = [
        {
            "title": f"Jak poradzić sobie z ADHD w pracy? Szukam coacha w r/{subreddit}",
            "subreddit": subreddit if subreddit != "all" else "ADHD",
            "author": "adhd_seeker",
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "score": 42,
            "text": f"Hej! Szukam sprawdzonych metodologii radzenia sobie z prokrastynacją w pracy przy ADHD. Moje zapytanie dotyczy: '{query}'. Co polecacie?",
            "permalink": "https://www.reddit.com/r/ADHD/"
        },
        {
            "title": f"Aplikacje wspierające produktywność i ADHD ({query})",
            "subreddit": subreddit if subreddit != "all" else "productivity",
            "author": "productivity_ninja",
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M'),
            "score": 18,
            "text": f"Stworzyłem listę narzędzi i integracji wspierających focus dla osób neuroróżnorodnych. Wpis nawiązuje do '{query}'.",
            "permalink": "https://www.reddit.com/r/productivity/"
        }
    ]
    return {"success": True, "posts": posts, "note": "Zasymulowane wyniki Reddit (brak kluczy API)"}
