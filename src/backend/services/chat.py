import os
import google.generativeai as genai

# Configure Gemini (Expects API key in environment)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "dummy-key"))

def get_gemini_response(prompt):
    """
    Calls Google Gemini API with fallback logic.
    """
    try:
        # In production, use standard model. Using dummy logic if no key.
        if os.environ.get("GEMINI_API_KEY") == "dummy-key" or not os.environ.get("GEMINI_API_KEY"):
            return "This is a simulated Gemini response based on your query: " + prompt
            
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            f"You are Civic360, a helpful Indian Election assistant. Answer safely and neutrally: {prompt}"
        )
        return response.text
    except Exception as e:
        # Fallback if Gemini quota is exceeded or API fails
        print(f"Gemini API Error: {e}")
        return "I am currently experiencing high traffic. Please check the official Election Commission website for immediate updates."
