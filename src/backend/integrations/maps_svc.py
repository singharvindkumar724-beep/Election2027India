import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

def get_polling_location() -> Dict[str, Any]:
    """
    Fetches polling location via Google Maps API.
    Provides a gracefully degraded mock if API keys are missing.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key or api_key == "AIzaSyYourFakeApiKeyForHackathon":
        return {
            "status": "mock",
            "service": "Maps",
            "data": {
                "nearest_location": "Lincoln High School Gymnasium",
                "address": "123 Civic Way, Springfield",
                "distance": "0.8 miles away",
                "accessible_transit": ["Bus Route 42 (Wheelchair accessible)", "Subway Blue Line (Stop: Civic Center)"]
            }
        }
        
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=polling+locations+near+me&key={api_key}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {
             "status": "error",
             "service": "Maps",
             "data": {"message": "Failed to fetch from Maps API."}
        }

    results = response.json().get('results', [])
    
    if not results:
         return {
             "status": "live",
             "service": "Maps",
             "data": {
                 "nearest_location": "No locations found nearby.",
                 "address": "N/A",
                 "distance": "N/A",
                 "accessible_transit": []
             }
         }

    first_result = results[0]

    return {
         "status": "live",
         "service": "Maps",
         "data": {
            "nearest_location": first_result.get('name', 'Unknown Location'),
            "address": first_result.get('formatted_address', 'Unknown Address'),
            "distance": "Distance info not available in textsearch",
            "accessible_transit": ["Transit info not available"]
         }
    }

