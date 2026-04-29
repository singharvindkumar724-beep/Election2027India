import functools
from typing import Dict

@functools.lru_cache(maxsize=128)
def translate_text(text: str, target_language: str) -> str:
    """
    Mock Google Cloud Translation API for dynamic chat localization.
    Uses lru_cache for efficiency so repeated translations resolve instantly.
    
    Args:
        text (str): The text to translate.
        target_language (str): The target language code (e.g., 'hi', 'ta', 'te').
        
    Returns:
        str: The translated text.
    """
    if target_language == 'en':
        return text
    
    # Mock translations for demo
    translations: Dict[str, str] = {
        "hi": f"[Hindi]: {text}",
        "ta": f"[Tamil]: {text}",
        "te": f"[Telugu]: {text}"
    }
    
    return translations.get(target_language, f"[{target_language.upper()}]: {text}")
