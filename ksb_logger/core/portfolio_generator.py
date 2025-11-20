import os
import logging
import json
import time
import random
from typing import List, Dict, Any
from datetime import datetime
from .ksb_loader import KSB
from ..clients.github_client import PullRequest
from ..clients.llm_client import LLMClient, LLMAPIError, LLMResponseError
from langchain_core.prompts import ChatPromptTemplate

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def assess_prs_against_ksbs(prs: List[PullRequest], ksbs: List[KSB], llm_client: LLMClient) -> List[Dict[str, Any]]:
    """Assesses each PR against a list of KSBs using the LLM and returns a list of rated work."""
    rated_work = []
    logging.info(f"Starting assessment of {len(prs)} PRs against {len(ksbs)} KSBs...")

    for i, pr in enumerate(prs, 1):
        pr_details = {
            "title": pr.title if pr.title is not None else "",
            "body": pr.body if pr.body is not None else "",
            "commit_messages": os.linesep + '- '.join(pr.commit_messages) if pr.commit_messages else 'None',
            
            "comments": json.dumps(pr.comments) if pr.comments else '[]'
        }
        ksb_list_for_llm = [{'id': ksb.id, 'description': ksb.description} for ksb in ksbs]

        try:
            logging.info(f"Processing PR {i}/{len(prs)}: {pr.id} - \"{pr.title}\"...")
            ratings = llm_client.rate_pr_against_ksbs(pr_details, ksb_list_for_llm)
            for rating in ratings:
                rated_work.append({
                    "pr_id": pr.id,
                    "ksb_id": rating["ksb_id"],
                    "score": rating["score"],
                    "justification": rating["justification"]
                })
            logging.info(f"✓ Completed PR {i}/{len(prs)}: {pr.id}")
        except (LLMAPIError, LLMResponseError) as e:
            logging.error(f"Error assessing PR {i}/{len(prs)} (ID {pr.id}) with LLM: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during LLM assessment for PR {i}/{len(prs)} (ID {pr.id}): {e}")
    
    logging.info(f"Finished PR assessment. Total rated work entries: {len(rated_work)}")
    return rated_work

def select_best_pr_per_ksb(rated_work: List[Dict[str, Any]], prs: List[PullRequest], ksbs: List[KSB]) -> Dict[str, Dict[str, Any]]:
    """Selects the best PR for each KSB based on score, breaking ties by recency."""
    best_prs_per_ksb = {}
    pr_map = {pr.id: pr for pr in prs}
    valid_ksb_ids = {ksb.id for ksb in ksbs}

    for item in rated_work:
        ksb_id = item["ksb_id"]
        pr_id = item["pr_id"]
        score = item["score"]

        # Validate that the KSB ID exists in the loaded KSB list
        if ksb_id not in valid_ksb_ids:
            logging.warning(f"Invalid KSB ID '{ksb_id}' found in rated work (not in ksbs.csv). Skipping.")
            continue

        pr = pr_map.get(pr_id)
        if not pr:
            logging.warning(f"PR with ID {pr_id} not found in fetched PRs. Skipping rated work entry for KSB {ksb_id}.")
            continue # Skip if PR not found

        if ksb_id not in best_prs_per_ksb:
            best_prs_per_ksb[ksb_id] = {"pr_id": pr_id, "score": score, "pr": pr}
        else:
            current_best = best_prs_per_ksb[ksb_id]
            if score > current_best["score"]:
                best_prs_per_ksb[ksb_id] = {"pr_id": pr_id, "score": score, "pr": pr}
            elif score == current_best["score"]:
                # Tie-breaking: select the most recent PR
                current_pr_date = datetime.fromisoformat(current_best["pr"].created_at.replace("Z", "+00:00"))
                new_pr_date = datetime.fromisoformat(pr.created_at.replace("Z", "+00:00"))
                if new_pr_date > current_pr_date:
                    best_prs_per_ksb[ksb_id] = {"pr_id": pr_id, "score": score, "pr": pr}

    # Format the output to match the expected return type
    formatted_output = {}
    for ksb_id, data in best_prs_per_ksb.items():
        formatted_output[ksb_id] = {
            "pr_id": data["pr_id"],
            "score": data["score"],
            "pr": data["pr"]
        }
    logging.info(f"Selected best PRs for {len(formatted_output)} KSBs.")
    return formatted_output



def load_code_snippets() -> Dict[str, Any]:
    """Load extracted code snippets from JSON file."""
    code_snippets_json = "output/code_snippets.json"
    try:
        with open(code_snippets_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.warning(f"Code snippets file not found: {code_snippets_json}. Placeholders will remain.")
        return {}
    except Exception as e:
        logging.warning(f"Error loading code snippets: {e}. Placeholders will remain.")
        return {}

def replace_code_placeholders(content: str, pr_id: int, code_snippets: Dict[str, Any]) -> str:
    """Replace code placeholders with actual extracted code snippets."""
    pr_key = str(pr_id)
    if pr_key not in code_snippets:
        return content
    
    pr_snippets = code_snippets[pr_key]['snippets']
    if not pr_snippets:
        return content
    
    import re
    
    # Find all code placeholders in the content
    placeholder_pattern = r'\[==insert code snippet of: ([^]]+)==\]'
    placeholders = re.findall(placeholder_pattern, content)
    
    if not placeholders:
        return content
    
    # Replace placeholders with actual code snippets
    modified_content = content
    for i, placeholder_desc in enumerate(placeholders):
        if i < len(pr_snippets):
            snippet = pr_snippets[i]
            
            # Create formatted code block
            code_block = f"```{snippet['language']}\n{snippet['code']}\n```\n"
            code_block += f"*From {snippet['filename']}*"
            
            # Replace the placeholder
            old_placeholder = f"[==insert code snippet of: {placeholder_desc}==]"
            modified_content = modified_content.replace(old_placeholder, code_block, 1)
    
    return modified_content

def generate_portfolio_markdown(best_prs_per_ksb: Dict[str, Dict[str, Any]], ksbs: List[KSB], output_file: str, llm_client: LLMClient):
    """Generates the portfolio markdown file."""
    portfolio_content = []
    ksb_descriptions = {ksb.id: ksb.description for ksb in ksbs}
    
    # Load code snippets for placeholder replacement
    code_snippets = load_code_snippets()
    logging.info(f"Loaded code snippets for {len(code_snippets)} PRs")
    
    # Generate KSB matching table at the beginning
    table_lines = [
        "# Portfolio",
        "",
        "## KSB Evidence Summary",
        "",
        "| KSB ID | Description | Evidence |",
        "|--------|-------------|----------|"
    ]
    
    # Sort KSBs by K, S, B order, then by number
    def ksb_sort_key(ksb):
        ksb_id = ksb.id
        # Extract the letter and number parts
        letter = ksb_id[0]  # K, S, or B
        number = int(ksb_id[1:])  # The number part
        
        # Define order: K=1, S=2, B=3
        letter_order = {'K': 1, 'S': 2, 'B': 3}
        return (letter_order.get(letter, 4), number)
    
    sorted_ksbs = sorted(ksbs, key=ksb_sort_key)
    
    for ksb in sorted_ksbs:
        ksb_id = ksb.id
        description = ksb.description[:60] + "..." if len(ksb.description) > 60 else ksb.description
        
        if ksb_id in best_prs_per_ksb:
            # Create anchor link to section (convert to lowercase, replace spaces with hyphens)
            anchor = f"ksb-{ksb_id.lower()}"
            evidence_link = f"[View Evidence](#{anchor})"
        else:
            evidence_link = "❌ No evidence yet"
        
        table_lines.append(f"| {ksb_id} | {description} | {evidence_link} |")
    
    table_lines.extend(["", "---", ""])
    portfolio_content.extend(table_lines)

    # Load the variety kit
    try:
        # Get the correct path to prompts directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        variety_kit_path = os.path.join(project_root, "ksb_logger", "data", "prompts", "portfolio_variety_kit.md")
        
        with open(variety_kit_path, 'r', encoding='utf-8') as f:
            variety_content = f.read()
        
        sections = variety_content.split('## ')[1:]
        narrative_angles = [line.strip() for line in sections[0].split('\n')[2:] if line.strip()]
        opening_hooks = [line.strip() for line in sections[1].split('\n')[2:] if line.strip()]
        reflection_phrases = [line.strip() for line in sections[2].split('\n')[2:] if line.strip()]

    except (FileNotFoundError, IndexError) as e:
        logging.error(f"Could not load or parse portfolio_variety_kit.md: {e}. Proceeding without it.")
        narrative_angles, opening_hooks, reflection_phrases = [], [], []

    try:
        # Get the correct path to prompts directory  
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        prompt_template_path = os.path.join(project_root, "ksb_logger", "data", "prompts", "generate_narrative_portfolio_chapter.md")
        
        with open(prompt_template_path, 'r', encoding='utf-8') as f:
            chapter_prompt_template = f.read()
    except FileNotFoundError:
        logging.error(f"Prompt file not found: {prompt_template_path}. Cannot generate portfolio chapters.")
        return
    except Exception as e:
        logging.error(f"Error loading prompt file {prompt_template_path}: {e}")
        return

    logging.info(f"Generating portfolio chapters for {len(best_prs_per_ksb)} KSBs...")
    previous_chapter_context = "" # Initialize previous_chapter_context
    
    # Sort sections by KSB ID to match table order (K, S, B)
    def ksb_id_sort_key(item):
        ksb_id = item[0]  # Extract KSB ID from the tuple
        # Extract the letter and number parts
        letter = ksb_id[0]  # K, S, or B
        number = int(ksb_id[1:])  # The number part
        
        # Define order: K=1, S=2, B=3
        letter_order = {'K': 1, 'S': 2, 'B': 3}
        return (letter_order.get(letter, 4), number)
    
    sorted_ksb_items = sorted(best_prs_per_ksb.items(), key=ksb_id_sort_key)
    
    for ksb_id, data in sorted_ksb_items:
        pr = data["pr"]
        ksb_description = ksb_descriptions.get(ksb_id, "N/A")

        # Randomly select from the variety kit
        narrative_angle = random.choice(narrative_angles) if narrative_angles else ""
        opening_hook = random.choice(opening_hooks) if opening_hooks else ""
        reflection_phrase = random.choice(reflection_phrases) if reflection_phrases else ""

        # Prepare input for the LLM
        pr_details = {
            "ksb_id": ksb_id,
            "ksb_description": ksb_description,
            "pr_title": pr.title,
            "pr_body": pr.body,
            "pr_url": pr.url,
            "pr_created_at": pr.created_at,
            "commit_messages": "\n- " + "\n- ".join(pr.commit_messages) if pr.commit_messages else "None",
            "pr_comments": json.dumps(pr.comments) if pr.comments else "[]",
            "narrative_angle": narrative_angle,
            "opening_hook": opening_hook,
            "reflection_phrase": reflection_phrase,
            "previous_chapter_context": previous_chapter_context
        }

        try:
            logging.info(f"Generating chapter for KSB {ksb_id} with PR ID {pr.id}...")
            prompt = ChatPromptTemplate.from_template(chapter_prompt_template)
            chain = prompt | llm_client.llm
            response = chain.invoke(pr_details)
            
            # Generate the chapter title
            chapter_title = llm_client.generate_chapter_title(response.content)

            # Replace code placeholders with actual code snippets
            chapter_content = replace_code_placeholders(response.content, pr.id, code_snippets)

            # Add the KSB heading with anchor, PR link, and the refined chapter to the portfolio
            anchor_id = f"ksb-{ksb_id.lower()}"
            ksb_heading = f"## <a id=\"{anchor_id}\"></a>{ksb_id}: {ksb_description} - {chapter_title}"
            pr_link_tag = f"[==PR Link {pr.url} ==]"
            portfolio_content.append(ksb_heading)
            portfolio_content.append(pr_link_tag)
            portfolio_content.append(chapter_content)
            
            # Update previous_chapter_context for the next iteration
            previous_chapter_context = response.content

            logging.info(f"Successfully generated and refined chapter for KSB {ksb_id}.")
            time.sleep(5)  # Add a 5-second delay to avoid rate limiting
        except (LLMAPIError, LLMResponseError) as e:
            logging.error(f"Error generating chapter for KSB {ksb_id} with LLM: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during chapter generation for KSB {ksb_id}: {e}")

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(portfolio_content))
        logging.info(f"Portfolio markdown generated successfully at {output_file}")
    except IOError as e:
        logging.error(f"Error writing portfolio markdown to {output_file}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while writing portfolio markdown: {e}")



