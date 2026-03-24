"""
pdf_processor.py
-----------------
Reads text from PDF files using pdfplumber.
Two simple functions — one for single PDF, one for multiple PDFs.
"""

import pdfplumber
import io


def read_pdf(uploaded_file) -> str:
    """Read one PDF and return all its text as a string."""
    try:
        pdf_bytes = uploaded_file.read()
        text = ""
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return f"Could not read PDF: {e}"


def read_multiple_pdfs(files: list) -> str:
    """Read multiple PDFs and combine all text together."""
    combined = ""
    for i, f in enumerate(files):
        combined += f"\n\n=== Paper {i+1}: {f.name} ===\n\n"
        combined += read_pdf(f)
    return combined
