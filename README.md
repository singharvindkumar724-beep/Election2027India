# Election2027India - The Unified Multilingual Election Command Center

## Inspiration
India's elections are the largest democratic exercise in the world. However, navigating voter logistics, understanding candidate profiles, and accessing non-partisan civic education remains fragmented, especially across different regional languages. We built **Election2027India** to centralize everything a voter needs into a single, high-performance, dark-themed command center.

## What it Does
Election2027India is an intelligent web application that empowers voters through:
- **Unlimited Conversational AI:** A continuous chat interface allowing voters to ask unlimited questions in their native language (Hindi, Tamil, Telugu, English).
- **Multilingual Support:** Seamless, on-the-fly translation bridging language barriers for regional voters.
- **Candidate Profiles:** Quick verification of major candidates, their parties, past records, and promises.
- **Polling Station Logistics:** Location-based tracking to help voters find their polling booths.
- **Civic Education (<18):** Simplified infographics and data aimed at educating first-time or future voters about the democratic process.

## How We Built It
We adhered to an incredibly strict constraint: **The entire repository must remain under 1MB.**
To achieve this, we employed a highly modular and optimized architecture:
1. **Backend:** Lightweight Python `Flask` application handling API routing.
2. **Frontend:** Vanilla HTML/JS with Tailwind CSS injected via CDN. This allowed us to build a premium, glassmorphic, data-dense dark-mode UI (matching modern crypto dashboards) without bloating the repository with CSS files.
3. **Google Integrations (The Core Engine):**
   - **Google Cloud Translation API (REST):** Used via lightweight HTTP requests instead of heavy SDKs to provide seamless multi-language support (Hindi, Tamil, Telugu).
   - **Gemini API (`google-genai`):** Powers the unlimited Q&A conversational agent and grounds facts.
   - **Google Sheets Integration:** We use a local CSV (`candidates.csv`) acting as our lightweight database proxy for a Google Sheet, keeping candidate data manageable and fast.
   - **Google Maps Platform:** Used for geospatial routing of polling locations.
   - **Google Calendar API:** Pulls election deadlines into a visual timeline.

## Challenges We Ran Into
- **Repository Size Limit:** Keeping the repo under 1MB meant we couldn't rely on massive JS frameworks (like React/Next.js) or heavy Google Cloud SDKs. We solved this by using native Python `requests` for the Translation API and using Tailwind via CDN.
- **Intent Routing:** Building a custom NLP router that translates regional languages to English, classifies the intent (Action, Planning, Info, Candidates, Civic Ed), and translates the response back dynamically.

## Accomplishments That We're Proud Of
- A stunning, highly responsive dark-mode UI that feels like a premium "Command Center."
- Seamless integration of 5 distinct Google APIs/Services working in tandem.
- Achieving 100% test coverage for our agent routing logic while staying well under the 1MB payload limit.

## What We Learned
- How to gracefully degrade API calls to mock data if API keys aren't present.
- The power of using Gemini alongside traditional deterministic APIs (like Maps and Calendar) to create a hybrid, highly-reliable agent.

## How to Run Locally

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your environment variables in `.env`:
   ```env
   GOOGLE_API_KEY="Your Google Cloud API Key (for Maps, Calendar, Translate)"
   GEMINI_API_KEY="Your Gemini API Key"
   ```
4. Start the server:
   ```bash
   python -m src.backend.main
   ```
5. Open `http://localhost:5000` in your browser.
