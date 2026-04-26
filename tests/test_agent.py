import pytest
from src.backend.agent import process_chat_intent

def test_agent_timeline_intent():
    # Test intent routing
    response = process_chat_intent("When are the elections?", language="en")
    assert response['status'] == 'success'
    assert "starts on" in response['response'].lower()

def test_agent_gemini_fallback():
    # Test fallback to simulated response when dummy key is used
    response = process_chat_intent("Who is the president?", language="en")
    assert response['status'] == 'success'
    # Checking for dummy response or actual fallback
    assert "simulated gemini response" in response['response'].lower() or "high traffic" in response['response'].lower()

def test_dynamic_translation():
    # Test mock translation logic
    response = process_chat_intent("Hello", language="hi")
    assert response['status'] == 'success'
    assert "[Hindi]" in response['response'] or "simulated" in response['response'].lower()
