
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS = [
    "python", "java", "sql", "mysql",
    "machine learning", "deep learning",
    "generative ai", "natural language processing",
    "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "html", "css",
    "javascript", "react", "node.js",
    "django", "flask", "git", "docker",
    "aws", "linux", "rest api", "data analysis",
]


def extract_skills(text):
    text = text.lower()
    found = set()

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text):
            found.add(skill)

    return sorted(found)


def calculate_match(resume_text, job_description):
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(documents)

    score = cosine_similarity(
        vectors[0:1], vectors[1:2]
    )[0][0]

    return round(float(score) * 100, 1)


def analyze_resume(resume_text, job_description):
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))

    matching = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)

    skill_score = (
        round(len(matching) / len(job_skills) * 100, 1)
        if job_skills else 0.0
    )

    return {
        "similarity_score": calculate_match(
            resume_text, job_description
        ),
        "skill_match_score": skill_score,
        "matching_skills": matching,
        "missing_skills": missing,
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
    }
