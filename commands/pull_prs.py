import os
import logging
import click
from data_persistence import save_pull_requests
from github_client import GitHubClient, GitHubAPIError

@click.command()
@click.option('--username', required=True, help='GitHub username to fetch PRs for.')
@click.option('--days-back', type=int, default=365, help='Number of days back to fetch PRs.')
def pull_prs(username, days_back):
    """Pulls PRs from GitHub and saves them to a local file."""
    github_token = os.getenv("GITHUB_API")
    if not github_token:
        logging.error("GITHUB_TOKEN environment variable not set.")
        return

    github_client = GitHubClient(token=github_token)
    pull_requests_csv = "output/pull_requests.csv"

    logging.info(f"Searching for PRs authored by {username} from the last {days_back} days...")
    try:
        prs = github_client.search_pull_requests_by_author(username, days_back)
        save_pull_requests(pull_requests_csv, prs)
        logging.info(f"Fetched and saved {len(prs)} PRs.")
    except GitHubAPIError as e:
        logging.error(f"Failed to fetch PRs from GitHub: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching PRs: {e}")
