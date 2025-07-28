import requests
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors."""
    pass

class PullRequest:
    def __init__(self, id: int, title: str, body: str, url: str, created_at: str, commit_messages: List[str], comments: List[Dict[str, Any]] = []):
        self.id = id
        self.title = title
        self.body = body
        self.url = url
        self.created_at = created_at
        self.commit_messages = commit_messages
        self.comments = comments

class GitHubClient:
    def __init__(self, token: str):
        self.token = token
        self.headers = {"Authorization": f"token {self.token}"}

    def _make_request(self, url: str, media_type: str = "") -> Dict[str, Any]:
        headers = self.headers.copy()
        if media_type:
            headers["Accept"] = media_type

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Network or request error while fetching {url}: {e}")
            raise GitHubAPIError(f"Failed to fetch data from {url} due to network error: {e}")
        except Exception as e:
            logging.error(f"GitHub API request failed for {url}: {e}")
            raise GitHubAPIError(f"Failed to fetch data from {url}: {e}")

    def get_user_public_repos(self, username: str) -> List[Dict[str, Any]]:
        logging.info(f"Fetching public repositories for {username}")
        url = f"https://api.github.com/users/{username}/repos?type=public&per_page=100"
        repos = []
        while url:
            try:
                data = self._make_request(url)
                repos.extend(data)
                url = requests.get(url, headers=self.headers).links.get('next', {}).get('url')
            except GitHubAPIError as e:
                logging.error(f"Failed to fetch public repositories for {username}: {e}")
                return []
            except Exception as e:
                logging.error(f"An unexpected error occurred while fetching public repositories for {username}: {e}")
                return []
        return repos

    def get_pull_request_comments(self, comments_url: str) -> List[Dict[str, Any]]:
        logging.info(f"Fetching comments for {comments_url}")
        try:
            comments_data = self._make_request(comments_url)
            return comments_data
        except GitHubAPIError as e:
            logging.warning(f"Could not fetch comments for {comments_url}: {e}")
            return []
        except Exception as e:
            logging.warning(f"An unexpected error occurred while fetching comments for {comments_url}: {e}")
            return []

    def search_pull_requests_by_author(self, username: str, days_back: int) -> List[PullRequest]:
        """Search for pull requests authored by a user across all of GitHub."""
        since_date = datetime.now() - timedelta(days=days_back)
        since_str = since_date.strftime("%Y-%m-%d")
        
        # GitHub search API for PRs authored by user since a specific date
        url = f"https://api.github.com/search/issues?q=type:pr+author:{username}+created:>={since_str}&per_page=100"
        
        all_pull_requests = []
        
        while url:
            try:
                search_data = self._make_request(url)
                items = search_data.get('items', [])
                
                for pr_item in items:
                    # Extract PR details from search result
                    pr_number = pr_item["number"]
                    pr_url = pr_item["pull_request"]["url"]  # API URL
                    html_url = pr_item["pull_request"]["html_url"]  # Web URL
                    
                    # Get full PR details
                    pr_details = self._make_request(pr_url)
                    
                    # Fetch commit messages
                    commits_url = pr_url + "/commits"
                    commit_messages = []
                    try:
                        commits_data = self._make_request(commits_url)
                        for commit in commits_data:
                            commit_messages.append(commit["commit"]["message"])
                    except GitHubAPIError as e:
                        logging.warning(f"Could not fetch commits for PR {pr_number}: {e}")
                    
                    all_pull_requests.append(PullRequest(
                        id=pr_number,
                        title=pr_details["title"],
                        body=pr_details["body"],
                        url=html_url,
                        created_at=pr_details["created_at"],
                        commit_messages=commit_messages,
                        comments=[]
                    ))
                
                # Check for next page in search results
                response = requests.get(url, headers=self.headers)
                url = response.links.get('next', {}).get('url')
                
            except GitHubAPIError as e:
                logging.error(f"Failed to search for pull requests: {e}")
                break
            except Exception as e:
                logging.error(f"An unexpected error occurred while searching PRs: {e}")
                break
        
        return all_pull_requests

    def get_pull_requests(self, username: str, days_back: int) -> List[PullRequest]:
        """Fetch pull requests for a user from their public repositories from the last N days."""
        all_pull_requests = []
        since_date = datetime.now() - timedelta(days=days_back)

        public_repos = self.get_user_public_repos(username)
        if not public_repos:
            logging.info(f"No public repositories found for {username} or failed to fetch them.")
            return []

        for repo in public_repos:
            repo_owner = repo["owner"]["login"]
            repo_name = repo["name"]
            logging.info(f"Fetching PRs for repository: {repo_owner}/{repo_name}")

            # GitHub API for listing pull requests in a repository
            # state=all includes open, closed, and merged PRs
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls?state=all&per_page=100"
            
            while url:
                try:
                    prs_data = self._make_request(url)
                    for pr_item in prs_data:
                        # Filter by author and creation date
                        if pr_item["user"]["login"] == username and datetime.strptime(pr_item["created_at"], "%Y-%m-%dT%H:%M:%SZ") >= since_date:
                            pr_id = pr_item["number"]
                            pr_url = pr_item["url"]

                            # Fetch commit messages
                            commits_url = pr_url + "/commits"
                            commit_messages = []
                            try:
                                commits_data = self._make_request(commits_url)
                                for commit in commits_data:
                                    commit_messages.append(commit["commit"]["message"])
                            except GitHubAPIError as e:
                                logging.warning(f"Could not fetch commits for PR {pr_id} in {repo_owner}/{repo_name}: {e}")
                            except Exception as e:
                                logging.warning(f"An unexpected error occurred while fetching commits for PR {pr_id} in {repo_owner}/{repo_name}: {e}")

                            all_pull_requests.append(PullRequest(
                                id=pr_id,
                                title=pr_item["title"],
                                body=pr_item["body"],
                                url=pr_item["html_url"],
                                created_at=pr_item["created_at"],
                                commit_messages=commit_messages,
                                comments=[] # Comments are explicitly excluded
                            ))
                    # Check for next page
                    url = requests.get(url, headers=self.headers).links.get('next', {}).get('url')
                except GitHubAPIError as e:
                    logging.error(f"Failed to fetch pull requests for {repo_owner}/{repo_name}: {e}")
                    break # Move to next repository if there's an API error
                except Exception as e:
                    logging.error(f"An unexpected error occurred while fetching PRs for {repo_owner}/{repo_name}: {e}")
                    break # Move to next repository if there's an unexpected error
        return all_pull_requests
