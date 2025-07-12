Here’s your **updated `README.md`** for the **🕵️‍♂️ Fraudo** project – fully documenting **how it works**, what **technologies** are used, how to **run it**, and the core **features** explained clearly.

---

````markdown
# 🕵️‍♂️ Fraudo – AI-Powered Job Scam Detector

**Fraudo** is an AI-based tool designed to help students, freshers, and job seekers **verify job or internship offers** and protect themselves from potential scams. It leverages **Gemini AI**, **DuckDuckGo search**, and **WHOIS lookup** to analyze offer letters (text or PDF) and perform deep web verification checks.

---

## 🚀 Features

### 🔍 Intelligent AI Analysis (Gemini)
- Detect red flags in job offers (vague terms, missing info, urgency, informal tone).
- Generates a detailed 6-point analysis report:
  - Introduction  
  - Red Flags & Observations  
  - Missing Information  
  - Legitimacy Evaluation  
  - Web Verification  
  - Final Recommendation  

### 📄 Input Options
- ✅ Paste job offer message
- ✅ Upload PDF offer letters

### 🌐 Web Verification Module
1. **Company Detection & Search**
   - Extracts company name from AI analysis.
   - Searches for the official company site via DuckDuckGo.

2. **Email Domain Match**
   - Checks if the domain in the offer email (e.g. `@xyz.com`) matches any of the verified company URLs.

3. **Domain Age Check**
   - Performs WHOIS lookup to find domain creation date.
   - Flags domains younger than 180 days as suspicious.
   - Displays registrar, country, and expiration.

4. **Contact Info Match**
   - Extracts phone numbers and emails from the offer letter.
   - Crawls the official company website to check if those contact details exist on the real site.

---

## ⚙️ Tech Stack

| Tool / Library         | Purpose                                      |
|------------------------|----------------------------------------------|
| **Streamlit**          | UI framework for fast web app development    |
| **Gemini API (Google)**| LLM-based analysis of job/internship offers |
| **DuckDuckGo Search**  | Fetches top links for the company            |
| **WHOIS Python**       | Gets domain age and registrar info           |
| **BeautifulSoup**      | Extracts contact data from webpages          |
| **PyPDF2**             | Extracts text from uploaded PDF offer letters|
| **dotenv**             | Loads Gemini API key securely from `.env`    |

---

## 🛠️ Setup Instructions

### 🔐 Prerequisites
- Python 3.9+
- Gemini API Key (Get it from https://makersuite.google.com/app/apikey)

### 📦 Installation

```bash
git clone https://github.com/yourusername/fraudo.git
cd fraudo

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
````

### 🔑 Configure Gemini API Key

Create a `.env` file in the project root:

```
GEMINI_API_KEY=your_actual_gemini_api_key
```

---

## 🖥️ Running the App

```bash
streamlit run streamlit_app.py
```

Then open: [http://localhost:8501](http://localhost:8501)

---

## 🧠 How It Works

1. **Text Extraction**

   * If a PDF is uploaded, text is extracted using PyPDF2.
   * Else, direct input is used.

2. **AI Analysis**

   * Gemini API generates an in-depth, human-like audit of the offer.

3. **Company Detection**

   * Smart regex extracts the most likely company name from the Gemini report.

4. **Web Verification Module**

   * `DuckDuckGo` searches for official links.
   * `WHOIS` checks domain age and trust score.
   * `BeautifulSoup` scrapes company site and checks contact info.
   * Results are rendered with appropriate ✅ or ⚠️ indicators.


## 🧩 Folder Structure

```
fraudo/
│
├── analyze.py               # Gemini prompt logic
├── web_check.py             # Domain, email, contact verifications
├── pdf_utils.py             # Extract text from PDFs
├── utils.py                 # Company name extractor, etc.
├── streamlit_app.py         # Main Streamlit UI
├── requirements.txt
├── .env                     # (not committed) API Key
└── README.md
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 🛡️ Disclaimer

This tool provides **assistance**, not legal or professional employment verification. Always cross-check with official resources and use your judgment before proceeding with job offers.

---



## ⭐ If you find this project useful, please give it a ⭐ on GitHub!

```

