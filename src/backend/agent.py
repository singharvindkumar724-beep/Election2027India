from typing import Dict, Any, List
from src.backend.integrations.calendar_svc import get_election_deadlines
from src.backend.integrations.maps_svc import get_polling_location
from src.backend.integrations.search_svc import get_election_facts
from src.backend.integrations.sheets_svc import get_candidates
from src.backend.integrations.translate_svc import translate_text

class IntentRouter:
    def __init__(self):
        self.calendar_keywords = ["when", "date", "time", "deadline", "schedule", "calendar"]
        self.maps_keywords = ["where", "location", "place", "polling", "map", "address", "go"]
        self.candidate_keywords = ["candidate", "who", "politician", "party", "profile", "leader"]
        self.civic_keywords = ["how to vote", "why vote", "civic", "education", "under 18", "youth"]

    def route_query(self, query: str, lang: str = "en") -> Dict[str, Any]:
        """
        Routes the user's text query to the appropriate service module.
        Translates from the requested language to English for routing, then back.
        """
        # 1. Translate input to English (if needed)
        eng_query = translate_text(query, "en") if lang != "en" else query
        query_lower = eng_query.lower()
        
        # 2. Routing Logic
        if any(keyword in query_lower for keyword in self.maps_keywords):
            response_data = get_polling_location()
            intent = "action_phase"
        elif any(keyword in query_lower for keyword in self.candidate_keywords):
            response_data = get_candidates()
            intent = "candidate_profiles"
        elif any(keyword in query_lower for keyword in self.calendar_keywords):
            response_data = get_election_deadlines()
            intent = "planning_phase"
        elif any(keyword in query_lower for keyword in self.civic_keywords):
            response_data = {
                "status": "live",
                "service": "Civic Education",
                "data": {
                    "facts": [
                        "Voting is a fundamental democratic right in India.",
                        "You must be 18 years old to vote.",
                        "Registering to vote is simple and can be done online."
                    ]
                }
            }
            intent = "civic_education"
        else:
            # Fallback to general conversational chat (Gemini)
            # We'll use the search service but it acts as general Q&A
            response_data = get_election_facts(eng_query) # Passing the specific query
            intent = "information_phase"

        # 3. Translate string fields in response back to target language (Basic implementation)
        if lang != "en":
            # For hackathon simplicity, we just add a localized flag or translate the main message
            # In a full app, we'd recursively traverse the JSON and translate all text values.
            response_data["service"] = f"{response_data.get('service', '')} (Translated)"
            if "message" in response_data.get("data", {}):
                response_data["data"]["message"] = translate_text(response_data["data"]["message"], lang)

        return {
            "intent": intent,
            "response": response_data,
            "detected_language": lang
        }
