import pandas as pd
import logging

def load_csv(file):
    try:
        df = pd.read_csv(file)
        logging.info(f"Loaded CSV file: {file.name}")
        return df
    except Exception as e:
        logging.error(f"Error loading CSV: {e}")
        return None
