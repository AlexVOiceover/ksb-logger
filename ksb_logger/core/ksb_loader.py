import csv
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class KSB:
    def __init__(self, id: str, description: str):
        self.id = id
        self.description = description

def load_ksbs(file_path: str) -> List[KSB]:
    """Load KSBs from a CSV file."""
    ksbs = []
    try:
        with open(file_path, newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    ksbs.append(KSB(row['ID'], row['Description']))
                except KeyError as e:
                    logging.error(f"Malformed row in {file_path}: Missing expected column {e}. Skipping row.")
    except FileNotFoundError:
        logging.error(f"KSB file not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading KSBs from {file_path}: {e}")
        raise
    return ksbs

