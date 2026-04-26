import os
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from src.backend.routes import register_routes

# Create absolute path to frontend directory
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
app = Flask(__name__, static_folder=frontend_dir, static_url_path='')

# Security: CORS implementation
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Security: Rate Limiter (5 requests per minute per IP)
RATE_LIMIT = 5
RATE_LIMIT_WINDOW = 60 # seconds
request_history = {}

@app.before_request
def rate_limiter():
    if not request.path.startswith('/api/chat'):
        return
    ip = request.remote_addr
    current_time = time.time()
    
    if ip not in request_history:
        request_history[ip] = []
    
    # Filter out requests older than the window
    request_history[ip] = [t for t in request_history[ip] if current_time - t < RATE_LIMIT_WINDOW]
    
    if len(request_history[ip]) >= RATE_LIMIT:
        return jsonify({"error": "Rate limit exceeded. Maximum 5 requests per minute."}), 429
        
    request_history[ip].append(current_time)

# Security Headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# Serve Frontend Files
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

register_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
