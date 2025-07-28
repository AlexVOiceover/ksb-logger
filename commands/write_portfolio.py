import os
import logging
import click
from data_persistence import load_pull_requests, load_rated_work
from llm_client import LLMClient
from ksb_loader import load_ksbs
from portfolio_generator import select_best_pr_per_ksb, generate_portfolio_markdown

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
    pull_requests_csv = "output/pull_requests.csv"
    rated_work_csv = "rated_work.csv"
    ksbs_csv = "ksbs.csv"
    portfolio_md = "output/portfolio.md"

    try:
        prs = load_pull_requests(pull_requests_csv)
        rated_work = load_rated_work(rated_work_csv)
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
    best_prs_per_ksb = select_best_pr_per_ksb(rated_work, prs)
    if not best_prs_per_ksb:
        logging.warning("No best PRs selected for any KSB. Exiting.")
        return

    logging.info(f"Generating portfolio markdown to {portfolio_md}...")
    generate_portfolio_markdown(best_prs_per_ksb, ksbs, portfolio_md, llm_client)

    logging.info("Portfolio generation process completed.")
