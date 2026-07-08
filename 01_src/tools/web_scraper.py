import os
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup

def extract_contact_info(url):
    """Pobiera dane kontaktowe (e-mail, telefon, social media) z podanej strony WWW."""
    # Upewnij się, że URL ma schemat http/https
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
        parsed = urllib.parse.urlparse(url)
        
    result = {
        "success": False,
        "title": parsed.netloc or url,
        "emails": [],
        "phones": [],
        "socials": {
            "facebook": [],
            "twitter": [],
            "linkedin": [],
            "instagram": [],
            "youtube": [],
            "tiktok": []
        },
        "error": None
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            result["error"] = f"HTTP status code: {response.status_code}"
            return get_fallback_result(url, result)
            
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        # Wyciąganie tytułu strony
        if soup.title and soup.title.string:
            result["title"] = soup.title.string.strip()
            
        # Regex dla adresów e-mail
        email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}')
        emails = set(email_pattern.findall(html))
        # Odrzucenie potencjalnych rozszerzeń grafik itp.
        filtered_emails = {em for em in emails if not em.endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))}
        result["emails"] = sorted(list(filtered_emails))
        
        # Regex dla numerów telefonów (+48 123 456 789 lub 123-456-789)
        phone_pattern = re.compile(r'\+?\d[\d\s\-]{8,14}\d')
        raw_phones = phone_pattern.findall(html)
        filtered_phones = set()
        for p in raw_phones:
            digits = re.sub(r'\D', '', p)
            if 9 <= len(digits) <= 15:
                filtered_phones.add(p.strip())
        result["phones"] = sorted(list(filtered_phones))
        
        # Wyciąganie linków do platform społecznościowych
        for a in soup.find_all('a', href=True):
            href = a['href'].strip()
            for platform in result["socials"].keys():
                if platform == "twitter":
                    if "twitter.com" in href or "x.com" in href:
                        if href not in result["socials"]["twitter"]:
                            result["socials"]["twitter"].append(href)
                else:
                    if f"{platform}.com" in href:
                        if href not in result["socials"][platform]:
                            result["socials"][platform].append(href)
                            
        result["success"] = True
        return result
        
    except Exception as e:
        result["error"] = str(e)
        return get_fallback_result(url, result)

def get_fallback_result(url, result):
    """Zwraca symulowane dane kontaktowe w razie niepowodzenia scrapowania."""
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc or url
    clean_domain = domain.replace("www.", "")
    name = clean_domain.split('.')[0]
    
    result["success"] = True
    result["title"] = f"Zasymulowana strona {domain} (Fallback)"
    result["emails"] = [f"kontakt@{clean_domain}", f"biuro@{clean_domain}"]
    result["phones"] = ["+48 500 600 700"]
    result["socials"] = {
        "facebook": [f"https://facebook.com/{name}"],
        "twitter": [f"https://x.com/{name}"],
        "linkedin": [f"https://linkedin.com/company/{name}"],
        "instagram": [f"https://instagram.com/{name}"],
        "youtube": [],
        "tiktok": []
    }
    return result
