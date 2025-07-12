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
import time

# Page configuration
st.set_page_config(
    page_title="Fraudo – AI Job Scam Detector", 
    page_icon="🕵️‍♂️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Advanced CSS with animations and dark/light mode support
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Dark/Light mode variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        --warning-gradient: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        --danger-gradient: linear-gradient(135deg, #ff7675 0%, #fd79a8 100%);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
        --text-primary: #2c3e50;
        --text-secondary: #7f8c8d;
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fa;
        --shadow: rgba(0, 0, 0, 0.1);
    }
    
    /* Dark mode */
    @media (prefers-color-scheme: dark) {
        :root {
            --glass-bg: rgba(0, 0, 0, 0.2);
            --glass-border: rgba(255, 255, 255, 0.1);
            --text-primary: #ecf0f1;
            --text-secondary: #bdc3c7;
            --bg-primary: #2c3e50;
            --bg-secondary: #34495e;
            --shadow: rgba(0, 0, 0, 0.3);
        }
    }
    
    /* Force dark mode styles for Streamlit dark theme */
    .stApp[data-theme="dark"] {
        --glass-bg: rgba(0, 0, 0, 0.2);
        --glass-border: rgba(255, 255, 255, 0.1);
        --text-primary: #ecf0f1;
        --text-secondary: #bdc3c7;
        --bg-primary: #2c3e50;
        --bg-secondary: #34495e;
        --shadow: rgba(0, 0, 0, 0.3);
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.3) 0%, transparent 50%);
        z-index: -1;
        animation: backgroundShift 20s ease-in-out infinite;
    }
    
    @keyframes backgroundShift {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Floating particles */
    .particle {
        position: absolute;
        background: rgba(102, 126, 234, 0.6);
        border-radius: 50%;
        pointer-events: none;
        animation: float 6s ease-in-out infinite;
    }
    
    .particle:nth-child(1) { width: 4px; height: 4px; left: 10%; animation-delay: 0s; }
    .particle:nth-child(2) { width: 6px; height: 6px; left: 20%; animation-delay: 1s; }
    .particle:nth-child(3) { width: 3px; height: 3px; left: 30%; animation-delay: 2s; }
    .particle:nth-child(4) { width: 5px; height: 5px; left: 40%; animation-delay: 3s; }
    .particle:nth-child(5) { width: 4px; height: 4px; left: 50%; animation-delay: 4s; }
    .particle:nth-child(6) { width: 7px; height: 7px; left: 60%; animation-delay: 5s; }
    .particle:nth-child(7) { width: 3px; height: 3px; left: 70%; animation-delay: 6s; }
    .particle:nth-child(8) { width: 5px; height: 5px; left: 80%; animation-delay: 7s; }
    .particle:nth-child(9) { width: 4px; height: 4px; left: 90%; animation-delay: 8s; }
    
    @keyframes float {
        0%, 100% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
    }
    
    /* Main header with glassmorphism */
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        border-radius: 25px;
        margin-bottom: 3rem;
        color: var(--text-primary);
        box-shadow: 0 20px 40px var(--shadow);
        position: relative;
        overflow: hidden;
        animation: slideInDown 1s ease-out;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: var(--primary-gradient);
        opacity: 0.1;
        animation: rotate 20s linear infinite;
        z-index: -1;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes slideInDown {
        from { transform: translateY(-100px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .main-title {
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 1rem;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: pulse 2s ease-in-out infinite;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .main-subtitle {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        color: var(--text-primary);
        animation: fadeInUp 1s ease-out 0.5s both;
    }
    
    .main-description {
        font-size: 1.1rem;
        color: var(--text-secondary);
        animation: fadeInUp 1s ease-out 1s both;
    }
    
    @keyframes fadeInUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Animated stats */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
        animation: fadeInUp 1s ease-out 1.5s both;
    }
    
    .stat-item {
        text-align: center;
        padding: 2rem 1rem;
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        box-shadow: 0 10px 30px var(--shadow);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .stat-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stat-item:hover::before {
        left: 100%;
    }
    
    .stat-item:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 20px 50px var(--shadow);
    }
    
    .stat-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-10px); }
        60% { transform: translateY(-5px); }
    }
    
    /* Input section with advanced styling */
    .input-section {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 0 15px 35px var(--shadow);
        margin: 3rem 0;
        position: relative;
        animation: slideInUp 1s ease-out 2s both;
    }
    
    @keyframes slideInUp {
        from { transform: translateY(50px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    .feature-card {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 1px solid var(--glass-border);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px var(--shadow);
        margin: 1rem 0;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--primary-gradient);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover::after {
        transform: scaleX(1);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px var(--shadow);
    }
    
    /* Analysis section with dynamic effects */
    .analysis-section {
        background: var(--secondary-gradient);
        padding: 3rem;
        border-radius: 25px;
        color: white;
        margin: 3rem 0;
        position: relative;
        overflow: hidden;
        animation: slideInLeft 1s ease-out;
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-100px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .analysis-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: spin 15s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Verification cards with hover effects */
    .verification-card {
        background: var(--glass-bg);
        backdrop-filter: blur(15px);
        border: 1px solid var(--glass-border);
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        transition: all 0.3s ease;
        position: relative;
        color: var(--text-primary);
        box-shadow: 0 10px 30px var(--shadow);
    }
    
    .verification-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px var(--shadow);
    }
    
    /* Result cards with animations */
    .success-card {
        background: var(--success-gradient);
        padding: 2rem;
        border-radius: 20px;
        color: #2d5a27;
        font-weight: 600;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(132, 250, 176, 0.3);
        animation: successPulse 2s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes successPulse {
        0%, 100% { box-shadow: 0 10px 30px rgba(132, 250, 176, 0.3); }
        50% { box-shadow: 0 15px 40px rgba(132, 250, 176, 0.5); }
    }
    
    .warning-card {
        background: var(--warning-gradient);
        padding: 2rem;
        border-radius: 20px;
        color: #8b4513;
        font-weight: 600;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(255, 234, 167, 0.3);
        animation: warningShake 3s ease-in-out infinite;
    }
    
    @keyframes warningShake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-2px); }
        75% { transform: translateX(2px); }
    }
    
    .danger-card {
        background: var(--danger-gradient);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        font-weight: 600;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(255, 118, 117, 0.4);
        animation: dangerBlink 2s ease-in-out infinite;
    }
    
    @keyframes dangerBlink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Section headers with underline animation */
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 3rem 0 2rem 0;
        padding-bottom: 1rem;
        position: relative;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 0;
        height: 4px;
        background: var(--primary-gradient);
        border-radius: 2px;
        animation: expandWidth 2s ease-out 0.5s both;
    }
    
    @keyframes expandWidth {
        to { width: 100px; }
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        padding: 1rem 3rem !important;
        border-radius: 50px !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: var(--primary-gradient) !important;
        border-radius: 10px !important;
        animation: progressGlow 2s ease-in-out infinite !important;
    }
    
    @keyframes progressGlow {
        0%, 100% { box-shadow: 0 0 10px rgba(102, 126, 234, 0.5); }
        50% { box-shadow: 0 0 20px rgba(102, 126, 234, 0.8); }
    }
    
    /* Trust score animation */
    .trust-score {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        margin: 2rem 0;
        animation: countUp 2s ease-out;
    }
    
    @keyframes countUp {
        from { transform: scale(0); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    /* Footer styling */
    .footer-section {
        background: var(--glass-bg);
        backdrop-filter: blur(20px);
        border: 1px solid var(--glass-border);
        padding: 3rem;
        border-radius: 25px;
        margin-top: 4rem;
        text-align: center;
        color: var(--text-primary);
        box-shadow: 0 15px 35px var(--shadow);
        animation: fadeIn 1s ease-out 3s both;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title { font-size: 2.5rem; }
        .stats-container { grid-template-columns: 1fr; }
        .input-section { padding: 2rem; }
        .section-header { font-size: 1.5rem; }
    }
    
    /* Loading spinner */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(102, 126, 234, 0.3);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
        margin-right: 10px;
    }
    
    /* Glowing text effect */
    .glow-text {
        animation: textGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes textGlow {
        from { text-shadow: 0 0 10px rgba(102, 126, 234, 0.5); }
        to { text-shadow: 0 0 20px rgba(102, 126, 234, 0.8), 0 0 30px rgba(102, 126, 234, 0.6); }
    }
</style>
""", unsafe_allow_html=True)

# Floating particles
st.markdown("""
<div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: -1;">
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
    <div class="particle"></div>
</div>
""", unsafe_allow_html=True)

# Main header with enhanced animations
st.markdown("""
<div class="main-header">
    <div class="main-title glow-text">🕵️‍♂️ FRAUDO</div>
    <div class="main-subtitle">AI-Powered Job Scam Detector</div>
    <div class="main-description">Protect yourself from fraudulent job offers with cutting-edge AI analysis and real-time verification</div>
</div>
""", unsafe_allow_html=True)

# Enhanced statistics section
st.markdown("""
<div class="stats-container">
    <div class="stat-item">
        <span class="stat-icon">🛡️</span>
        <h3 style="margin: 0; color: var(--text-primary);">AI Protection</h3>
        <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">Advanced threat detection</p>
    </div>
    <div class="stat-item">
        <span class="stat-icon">🔍</span>
        <h3 style="margin: 0; color: var(--text-primary);">Deep Analysis</h3>
        <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">Multi-layer verification</p>
    </div>
    <div class="stat-item">
        <span class="stat-icon">🌐</span>
        <h3 style="margin: 0; color: var(--text-primary);">Web Verification</h3>
        <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">Real-time web checks</p>
    </div>
    <div class="stat-item">
        <span class="stat-icon">⚡</span>
        <h3 style="margin: 0; color: var(--text-primary);">Instant Results</h3>
        <p style="margin: 0.5rem 0 0 0; color: var(--text-secondary);">Lightning-fast analysis</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced input section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">📝 Submit Your Job Offer</h2>', unsafe_allow_html=True)

# Create two columns for input options
input_col1, input_col2 = st.columns([1, 1])

with input_col1:
    st.markdown("""
    <div class="feature-card">
        <h4 style="color: var(--text-primary); margin-top: 0; font-size: 1.3rem;">📋 Text Input</h4>
        <p style="color: var(--text-secondary); margin-bottom: 0;">Paste your job offer message directly for instant analysis</p>
    </div>
    """, unsafe_allow_html=True)

with input_col2:
    st.markdown("""
    <div class="feature-card">
        <h4 style="color: var(--text-primary); margin-top: 0; font-size: 1.3rem;">📄 PDF Upload</h4>
        <p style="color: var(--text-secondary); margin-bottom: 0;">Upload your offer letter document for comprehensive review</p>
    </div>
    """, unsafe_allow_html=True)

option = st.radio(
    "Choose your preferred input method:",
    ["📋 Paste Job Message", "📄 Upload Offer Letter (PDF)"],
    horizontal=True
)

job_text = ""

if option == "📋 Paste Job Message":
    job_text = st.text_area(
        "Paste the job offer/message here:",
        height=200,
        placeholder="Paste your job offer, email, WhatsApp message, or any suspicious job communication here...",
        help="Include all details like company name, contact information, job description, and any requirements mentioned"
    )
else:
    pdf_file = st.file_uploader(
        "Upload a job offer letter (PDF)", 
        type=["pdf"],
        help="Upload your PDF job offer letter for comprehensive analysis"
    )
    if pdf_file is not None:
        with st.spinner("🔄 Extracting text from PDF..."):
            job_text = extract_text_from_pdf(pdf_file)
        st.success("✅ PDF text extracted successfully!")
        with st.expander("📄 View Extracted Text"):
            st.text_area("Extracted content:", job_text, height=200, disabled=True)

st.markdown('</div>', unsafe_allow_html=True)

# Enhanced analyze button
if st.button("🚀 Analyze Job Offer", type="primary"):
    if job_text.strip():
        # Create dynamic progress tracking
        progress_container = st.container()
        with progress_container:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Enhanced analysis section with animation
            st.markdown("""
            <div class="analysis-section">
                <h2 style="margin-top: 0; font-size: 2.5rem;">🤖 AI Analysis in Progress</h2>
                <p style="font-size: 1.2rem; opacity: 0.9;">Our advanced AI is examining your job offer for potential red flags and suspicious patterns...</p>
                <div style="display: flex; align-items: center; justify-content: center; margin-top: 2rem;">
                    <div class="loading-spinner"></div>
                    <span style="font-size: 1.1rem;">Processing with Gemini AI...</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Step 1: AI Analysis with enhanced feedback
        status_text.markdown("🧠 **Analyzing with Gemini AI...** *Detecting patterns and red flags*")
        progress_bar.progress(20)
        time.sleep(0.5)  # Small delay for visual effect
        
        with st.spinner("Analyzing with AI..."):
            report_text = analyze_text_gemini(job_text)
        
        progress_bar.progress(40)
        
        # Display AI Analysis with enhanced styling
        st.markdown('<h2 class="section-header">📋 AI Analysis Report</h2>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="verification-card">
            <div style="font-size: 1.1rem; line-height: 1.6;">
                {report_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Step 2: Company Detection with animation
        status_text.markdown("🔍 **Detecting company information...** *Extracting business details*")
        progress_bar.progress(60)
        time.sleep(0.3)
        
        company = extract_company_name_from_report(report_text)
        
        # Enhanced Web Verification Section
        st.markdown('<h2 class="section-header">🌐 Web Verification Results</h2>', unsafe_allow_html=True)
        
        verification_col1, verification_col2 = st.columns([1, 1])
        
        with verification_col1:
            if company:
                st.markdown(f"""
                <div class="success-card">
                    <h4 style="margin-top: 0; font-size: 1.4rem;">🏢 Company Detected</h4>
                    <div class="trust-score" style="font-size: 2rem; margin: 1rem 0;">{company}</div>
                    <p style="margin-bottom: 0; opacity: 0.8;">Successfully identified from job offer</p>
                </div>
                """, unsafe_allow_html=True)
                
                status_text.markdown("🌐 **Searching company information...** *Verifying online presence*")
                progress_bar.progress(70)
                time.sleep(0.3)
                
                web_data = search_company_info(company)
                if web_data["found"]:
                    st.markdown("**🔗 Official Website Results:**")
                    for i, link in enumerate(web_data["top_links"][:3], 1):
                        st.markdown(f"🔹 **Result {i}:** {link}")
                    
                    st.markdown(f"""
                    <div class="verification-card">
                        <h4 style="color: var(--text-primary); margin-top: 0;">📊 Trust Assessment</h4>
                        <p style="color: var(--text-secondary); margin-bottom: 0; font-size: 1.1rem;">{web_data["trust_summary"]}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="warning-card">
                        <h4 style="margin-top: 0;">⚠️ No Official Website Found</h4>
                        <p style="margin-bottom: 0;">Could not locate an official company website - this could be a red flag</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="danger-card">
                    <h4 style="margin-top: 0;">❗ Company Detection Failed</h4>
                    <p style="margin-bottom: 0;">Could not identify company name from the message - major red flag</p>
                </div>
                """, unsafe_allow_html=True)
                web_data = {"top_links": []}
        
        with verification_col2:
            # Enhanced Domain Match Check
            status_text.markdown("🔐 **Verifying email domains...** *Checking sender authenticity*")
            progress_bar.progress(80)
            time.sleep(0.3)
            
            domain_match, domain_msg = domain_match_check(web_data["top_links"], job_text)
            if "match" in domain_msg.lower():
                st.markdown(f"""
                <div class="success-card">
                    <h4 style="margin-top: 0;">🔐 Domain Verification</h4>
                    <p style="margin-bottom: 0;">{domain_msg}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="warning-card">
                    <h4 style="margin-top: 0;">🔐 Domain Verification</h4>
                    <p style="margin-bottom: 0;">{domain_msg}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Enhanced additional verification checks
        st.markdown('<h3 class="section-header">🔍 Additional Security Checks</h3>', unsafe_allow_html=True)
        
        check_col1, check_col2 = st.columns([1, 1])
        
        with check_col1:
            # Enhanced Domain Age Check
            status_text.markdown("📅 **Checking domain age...** *Verifying website credibility*")
            progress_bar.progress(90)
            time.sleep(0.3)
            
            domain_age_ok, domain_age_msg = check_domain_age(web_data["top_links"])
            if "trustworthy" in domain_age_msg.lower():
                st.markdown(f"""
                <div class="success-card">
                    <h4 style="margin-top: 0;">📅 Domain Age Check</h4>
                    <p style="margin-bottom: 0;">{domain_age_msg}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="warning-card">
                    <h4 style="margin-top: 0;">📅 Domain Age Check</h4>
                    <p style="margin-bottom: 0;">{domain_age_msg}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with check_col2:
            # Enhanced Contact Info Match
            status_text.markdown("☎️ **Verifying contact information...** *Cross-checking details*")
            progress_bar.progress(95)
            time.sleep(0.3)
            
            contact_info = extract_contact_info(job_text)
            contact_result = match_contact_info_on_web(contact_info, web_data["top_links"])
            
            if contact_result["matched"]:
                st.markdown("""
                <div class="success-card">
                    <h4 style="margin-top: 0;">☎️ Contact Verification</h4>
                    <p style="margin-bottom: 0;">✅ Contact info verified on official website</p>
                </div>
                """, unsafe_allow_html=True)
                
                if contact_result["found_emails"]:
                    st.markdown("**📧 Verified Emails:**")
                    for e in contact_result["found_emails"]:
                        st.markdown(f"✅ {e}")
                
                if contact_result["found_phones"]:
                    st.markdown("**📞 Verified Phone Numbers:**")
                    for p in contact_result["found_phones"]:
                        st.markdown(f"✅ {p}")
            else:
                st.markdown("""
                <div class="danger-card">
                    <h4 style="margin-top: 0;">☎️ Contact Verification</h4>
                    <p style="margin-bottom: 0;">⚠️ Contact info NOT found on official website</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Complete analysis with enhanced feedback
        progress_bar.progress(100)
        status_text.markdown("✅ **Analysis Complete!** *Generating final report...*")
        time.sleep(0.5)
        
        # Enhanced Final recommendation with dynamic scoring
        st.markdown('<h2 class="section-header">🎯 Final Security Assessment</h2>', unsafe_allow_html=True)
        
        # Enhanced scoring logic
        score = 0
        risk_factors = []
        
        if company: 
            score += 25
        else:
            risk_factors.append("No company name detected")
            
        if web_data.get("found", False): 
            score += 25
        else:
            risk_factors.append("No official website found")
            
        if "match" in domain_msg.lower(): 
            score += 25
        else:
            risk_factors.append("Email domain mismatch")
            
        if contact_result.get("matched", False): 
            score += 25
        else:
            risk_factors.append("Contact info not verified")
        
        # Dynamic trust score display
        if score >= 75:
            st.markdown(f"""
            <div class="success-card" style="text-align: center; padding: 3rem; margin: 2rem 0;">
                <h3 style="margin-top: 0; font-size: 2rem;">🟢 LIKELY LEGITIMATE</h3>
                <div class="trust-score glow-text">{score}/100</div>
                <p style="font-size: 1.2rem; margin-bottom: 0;">This job offer appears to be from a legitimate source based on our comprehensive analysis.</p>
            </div>
            """, unsafe_allow_html=True)
        elif score >= 50:
            st.markdown(f"""
            <div class="warning-card" style="text-align: center; padding: 3rem; margin: 2rem 0;">
                <h3 style="margin-top: 0; font-size: 2rem;">🟡 PROCEED WITH CAUTION</h3>
                <div class="trust-score">{score}/100</div>
                <p style="font-size: 1.2rem; margin-bottom: 1rem;">Some red flags detected. Verify independently before proceeding.</p>
                <div style="text-align: left; background: rgba(0,0,0,0.1); padding: 1rem; border-radius: 10px;">
                    <strong>Risk Factors:</strong><br>
                    {'<br>'.join([f"• {factor}" for factor in risk_factors])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="danger-card" style="text-align: center; padding: 3rem; margin: 2rem 0;">
                <h3 style="margin-top: 0; font-size: 2rem;">🔴 HIGH RISK - LIKELY SCAM</h3>
                <div class="trust-score">{score}/100</div>
                <p style="font-size: 1.2rem; margin-bottom: 1rem;">Multiple red flags detected. Exercise extreme caution!</p>
                <div style="text-align: left; background: rgba(0,0,0,0.2); padding: 1rem; border-radius: 10px;">
                    <strong>Major Risk Factors:</strong><br>
                    {'<br>'.join([f"• {factor}" for factor in risk_factors])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
    else:
        st.markdown("""
        <div class="warning-card" style="text-align: center; padding: 2rem;">
            <h4 style="margin-top: 0;">⚠️ Input Required</h4>
            <p style="margin-bottom: 0;">Please paste a job message or upload a PDF file first to begin the analysis.</p>
        </div>
        """, unsafe_allow_html=True)

# Enhanced footer with animations
st.markdown("---")
st.markdown("""
<div class="footer-section">
    <h4 style="color: var(--text-primary); font-size: 1.8rem; margin-bottom: 1.5rem;">🛡️ Stay Safe from Job Scams</h4>
    <p style="font-size: 1.2rem; margin-bottom: 2rem; color: var(--text-secondary);">
        Always verify job offers independently. If something seems too good to be true, it probably is!
    </p>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-top: 2rem;">
        <div style="text-align: left;">
            <h5 style="color: var(--text-primary); margin-bottom: 1rem;">🚨 Red Flags to Watch:</h5>
            <ul style="color: var(--text-secondary); text-align: left;">
                <li>Requests for upfront payments</li>
                <li>Unrealistic salary offers</li>
                <li>Poor grammar and spelling</li>
                <li>Urgent response deadlines</li>
            </ul>
        </div>
        <div style="text-align: left;">
            <h5 style="color: var(--text-primary); margin-bottom: 1rem;">✅ Safety Tips:</h5>
            <ul style="color: var(--text-secondary); text-align: left;">
                <li>Research the company thoroughly</li>
                <li>Verify contact information</li>
                <li>Trust your instincts</li>
                <li>Never share personal documents</li>
            </ul>
        </div>
    </div>
    <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--glass-border);">
        <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">
            <strong>Fraudo</strong> - Powered by AI • Protecting job seekers worldwide
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
