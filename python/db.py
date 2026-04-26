import logging
from config import DB_CONFIG
import pymysql

logger = logging.getLogger()


def get_connection():
    return pymysql.connect(**DB_CONFIG)


def get_resume_by_id(resume_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT file_path, job_description, resume_text FROM resume_analyzer WHERE id=%s",
            (resume_id,)
        )

        result = cursor.fetchone()
        conn.close()

        logger.info(f"Fetched resume ID: {resume_id}")
        return result

    except Exception as e:
        logger.error(f"DB fetch error: {str(e)}")
        return None


def update_resume_text(resume_id, text):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE resume_analyzer 
            SET resume_text=%s, updated_at=NOW()
            WHERE id=%s
        """, (text, resume_id))

        conn.commit()
        conn.close()

        logger.info(f"Updated resume_text for ID: {resume_id}")

    except Exception as e:
        logger.error(f"DB update error: {str(e)}")

def insert_log(resume_id, level, message):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO python_logs (resume_id, level, message, created_at, updated_at)
            VALUES (%s, %s, %s, NOW(), NOW())
        """

        cursor.execute(query, (resume_id, level, message))
        conn.commit()
        conn.close()

    except Exception as e:
        print("DB Log Error:", str(e))