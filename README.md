# EduGenie: AI-Powered Educational Content Creator

A web tool that generates a full course outline — objective, syllabus,
3 measurable learning outcomes (mapped to Bloom's Taxonomy), assessment
methods, and recommended readings — from just a course title, using
Groq's API.

Built for: Generative AI course capstone project (Internshala Trainings)

---

## Tech Stack
- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript (vanilla, no framework)
- **AI:** Groq API (`llama-3.1-8b-instant`) — OpenAI-compatible endpoint, accessed via the `openai` Python SDK pointed at Groq's `base_url`

## Project Structure
```
edugenie/
├── app.py                # Flask server + Groq API logic
├── requirements.txt      # Python dependencies
├── .env.example           # Template for your API key
├── Procfile               # Tells Render how to run the app
├── templates/
│   └── index.html        # Main page
└── static/
    ├── style.css          # UI styling
    └── script.js          # Frontend logic (fetch call, error handling, copy button)
```
## How it Works
1. User enters a course title in the browser and clicks Generate Content.
2. script.js sends a POST request to /generate with the title as JSON.
3. app.py validates the input (not empty, not too long, safe characters only), then builds a structured prompt and sends it to Groq's API.
4. The prompt explicitly asks for outcomes labeled by Bloom's Taxonomy level (Remember, Understand, Apply, Analyze, Evaluate, Create) so the output is academically measurable, not just generic text.
5. The AI's response is sent back as JSON and rendered in the Output box.
6. Errors (empty input, missing API key, API request failure, network issues) are caught and shown as a readable message instead of a crash.

## Setup Instructions

### 1. Install dependencies
pip install -r requirements.txt

### 2. Add your Groq API key
Copy .env.example to .env and paste your real key:
cp .env.example .env

Then edit .env:
OPENAI_API_KEY=gsk-your-real-groq-key-here

Get a free key from https://console.groq.com/keys

### 3. Run the app
python app.py
<<<<<<< HEAD

Open your browser at: http://127.0.0.1:8080

## Live Demo
Deployed on Render: https://edugenie-zvjd.onrender.com
(Free tier — the app may take up to 50 seconds to wake up if it hasn't been used recently.)

## Data Privacy
The course title is sent to Groq's API only to generate the response for that one request. This app does not write the title, the AI response, or any user data to a database, file, or log — it only lives in memory during the request.
=======
```
Open your browser at: **https://edugenie-zvjd.onrender.com/**

## Data Privacy
The course title is sent to OpenAI only to generate the response for that
one request. This app does not write the title, the AI response, or any
user data to a database, file, or log — it only lives in memory during
the request.

## Testing Checklist (mentioned as required in the problem statement)
- [ ] Empty input → shows "Course title cannot be empty."
- [ ] Very long input (>120 chars) → shows length error
- [ ] Special characters (e.g. `<script>`) → rejected by validation
- [ ] Missing `.env` / API key → shows a clear server error, not a crash
- [ ] Valid input (e.g. "Operating Systems", "Data Structures") → generates
      full structured output with all 5 sections
- [ ] Copy button copies exact output text to clipboard
- [ ] Works on both desktop and mobile screen widths

## Possible Future Improvements (good talking points for interviews)
- Add a dropdown to pick difficulty level (beginner/intermediate/advanced)
- Export generated content as PDF
- Add response caching so repeated course titles don't call the API again
- Deploy on Render/Railway (free tier) since Flask apps aren't Streamlit-native
>>>>>>> 143cb12de662f232010e371b9c9096204309dded
