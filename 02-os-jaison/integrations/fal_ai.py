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
        # Optymalizacja rozmiaru obrazów do max 512x512 JPEG za pomocą PIL przed wysłaniem
        # Zapobiega to timeoutom sieciowym i oszczędza transfer przy zachowaniu idealnej ostrości twarzy
        from PIL import Image
        import io
        
        def optimize_and_encode(img_bytes):
            try:
                img = Image.open(io.BytesIO(img_bytes))
                img.thumbnail((512, 512))
                # Konwertujemy do RGB na wypadek kanału Alfa w PNG
                img = img.convert("RGB")
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=85)
                opt_bytes = buf.getvalue()
                b64 = base64.b64encode(opt_bytes).decode("utf-8")
                return f"data:image/jpeg;base64,{b64}"
            except Exception:
                # Fallback w przypadku błędu PIL
                b64 = base64.b64encode(img_bytes).decode("utf-8")
                return f"data:image/png;base64,{b64}"

        base_data_uri = optimize_and_encode(base_image_bytes)
        swap_data_uri = optimize_and_encode(swap_image_bytes)

        payload = {
            "base_image_url": base_data_uri,
            "swap_image_url": swap_data_uri,
            "upscale": True,      # 2x upscaling i poprawa ostrości
            "detailer": True      # Detailing rysów twarzy (Beta) dla maksymalnego fotorealizmu
        }

        # Wywołanie synchroniczne fal.ai
        url = "https://fal.run/fal-ai/face-swap"
        response = requests.post(url, json=payload, headers=headers, timeout=180)
        
        if response.status_code == 200:
            res_json = response.json()
            image_url = res_json.get("image", {}).get("url")
            if image_url:
                # Pobierz wygenerowany obraz
                img_res = requests.get(image_url, timeout=60)
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
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            res_json = response.json()
            images = res_json.get("images", [])
            if images:
                image_url = images[0].get("url")
                img_res = requests.get(image_url, timeout=60)
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
        response = requests.post(url, json=payload, headers=headers, timeout=180)
        
        if response.status_code == 200:
            res_json = response.json()
            images = res_json.get("images", [])
            if images:
                image_url = images[0].get("url")
                img_res = requests.get(image_url, timeout=60)
                if img_res.status_code == 200:
                    return img_res.content, None
                return None, f"Nie udało się pobrać wygenerowanego obrazu z CDN: {img_res.status_code}"
            return None, "API nie zwróciło adresu URL wygenerowanego obrazu."
        else:
            return None, f"Błąd fal.ai API ({response.status_code}): {response.text}"
            
    except Exception as ex:
        return None, f"Wystąpił nieoczekiwany wyjątek: {str(ex)}"


def run_background_removal(image_bytes):
    """
    Usuwa tło z obrazu za pomocą modelu fal-ai/birefnet na platformie fal.ai.
    Idealne rozwiązanie dla produktów e-commerce i szybkich wycinek.
    """
    headers = get_fal_headers()
    if not headers:
        return None, "Brak klucza FAL_KEY w pliku .env!"

    try:
        # Kodowanie obrazu do Base64 Data URI
        img_b64 = base64.b64encode(image_bytes).decode("utf-8")
        img_data_uri = f"data:image/png;base64,{img_b64}"

        payload = {
            "image_url": img_data_uri
        }

        # Wywołanie fal.ai (BiRefNet)
        url = "https://fal.run/fal-ai/birefnet"
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            res_json = response.json()
            image_url = res_json.get("image", {}).get("url")
            if image_url:
                img_res = requests.get(image_url, timeout=60)
                if img_res.status_code == 200:
                    return img_res.content, None
                return None, f"Nie udało się pobrać wygenerowanego obrazu: {img_res.status_code}"
            return None, "API nie zwróciło adresu URL obrazu bez tła."
        else:
            return None, f"Błąd fal.ai API ({response.status_code}): {response.text}"
            
    except Exception as ex:
        return None, f"Wyjątek podczas usuwania tła: {str(ex)}"


def run_flux_lora_generation(prompt, lora_url, scale=1.0, aspect_ratio="square_hd"):
    """
    Generuje obraz przy użyciu modelu fal-ai/flux-lora oraz przesłanego pliku wag LoRA (.safetensors).
    """
    headers = get_fal_headers()
    if not headers:
        return None, "Brak klucza FAL_KEY w pliku .env!"

    try:
        payload = {
            "prompt": prompt,
            "loras": [
                {
                    "path": lora_url,
                    "scale": scale
                }
            ],
            "image_size": aspect_ratio,
            "num_inference_steps": 28,
            "enable_safety_checker": True
        }

        url = "https://fal.run/fal-ai/flux-lora"
        response = requests.post(url, json=payload, headers=headers, timeout=120)
        
        if response.status_code == 200:
            res_json = response.json()
            images = res_json.get("images", [])
            if images:
                image_url = images[0].get("url")
                img_res = requests.get(image_url, timeout=60)
                if img_res.status_code == 200:
                    return img_res.content, None
                return None, f"Nie udało się pobrać wygenerowanego obrazu: {img_res.status_code}"
            return None, "API nie zwróciło żadnego obrazu."
        else:
            return None, f"Błąd fal.ai API ({response.status_code}): {response.text}"
            
    except Exception as ex:
        return None, f"Wyjątek podczas generowania obrazu LoRA: {str(ex)}"


def start_lora_training(zip_file_path, trigger_word="tomasz_hero", steps=1000, is_style=False):
    """
    Rozpoczyna trening LoRA na fal.ai za pomocą biblioteki fal_client.
    Wgrywa lokalny plik ZIP na CDN fal.ai i wysyła asynchroniczne zlecenie treningu.
    Zwraca request_id lub None i błąd.
    """
    import fal_client
    try:
        # Upewniamy się, że klucz jest ustawiony w środowisku dla fal_client
        key = os.getenv("FAL_KEY") or FAL_KEY
        if key:
            os.environ["FAL_KEY"] = key
        else:
            return None, "Brak klucza FAL_KEY w środowisku lub .env!"

        # 1. Wgranie pliku ZIP do fal.ai storage (CDN)
        images_url = fal_client.upload_file(zip_file_path)
        if not images_url:
            return None, "Nie udało się wgrać pliku ZIP do storage fal.ai."
        
        # 2. Wysłanie zlecenia treningowego w tle (asynchronicznie)
        handler = fal_client.submit(
            "fal-ai/flux-lora-fast-training",
            arguments={
                "images_data_url": images_url,
                "trigger_word": trigger_word,
                "steps": steps,
                "is_style": is_style,
                "create_masks": True
            }
        )
        
        if hasattr(handler, "request_id"):
            return handler.request_id, None
        return None, "Nie udało się uzyskać request_id z handlera fal_client."
    except Exception as ex:
        return None, f"Błąd podczas rozpoczynania treningu LoRA: {str(ex)}"


def check_training_status(request_id):
    """
    Sprawdza stan asynchronicznego treningu LoRA na fal.ai.
    Zwraca status i logi lub None i błąd.
    """
    import fal_client
    try:
        key = os.getenv("FAL_KEY") or FAL_KEY
        if key:
            os.environ["FAL_KEY"] = key

        status = fal_client.status("fal-ai/flux-lora-fast-training", request_id, with_logs=True)
        return status, None
    except Exception as ex:
        return None, f"Błąd podczas sprawdzania statusu treningu: {str(ex)}"


def get_training_result(request_id):
    """
    Pobiera wynik zakończonego treningu LoRA na fal.ai.
    Zwraca URL do pliku wag (.safetensors) lub None i błąd.
    """
    import fal_client
    try:
        key = os.getenv("FAL_KEY") or FAL_KEY
        if key:
            os.environ["FAL_KEY"] = key

        result = fal_client.result("fal-ai/flux-lora-fast-training", request_id)
        if result and "diffusers_lora_file" in result:
            return result["diffusers_lora_file"]["url"], None
        return None, f"Brak klucza diffusers_lora_file w wyniku treningu. Otrzymano: {result}"
    except Exception as ex:
        return None, f"Błąd podczas pobierania wyniku treningu: {str(ex)}"
