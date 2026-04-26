import logging
import os

def setup_logger():
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'app.log')

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )

    return logging.getLogger()