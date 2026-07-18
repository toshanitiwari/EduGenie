# EduGenie: AI-Powered Educational Content Creator

A web tool that generates a full course outline — objective, syllabus,
3 measurable learning outcomes (mapped to Bloom's Taxonomy), assessment
methods, and recommended readings — from just a course title, using
OpenAI's API.

Built for: Generative AI course capstone project (Internshala Trainings)

---

## Tech Stack
- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript (vanilla, no framework)
- **AI:** OpenAI Chat Completions API (`gpt-4o-mini`)

## Project Structure
```
edugenie/
├── app.py                # Flask server + OpenAI logic
├── requirements.txt      # Python dependencies
├── .env.example          # Template for your API key
├── templates/
│   └── index.html        # Main page
└── static/
    ├── style.css          # UI styling
    └── script.js          # Frontend logic (fetch call, error handling, copy button)
```

## How It Works (for your viva / interview)
1. User types a course title in the browser and clicks **Generate Content**.
2. `script.js` sends a `POST` request to `/generate` with the title as JSON.
3. `app.py` validates the input (not empty, not too long, safe characters only),
   then builds a structured prompt and sends it to OpenAI's API.
4. The prompt explicitly asks for outcomes labeled by **Bloom's Taxonomy level**
   (Remember, Understand, Apply, Analyze, Evaluate, Create) so the output is
   academically measurable, not just generic text.
5. The AI's response is sent back as JSON and rendered in the **Output** box.
6. Errors (empty input, missing API key, OpenAI request failure, network
   issues) are all caught and shown as a friendly message instead of crashing.

## Setup Instructions

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your OpenAI API key
Copy `.env.example` to `.env` and paste your real key:
```bash
cp .env.example .env
```
Then edit `.env`:
```
OPENAI_API_KEY=sk-your-real-key-here
```
Get a key from https://platform.openai.com/api-keys (small free/paid credits needed).

### 3. Run the app
```bash
python app.py
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
