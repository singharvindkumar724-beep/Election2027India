import html
from src.backend.services.chat import get_gemini_response
from src.backend.services.calendar import get_election_timeline

def translate_text(text, target_language):
    """
    Mock Google Cloud Translation API for dynamic chat localization.
    In a real scenario, this would call the Google Cloud Translation API.
    """
    if target_language == 'en':
        return text
    # Mock translations for demo
    translations = {
        "hi": f"[Hindi]: {text}",
        "ta": f"[Tamil]: {text}",
        "te": f"[Telugu]: {text}"
    }
    return translations.get(target_language, f"[{target_language.upper()}]: {text}")

def process_chat_intent(message, language='en'):
    """
    NLP Router: Determines intent and calls appropriate services.
    Ensures output is also sanitized.
    """
    lower_msg = message.lower()
    
    try:
        if 'when' in lower_msg or 'timeline' in lower_msg or 'date' in lower_msg:
            timeline = get_election_timeline()
            # Safety check if timeline failed
            if timeline.get("status") == "error":
                response_text = "I'm having trouble fetching the timeline right now."
            else:
                response_text = f"The upcoming election starts on {timeline['phases'][0]['date']}."
        else:
            # Call Gemini API for core conversational assistant
            response_text = get_gemini_response(message)
            
        # Dynamic translation based on user preference
        translated_response = translate_text(response_text, language)
        
        # Security: Sanitize output before sending to client
        safe_output = html.escape(translated_response)
        
        return {"response": safe_output, "status": "success"}
    except Exception as e:
        # Fallback logic
        error_msg = html.escape(f"Service temporarily unavailable: {str(e)}. Please refer to our static FAQ.")
        translated_error = translate_text(error_msg, language)
        return {"response": translated_error, "status": "error"}
