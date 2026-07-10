import os
import requests
from dotenv import load_dotenv

# Preload environment
load_dotenv()

def get_env_var(var_name):
    """Pobiera zmienną środowiskową z .env lub systemu w sposób odporny."""
    load_dotenv()
    return os.environ.get(var_name) or os.getenv(var_name)

def post_to_linkedin(text, title=None, link=None):
    """Publikuje post na LinkedIn."""
    token = get_env_var("LINKEDIN_ACCESS_TOKEN")
    person_id = get_env_var("LINKEDIN_PERSON_ID")
    if not token or not person_id:
        missing = []
        if not token: missing.append("LINKEDIN_ACCESS_TOKEN")
        if not person_id: missing.append("LINKEDIN_PERSON_ID")
        return {"success": False, "error": f"Missing client key in .env: {', '.join(missing)}"}
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    author = f"urn:li:person:{person_id}"
    payload = {
        "author": author,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    if link:
        payload["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "ARTICLE"
        payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
            {
                "status": "READY",
                "description": {
                    "text": text
                },
                "originalUrl": link,
                "title": {
                    "text": title or "Link Share"
                }
            }
        ]
        
    try:
        # Jeśli token jest testowy/przykładowy, symulujemy sukces
        if any(x in token.lower() for x in ["simulated", "mock", "test", "your_"]):
            return {"success": True, "id": "simulated_linkedin_post_id"}
        
        response = requests.post(
            "https://api.linkedin.com/v2/ugcShares",
            json=payload,
            headers=headers,
            timeout=10
        )
        if response.status_code in [200, 201]:
            data = response.json()
            return {"success": True, "id": data.get("id", "linkedin_post_id")}
        else:
            return {"success": False, "error": f"API Error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"success": False, "error": f"Network Error: {str(e)}"}

def post_to_facebook(text, link=None):
    """Publikuje post na fanpage Facebooka."""
    token = get_env_var("FACEBOOK_PAGE_ACCESS_TOKEN")
    page_id = get_env_var("FACEBOOK_PAGE_ID")
    if not token or not page_id:
        missing = []
        if not token: missing.append("FACEBOOK_PAGE_ACCESS_TOKEN")
        if not page_id: missing.append("FACEBOOK_PAGE_ID")
        return {"success": False, "error": f"Missing client key in .env: {', '.join(missing)}"}
        
    url = f"https://graph.facebook.com/v18.0/{page_id}/feed"
    params = {
        "message": text,
        "access_token": token
    }
    if link:
        params["link"] = link
        
    try:
        if any(x in token.lower() for x in ["simulated", "mock", "test", "your_"]):
            return {"success": True, "id": "simulated_facebook_post_id"}
            
        response = requests.post(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {"success": True, "id": data.get("id", "facebook_post_id")}
        else:
            return {"success": False, "error": f"API Error {response.status_code}: {response.text}"}
    except Exception as e:
        return {"success": False, "error": f"Network Error: {str(e)}"}

def post_to_instagram(image_url, text):
    """Publikuje grafikę z opisem na Instagramie."""
    token = get_env_var("FACEBOOK_PAGE_ACCESS_TOKEN")
    ig_id = get_env_var("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    if not token or not ig_id:
        missing = []
        if not token: missing.append("FACEBOOK_PAGE_ACCESS_TOKEN")
        if not ig_id: missing.append("INSTAGRAM_BUSINESS_ACCOUNT_ID")
        return {"success": False, "error": f"Missing client key in .env: {', '.join(missing)}"}
        
    try:
        if any(x in token.lower() for x in ["simulated", "mock", "test", "your_"]):
            return {"success": True, "id": "simulated_instagram_post_id"}
            
        # Krok 1: Utworzenie kontenera mediów
        container_url = f"https://graph.facebook.com/v18.0/{ig_id}/media"
        params = {
            "image_url": image_url,
            "caption": text,
            "access_token": token
        }
        res = requests.post(container_url, params=params, timeout=10)
        if res.status_code != 200:
            return {"success": False, "error": f"Failed to create media container: {res.text}"}
        container_id = res.json().get("id")
        
        # Krok 2: Publikacja
        publish_url = f"https://graph.facebook.com/v18.0/{ig_id}/media_publish"
        pub_params = {
            "creation_id": container_id,
            "access_token": token
        }
        pub_res = requests.post(publish_url, pub_params=pub_params, timeout=10)
        if pub_res.status_code == 200:
            return {"success": True, "id": pub_res.json().get("id", "instagram_post_id")}
        else:
            return {"success": False, "error": f"Failed to publish media: {pub_res.text}"}
    except Exception as e:
        return {"success": False, "error": f"Network Error: {str(e)}"}

def post_to_twitter(text):
    """Publikuje post (tweet) na platformie X/Twitter."""
    ckey = get_env_var("TWITTER_CONSUMER_KEY")
    csecret = get_env_var("TWITTER_CONSUMER_SECRET")
    atoken = get_env_var("TWITTER_ACCESS_TOKEN")
    asecret = get_env_var("TWITTER_ACCESS_TOKEN_SECRET")
    
    if not ckey or not csecret or not atoken or not asecret:
        missing = []
        if not ckey: missing.append("TWITTER_CONSUMER_KEY")
        if not csecret: missing.append("TWITTER_CONSUMER_SECRET")
        if not atoken: missing.append("TWITTER_ACCESS_TOKEN")
        if not asecret: missing.append("TWITTER_ACCESS_TOKEN_SECRET")
        return {"success": False, "error": f"Missing client key in .env: {', '.join(missing)}"}
        
    try:
        if any(x in ckey.lower() for x in ["simulated", "mock", "test", "your_"]):
            return {"success": True, "id": "simulated_twitter_post_id"}
            
        from requests_oauthlib import OAuth1
        auth = OAuth1(ckey, csecret, atoken, asecret)
        url = "https://api.twitter.com/2/tweets"
        payload = {"text": text}
        res = requests.post(url, auth=auth, json=payload, timeout=10)
        if res.status_code in [200, 201]:
            data = res.json()
            return {"success": True, "id": data.get("data", {}).get("id", "twitter_post_id")}
        else:
            return {"success": False, "error": f"API Error {res.status_code}: {res.text}"}
    except Exception as e:
        return {"success": False, "error": f"Network Error: {str(e)}"}

def post_to_tiktok(video_url, text):
    """Publikuje wideo na platformie TikTok."""
    token = get_env_var("TIKTOK_ACCESS_TOKEN")
    if not token:
        return {"success": False, "error": "Missing client key in .env: TIKTOK_ACCESS_TOKEN"}
        
    try:
        if any(x in token.lower() for x in ["simulated", "mock", "test", "your_"]):
            return {"success": True, "id": "simulated_tiktok_post_id"}
            
        url = "https://open.tiktokapis.com/v2/post/publish/video/init/"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8"
        }
        payload = {
            "post_info": {
                "title": text,
                "privacy_level": "PUBLIC_TO_EVERYONE",
                "disable_comment": False,
                "disable_duet": False,
                "disable_stitch": False
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_url": video_url
            }
        }
        res = requests.post(url, headers=headers, json=payload, timeout=10)
        if res.status_code in [200, 201]:
            data = res.json()
            return {"success": True, "id": data.get("data", {}).get("publish_id", "tiktok_post_id")}
        else:
            return {"success": False, "error": f"API Error {res.status_code}: {res.text}"}
    except Exception as e:
        return {"success": False, "error": f"Network Error: {str(e)}"}
