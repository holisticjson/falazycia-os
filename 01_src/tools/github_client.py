import os
import urllib.request
import urllib.parse
import json

def search_repositories(query, language=None, sort="stars", order="desc", per_page=15):
    """Wyszukuje repozytoria na GitHubie dla zadanego zapytania."""
    q_str = query
    if language:
        q_str = f"{query} language:{language}"
    encoded_query = urllib.parse.quote(q_str)
    url = f"https://api.github.com/search/repositories?q={encoded_query}&sort={sort}&order={order}&per_page={per_page}"
    req = urllib.request.Request(url, headers={"User-Agent": "Holistic-Jason-App"})
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode())
            return data.get("items", [])
    except Exception as e:
        print(f"Błąd wyszukiwania: {e}")
        return []

def get_readme(full_name):
    """Pobiera zawartość pliku README.md dla danego repozytorium (np. 'facebook/react')."""
    url = f"https://api.github.com/repos/{full_name}/readme"
    req = urllib.request.Request(url, headers={"User-Agent": "Holistic-Jason-App", "Accept": "application/vnd.github.v3.raw"})
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Błąd pobierania README: {e}")
        return "Brak pliku README lub wystąpił błąd podczas pobierania."
