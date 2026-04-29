import pytest
from src.backend.main import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Reset rate limit history
    from src.backend.main import request_history
    request_history.clear()
    with app.test_client() as client:
        yield client

def test_rate_limiter_trigger(client) -> None:
    """Test the rate limiter gets triggered after 5 requests."""
    # Send 5 requests within the window
    for _ in range(5):
        response = client.post('/api/chat', json={'message': 'hello', 'language': 'en'})
        assert response.status_code != 429
        
    # The 6th request should hit the rate limiter
    response = client.post('/api/chat', json={'message': 'hello', 'language': 'en'})
    assert response.status_code == 429
    assert b"Rate limit exceeded" in response.data

def test_input_sanitization(client) -> None:
    """Test XSS prevention via HTML escaping."""
    malicious_payload = "<script>alert('XSS')</script>"
    response = client.post('/api/chat', json={'message': malicious_payload, 'language': 'en'})
    
    assert response.status_code == 200
    assert b"<script>" not in response.data
    assert b"&lt;script&gt;" in response.data

def test_security_headers(client) -> None:
    """Test that all required security headers are present."""
    response = client.get('/api/timeline')
    headers = response.headers
    assert 'Content-Security-Policy' in headers
    assert 'nosniff' in headers.get('X-Content-Type-Options', '')
    assert 'DENY' in headers.get('X-Frame-Options', '')
    assert 'max-age=31536000; includeSubDomains' in headers.get('Strict-Transport-Security', '')

def test_invalid_payload(client) -> None:
    """Test missing parameters return 400 error."""
    response = client.post('/api/chat', json={})
    assert response.status_code == 400
    
    response_loc = client.post('/api/location', json={})
    assert response_loc.status_code == 400
