import os
import logging
from db import insert_log


class DBHandler(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            level = record.levelname

            resume_id = getattr(record, "resume_id", None)

            # 🔥 USE EXISTING DB FUNCTION
            insert_log(resume_id, level, msg)

        except Exception as e:
            print("Logger DB error:", str(e))


def setup_logger():
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'app.log')

    logger = logging.getLogger("ai_resume_logger")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

    # File logging
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # DB logging
    db_handler = DBHandler()
    db_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(db_handler)

    return logger