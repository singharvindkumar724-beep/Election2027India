import os
import functools
from typing import Optional
import google.generativeai as genai

# Configure Gemini (Expects API key in environment)
api_key: Optional[str] = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@functools.lru_cache(maxsize=256)
def get_gemini_response(prompt: str) -> str:
    """
    Calls Google Gemini API with fallback logic.
    Uses lru_cache to prevent duplicate network calls for the same prompt.
    
    Args:
        prompt (str): The user's input prompt.
        
    Returns:
        str: The generated response from Gemini or a fallback message.
    """
    try:
        # In production, use standard model. Using dummy logic if no key or dummy key.
        if os.environ.get("GEMINI_API_KEY") == "dummy-key" or not os.environ.get("GEMINI_API_KEY"):
            return "This is a simulated Gemini response based on your query: " + prompt
            
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            f"You are Election2027India, a helpful Indian Election assistant. Answer safely and neutrally: {prompt}"
        )
        return response.text
    except Exception as e:
        # Fallback if Gemini quota is exceeded or API fails
        print(f"Gemini API Error: {e}")
        return "I am currently experiencing high traffic. Please check the official Election Commission website for immediate updates."
