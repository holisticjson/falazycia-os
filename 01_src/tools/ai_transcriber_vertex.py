import os
from google import genai
from google.genai import types
from pathlib import Path

# Path to your Service Account
SA_KEY_PATH = r"c:\Aplikacje MVP\Holistic Jason\holistic-dashboard-dev-dea2c872139e.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_KEY_PATH

def ai_transcribe_video(video_url):
    client = genai.Client(
        vertexai=True,
        project="holistic-dashboard-dev",
        location="us-central1"
    )
    
    print(f"Asking Gemini to analyze: {video_url}")
    
    prompt = """
    Przeanalizuj ten film z YouTube i wygeneruj bardzo szczegółową transkrypcję lub streszczenie lekcji punkt po punkcie. 
    Skup się na konkretnych technikach, promptach i radach, które padają w wideo.
    Zwróć wynik w formacie Markdown.
    """
    
    try:
        # Note: Gemini 1.5 Pro can take YouTube URLs in some configurations
        response = client.models.generate_content(
            model="gemini-1.5-pro",
            contents=[
                types.Part.from_uri(file_uri=video_url, mime_type="video/mp4"), # Experimental URI support
                prompt
            ]
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test for the first lesson
    url = "https://www.youtube.com/watch?v=xlG3SRkIzRQ"
    result = ai_transcribe_video(url)
    print(result)
