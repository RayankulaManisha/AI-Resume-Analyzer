
import streamlit as st

from src.resume_parser import extract_resume_text
from src.analyzer import analyze_resume


st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
)

# Dashboard styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F5F7FB;
    }
    .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📄 AI Resume Analyzer")
st.caption(
    "Understand your resume's alignment with your target job."
)

st.divider()

left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("1. Upload your resume")

    uploaded_file = st.file_uploader(
        "Choose a PDF resume",
        type=["pdf"],
    )

    st.info("Use a text-based PDF for the first version.")

with right:
    st.subheader("2. Target job")

    job_description = st.text_area(
        "Paste the job description",
        height=220,
        placeholder=(
            "Paste the job responsibilities and "
            "required skills here..."
        ),
    )

analyze_clicked = st.button(
    "Analyze Resume",
    type="primary",
    use_container_width=True,
)

if analyze_clicked:
    if uploaded_file is None:
        st.error("Please upload your resume PDF.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:
        try:
            with st.spinner("Analyzing your resume..."):
                resume_text = extract_resume_text(uploaded_file)

                if not resume_text:
                    st.warning(
                        "No selectable text was found. "
                        "This PDF may need OCR processing."
                    )
                else:
                    results = analyze_resume(
                        resume_text,
                        job_description,
                    )

                    st.divider()
                    st.header("Analysis Dashboard")

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Text Similarity",
                        f"{results['similarity_score']}%",
                    )

                    col2.metric(
                        "Skill Match",
                        f"{results['skill_match_score']}%",
                    )

                    col3.metric(
                        "Matching Skills",
                        len(results["matching_skills"]),
                    )

                    st.caption(
                        "Scores are estimates based on text "
                        "similarity and recognized skills."
                    )

                    st.subheader("Skill Match Overview")

                    st.progress(
                        results["skill_match_score"] / 100
                    )

                    match_col, gap_col = st.columns(2)

                    with match_col:
                        st.subheader("✅ Matching Skills")

                        if results["matching_skills"]:
                            for skill in results["matching_skills"]:
                                st.write(f"• {skill.title()}")
                        else:
                            st.write("No matching skills detected.")

                    with gap_col:
                        st.subheader("📌 Potential Skill Gaps")

                        if results["missing_skills"]:
                            for skill in results["missing_skills"]:
                                st.write(f"• {skill.title()}")
                        else:
                            st.write(
                                "No recognized skill gaps detected."
                            )

                    with st.expander("View all detected resume skills"):
                        st.write(
                            results["resume_skills"]
                            or "No known skills detected."
                        )

                    with st.expander("View extracted resume text"):
                        st.text(resume_text)

        except Exception as error:
            st.error(
                "The resume could not be analyzed. "
                "Check the PDF and try again."
            )
            st.exception(error)
