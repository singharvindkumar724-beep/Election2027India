import pytest
from src.backend.agent import IntentRouter

def test_intent_router_maps():
    """Test that location-based queries route to the Maps service."""
    router = IntentRouter()
    
    # User asks where to vote
    result1 = router.route_query("Where do I go to vote?")
    assert result1["intent"] == "action_phase"
    assert result1["response"]["service"] == "Maps"
    
    # User asks for nearest polling place
    result2 = router.route_query("Find nearest polling place")
    assert result2["intent"] == "action_phase"
    assert "address" in result2["response"]["data"]

def test_intent_router_calendar():
    """Test that timeline/date-based queries route to the Calendar service."""
    router = IntentRouter()
    
    # User asks for dates
    result1 = router.route_query("When is the registration deadline?")
    assert result1["intent"] == "planning_phase"
    assert result1["response"]["service"] == "Calendar"
    
    # User asks for schedule
    result2 = router.route_query("What is the election schedule?")
    assert result2["intent"] == "planning_phase"
    assert len(result2["response"]["data"]["events"]) > 0

def test_intent_router_search():
    """Test that general queries route to the Search service (Gemini)."""
    router = IntentRouter()
    
    # User asks general fact question
    result1 = router.route_query("What is the election procedure?")
    assert result1["intent"] == "information_phase"

def test_intent_router_candidates():
    """Test candidate queries."""
    router = IntentRouter()
    result = router.route_query("Who is running for candidate?")
    assert result["intent"] == "candidate_profiles"
    assert result["response"]["service"] == "Sheets (Local)"

def test_intent_router_civic():
    """Test civic education queries."""
    router = IntentRouter()
    result = router.route_query("Why vote in the elections?")
    assert result["intent"] == "civic_education"
    assert result["response"]["service"] == "Civic Education"

def test_intent_router_fallback():
    """Test that an unknown query hits the fallback logic (Gemini)."""
    router = IntentRouter()
    
    result = router.route_query("Tell me a joke")
    assert result["intent"] == "information_phase"
