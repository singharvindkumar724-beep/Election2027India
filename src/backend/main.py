import sys
import os
from flask import Flask, request, jsonify, render_template
from src.backend.agent import IntentRouter

# Set up Flask to point to the frontend directories
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir, static_url_path='/static')
router = IntentRouter()

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/ask', methods=['POST'])
def ask_agent():
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                "intent": "error",
                "response": {
                    "status": "error",
                    "data": {"message": "Invalid request. 'query' is required."}
                }
            }), 400

        user_query = data['query']
        lang = data.get('lang', 'en') # Default to English if not specified
        
        result = router.route_query(user_query, lang)
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in /api/ask: {e}", file=sys.stderr)
        return jsonify({
            "intent": "error",
            "response": {
                "status": "error",
                "data": {"message": f"An internal server error occurred: {str(e)}"}
            }
        }), 500

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)
