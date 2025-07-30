import os
import logging
import click
from ..core.data_persistence import save_pull_requests
from ..clients.github_client import GitHubClient, GitHubAPIError

@click.command()
@click.option('--username', required=True, help='GitHub username to fetch PRs for.')
@click.option('--interactive', '-i', is_flag=True, help='Interactively select repositories to include.')
def pull_prs(username, interactive):
    """Pulls PRs from GitHub and saves them to a local file."""
    github_token = os.getenv("GITHUB_API")
    if not github_token:
        logging.error("GITHUB_TOKEN environment variable not set.")
        return

    github_client = GitHubClient(token=github_token)
    pull_requests_csv = "output/pull_requests.csv"

    if interactive:
        # Interactive mode: show all repositories (personal + organization) sorted newest to oldest
        from ..core.repo_selector import select_repositories_interactive
        
        logging.info(f"Finding all repositories where {username} has activity...")
        try:
            # Get ALL repositories (personal + organization) without date filtering
            all_user_repos = github_client.get_all_user_repositories(username)
            if not all_user_repos:
                logging.error(f"No repositories found for {username}")
                return
                
            logging.info(f"Found {len(all_user_repos)} repositories (personal + organization)")
            
            # Let user select repositories interactively using arrow keys + spacebar
            selected_repos = select_repositories_interactive(all_user_repos)
            if not selected_repos:
                logging.info("No repositories selected. Exiting.")
                return
            
            # Now fetch PRs from selected repositories
            logging.info(f"Fetching PRs from {len(selected_repos)} selected repositories...")
            prs = github_client.search_pull_requests_by_author_filtered(username, selected_repos)
            
        except GitHubAPIError as e:
            logging.error(f"Failed to fetch repositories from GitHub: {e}")
            return
    else:
        # Non-interactive mode: search all repositories
        logging.info(f"Searching for PRs authored by {username}...")
        prs = github_client.search_pull_requests_by_author(username)

    try:
        save_pull_requests(pull_requests_csv, prs)
        logging.info(f"Fetched and saved {len(prs)} PRs.")
    except GitHubAPIError as e:
        logging.error(f"Failed to fetch PRs from GitHub: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching PRs: {e}")
