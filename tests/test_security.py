import pytest
from src.backend.main import app
import time

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_rate_limiter(client):
    # Send 5 requests within the window
    for _ in range(5):
        response = client.post('/api/chat', json={'message': 'hello', 'language': 'en'})
        # Should be successful, or at least not 429
        assert response.status_code != 429
        
    # The 6th request should hit the rate limiter
    response = client.post('/api/chat', json={'message': 'hello', 'language': 'en'})
    assert response.status_code == 429
    assert b"Rate limit exceeded" in response.data

def test_input_sanitization(client):
    # Test XSS prevention
    malicious_payload = "<script>alert('XSS')</script>"
    response = client.post('/api/chat', json={'message': malicious_payload, 'language': 'en'})
    
    # We should not see raw HTML tags in the response payload
    assert response.status_code == 200
    assert b"<script>" not in response.data
    assert b"&lt;script&gt;" in response.data or b"error" in response.data # It should be HTML escaped

def test_security_headers(client):
    response = client.get('/api/timeline')
    assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    assert response.headers.get('X-Frame-Options') == 'DENY'
    assert response.headers.get('X-XSS-Protection') == '1; mode=block'
