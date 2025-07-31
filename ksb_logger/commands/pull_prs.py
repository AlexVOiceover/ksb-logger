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
            selected_repo_choices = select_repositories_interactive(all_user_repos)
            if not selected_repo_choices:
                logging.info("No repositories selected. Exiting.")
                return
            
            # Separate repos by analysis method
            pr_repos = [choice[0] for choice in selected_repo_choices if choice[1] == 'PRs']
            commit_repos = [choice[0] for choice in selected_repo_choices if choice[1] == 'commits']
            
            all_prs = []
            
            # Fetch PRs from repositories selected for PR analysis
            if pr_repos:
                logging.info(f"Fetching PRs from {len(pr_repos)} repositories selected for PR analysis...")
                prs_from_repos = github_client.search_pull_requests_by_author_filtered(username, pr_repos)
                all_prs.extend(prs_from_repos)
            
            # Fetch commits from repositories selected for commit analysis
            if commit_repos:
                logging.info(f"Fetching commits from {len(commit_repos)} repositories selected for commit analysis...")
                commits_as_prs = github_client.get_commits_by_author(username, commit_repos)
                all_prs.extend(commits_as_prs)
            
            prs = all_prs
            
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
