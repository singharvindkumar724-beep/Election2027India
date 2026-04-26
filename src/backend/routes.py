from flask import jsonify, request
import html
from src.backend.agent import process_chat_intent
from src.backend.services.calendar import get_election_timeline
from src.backend.services.maps import get_nearest_polling_station

def register_routes(app):
    @app.route('/api/chat', methods=['POST'])
    def chat_endpoint():
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Invalid payload"}), 400
            
        # Security: Input Sanitization (HTML Escaping) to prevent XSS
        raw_message = data.get('message', '')
        sanitized_message = html.escape(raw_message)
        language = data.get('language', 'en')
        
        response = process_chat_intent(sanitized_message, language)
        return jsonify(response)

    @app.route('/api/timeline', methods=['GET'])
    def timeline_endpoint():
        # Returns election phases
        return jsonify(get_election_timeline())

    @app.route('/api/location', methods=['POST'])
    def location_endpoint():
        data = request.get_json()
        if not data or 'zipcode' not in data:
            return jsonify({"error": "zipcode required"}), 400
        
        # Security: Input Sanitization
        zipcode = html.escape(str(data.get('zipcode')))
        return jsonify(get_nearest_polling_station(zipcode))
