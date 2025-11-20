import os
import logging
import click
from ..core.data_persistence import load_pull_requests, load_rated_work
from ..clients.llm_client import LLMClient
from ..core.ksb_loader import load_ksbs
from ..core.portfolio_generator import select_best_pr_per_ksb, generate_portfolio_markdown

@click.command()
def write_portfolio():
    """Writes the portfolio markdown file."""
    # groq_api_key = os.getenv("GROQ_API")  # Groq version
    # if not groq_api_key:
    #     logging.error("GROQ_API_KEY environment variable not set.")
    #     return
    # llm_client = LLMClient(api_key=groq_api_key)  # Groq version
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        logging.error("OPENAI_API_KEY environment variable not set.")
        return

    llm_client = LLMClient(api_key=openai_api_key)
    pull_requests_json = "output/pull_requests.json"
    rated_work_json = "rated_work.json"
    # Path to KSBs CSV file in the data directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    ksbs_csv = os.path.join(project_root, "ksb_logger", "data", "ksbs.csv")
    portfolio_md = "output/portfolio.md"

    try:
        prs = load_pull_requests(pull_requests_json)
        rated_work = load_rated_work(rated_work_json)
        ksbs = load_ksbs(ksbs_csv)
    except FileNotFoundError as e:
        logging.error(f"Required file not found: {e}. Please run the pull-prs and rate-work commands first.")
        return
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return

    if not rated_work:
        logging.warning("No rated work entries generated. Exiting.")
        return

    logging.info("Selecting best PR per KSB...")
    best_prs_per_ksb = select_best_pr_per_ksb(rated_work, prs, ksbs)
    if not best_prs_per_ksb:
        logging.warning("No best PRs selected for any KSB. Exiting.")
        return

    logging.info(f"Generating portfolio markdown to {portfolio_md}...")
    generate_portfolio_markdown(best_prs_per_ksb, ksbs, portfolio_md, llm_client)

    logging.info("Portfolio generation process completed.")
    
    # Display session statistics
    stats = llm_client.get_session_stats()
    if "error" not in stats:
        duration = stats["session_duration_minutes"]
        tokens = stats["total_tokens"]
        estimated_cost = stats["estimated_cost"]
        logging.info(f"Session completed in {duration:.1f} minutes. Tokens used: {tokens:,} (~${estimated_cost:.4f})")
    else:
        logging.warning(f"Could not retrieve session statistics: {stats['error']}")
