import os
from unittest.mock import patch, MagicMock
from src.backend.integrations.maps_svc import get_polling_location
from src.backend.integrations.calendar_svc import get_election_deadlines
from src.backend.integrations.search_svc import get_election_facts

@patch('src.backend.integrations.maps_svc.os.getenv')
@patch('src.backend.integrations.maps_svc.requests.get')
def test_maps_live_branch(mock_get, mock_getenv):
    # Setup mock to simulate having a real key
    mock_getenv.return_value = "REAL_TEST_KEY"
    
    # Setup mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [
            {
                "name": "Live Mock High School",
                "formatted_address": "456 Test Ave, City"
            }
        ]
    }
    mock_get.return_value = mock_response
    
    result = get_polling_location()
    
    assert result["status"] == "live"
    assert result["service"] == "Maps"
    assert result["data"]["nearest_location"] == "Live Mock High School"
    assert result["data"]["address"] == "456 Test Ave, City"

@patch('src.backend.integrations.calendar_svc.os.getenv')
@patch('src.backend.integrations.calendar_svc.build')
def test_calendar_live_branch(mock_build, mock_getenv):
    # Setup mock to simulate having a real key
    mock_getenv.return_value = "REAL_TEST_KEY"
    
    # Setup mock calendar service response
    mock_service = MagicMock()
    mock_events = MagicMock()
    mock_list_request = MagicMock()
    
    mock_list_request.execute.return_value = {
        "items": [
            {
                "summary": "Live Mock Election Day",
                "start": {"date": "2024-11-05"}
            }
        ]
    }
    
    mock_events.list.return_value = mock_list_request
    mock_service.events.return_value = mock_events
    mock_build.return_value = mock_service
    
    result = get_election_deadlines()
    
    assert result["status"] == "live"
    assert result["service"] == "Calendar"
    assert len(result["data"]["events"]) == 1
    assert result["data"]["events"][0]["name"] == "Live Mock Election Day"
    assert result["data"]["events"][0]["date"] == "2024-11-05"

@patch('src.backend.integrations.search_svc.os.getenv')
@patch('src.backend.integrations.search_svc.genai.Client')
def test_search_live_branch(mock_client, mock_getenv):
    # Setup mock to simulate having a real key
    mock_getenv.return_value = "REAL_TEST_KEY"
    
    # Setup mock Gemini response
    mock_client_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "- Live Fact 1\n- Live Fact 2"
    
    mock_client_instance.models.generate_content.return_value = mock_response
    mock_client.return_value = mock_client_instance
    
    result = get_election_facts()
    
    assert result["status"] == "live"
    assert result["service"] == "Search (Gemini)"
    assert len(result["data"]["facts"]) == 2
    assert "Live Fact 1" in result["data"]["facts"]
    assert "Live Fact 2" in result["data"]["facts"]
