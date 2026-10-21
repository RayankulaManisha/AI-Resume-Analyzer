
import pdfplumber
from pathlib import Path

# Find the project folder
project_folder = Path(__file__).parent

# Locate your resume PDF
pdf_path = "sample_resume.pdf"

# Read the PDF
with pdfplumber.open(pdf_path) as pdf:
    resume_text = ""

    for page in pdf.pages:
        page_text = page.extract_text() or ""
        resume_text += page_text + "\n"

# Display the extracted text
print("===== RESUME TEXT =====")
print(resume_text)
