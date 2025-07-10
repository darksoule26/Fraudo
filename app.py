import streamlit as st
from pdf_utils import extract_text_from_pdf
from analyze import analyze_text_gemini
from utils import extract_company_name_from_report
from web_check import (
    search_company_info,
    domain_match_check,
    check_domain_age,
    extract_contact_info,
    match_contact_info_on_web
)
from utils import extract_company_name_from_report  # 🆕 Smart company name extractor

st.set_page_config(page_title="Fraudo – AI Job Scam Detector", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ Fraudo")
st.write("Protect Yourself from Job Scams with AI")

# --- Input Section ---
option = st.radio("Choose Input Type:", ["Paste Job Message", "Upload Offer Letter (PDF)"])
job_text = ""

if option == "Paste Job Message":
    job_text = st.text_area("Paste the job offer/message here:")
else:
    pdf_file = st.file_uploader("Upload a job offer letter (PDF)", type=["pdf"])
    if pdf_file is not None:
        job_text = extract_text_from_pdf(pdf_file)
        st.success("✅ PDF text extracted successfully!")
        with st.expander("📄 Extracted Text Preview"):
            st.write(job_text)

email = st.text_input("Enter your email to receive the full report (optional)")

# --- Analyze Button ---
if st.button("Analyze Offer"):
    if job_text.strip():
        with st.spinner("Analyzing with Gemini AI..."):
            report_text = analyze_text_gemini(job_text)

        st.subheader("📋 AI Analysis Report")
        st.markdown(report_text)

        # 🔍 Extract Company Name
        company = extract_company_name_from_report(report_text)

        st.subheader("🌐 Web Verification")
        if company:
            st.markdown(f"**Detected Company Name:** `{company}`")

            web_data = search_company_info(company)
            if web_data["found"]:
                st.markdown("**🔗 Top Results:**")
                for link in web_data["top_links"]:
                    st.write(f"🔹 {link}")
                st.markdown("**📊 Trust Summary:**")
                st.info(web_data["trust_summary"])
            else:
                st.warning("No official company website found.")
        else:
            st.warning("❗ Could not detect company name from the message.")
            web_data = {"top_links": []}  # prevent crash in next steps

        # 🔐 Domain Match Check
        st.subheader("🔐 Email Domain Match")
        domain_match, domain_msg = domain_match_check(web_data["top_links"], job_text)
        if "match" in domain_msg.lower():
            st.success(domain_msg)
        else:
            st.warning(domain_msg)

        # 📅 Domain Age Check
        st.subheader("📅 Domain Age Check")
        domain_age_ok, domain_age_msg = check_domain_age(web_data["top_links"])
        if "trustworthy" in domain_age_msg.lower():
            st.success(domain_age_msg)
        else:
            st.warning(domain_age_msg)

        # ☎️ Contact Info Match
        st.subheader("☎️ Contact Info Match")
        contact_info = extract_contact_info(job_text)
        contact_result = match_contact_info_on_web(contact_info, web_data["top_links"])
        if contact_result["matched"]:
            st.success("✅ Contact info found on company website.")
            if contact_result["found_emails"]:
                st.markdown("**Matched Emails:**")
                for e in contact_result["found_emails"]:
                    st.write(f"📧 {e}")
            if contact_result["found_phones"]:
                st.markdown("**Matched Phone Numbers:**")
                for p in contact_result["found_phones"]:
                    st.write(f"📞 {p}")
        else:
            st.warning("⚠️ Contact info from the job offer was NOT found on the official site.")

    else:
        st.warning("⚠️ Please paste or upload a job message first.")

