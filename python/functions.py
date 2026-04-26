import PyPDF2
import logging

logger = logging.getLogger()

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