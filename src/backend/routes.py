from flask import jsonify, request, Flask, Response
import html
from typing import Dict, Any, Tuple

from src.backend.agent import process_chat_intent
from src.backend.services.calendar import get_election_timeline
from src.backend.services.maps import get_nearest_polling_station

def register_routes(app: Flask) -> None:
    """
    Registers all API routes for the Flask application.
    
    Args:
        app (Flask): The Flask application instance.
    """
    
    @app.route('/api/chat', methods=['POST'])
    def chat_endpoint() -> Tuple[Response, int]:
        """
        Endpoint for chat interactions.
        
        Returns:
            Tuple[Response, int]: The JSON response and HTTP status code.
        """
        data: Dict[str, Any] = request.get_json() or {}
        if not data or 'message' not in data:
            return jsonify({"error": "Invalid payload"}), 400
            
        # Security: Input Sanitization (HTML Escaping) to prevent XSS
        raw_message: str = data.get('message', '')
        sanitized_message: str = html.escape(raw_message)
        language: str = data.get('language', 'en')
        
        response: Dict[str, Any] = process_chat_intent(sanitized_message, language)
        return jsonify(response), 200

    @app.route('/api/timeline', methods=['GET'])
    def timeline_endpoint() -> Response:
        """
        Endpoint to retrieve the election timeline.
        
        Returns:
            Response: The JSON response containing the election phases.
        """
        # Returns election phases
        return jsonify(get_election_timeline())

    @app.route('/api/location', methods=['POST'])
    def location_endpoint() -> Tuple[Response, int]:
        """
        Endpoint to retrieve the nearest polling station based on zipcode.
        
        Returns:
            Tuple[Response, int]: The JSON response and HTTP status code.
        """
        data: Dict[str, Any] = request.get_json() or {}
        if not data or 'zipcode' not in data:
            return jsonify({"error": "zipcode required"}), 400
        
        # Security: Input Sanitization
        zipcode: str = html.escape(str(data.get('zipcode')))
        return jsonify(get_nearest_polling_station(zipcode)), 200
