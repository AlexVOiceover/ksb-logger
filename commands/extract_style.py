import os
import logging
import click
from llm_client import LLMClient, LLMAPIError, LLMResponseError

@click.command()
def extract_style():
    """Analyzes the writing style of the existing portfolio content."""
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
    portfolio_md = "portfolio.md"

    if not os.path.exists(portfolio_md):
        logging.error(f"Portfolio file not found: {portfolio_md}")
        return

    with open(portfolio_md, 'r', encoding='utf-8') as f:
        portfolio_content = f.read()

    try:
        style_guide = llm_client.analyze_writing_style(portfolio_content)
        logging.info("Writing style analysis complete.")
        # The style guide is returned as a dictionary, so we'll print it for now
        # In a real application, you might want to save this to a file
        click.echo(style_guide)
    except (LLMAPIError, LLMResponseError) as e:
        logging.error(f"Error analyzing writing style with LLM: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during style analysis: {e}")
