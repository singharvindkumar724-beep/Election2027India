import os
import requests

def translate_text(text: str, target_lang: str) -> str:
    """
    Translates text to the target language using Google Cloud Translation API (REST).
    If it fails, it gracefully falls back to the original text.
    """
    if target_lang == "en" or not text:
        return text

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key.startswith("AIzaSyYourFakeApiKey"):
        # Mock behavior for local testing if no translation key
        if target_lang == "hi":
             return f"[Hindi Translation] {text}"
        return text

    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
    
    payload = {
        "q": text,
        "target": target_lang
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            return data["data"]["translations"][0]["translatedText"]
        else:
            print(f"Translation error: {response.text}")
            return text
    except Exception as e:
        print(f"Translation exception: {str(e)}")
        return text
