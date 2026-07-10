import requests
import json
import logging

logger = logging.getLogger(__name__)

class HolisticRedditScanner:
    """
    Wtyczka dla Hermes OS (Skill).
    Skanuje Reddit przy użyciu endpointu .json (omijając CAPTCHA), 
    aby odnajdywać osoby potrzebujące pomocy z ADHD / organizacją.
    """
    
    def __init__(self, config=None):
        self.config = config or {}
        self.default_subreddit = self.config.get("subreddit", "adhd")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def execute(self, params):
        """Główna metoda wywoływana przez orkiestratora Hermesa."""
        query = params.get("query", "help with planning")
        subreddit = params.get("subreddit", self.default_subreddit)
        limit = params.get("limit", 10)
        
        url = f"https://www.reddit.com/r/{subreddit}/search.json"
        
        req_params = {
            'q': query,
            'restrict_sr': 'on',
            'sort': 'new',
            'limit': limit
        }
        
        try:
            logger.info(f"Skanowanie Reddita (r/{subreddit}) dla zapytania: '{query}'...")
            response = requests.get(url, headers=self.headers, params=req_params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                for item in data.get('data', {}).get('children', []):
                    post_data = item['data']
                    results.append({
                        'title': post_data.get('title'),
                        'author': post_data.get('author'),
                        'url': f"https://www.reddit.com{post_data.get('permalink')}",
                        'text_snippet': post_data.get('selftext', '')[:200] + "..."
                    })
                
                return {
                    "status": "success",
                    "results_count": len(results),
                    "data": results,
                    "action_required": "Oceń te leady i dodaj najlepsze do tablicy Kanban."
                }
            else:
                return {
                    "status": "error",
                    "message": f"Reddit zwrócił błąd HTTP {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Błąd Reddit Scrapera: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

# Punkt wejścia dla systemu wtyczek Hermes
def register_plugin(registry):
    registry.register_skill("holistic_reddit_scanner", HolisticRedditScanner)
