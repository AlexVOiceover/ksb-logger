import os
import json
import logging
from typing import List, Dict, Any
from ..clients.github_client import PullRequest

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def save_pull_requests(file_path: str, prs: List[PullRequest]):
    """Saves a list of PullRequest objects to a JSON file."""
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Convert PullRequest objects to dictionaries
        prs_data = []
        for pr in prs:
            prs_data.append({
                'id': pr.id,
                'title': pr.title,
                'body': pr.body,
                'url': pr.url,
                'created_at': pr.created_at,
                'commit_messages': pr.commit_messages,
                'comments': pr.comments,
                'file_changes': pr.file_changes
            })
        
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(prs_data, jsonfile, indent=2, ensure_ascii=False)
        
        logging.info(f"Successfully saved {len(prs)} pull requests to {file_path}")
    except IOError as e:
        logging.error(f"Error saving pull requests to {file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while saving pull requests: {e}")
        raise

def load_pull_requests(file_path: str) -> List[PullRequest]:
    """Loads a list of PullRequest objects from a JSON file."""
    if not os.path.exists(file_path):
        logging.warning(f"Pull request file not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")
    
    prs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            prs_data = json.load(jsonfile)
            
            for pr_data in prs_data:
                try:
                    prs.append(PullRequest(
                        id=pr_data['id'],
                        title=pr_data.get('title', ''),
                        body=pr_data.get('body', ''),
                        url=pr_data.get('url', ''),
                        created_at=pr_data.get('created_at', ''),
                        commit_messages=pr_data.get('commit_messages', []),
                        comments=pr_data.get('comments', []),
                        file_changes=pr_data.get('file_changes', [])
                    ))
                except KeyError as e:
                    logging.warning(f"Malformed PR data in {file_path}: Missing expected field {e}. Skipping PR.")
                except Exception as e:
                    logging.warning(f"Error processing PR data in {file_path}: {e}. Skipping PR.")
        
        logging.info(f"Successfully loaded {len(prs)} pull requests from {file_path}")
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in {file_path}: {e}")
        raise
    except IOError as e:
        logging.error(f"Error loading pull requests from {file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading pull requests: {e}")
        raise
    return prs

def save_rated_work(file_path: str, rated_work: List[Dict[str, Any]]):
    """Saves a list of rated KSB-PR mappings to a JSON file."""
    file_path = os.path.join('output', file_path)
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(rated_work, jsonfile, indent=2, ensure_ascii=False)
        
        logging.info(f"Successfully saved {len(rated_work)} rated work entries to {file_path}")
    except IOError as e:
        logging.error(f"Error saving rated work to {file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while saving rated work: {e}")
        raise

def load_rated_work(file_path: str) -> List[Dict[str, Any]]:
    """Loads a list of rated KSB-PR mappings from a JSON file."""
    file_path = os.path.join('output', file_path)
    if not os.path.exists(file_path):
        logging.warning(f"Rated work file not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            rated_work = json.load(jsonfile)
        
        logging.info(f"Successfully loaded {len(rated_work)} rated work entries from {file_path}")
        return rated_work
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in {file_path}: {e}")
        raise
    except IOError as e:
        logging.error(f"Error loading rated work from {file_path}: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading rated work: {e}")
        raise
