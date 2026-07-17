"""
EduGenie: AI-Powered Educational Content Creator
--------------------------------------------------
A simple Flask backend that takes a course title from the user,
sends a prompt to OpenAI's API, and returns structured educational
content: objective, syllabus, 3 measurable learning outcomes
(aligned to Bloom's Taxonomy), assessment methods, and readings.

Author: Toshani Tiwari
"""

import os
import re
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Load OPENAI_API_KEY from a local .env file (never hardcode keys in code)
load_dotenv()

app = Flask(__name__)

# ---------------------------------------------------------------------
# OpenAI client setup
# ---------------------------------------------------------------------
API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1") if API_KEY else None


def build_prompt(course_title: str) -> str:
    """
    Builds a single, well-structured prompt so the model returns
    predictable, easy-to-parse sections. Asking for Bloom's Taxonomy
    levels explicitly keeps the outcomes measurable and academically sound.
    """
    return f"""
You are an experienced curriculum designer. Create educational content for
a course titled: "{course_title}"

Return the content in EXACTLY this format (keep the headers as shown):

**Objective of the Course:**
<2-3 sentence course objective>

**Sample Syllabus:**
1. <topic 1>
2. <topic 2>
... (8-10 topics total)

**Three Measurable Learning Outcomes:**
1. <Bloom's level e.g. Remember/Understand/Apply/Analyze/Evaluate/Create>: <outcome statement using an action verb>
2. <Bloom's level>: <outcome statement>
3. <Bloom's level>: <outcome statement>

**Assessment Methods:**
1. <method>: <one line on what it evaluates>
2. <method>: <one line on what it evaluates>
3. <method>: <one line on what it evaluates>

**Recommended Readings:**
1. <book/resource title and author>
2. <book/resource title and author>
3. <book/resource title and author>

Keep the tone academic, concise, and clear. Do not add extra commentary
before or after the sections.
"""


def validate_course_title(title: str) -> str | None:
    """
    Basic input validation. Returns an error message string if invalid,
    otherwise returns None.
    """
    if not title or not title.strip():
        return "Course title cannot be empty."
    if len(title) > 120:
        return "Course title is too long (max 120 characters)."
    # Allow letters, numbers, spaces and common punctuation only
    if not re.match(r"^[a-zA-Z0-9\s\-\&\,\.\:\(\)]+$", title):
        return "Course title contains unsupported characters."
    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """
    Receives {course_title: "..."} as JSON, calls OpenAI, and returns
    {content: "..."} or {error: "..."} with an appropriate status code.

    NOTE ON PRIVACY: the course title is sent to OpenAI only for the
    duration of this request. It is not written to any file, database,
    or log by this application.
    """
    data = request.get_json(silent=True) or {}
    course_title = data.get("course_title", "").strip()

    error = validate_course_title(course_title)
    if error:
        return jsonify({"error": error}), 400

    if client is None:
        return jsonify({
            "error": "Server is missing OPENAI_API_KEY. "
                     "Add it to a .env file and restart the server."
        }), 500

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",       # small + cheap, good enough for this task
            messages=[
                {"role": "system", "content": "You are a helpful curriculum design assistant."},
                {"role": "user", "content": build_prompt(course_title)}
            ],
            temperature=0.7,
            max_tokens=700,
        )
        content = response.choices[0].message.content
        return jsonify({"content": content}), 200

    except Exception as e:
        # Catch-all so the frontend always gets a readable error
        # instead of a raw stack trace or a hung "Generating..." state.
        return jsonify({"error": f"Failed to generate content: {str(e)}"}), 502


if __name__ == "__main__":
    # host="0.0.0.0" is needed on Replit (and most cloud environments) so
    # their proxy can reach the app. Locally on your own laptop, this
    # still works fine at http://127.0.0.1:8080
    app.run(host="0.0.0.0", port=8080, debug=True)