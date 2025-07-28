import logging
import click
from dotenv import load_dotenv

from commands.pull_prs import pull_prs
from commands.extract_style import extract_style
from commands.rate_work import rate_work
from commands.write_portfolio import write_portfolio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

@click.group()
@click.option('--verbose', is_flag=True, help="Enable verbose logging.")
def cli(verbose):
    """A CLI tool to generate a professional software development portfolio from GitHub PRs."""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    load_dotenv()

cli.add_command(pull_prs)
cli.add_command(extract_style)
cli.add_command(rate_work)
cli.add_command(write_portfolio)

if __name__ == '__main__':
    cli()