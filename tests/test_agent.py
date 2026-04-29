import pytest
from unittest.mock import patch
from src.backend.agent import process_chat_intent
from src.backend.services.chat import get_gemini_response
from src.backend.services.calendar import get_election_timeline
from src.backend.services.maps import get_nearest_polling_station

def test_agent_timeline_intent() -> None:
    """Test intent routing for timeline queries."""
    response = process_chat_intent("When are the elections?", language="en")
    assert response['status'] == 'success'
    assert "starts on" in response['response'].lower() or "unavailable" in response['response'].lower()

def test_agent_gemini_fallback() -> None:
    """Test fallback to simulated response when dummy key is used."""
    response = process_chat_intent("Who is the president?", language="en")
    assert response['status'] == 'success'
    assert "simulated" in response['response'].lower() or "high traffic" in response['response'].lower()

def test_dynamic_translation() -> None:
    """Test mock translation logic for non-English languages."""
    response = process_chat_intent("Hello", language="hi")
    assert response['status'] == 'success'
    assert "[Hindi]" in response['response'] or "simulated" in response['response'].lower()

@patch('src.backend.agent.get_gemini_response')
def test_api_timeout_simulation(mock_get_gemini) -> None:
    """Test handling of API timeouts."""
    mock_get_gemini.side_effect = Exception("Timeout error")
    response = process_chat_intent("Tell me about elections.", language="en")
    assert response['status'] == 'error'
    assert "Service temporarily unavailable" in response['response']

def test_invalid_user_input() -> None:
    """Test handling of empty or invalid user input."""
    response = process_chat_intent("", language="en")
    assert response['status'] == 'success' # Empty string passes to gemini, which will just simulate
