import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re

# Load .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_json(text):
    """Extract JSON object from AI response using regex"""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return None
    return None

def analyze_text(job_text):
    prompt = f"""
You are an AI that analyzes job messages to detect potential job scams.

Return a JSON object ONLY in this format:

{{
  "classification": "Legit | Suspicious | Scam",
  "risk_score": int (0 to 100),
  "company_name": "Name of the company or None",
  "red_flags": [list of problems],
  "suggestion": "Advice to the user"
}}

DO NOT include any explanation or extra text.

Job Message:
\"\"\"
{job_text}
\"\"\"
"""

    try:
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")
        response = model.generate_content(prompt)

        data = extract_json(response.text)

        if data is None:
            raise ValueError("Could not extract JSON from AI response.")

        return data

    except Exception as e:
        return {
            "classification": "Unknown",
            "risk_score": 50,
            "company_name": "None",
            "red_flags": [f"Error: {str(e)}"],
            "suggestion": "Try again or check your input."
        }
