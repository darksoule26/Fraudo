import re

def extract_company_name_from_report(report_text):
    """
    Extracts only the core company name from the Gemini-generated report text.
    Trims trailing phrases like job titles.
    """
    # Pattern 1: "company called Proxenix"
    match = re.search(r'company (?:named|called)?\s*([A-Z][A-Za-z0-9&.\- ]{2,})', report_text)
    if match:
        raw_name = match.group(1).strip()
        clean_name = re.split(r'\s+(for|offering|doing|working)', raw_name)[0]
        return clean_name.strip()

    # Pattern 2: fallback "from [Company]"
    match = re.search(r'from\s+(?:the\s+company\s+)?([A-Z][A-Za-z0-9&.\- ]+)', report_text)
    if match:
        raw_name = match.group(1).strip()
        clean_name = re.split(r'\s+(for|offering|doing|working)', raw_name)[0]
        return clean_name.strip()

    return ""
