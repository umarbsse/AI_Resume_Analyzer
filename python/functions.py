import os
import PyPDF2

from utils.logger import setup_logger
from db import get_resume_by_id, update_resume_text
from services.analyzer import analyze_resume_text, update_analysis

logger = setup_logger()

def read_pdf(input_file_path):
    text = ""

    try:
        with open(input_file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                text += page.extract_text() or ""

        logger.info("PDF read successfully")

    except Exception as e:
        logger.error(f"Error reading PDF: {str(e)}")

    return text


def process_resume(resume_id):
    try:
        # -----------------------------
        # START LOG
        # -----------------------------
        logger.info("Script started", extra={"resume_id": resume_id})

        logger.info(
            f"Processing resume ID: {resume_id}",
            extra={"resume_id": resume_id}
        )

        # -----------------------------
        # FETCH FROM DB
        # -----------------------------
        result = get_resume_by_id(resume_id)

        if not result:
            logger.error(
                "No record found in DB",
                extra={"resume_id": resume_id}
            )
            return False

        # -----------------------------
        # DB VALUES
        # Expected:
        # result = (file_path, job_description, resume_text)
        # -----------------------------
        file_path = result[0]
        job_description = result[1] if len(result) > 1 else ""
        resume_text = result[2] if len(result) > 2 else None

        # -----------------------------
        # BUILD FULL FILE PATH (fallback if needed)
        # -----------------------------
        base_path = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        full_path = os.path.join(base_path, file_path)

        logger.info(
            f"File path resolved: {full_path}",
            extra={"resume_id": resume_id}
        )

        # -----------------------------
        # STEP 1: GET RESUME TEXT
        # -----------------------------
        if not resume_text or resume_text.strip() == "":

            logger.info(
                "Resume text not found in DB, reading PDF...",
                extra={"resume_id": resume_id}
            )

            from functions import read_pdf
            resume_text = read_pdf(full_path)

            if not resume_text or resume_text.strip() == "":
                logger.warning(
                    "No text extracted from PDF",
                    extra={"resume_id": resume_id}
                )
                return False

            update_resume_text(resume_id, resume_text)

            logger.info(
                "Resume text stored in DB",
                extra={"resume_id": resume_id}
            )

        else:
            logger.info(
                "Using existing resume_text from DB",
                extra={"resume_id": resume_id}
            )

        # -----------------------------
        # STEP 2: AI ANALYSIS
        # -----------------------------
        logger.info(
            "Starting AI analysis",
            extra={"resume_id": resume_id}
        )

        analysis = analyze_resume_text(resume_text, job_description)

        # -----------------------------
        # STEP 3: STORE ANALYSIS
        # -----------------------------
        update_analysis(resume_id, analysis)

        logger.info(
            f"Analysis completed | Score: {analysis['match_score']}",
            extra={"resume_id": resume_id}
        )

        return True

    except Exception as e:
        logger.error(
            f"Error occurred: {str(e)}",
            extra={"resume_id": resume_id}
        )
        return False
    try:
        # -----------------------------
        # LOG START
        # -----------------------------
        logger.info("Script started", extra={"resume_id": resume_id})

        logger.info(
            f"Processing resume ID: {resume_id}",
            extra={"resume_id": resume_id}
        )

        # -----------------------------
        # FETCH FROM DB
        # -----------------------------
        result = get_resume_by_id(resume_id)

        if not result:
            logger.error(
                "No record found in DB",
                extra={"resume_id": resume_id}
            )
            return False

        relative_path = result[0]

        # -----------------------------
        # BUILD FILE PATH
        # -----------------------------
        base_path = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        full_path = os.path.join(base_path, relative_path)

        logger.info(
            f"Reading file: {full_path}",
            extra={"resume_id": resume_id}
        )

        # -----------------------------
        # READ PDF
        # -----------------------------
        text = read_pdf(full_path)

        if not text or text.strip() == "":
            logger.warning(
                "No text extracted from PDF",
                extra={"resume_id": resume_id}
            )

        # -----------------------------
        # STORE IN DB
        # -----------------------------
        update_resume_text(resume_id, text)

        logger.info(
            "Resume text stored successfully",
            extra={"resume_id": resume_id}
        )

        return True

    except Exception as e:
        logger.error(
            f"Error occurred: {str(e)}",
            extra={"resume_id": resume_id}
        )
        return False