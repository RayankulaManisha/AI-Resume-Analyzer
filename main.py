
from pathlib import Path
import re

import pdfplumber
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.write(
    "Upload your resume, paste a job description, "
    "and check how well your skills match the job."
)


# -----------------------------
# Extract text from PDF
# -----------------------------
def extract_resume_text(uploaded_file):
    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += (page.extract_text() or "") + "\n"

    return text


# -----------------------------
# Clean and identify words
# -----------------------------
def get_words(text):
    return set(re.findall(r"[a-zA-Z][a-zA-Z+#.]*", text.lower()))


# -----------------------------
# Calculate text similarity
# -----------------------------
def calculate_similarity(resume_text, job_text):
    documents = [resume_text, job_text]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(documents)

    score = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(score * 100, 2)


# -----------------------------
# User inputs
# -----------------------------
uploaded_resume = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste the job description",
    height=220,
    placeholder="Paste the job responsibilities and required skills here..."
)


# -----------------------------
# Analyze button
# -----------------------------
if st.button("Analyze Resume", type="primary"):

    if uploaded_resume is None:
        st.error("Please upload your resume PDF.")

    elif not job_description.strip():
        st.error("Please paste a job description.")

    else:
        try:
            resume_text = extract_resume_text(uploaded_resume)

            if not resume_text.strip():
                st.error(
                    "No selectable text found. "
                    "Your PDF may be scanned. OCR support can be added later."
                )

            else:
                score = calculate_similarity(
                    resume_text,
                    job_description
                )

                resume_words = get_words(resume_text)
                job_words = get_words(job_description)

                # Simple keyword comparison for the first version.
                # This is not yet a complete skill extraction system.
                common_words = resume_words & job_words
                missing_words = job_words - resume_words

                st.subheader("Analysis Results")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Text Similarity", f"{score}%")

                with col2:
                    st.metric(
                        "Common Keywords",
                        len(common_words)
                    )

                st.progress(score / 100)

                st.caption(
                    "This percentage measures text similarity. "
                    "It is not a guarantee of job suitability."
                )

                with st.expander("View matching keywords"):
                    if common_words:
                        st.write(", ".join(sorted(common_words)))
                    else:
                        st.write("No common keywords found.")

                with st.expander("View potentially missing keywords"):
                    if missing_words:
                        st.write(", ".join(sorted(missing_words)))
                    else:
                        st.write("No missing keywords found.")

                st.subheader("Resume Text Preview")
                st.text_area(
                    "Extracted text",
                    resume_text,
                    height=200
                )

        except Exception as error:
            st.error(
                "Unable to analyze this PDF. "
                "Please check that it is a valid, readable PDF."
            )
            st.code(str(error))
