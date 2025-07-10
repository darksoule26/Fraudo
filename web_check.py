from duckduckgo_search import DDGS
from urllib.parse import urlparse
import re
import whois
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# --- DOMAIN UTILS ---
def get_domain_from_url(url):
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    return domain

# --- SMART SEARCH ---
def search_company_info(company_name):
    try:
        query = f"{company_name} official site"
        raw_results = []

        with DDGS() as ddgs:
            for r in ddgs.text(query, region='in-en', safesearch='Moderate', max_results=10):
                link = r.get("href")
                if link:
                    raw_results.append(link)

        # Filter only those that likely belong to the company
        filtered = [link for link in raw_results if company_name.lower() in get_domain_from_url(link).lower()]

        return {
            "found": bool(filtered),
            "top_links": filtered,
            "trust_summary": "✅ Company website and info found online." if filtered else f"❌ No reliable official website found for '{company_name}'."
        }

    except Exception as e:
        return {
            "found": False,
            "top_links": [],
            "trust_summary": f"❌ Search error: {str(e)}"
        }

# --- EMAIL DOMAIN CHECK ---
def domain_match_check(company_links, offer_text):
    offer_domains = re.findall(r'@([A-Za-z0-9.-]+\.[a-z]+)', offer_text)
    if not offer_domains:
        return False, "❌ No email domain found in offer letter."

    detected_offer_domain = offer_domains[0]
    for link in company_links:
        site_domain = get_domain_from_url(link)
        if detected_offer_domain in site_domain:
            return True, f"✅ Email domain matches company website: `{detected_offer_domain}`"

    return False, f"⚠️ Email domain `{detected_offer_domain}` does NOT match any official site."

# --- DOMAIN AGE CHECK ---
def check_domain_age(company_links):
    if not company_links:
        return False, "⚠️ No links found to verify domain age."

    domain = get_domain_from_url(company_links[0])
    try:
        info = whois.whois(domain)
        creation_date = info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if not creation_date:
            raise ValueError("No creation date available.")

        age_days = (datetime.now() - creation_date).days
        if age_days < 180:
            return False, f"⚠️ Domain `{domain}` is too new ({age_days} days old) – be cautious."
        else:
            return True, f"✅ Domain `{domain}` is {age_days} days old – trustworthy."

    except Exception as e:
        return False, f"❌ WHOIS check failed: {str(e)}"

# --- EXTRACT CONTACT INFO FROM OFFER LETTER ---
def extract_contact_info(text):
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", text)
    phones = re.findall(r"\+?\d[\d\s-]{8,}\d", text)
    return {
        "emails": list(set(emails)),
        "phones": list(set(phones))
    }

# --- VERIFY CONTACT INFO ON WEBSITE ---
def match_contact_info_on_web(contact_info, company_links):
    found_emails = []
    found_phones = []

    headers = {"User-Agent": "Mozilla/5.0"}
    
    for url in company_links[:2]:  # Limit for speed
        try:
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            page_text = soup.get_text()

            for email in contact_info["emails"]:
                if email in page_text:
                    found_emails.append(email)

            for phone in contact_info["phones"]:
                if phone in page_text:
                    found_phones.append(phone)

        except Exception:
            continue

    matched = bool(found_emails or found_phones)
    return {
        "matched": matched,
        "found_emails": found_emails,
        "found_phones": found_phones
    }
