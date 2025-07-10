import fitz

def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file."""
    text=""
    pdf=fitz.open(stream=uploaded_file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

