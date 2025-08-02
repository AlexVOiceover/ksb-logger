import os
import logging
import click
import re
from typing import List, Dict, Any
from ..core.data_persistence import load_pull_requests, load_rated_work

def get_config_value(key: str, default: int) -> int:
    """Get configuration value from environment with fallback to default."""
    try:
        return int(os.getenv(key, default))
    except (ValueError, TypeError):
        logging.warning(f"Invalid value for {key}, using default: {default}")
        return default

@click.command()
def extract_code():
    """Extracts relevant code snippets from high-scoring PRs for portfolio generation."""
    pull_requests_json = "output/pull_requests.json"
    rated_work_json = "rated_work.json"  # load_rated_work adds output/ prefix automatically
    code_snippets_json = "output/code_snippets.json"
    
    # Load configuration values
    max_lines = get_config_value('CODE_MAX_LINES', 20)
    min_lines = get_config_value('CODE_MIN_LINES', 3)
    truncate_threshold = get_config_value('CODE_TRUNCATE_THRESHOLD', 15)
    max_snippets_per_pr = get_config_value('CODE_MAX_SNIPPETS_PER_PR', 5)
    
    logging.info(f"Code extraction config: max_lines={max_lines}, min_lines={min_lines}, truncate_threshold={truncate_threshold}, max_snippets_per_pr={max_snippets_per_pr}")
    
    try:
        prs = load_pull_requests(pull_requests_json)
        rated_work = load_rated_work(rated_work_json)
    except FileNotFoundError as e:
        logging.error(f"Required file not found: {e}. Please run pull-prs and rate-work commands first.")
        return
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return

    if not prs or not rated_work:
        logging.warning("No PRs or rated work found. Nothing to extract.")
        return

    logging.info(f"Extracting code from {len(prs)} PRs based on {len(rated_work)} ratings...")
    
    # Group rated work by PR ID for easy lookup
    pr_ratings = {}
    for rating in rated_work:
        pr_id = rating['pr_id']
        if pr_id not in pr_ratings:
            pr_ratings[pr_id] = []
        pr_ratings[pr_id].append(rating)
    
    # Find high-scoring PRs (score >= 7)
    high_scoring_prs = []
    for pr in prs:
        if pr.id in pr_ratings:
            max_score = max(rating['score'] for rating in pr_ratings[pr.id])
            if max_score >= 7:
                high_scoring_prs.append(pr)
    
    logging.info(f"Found {len(high_scoring_prs)} high-scoring PRs (score >= 7) for code extraction")
    
    # Extract code snippets from high-scoring PRs
    code_snippets = {}
    for i, pr in enumerate(high_scoring_prs, 1):
        logging.info(f"Processing PR {i}/{len(high_scoring_prs)}: {pr.id} - \"{pr.title}\"")
        
        pr_snippets = extract_code_from_pr(pr, max_lines, min_lines, truncate_threshold, max_snippets_per_pr)
        if pr_snippets:
            code_snippets[str(pr.id)] = {
                'pr_title': pr.title,
                'pr_url': pr.url,
                'snippets': pr_snippets
            }
            logging.info(f"✓ Extracted {len(pr_snippets)} code snippets from PR {pr.id}")
        else:
            logging.info(f"No relevant code found in PR {pr.id}")
    
    # Save extracted code snippets
    try:
        import json
        os.makedirs(os.path.dirname(code_snippets_json), exist_ok=True)
        with open(code_snippets_json, 'w', encoding='utf-8') as f:
            json.dump(code_snippets, f, indent=2, ensure_ascii=False)
        
        total_snippets = sum(len(data['snippets']) for data in code_snippets.values())
        logging.info(f"Saved {total_snippets} code snippets from {len(code_snippets)} PRs to {code_snippets_json}")
    except Exception as e:
        logging.error(f"Error saving code snippets: {e}")

def extract_code_from_pr(pr, max_lines: int, min_lines: int, truncate_threshold: int, max_snippets_per_pr: int) -> List[Dict[str, Any]]:
    """Extract meaningful code snippets from a PR's file changes."""
    if not pr.file_changes:
        return []
    
    snippets = []
    
    for file_change in pr.file_changes:
        # Skip non-code files and very large files
        if file_change['language'] == 'text' or file_change['changes'] > 200:
            continue
        
        # Focus on added and modified files
        if file_change['status'] not in ['added', 'modified']:
            continue
        
        # Extract meaningful code from the patch
        patch = file_change.get('patch', '')
        if not patch:
            continue
        
        # Parse the patch to extract added lines (starting with +)
        added_lines = []
        for line in patch.split('\n'):
            if line.startswith('+') and not line.startswith('+++'):
                # Remove the + prefix and clean up
                clean_line = line[1:].rstrip()
                if clean_line.strip() and not is_trivial_line(clean_line):
                    added_lines.append(clean_line)
        
        if added_lines:
            # Group consecutive added lines into code blocks
            code_blocks = group_consecutive_lines(added_lines)
            
            for block in code_blocks:
                if min_lines <= len(block) <= max_lines:  # Only blocks within configured range
                    snippet = {
                        'filename': file_change['filename'],
                        'language': file_change['language'],
                        'code': '\n'.join(block),
                        'additions': len(block),
                        'context': f"Changes in {file_change['filename']}"
                    }
                    snippets.append(snippet)
                elif len(block) > max_lines:  # Large blocks - try to truncate smartly
                    truncated_block = smart_truncate_code_block(block, file_change['language'], truncate_threshold)
                    if truncated_block:
                        snippet = {
                            'filename': file_change['filename'],
                            'language': file_change['language'],
                            'code': '\n'.join(truncated_block),
                            'additions': len(truncated_block),
                            'context': f"Key changes in {file_change['filename']} (truncated)"
                        }
                        snippets.append(snippet)
    
    # Sort by number of additions (most significant changes first)
    snippets.sort(key=lambda x: x['additions'], reverse=True)
    
    # Limit snippets per PR based on config
    return snippets[:max_snippets_per_pr]

def is_trivial_line(line: str) -> bool:
    """Check if a line is trivial (comments, whitespace, imports, etc.)."""
    stripped = line.strip()
    
    # Empty lines
    if not stripped:
        return True
    
    # Comment lines
    if stripped.startswith(('/', '#', '*', '//', '<!--', '--')):
        return True
    
    # Import/require statements
    if re.match(r'^(import|from|require|include|using)\s+', stripped):
        return True
    
    # Simple variable declarations without logic
    if re.match(r'^\s*(const|let|var|int|string|bool)\s+\w+\s*[=;]', stripped):
        return True
    
    # Closing braces/brackets only
    if re.match(r'^[}\]\)]+[;,]*$', stripped):
        return True
    
    return False

def group_consecutive_lines(lines: List[str]) -> List[List[str]]:
    """Group consecutive non-empty lines into code blocks."""
    if not lines:
        return []
    
    blocks = []
    current_block = []
    
    for line in lines:
        if line.strip():  # Non-empty line
            current_block.append(line)
        else:
            # Empty line - end current block if it has content
            if current_block:
                blocks.append(current_block)
                current_block = []
    
    # Add final block if it has content
    if current_block:
        blocks.append(current_block)
    
    return blocks

def smart_truncate_code_block(block: List[str], language: str, truncate_threshold: int = 15) -> List[str]:
    """Intelligently truncate large code blocks to keep the most meaningful parts."""
    if len(block) <= truncate_threshold:
        return block
    
    # Find important lines (function definitions, class definitions, etc.)
    important_patterns = {
        'javascript': [r'^\s*(function|class|const|let|var|export|import)', r'^\s*[}\]]\s*[,;]?\s*$'],
        'python': [r'^\s*(def|class|import|from|@)', r'^\s*return\s+', r'^\s*(if|for|while|try|except|finally)\s+'],
        'java': [r'^\s*(public|private|protected|static|class|interface)', r'^\s*[}\]]\s*$'],
        'typescript': [r'^\s*(function|class|interface|type|const|let|var|export|import)', r'^\s*[}\]]\s*[,;]?\s*$']
    }
    
    patterns = important_patterns.get(language, important_patterns.get('javascript', []))
    
    # Mark important lines
    important_indices = set()
    for i, line in enumerate(block):
        for pattern in patterns:
            if re.match(pattern, line):
                important_indices.add(i)
                break
    
    # Always include the first few and last few lines
    result = []
    
    # Include first 5 lines
    result.extend(block[:5])
    
    # Add separator if we're skipping content
    if len(block) > 12:
        result.append("  // ... (truncated for brevity)")
    
    # Include important lines from the middle
    middle_important = [i for i in important_indices if 5 <= i < len(block) - 3]
    if middle_important:
        # Take up to 3 important middle lines
        for i in sorted(middle_important)[:3]:
            result.append(block[i])
    
    # Include last 3 lines if the block is long enough
    if len(block) > 8:
        if len(block) > 12:
            result.append("  // ... (truncated)")
        result.extend(block[-3:])
    
    return result