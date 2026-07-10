import os
import base64
import requests
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe (.env)
load_dotenv()

FAL_KEY = os.getenv("FAL_KEY")

def get_fal_headers():
    """
    Zwraca nagłówki autoryzacyjne dla API fal.ai.
    """
    key = os.getenv("FAL_KEY") or FAL_KEY
    if not key:
        return None
    return {
        "Authorization": f"Key {key}",
        "Content-Type": "application/json"
    }

def run_face_swap(base_image_bytes, swap_image_bytes):
    """
    Wykonuje operację Face Swap za pomocą modelu fal-ai/face-swap.
    Przyjmuje surowe bajty obu obrazów, koduje je do Base64 i przesyła do API.
    """
    headers = get_fal_headers()
    if not headers:
        return None, "Brak klucza FAL_KEY w pliku .env!"

    try:
        # Kodowanie obrazów do formatu Data URI (Base64)
        base_b64 = base64.b64encode(base_image_bytes).decode("utf-8")
        swap_b64 = base64.b64encode(swap_image_bytes).decode("utf-8")
        
        base_data_uri = f"data:image/png;base64,{base_b64}"
        swap_data_uri = f"data:image/png;base64,{swap_b64}"

        payload = {
            "base_image_url": base_data_uri,
            "swap_image_url": swap_data_uri
        }

        # Wywołanie synchroniczne fal.ai
        url = "https://fal.run/fal-ai/face-swap"
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            res_json = response.json()
            image_url = res_json.get("image", {}).get("url")
            if image_url:
                # Pobierz wygenerowany obraz
                img_res = requests.get(image_url, timeout=30)
                if img_res.status_code == 200:
                    return img_res.content, None
                return None, f"Nie udało się pobrać wygenerowanego obrazu z CDN: {img_res.status_code}"
            return None, "API nie zwróciło adresu URL wygenerowanego obrazu."
        else:
            return None, f"Błąd fal.ai API ({response.status_code}): {response.text}"
            
    except Exception as ex:
        return None, f"Wystąpił nieoczekiwany wyjątek: {str(ex)}"

def run_flux_generation(prompt):
    """
    Generuje obraz za pomocą modelu fal-ai/flux/schnell (super szybki i tani Flux).
    Zwraca surowe bajty wygenerowanego obrazu lub None i błąd.
    """
    headers = get_fal_headers()
    if not headers:
        return None, "Brak klucza FAL_KEY w pliku .env!"

    try:
        payload = {
            "prompt": prompt,
            "image_size": "square_hd", # Domyślny ładny rozmiar (1024x1024)
            "num_inference_steps": 4,  # Szybka jakość dla Schnell
            "enable_safety_checker": True
        }

        url = "https://fal.run/fal-ai/flux/schnell"
        response = requests.post(url, json=payload, headers=headers, timeout=45)
        
        if response.status_code == 200:
            res_json = response.json()
            images = res_json.get("images", [])
            if images:
                image_url = images[0].get("url")
                img_res = requests.get(image_url, timeout=30)
                if img_res.status_code == 200:
                    return img_res.content, None
                return None, f"Nie udało się pobrać wygenerowanego obrazu: {img_res.status_code}"
            return None, "API nie zwróciło żadnego obrazu."
        else:
            return None, f"Błąd fal.ai API ({response.status_code}): {response.text}"
            
    except Exception as ex:
        return None, f"Wyjątek podczas generowania obrazu: {str(ex)}"

def run_instant_character(face_image_bytes, prompt):
    """
    Generuje kompletną postać na podstawie twarzy referencyjnej oraz promptu tekstowego.
    Używa modelu fal-ai/instant-character.
    """
    headers = get_fal_headers()
    if not headers:
        return None, "Brak klucza FAL_KEY w pliku .env!"

    try:
        # Kodowanie obrazu do Base64 Data URI
        face_b64 = base64.b64encode(face_image_bytes).decode("utf-8")
        face_data_uri = f"data:image/png;base64,{face_b64}"

        payload = {
            "image_url": face_data_uri,
            "prompt": prompt,
            "enable_safety_checker": True
        }

        # Wywołanie fal.ai
        url = "https://fal.run/fal-ai/instant-character"
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            res_json = response.json()
            images = res_json.get("images", [])
            if images:
                image_url = images[0].get("url")
                img_res = requests.get(image_url, timeout=30)
                if img_res.status_code == 200:
                    return img_res.content, None
                return None, f"Nie udało się pobrać wygenerowanego obrazu z CDN: {img_res.status_code}"
            return None, "API nie zwróciło adresu URL wygenerowanego obrazu."
        else:
            return None, f"Błąd fal.ai API ({response.status_code}): {response.text}"
            
    except Exception as ex:
        return None, f"Wystąpił nieoczekiwany wyjątek: {str(ex)}"

