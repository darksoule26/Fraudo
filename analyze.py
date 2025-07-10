import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def analyze_text_gemini(job_text):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")  # ⬅️ Using flash model

    prompt = f"""

You are a professional AI assistant that helps people verify job and internship offers to detect potential frauds or scams.

Analyze the following message or offer letter in depth. Provide a comprehensive report with the following structure:

1. Introduction
   - Briefly summarize what the message is about and what type of communication it is (e.g., internship offer, recruitment email, onboarding instructions).

2. Detailed Observations
   - List as many red flags or concerns as possible.
   - For each red flag, give a full explanation. Cover things like tone, language, urgency, contact method (WhatsApp), grammar, use of official-looking language, lack of company details, etc.
   - Be professional and precise. Avoid fear-mongering.

3. Missing Information
   - Clearly mention what important info is missing (e.g., compensation, official email, company address, proper signature, etc.)
   - Say why these are important.

4. Legitimacy Evaluation
   - Based on the message alone (not external search), assess whether it sounds like a legitimate offer or something that needs verification.

5. Web Verification
   - Search for the company name or key details online.
   - Provide a summary of the search results, including:
     - Top links found (if any).
     - Any trustworthiness indicators (e.g., official website, social media presence).
     - Mention if the company has a verified website or not.

6. Final Recommendation
   - One clear, human-friendly paragraph on what the user should do next.
   - Include advice on what to verify (e.g., company site, LinkedIn, email domain).
   - Assume the user is a student or fresher who might not know these things.

Here is the message to analyze:

\"\"\"
{job_text}
\"\"\"
"""

    response = model.generate_content(prompt)
    return response.text
