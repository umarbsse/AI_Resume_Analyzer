import sys
import pymysql
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -------------------------------
# CONFIG DB
# -------------------------------
db = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="ai_resume_analyzer",
    port=3307,
    charset="utf8mb4"
)

cursor = db.cursor()


# -------------------------------
# GET INPUT (Laravel passes ID)
# -------------------------------
resume_id = sys.argv[1]


# -------------------------------
# FETCH DATA FROM DB
# -------------------------------
cursor.execute("SELECT file_path, job_description FROM resume_analyzer WHERE id=%s", (resume_id,))
row = cursor.fetchone()

file_path = row[0]
job_description = row[1]


# -------------------------------
# READ PDF RESUME
# -------------------------------
def extract_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

resume_text = extract_text(file_path)


# -------------------------------
# MATCH SCORE (TF-IDF)
# -------------------------------
docs = [resume_text, job_description]

vectorizer = TfidfVectorizer(stop_words='english')
tfidf = vectorizer.fit_transform(docs)

score = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
match_score = int(score * 100)


# -------------------------------
# SIMPLE AI LOGIC (RULE BASED)
# -------------------------------
resume_words = set(resume_text.lower().split())
job_words = set(job_description.lower().split())

common = resume_words.intersection(job_words)

strengths = list(common)[:5]
improvements = list(job_words - resume_words)[:5]
suggestions = [
    "Add more keywords from job description",
    "Improve technical skill section",
    "Highlight measurable achievements"
]


# Convert lists to string
strengths_str = ", ".join(strengths)
improvements_str = ", ".join(improvements)
suggestions_str = ", ".join(suggestions)


# -------------------------------
# UPDATE DATABASE
# -------------------------------
update_query = """
UPDATE resume_analyzer 
SET match_score=%s,
    strengths=%s,
    improvements_needed=%s,
    suggestions=%s,
    updated_at=NOW()
WHERE id=%s
"""

cursor.execute(update_query, (
    match_score,
    strengths_str,
    improvements_str,
    suggestions_str,
    resume_id
))

db.commit()
db.close()

print("Analysis Completed")