import re
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
from bs4 import BeautifulSoup

def get_channel_id_from_url_free(channel_url):
    """
    Darmowa metoda pobierania Channel ID z podanego URL kanału (np. @nazwa_kanalu).
    Wykorzystuje BeautifulSoup do wyciągnięcia meta-tagów.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        req = urllib.request.Request(channel_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # 1. Próba znalezienia meta-tagu itemprop="channelId"
        meta_channel_id = soup.find('meta', itemprop='channelId')
        if meta_channel_id and meta_channel_id.get('content'):
            return meta_channel_id.get('content')
            
        # 2. Próba znalezienia linku canonical z ID kanału
        meta_canonical = soup.find('link', rel='canonical')
        if meta_canonical and meta_canonical.get('href'):
            canonical_url = meta_canonical.get('href')
            match = re.search(r'/channel/([^/?#]+)', canonical_url)
            if match:
                return match.group(1)
                
        # 3. Próba znalezienia w tekście strony za pomocą regex
        match = re.search(r'"channelId":"([^"]+)"', html)
        if match:
            return match.group(1)
            
        # 4. Próba wyciągnięcia z tagów twitter:url
        meta_twitter = soup.find('meta', property='twitter:url')
        if meta_twitter and meta_twitter.get('content'):
            twitter_url = meta_twitter.get('content')
            match = re.search(r'/channel/([^/?#]+)', twitter_url)
            if match:
                return match.group(1)
                
        return None
    except Exception as e:
        print(f"Błąd podczas wyciągania Channel ID z {channel_url}: {e}")
        return None

def get_channel_videos_free(channel_id):
    """
    Pobiera najnowsze filmy z kanału za pomocą darmowego kanału RSS YouTube.
    Nie wymaga kluczy API, brak jakichkolwiek kosztów i limitów.
    Wyciąga 15 najnowszych filmów.
    """
    videos = []
    try:
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        req = urllib.request.Request(rss_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        
        # Namespace obsługiwane przez YouTube RSS
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'yt': 'http://www.youtube.com/xml/schemas/2015',
            'media': 'http://search.yahoo.com/mrss/'
        }
        
        for entry in root.findall('atom:entry', ns):
            video_id = entry.find('yt:videoId', ns).text if entry.find('yt:videoId', ns) is not None else ""
            title = entry.find('atom:title', ns).text if entry.find('atom:title', ns) is not None else ""
            link = entry.find('atom:link', ns).attrib['href'] if entry.find('atom:link', ns) is not None else ""
            published = entry.find('atom:published', ns).text if entry.find('atom:published', ns) is not None else ""
            
            # Pobieranie miniaturki i opisu z tagów media
            media_group = entry.find('media:group', ns)
            thumbnail_url = ""
            description = ""
            views = "N/A"
            likes = "N/A"
            
            if media_group is not None:
                media_thumbnail = media_group.find('media:thumbnail', ns)
                if media_thumbnail is not None:
                    thumbnail_url = media_thumbnail.attrib['url']
                    
                media_description = media_group.find('media:description', ns)
                if media_description is not None:
                    description = media_description.text
                    
                community = media_group.find('media:community', ns)
                if community is not None:
                    statistics = community.find('media:statistics', ns)
                    if statistics is not None:
                        views = statistics.attrib.get('views', "0")
                        
                    star_rating = community.find('media:starRating', ns)
                    if star_rating is not None:
                        likes = star_rating.attrib.get('count', "0")
                        
            videos.append({
                'id': video_id,
                'title': title,
                'url': link,
                'published_at': published[:10] if published else "N/A",
                'thumbnail': thumbnail_url if thumbnail_url else f"https://img.youtube.com/vi/{video_id}/0.jpg",
                'description': description[:300] + "..." if description else "",
                'views': views,
                'likes': likes,
                'source': 'RSS (Free)'
            })
    except Exception as e:
        print(f"Błąd podczas pobierania filmów przez RSS dla kanału {channel_id}: {e}")
    return videos

def search_videos_by_keyword_free(query):
    """
    Darmowy scraper wyników wyszukiwania YouTube bez klucza API.
    Pobiera HTML strony wyszukiwania, wyciąga JSON wstrzyknięty w tagu 'ytInitialData'
    i parsuje najpopularniejsze filmy.
    """
    videos = []
    try:
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
            
        # Wyciąganie json z ytInitialData
        match = re.search(r'var ytInitialData\s*=\s*({.*?});', html)
        if not match:
            return videos
            
        data_json = json.loads(match.group(1))
        
        # Parsowanie głębokiego JSON-a YouTube
        contents = (data_json.get('contents', {})
                             .get('twoColumnSearchResultsRenderer', {})
                             .get('primaryContents', {})
                             .get('sectionListRenderer', {})
                             .get('contents', []))
                             
        for section in contents:
            item_section = section.get('itemSectionRenderer', {})
            for item in item_section.get('contents', []):
                video_renderer = item.get('videoRenderer', {})
                if not video_renderer:
                    continue
                    
                video_id = video_renderer.get('videoId', '')
                if not video_id:
                    continue
                    
                title = ""
                title_runs = video_renderer.get('title', {}).get('runs', [])
                if title_runs:
                    title = title_runs[0].get('text', '')
                    
                views_text = video_renderer.get('viewCountText', {}).get('simpleText', '0 wyświetleń')
                
                # Czas trwania filmu
                duration = video_renderer.get('lengthText', {}).get('simpleText', 'N/A')
                
                # Miniaturka
                thumbnails = video_renderer.get('thumbnail', {}).get('thumbnails', [])
                thumbnail_url = thumbnails[0].get('url', '') if thumbnails else f"https://img.youtube.com/vi/{video_id}/0.jpg"
                
                # Data publikacji
                pub_text = video_renderer.get('publishedTimeText', {}).get('simpleText', 'N/A')
                
                videos.append({
                    'id': video_id,
                    'title': title,
                    'url': f"https://www.youtube.com/watch?v={video_id}",
                    'published_at': pub_text,
                    'thumbnail': thumbnail_url,
                    'views': views_text,
                    'duration': duration,
                    'source': 'Scraper (Free)'
                })
                
                if len(videos) >= 20:
                    break
            if len(videos) >= 20:
                break
    except Exception as e:
        print(f"Błąd podczas wyszukiwania bezkluczowego dla query '{query}': {e}")
    return videos

def get_channel_videos_api(channel_id, api_key):
    """
    Pobiera najpopularniejsze filmy z kanału przy użyciu oficjalnego YouTube API.
    Służy do głębszego sortowania po views/likes, jeśli Tomasz poda klucz.
    """
    videos = []
    try:
        from googleapiclient.discovery import build
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # 1. Pobranie playlisty uploads dla kanału
        channel_response = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()
        
        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # 2. Pobranie filmów z playlisty uploads
        playlist_response = youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=uploads_playlist_id,
            maxResults=30
        ).execute()
        
        video_ids = []
        video_map = {}
        for item in playlist_response.get('items', []):
            vid_id = item['contentDetails']['videoId']
            video_ids.append(vid_id)
            video_map[vid_id] = {
                'id': vid_id,
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={vid_id}",
                'published_at': item['snippet']['publishedAt'][:10],
                'thumbnail': item['snippet'].get('thumbnails', {}).get('high', {}).get('url', f"https://img.youtube.com/vi/{vid_id}/0.jpg"),
                'description': item['snippet']['description'][:300] + "...",
                'source': 'Official API'
            }
            
        # 3. Pobranie statystyk wideo (wyświetlenia, lajki)
        stats_response = youtube.videos().list(
            part='statistics,contentDetails',
            id=','.join(video_ids)
        ).execute()
        
        for item in stats_response.get('items', []):
            vid_id = item['id']
            stats = item.get('statistics', {})
            if vid_id in video_map:
                video_map[vid_id]['views'] = f"{int(stats.get('viewCount', 0)):,}"
                video_map[vid_id]['likes'] = f"{int(stats.get('likeCount', 0)):,}"
                video_map[vid_id]['duration'] = item.get('contentDetails', {}).get('duration', 'N/A')
                videos.append(video_map[vid_id])
                
        # Sortowanie po wyświetleniach malejąco
        videos.sort(key=lambda x: int(x['views'].replace(',', '') if 'views' in x and x['views'] != 'N/A' else 0), reverse=True)
    except Exception as e:
        print(f"Błąd podczas odpytywania YouTube API dla kanału {channel_id}: {e}")
        # Fallback do RSS
        return get_channel_videos_free(channel_id)
    return videos

def search_videos_by_keyword_api(query, api_key):
    """
    Wyszukuje filmy po słowie kluczowym za pomocą oficjalnego YouTube API.
    """
    videos = []
    try:
        from googleapiclient.discovery import build
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        search_response = youtube.search().list(
            q=query,
            part='snippet',
            type='video',
            maxResults=20,
            regionCode='PL',
            relevanceLanguage='pl'
        ).execute()
        
        video_ids = []
        video_map = {}
        for item in search_response.get('items', []):
            vid_id = item['id']['videoId']
            video_ids.append(vid_id)
            video_map[vid_id] = {
                'id': vid_id,
                'title': item['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={vid_id}",
                'published_at': item['snippet']['publishedAt'][:10],
                'thumbnail': item['snippet'].get('thumbnails', {}).get('high', {}).get('url', f"https://img.youtube.com/vi/{vid_id}/0.jpg"),
                'description': item['snippet']['description'][:300] + "...",
                'source': 'Official API'
            }
            
        # Pobranie statystyk i czasu trwania
        stats_response = youtube.videos().list(
            part='statistics,contentDetails',
            id=','.join(video_ids)
        ).execute()
        
        for item in stats_response.get('items', []):
            vid_id = item['id']
            stats = item.get('statistics', {})
            if vid_id in video_map:
                video_map[vid_id]['views'] = f"{int(stats.get('viewCount', 0)):,}"
                video_map[vid_id]['likes'] = f"{int(stats.get('likeCount', 0)):,}"
                video_map[vid_id]['duration'] = item.get('contentDetails', {}).get('duration', 'N/A')
                videos.append(video_map[vid_id])
    except Exception as e:
        print(f"Błąd podczas wyszukiwania przez YouTube API dla '{query}': {e}")
        # Fallback do scrapera
        return search_videos_by_keyword_free(query)
    return videos
