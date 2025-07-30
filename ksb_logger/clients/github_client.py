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
        page_num = 1
        
        logging.info(f"Starting search for PRs authored by {username} since {since_str}")
        
        while url:
            try:
                logging.info(f"Fetching page {page_num} of search results...")
                search_data = self._make_request(url)
                items = search_data.get('items', [])
                total_count = search_data.get('total_count', 0)
                
                logging.info(f"Found {len(items)} PRs on page {page_num} (total available: {total_count})")
                
                for i, pr_item in enumerate(items, 1):
                    # Extract PR details from search result
                    pr_number = pr_item["number"]
                    pr_url = pr_item["pull_request"]["url"]  # API URL
                    html_url = pr_item["pull_request"]["html_url"]  # Web URL
                    repo_name = pr_item.get("repository_url", "").split("/")[-1] if pr_item.get("repository_url") else "unknown"
                    
                    logging.info(f"Processing PR {i}/{len(items)}: #{pr_number} in {repo_name}")
                    
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
                page_num += 1
                
            except GitHubAPIError as e:
                logging.error(f"Failed to search for pull requests: {e}")
                break
            except Exception as e:
                logging.error(f"An unexpected error occurred while searching PRs: {e}")
                break
        
        return all_pull_requests

    def get_repositories_with_prs(self, username: str, days_back: int) -> List[Dict[str, Any]]:
        """Get a list of repositories where the user has PRs, without fetching full PR details."""
        since_date = datetime.now() - timedelta(days=days_back)
        since_str = since_date.strftime("%Y-%m-%d")
        
        # Quick search to find repositories (just get first page for speed)
        url = f"https://api.github.com/search/issues?q=type:pr+author:{username}+created:>={since_str}&per_page=100"
        
        try:
            logging.info("Doing quick search to find repositories with your PRs...")
            search_data = self._make_request(url)
            items = search_data.get('items', [])
            
            if not items:
                return []
            
            # Extract unique repositories
            repo_urls = set()
            for pr_item in items:
                repo_url = pr_item.get("repository_url", "")
                if repo_url:
                    repo_urls.add(repo_url)
            
            # Get repository details
            repos_with_prs = []
            for repo_url in repo_urls:
                try:
                    repo_data = self._make_request(repo_url)
                    repos_with_prs.append(repo_data)
                except GitHubAPIError as e:
                    logging.warning(f"Could not fetch details for repository {repo_url}: {e}")
            
            logging.info(f"Found {len(repos_with_prs)} repositories:")
            for repo in repos_with_prs:
                logging.info(f"  - {repo['owner']['login']}/{repo['name']}")
            
            return repos_with_prs
            
        except GitHubAPIError as e:
            logging.error(f"Failed to search for repositories: {e}")
            return []
        except Exception as e:
            logging.error(f"An unexpected error occurred while searching repositories: {e}")
            return []

    def search_pull_requests_by_author_filtered(self, username: str, days_back: int, selected_repos: List[Dict[str, Any]]) -> List[PullRequest]:
        """Search for pull requests authored by a user, filtered to specific repositories."""
        since_date = datetime.now() - timedelta(days=days_back)
        since_str = since_date.strftime("%Y-%m-%d")
        
        # Create a set of selected repository names for efficient lookup
        selected_repo_names = {f"{repo['owner']['login']}/{repo['name']}" for repo in selected_repos}
        
        # Build search query with repository filter - GitHub search supports multiple repo: filters
        repo_filters = " ".join([f"repo:{repo['owner']['login']}/{repo['name']}" for repo in selected_repos])
        query = f"type:pr author:{username} created:>={since_str} {repo_filters}"
        url = f"https://api.github.com/search/issues?q={query}&per_page=100"
        
        all_pull_requests = []
        page_num = 1
        
        logging.info(f"Searching for PRs authored by {username} since {since_str} in {len(selected_repos)} selected repositories")
        logging.info(f"Search query: {query}")
        
        while url:
            try:
                logging.info(f"Fetching page {page_num} of filtered search results...")
                search_data = self._make_request(url)
                items = search_data.get('items', [])
                total_count = search_data.get('total_count', 0)
                
                logging.info(f"Found {len(items)} PRs on page {page_num} (total available: {total_count})")
                
                for i, pr_item in enumerate(items, 1):
                    # Extract PR details from search result
                    pr_number = pr_item["number"]
                    pr_url = pr_item["pull_request"]["url"]  # API URL
                    html_url = pr_item["pull_request"]["html_url"]  # Web URL
                    repo_name = pr_item.get("repository_url", "").split("/")[-2:] 
                    repo_full_name = "/".join(repo_name[-2:]) if len(repo_name) >= 2 else "unknown"
                    
                    # Double-check that this PR is from a selected repository
                    if repo_full_name not in selected_repo_names:
                        logging.debug(f"Skipping PR #{pr_number} from unselected repo {repo_full_name}")
                        continue
                    
                    logging.info(f"Processing PR {i}/{len(items)}: #{pr_number} in {repo_full_name}")
                    
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
                page_num += 1
                
            except GitHubAPIError as e:
                logging.error(f"Failed to search for filtered pull requests: {e}")
                break
            except Exception as e:
                logging.error(f"An unexpected error occurred while searching filtered PRs: {e}")
                break
        
        logging.info(f"Completed filtered search. Found {len(all_pull_requests)} PRs from selected repositories.")
        return all_pull_requests

    def get_all_user_repositories(self, username: str) -> List[Dict[str, Any]]:
        """Get ALL repositories where the user has activity (personal + organization), sorted newest to oldest."""
        all_repos = {}  # Use dict to deduplicate by repo ID
        
        logging.info(f"Fetching all repositories where {username} has activity...")
        
        # 1. Get personal public repositories  
        try:
            personal_repos = self.get_user_public_repos(username)
            for repo in personal_repos:
                repo['repo_type'] = 'personal'
                all_repos[repo['id']] = repo
            logging.info(f"Found {len(personal_repos)} personal repositories")
        except GitHubAPIError as e:
            logging.warning(f"Could not fetch personal repositories: {e}")
        
        # 2. Find organization repositories by searching for user's activity
        try:
            # Search for repositories where user has activity (commits, PRs, issues)
            search_queries = [
                f"author:{username}",  # Repositories where user has commits
                f"committer:{username}",  # Repositories where user committed
            ]
            
            for query in search_queries:
                url = f"https://api.github.com/search/repositories?q={query}&per_page=100&sort=updated&order=desc"
                
                try:
                    search_data = self._make_request(url)
                    items = search_data.get('items', [])
                    
                    for repo in items:
                        # Skip if it's owned by the user (already got personal repos)
                        if repo['owner']['login'] != username:
                            repo['repo_type'] = 'organization'
                            all_repos[repo['id']] = repo
                    
                    logging.info(f"Search query '{query}' found {len(items)} additional repositories")
                    
                except GitHubAPIError as e:
                    logging.warning(f"Search query '{query}' failed: {e}")
            
            # Also search for repositories via PR search to find repos where user only has PRs
            try:
                pr_search_url = f"https://api.github.com/search/issues?q=type:pr+author:{username}&per_page=100"
                pr_search_data = self._make_request(pr_search_url)
                pr_items = pr_search_data.get('items', [])
                
                # Extract unique repositories from PR search
                pr_repo_urls = set()
                for pr_item in pr_items:
                    repo_url = pr_item.get('repository_url', '')
                    if repo_url:
                        pr_repo_urls.add(repo_url)
                
                # Fetch repository details for repos found via PR search
                for repo_url in pr_repo_urls:
                    try:
                        repo_data = self._make_request(repo_url)
                        if repo_data['owner']['login'] != username:  # Skip personal repos
                            repo_data['repo_type'] = 'organization'
                            all_repos[repo_data['id']] = repo_data
                    except GitHubAPIError as e:
                        logging.warning(f"Could not fetch repository details for {repo_url}: {e}")
                
                logging.info(f"PR search found {len(pr_repo_urls)} additional repositories")
                
            except GitHubAPIError as e:
                logging.warning(f"PR search failed: {e}")
        
        except Exception as e:
            logging.warning(f"Could not search for organization repositories: {e}")
        
        # 3. Convert to list and sort by updated_at (newest first)  
        repo_list = list(all_repos.values())
        repo_list.sort(key=lambda r: r.get('updated_at', ''), reverse=True)
        
        # 4. Separate and interleave personal vs organization repos
        personal_repos = [r for r in repo_list if r.get('repo_type') == 'personal']
        org_repos = [r for r in repo_list if r.get('repo_type') == 'organization']
        
        # Interleave: personal, org, personal, org, etc.
        interleaved_repos = []
        max_len = max(len(personal_repos), len(org_repos))
        
        for i in range(max_len):
            if i < len(personal_repos):
                interleaved_repos.append(personal_repos[i])
            if i < len(org_repos):
                interleaved_repos.append(org_repos[i])
        
        logging.info(f"Total repositories found: {len(interleaved_repos)} ({len(personal_repos)} personal, {len(org_repos)} organization)")
        for repo in interleaved_repos[:5]:  # Log first 5 for verification
            logging.info(f"  - {repo['owner']['login']}/{repo['name']} ({repo.get('repo_type', 'unknown')})")
        
        return interleaved_repos

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
