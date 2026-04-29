import html
from typing import Dict, Any

from src.backend.services.chat import get_gemini_response
from src.backend.services.calendar import get_election_timeline
from src.backend.services.translation import translate_text

def process_chat_intent(message: str, language: str = 'en') -> Dict[str, Any]:
    """
    NLP Router: Determines intent and calls appropriate services.
    Ensures output is also sanitized.
    
    Args:
        message (str): The user's input message.
        language (str): The target language code. Defaults to 'en'.
        
    Returns:
        Dict[str, Any]: A dictionary containing the response text and status.
    """
    lower_msg: str = message.lower()
    
    try:
        if 'when' in lower_msg or 'timeline' in lower_msg or 'date' in lower_msg:
            timeline: Dict[str, Any] = get_election_timeline()
            # Safety check if timeline failed
            if timeline.get("status") == "error":
                response_text: str = "I'm having trouble fetching the timeline right now."
            else:
                phases = timeline.get('phases', [])
                if phases:
                    response_text = f"The upcoming election starts on {phases[0]['date']}."
                else:
                    response_text = "Timeline information is currently unavailable."
        else:
            # Call Gemini API for core conversational assistant
            response_text = get_gemini_response(message)
            
        # Dynamic translation based on user preference
        translated_response: str = translate_text(response_text, language)
        
        # Security: Sanitize output before sending to client
        safe_output: str = html.escape(translated_response)
        
        return {"response": safe_output, "status": "success"}
    except Exception as e:
        # Fallback logic
        error_msg: str = f"Service temporarily unavailable: {str(e)}. Please refer to our static FAQ."
        translated_error: str = translate_text(error_msg, language)
        return {"response": html.escape(translated_error), "status": "error"}
