import sys
import os

from db import get_resume_by_id, update_resume_text
from functions import read_pdf
from utils.logger import setup_logger

logger = setup_logger()


def main():
    resume_id = None

    try:
        # -----------------------------
        # GET INPUT
        # -----------------------------
        resume_id = sys.argv[1]
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
            return

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

    except Exception as e:
        logger.error(
            f"Error occurred: {str(e)}",
            extra={"resume_id": resume_id}
        )

if __name__ == "__main__":
    main()