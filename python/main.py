import sys
import os

from db import get_resume_by_id, update_resume_text
from functions import read_pdf
from utils.logger import setup_logger

logger = setup_logger()


def main():
    try:
        logger.info("Script started")

        # Get ID
        resume_id = sys.argv[1]
        logger.info(f"Processing resume ID: {resume_id}")

        # Fetch from DB
        result = get_resume_by_id(resume_id)

        if not result:
            logger.error("No record found in DB")
            return

        relative_path = result[0]

        # Build full path
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        full_path = os.path.join(base_path, relative_path)

        logger.info(f"Reading file: {full_path}")

        # Read PDF
        text = read_pdf(full_path)

        if not text:
            logger.warning("No text extracted from PDF")

        # Store in DB
        update_resume_text(resume_id, text)

        logger.info("Resume text stored successfully")

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")


if __name__ == "__main__":
    main()