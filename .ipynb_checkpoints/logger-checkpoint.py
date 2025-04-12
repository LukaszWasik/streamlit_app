import logging
from datetime import datetime
import os

def setup_logger():
    # 📁 Ścieżka absolutna do katalogu logów w katalogu domowym
    log_dir = os.path.expanduser("/home/lukasz/app/logs/")
    os.makedirs(log_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = os.path.join(log_dir, f"log_{timestamp}.log")

    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s — %(levelname)s — %(message)s"
    )

    logging.info("Logger initialized.")
    return log_filename
