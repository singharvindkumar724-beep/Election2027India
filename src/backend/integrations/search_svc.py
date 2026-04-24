import os
from google import genai
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

def get_election_facts(query: str = "Provide 3 important, general facts about voting in US elections, formatted as a bulleted list. Do not include introductory or concluding text.") -> Dict[str, Any]:
    """
    Fetches election facts via Gemini.
    Provides a gracefully degraded mock if API keys are missing.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key == "AIzaSyYourFakeApiKeyForHackathon":
        return {
            "status": "mock",
            "service": "Search",
            "data": {
                "facts": [
                    "Voting is your democratic right.",
                    "The Election Commission of India conducts the elections.",
                    "EVMs (Electronic Voting Machines) are used widely."
                ]
            }
        }
        
    import time
    
    # Prevent google.genai from overriding our GEMINI_API_KEY with GOOGLE_API_KEY
    temp_google_key = os.environ.pop("GOOGLE_API_KEY", None)
    try:
        client = genai.Client(api_key=api_key)
    finally:
        if temp_google_key is not None:
            os.environ["GOOGLE_API_KEY"] = temp_google_key
            
    try:
        
        # Add retry loop for 503 Unavailable / High Demand
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=query,
                )
                
                # Simple parsing to get bullet points
                facts = [line.strip().lstrip('*- ') for line in response.text.split('\n') if line.strip().startswith(('*', '-'))]
                
                if not facts:
                    # Fallback if the model didn't format as bullets
                    facts = [response.text.strip()]

                return {
                    "status": "live",
                    "service": "Search (Gemini)",
                    "data": {
                        "facts": facts
                    }
                }
            except Exception as e:
                # If it's the last attempt or not a 503/429, break
                if attempt == max_retries - 1 or ('503' not in str(e) and '429' not in str(e)):
                    raise e
                time.sleep(2) # Wait 2 seconds before retrying
                
    except Exception as e:
        # Fallback gracefully to mock data if Gemini is overloaded
        print(f"Gemini API Error: {str(e)}. Falling back to mock data.")
        return {
            "status": "mock_fallback",
            "service": "Search (Gemini Fallback)",
            "data": {
                "facts": [
                    "Voting is your democratic right.",
                    "The Election Commission of India conducts the elections.",
                    "EVMs (Electronic Voting Machines) are used widely.",
                    "(Note: The AI model is currently experiencing high demand. This is a generic offline response.)"
                ]
            }
        }


