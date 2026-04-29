import os
import sys
import time
from typing import Dict, List, Any
from flask import Flask, request, jsonify, send_from_directory, Response
from flask_cors import CORS
from src.backend.routes import register_routes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def validate_env_variables() -> None:
    """
    Validates that all required environment variables are present on startup.
    Throws a fatal error if any are missing.
    """
    required_vars: List[str] = ["GEMINI_API_KEY"]
    missing_vars: List[str] = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"FATAL ERROR: Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)

# Validate before initializing the app
validate_env_variables()

# Create absolute path to frontend directory
frontend_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
app: Flask = Flask(__name__, static_folder=frontend_dir, static_url_path='')

# Security: CORS implementation
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Security: Rate Limiter (5 requests per minute per IP)
RATE_LIMIT: int = 5
RATE_LIMIT_WINDOW: int = 60 # seconds
request_history: Dict[str, List[float]] = {}

@app.before_request
def rate_limiter() -> Any:
    """
    Implements rate limiting for API endpoints.
    Allows 5 requests per minute per IP address.
    
    Returns:
        Response with 429 status code if limit exceeded, else None.
    """
    if not request.path.startswith('/api/'):
        return None
        
    ip: str = request.remote_addr or "unknown"
    current_time: float = time.time()
    
    if ip not in request_history:
        request_history[ip] = []
    
    # Filter out requests older than the window
    request_history[ip] = [t for t in request_history[ip] if current_time - t < RATE_LIMIT_WINDOW]
    
    if len(request_history[ip]) >= RATE_LIMIT:
        return jsonify({"error": "Rate limit exceeded. Maximum 5 requests per minute."}), 429
        
    request_history[ip].append(current_time)
    return None

@app.after_request
def add_security_headers(response: Response) -> Response:
    """
    Adds advanced security headers to every response.
    
    Args:
        response (Response): The Flask response object.
        
    Returns:
        Response: The modified Flask response object with added security headers.
    """
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; img-src 'self' data:;"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

@app.route('/')
def serve_frontend() -> Response:
    """
    Serves the main frontend index.html file.
    
    Returns:
        Response: The index.html file.
    """
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path: str) -> Response:
    """
    Serves static frontend files.
    
    Args:
        path (str): The path to the static file.
        
    Returns:
        Response: The static file.
    """
    return send_from_directory(app.static_folder, path)

register_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
