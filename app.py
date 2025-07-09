import streamlit as st
from pdf_utils import extract_text_from_pdf
from analyze import analyze_text
from web_check import search_company_info

st.set_page_config(page_title="Fraudo – AI Job Scam Detector", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ Fraudo")
st.write("Protect Yourself from Job Scams with AI")

# --- Input Selection ---
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

# --- Optional Email ---
email = st.text_input("Enter your email to receive the full report (optional)")

# --- Analyze Button ---
if st.button("Analyze Offer"):
    if job_text.strip():
        with st.spinner("Analyzing with AI..."):
            report = analyze_text(job_text)

        # Extract company name and search web
        company = report.get("company_name", "")
        if company and company.lower() != "none":
            web_data = search_company_info(company)
            report["web_check"] = web_data
        else:
            report["web_check"] = {
                "found": False,
                "top_links": [],
                "trust_summary": "Company name not found in text."
            }

        # --- Display AI Report ---
        st.subheader("📋 AI Analysis Report")

        st.markdown(f"**Classification:** `{report['classification']}`")
        st.markdown(f"**Risk Score:** `{report['risk_score']}/100`")
        st.progress(report['risk_score'] / 100)

        st.markdown("**🚩 Red Flags:**")
        for flag in report["red_flags"]:
            st.write(f"• {flag}")

        st.markdown("**💡 Suggestion:**")
        st.info(report["suggestion"])

        # --- Display Web Info ---
        st.subheader("🌐 Web Verification")
        st.markdown(f"**Detected Company Name:** `{company}`")
        if report["web_check"]["found"]:
            st.markdown("**🔗 Top Results:**")
            for link in report["web_check"]["top_links"]:
                st.write(f"🔹 {link}")
        else:
            st.warning("No company website found.")

        st.markdown("**📊 Trust Summary:**")
        st.info(report["web_check"]["trust_summary"])
        
    else:
        st.warning("⚠️ Please paste or upload a job message first.")
