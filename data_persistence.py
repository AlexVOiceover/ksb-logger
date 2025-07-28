import csv
import os
import json
import logging

csv.field_size_limit(2**25) # Set CSV field size limit to 32MB
from typing import List, Dict, Any
from github_client import PullRequest

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def save_pull_requests(file_path: str, prs: List[PullRequest]):
    """Saves a list of PullRequest objects to a CSV file."""
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'title', 'body', 'url', 'created_at', 'commit_messages']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for pr in prs:
                writer.writerow({
                    'id': pr.id,
                    'title': pr.title,
                    'body': pr.body,
                    'url': pr.url,
                    'created_at': pr.created_at,
                    'commit_messages': ';'.join(pr.commit_messages),
                    
                })
        logging.info(f"Successfully saved {len(prs)} pull requests to {file_path}")
    except IOError as e:
        logging.error(f"Error saving pull requests to {file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while saving pull requests: {e}")
        raise

def load_pull_requests(file_path: str) -> List[PullRequest]:
    """Loads a list of PullRequest objects from a CSV file."""
    if not os.path.exists(file_path):
        logging.warning(f"Pull request file not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    prs = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    comments_data = []

                    prs.append(PullRequest(
                        id=int(row['id']),
                        title=row['title'],
                        body=row['body'] if 'body' in row else '',
                        url=row['url'] if 'url' in row else '',
                        created_at=row['created_at'] if 'created_at' in row else '',
                        commit_messages=row['commit_messages'].split(';') if 'commit_messages' in row and row['commit_messages'] else [],
                        
                    ))
                except KeyError as e:
                    logging.warning(f"Malformed row in {file_path}: Missing expected column {e}. Skipping row.")
                except ValueError as e:
                    logging.warning(f"Data conversion error in {file_path} for row {row}: {e}. Skipping row.")
        logging.info(f"Successfully loaded {len(prs)} pull requests from {file_path}")
    except IOError as e:
        logging.error(f"Error loading pull requests from {file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading pull requests: {e}")
        raise
    return prs

def save_rated_work(file_path: str, rated_work: List[Dict[str, Any]]):
    file_path = os.path.join('output', file_path)
    """Saves a list of rated KSB-PR mappings to a CSV file."""
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            if rated_work:
                fieldnames = list(rated_work[0].keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rated_work)
            else:
                # If rated_work is empty, just write the header based on expected fields
                fieldnames = ["pr_id", "ksb_id", "score", "justification"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
        logging.info(f"Successfully saved {len(rated_work)} rated work entries to {file_path}")
    except IOError as e:
        logging.error(f"Error saving rated work to {file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while saving rated work: {e}")
        raise

def load_rated_work(file_path: str) -> List[Dict[str, Any]]:
    file_path = os.path.join('output', file_path)
    """Loads a list of rated KSB-PR mappings from a CSV file."""
    if not os.path.exists(file_path):
        logging.warning(f"Rated work file not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    rated_work = []
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    # Convert score and pr_id back to int if they exist
                    if 'score' in row and row['score']:
                        row['score'] = int(row['score'])
                    if 'pr_id' in row and row['pr_id']:
                        row['pr_id'] = int(row['pr_id'])
                    rated_work.append(row)
                except ValueError as e:
                    logging.warning(f"Data conversion error in {file_path} for row {row}: {e}. Skipping row.")
                except KeyError as e:
                    logging.warning(f"Malformed row in {file_path}: Missing expected column {e}. Skipping row.")
        logging.info(f"Successfully loaded {len(rated_work)} rated work entries from {file_path}")
    except IOError as e:
        logging.error(f"Error loading rated work from {file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading rated work: {e}")
        raise
    return rated_work
