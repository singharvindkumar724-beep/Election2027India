import os
from typing import Dict, Any
from dotenv import load_dotenv
from googleapiclient.discovery import build
import datetime

load_dotenv()

def get_election_deadlines() -> Dict[str, Any]:
    """
    Fetches election deadlines via Google Calendar API.
    Provides a gracefully degraded mock if API keys are missing.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # Fallback Mechanism: If no real key, provide rich, mock data.
    if not api_key or api_key == "AIzaSyYourFakeApiKeyForHackathon":
        return {
            "status": "mock",
            "service": "Calendar",
            "data": {
                "events": [
                    {"name": "Voter Registration Deadline", "date": "October 5th, 2024"},
                    {"name": "Early Voting Starts", "date": "October 24th, 2024"},
                    {"name": "Election Day", "date": "November 5th, 2024"}
                ]
            }
        }
    
    # Implementation for Google API Client
    try:
        service = build('calendar', 'v3', developerKey=api_key)
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        # US Holidays calendar as an example to get "Election Day" and other holidays
        # In a real app, this would be a specific state/local election calendar ID
        calendar_id = 'en.usa#holiday@group.v.calendar.google.com'
        
        events_result = service.events().list(
            calendarId=calendar_id, 
            timeMin=now,
            maxResults=10, 
            singleEvents=True,
            orderBy='startTime',
            q='Election' # Search for events with "Election" in the name
        ).execute()
        
        events = events_result.get('items', [])
        
        formatted_events = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            formatted_events.append({
                "name": event['summary'],
                "date": start
            })
            
        if not formatted_events:
            formatted_events = [{"name": "No upcoming election events found.", "date": "N/A"}]
            
        return {
            "status": "live",
            "service": "Calendar",
            "data": {
                "events": formatted_events
            }
        }
    except Exception as e:
         return {
            "status": "error",
            "service": "Calendar",
            "data": {
                "message": f"Failed to fetch from Calendar API: {str(e)}"
            }
        }

