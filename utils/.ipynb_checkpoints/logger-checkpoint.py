import logging
from datetime import datetime
import os
import json

def setup_logger():
    """
    Konfiguracja loggera z zapisem do pliku w katalogu domowym.
    """
    log_dir = os.path.expanduser("~/app/logs/")
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


def log_plots_state(state):
    """
    Loguje aktualny stan zapisanych wykresów.
    """
    logging.info("Aktualny stan wykresów:")
    for plot in state.get("plots", []):
        logging.info(json.dumps(plot, indent=2, default=str))


def log_event(message):
    """
    Loguje dowolne zdarzenie w aplikacji.
    """
    logging.info(message)
