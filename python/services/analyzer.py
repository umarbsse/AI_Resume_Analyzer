import re
from db import get_connection


# =====================================================
# ANALYZE RESUME VS JOB DESCRIPTION
# =====================================================
def analyze_resume_text(resume_text, job_description):

    # -----------------------------------------------------
    # SAFE CLEANING (IMPORTANT FIX)
    # -----------------------------------------------------
    resume_text = resume_text or ""
    job_description = job_description or ""

    resume_text = resume_text.strip()
    job_description = job_description.strip()

    # If still empty → return safe response
    if resume_text == "" or job_description == "":
        return {
            "match_score": 0,
            "strengths": "Resume or job description missing in analysis input",
            "improvements": "Ensure resume_text and job_description are stored in DB",
            "suggestions": "Check DB data insertion flow"
        }

    # -----------------------------------------------------
    # LOWERCASE FOR MATCHING
    # -----------------------------------------------------
    resume_text_lower = resume_text.lower()
    job_text_lower = job_description.lower()

    # -----------------------------------------------------
    # KEYWORD EXTRACTION
    # -----------------------------------------------------
    job_keywords = set(re.findall(r'\b[a-zA-Z]{3,}\b', job_text_lower))
    resume_keywords = set(re.findall(r'\b[a-zA-Z]{3,}\b', resume_text_lower))

    matched_keywords = job_keywords.intersection(resume_keywords)

    # -----------------------------------------------------
    # MATCH SCORE
    # -----------------------------------------------------
    if len(job_keywords) == 0:
        match_score = 0
    else:
        match_score = int((len(matched_keywords) / len(job_keywords)) * 100)

    # -----------------------------------------------------
    # INSIGHTS
    # -----------------------------------------------------
    strengths = []
    improvements = []
    suggestions = []

    # Strengths
    if match_score >= 70:
        strengths.append("Strong match with job description")
    elif match_score >= 40:
        strengths.append("Moderate match with job description")
    else:
        improvements.append("Low keyword match with job description")

    # Tech detection
    tech_keywords = ["python", "laravel", "php", "node", "react", "mysql"]

    for tech in tech_keywords:
        if tech in resume_text_lower:
            strengths.append(f"{tech.capitalize()} experience detected")

    # Improvements
    if "project" not in resume_text_lower:
        improvements.append("Add project experience section")

    if len(resume_text.split()) < 200:
        improvements.append("Resume content is too short")

    # Suggestions
    if match_score < 50:
        suggestions.append("Improve keyword alignment with job description")

    if match_score < 70:
        suggestions.append("Tailor resume for this specific role")

    if not strengths:
        strengths.append("Basic resume structure detected")

    # -----------------------------------------------------
    # RETURN RESULT
    # -----------------------------------------------------
    return {
        "match_score": match_score,
        "strengths": ", ".join(strengths),
        "improvements": ", ".join(improvements),
        "suggestions": ", ".join(suggestions)
    }


# =====================================================
# UPDATE DB
# =====================================================
def update_analysis(resume_id, analysis):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            UPDATE resume_analyzer
            SET match_score=%s,
                strengths=%s,
                improvements_needed=%s,
                suggestions=%s,
                updated_at=NOW()
            WHERE id=%s
        """

        cursor.execute(query, (
            analysis["match_score"],
            analysis["strengths"],
            analysis["improvements"],
            analysis["suggestions"],
            resume_id
        ))

        conn.commit()
        conn.close()

        print(f"Analysis updated for resume ID: {resume_id}")

    except Exception as e:
        print("DB update error:", str(e))