import requests
import logging
from datetime import datetime
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors."""
    pass

class PullRequest:
    def __init__(self, id: int, title: str, body: str, url: str, created_at: str, commit_messages: List[str], comments: List[Dict[str, Any]] = [], file_changes: List[Dict[str, Any]] = []):
        self.id = id
        self.title = title
        self.body = body
        self.url = url
        self.created_at = created_at
        self.commit_messages = commit_messages
        self.comments = comments
        self.file_changes = file_changes  # New field for storing file diffs and changes

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

    def get_pr_file_changes(self, pr_api_url: str) -> List[Dict[str, Any]]:
        """Fetch file changes for a specific PR."""
        files_url = pr_api_url + "/files"
        try:
            files_data = self._make_request(files_url)
            
            file_changes = []
            for file_info in files_data:
                # Extract key information about each changed file
                file_change = {
                    'filename': file_info.get('filename', ''),
                    'status': file_info.get('status', ''),  # added, modified, deleted, renamed
                    'additions': file_info.get('additions', 0),
                    'deletions': file_info.get('deletions', 0),
                    'changes': file_info.get('changes', 0),
                    'patch': file_info.get('patch', ''),  # The actual diff
                    'language': self._detect_language_from_filename(file_info.get('filename', ''))
                }
                file_changes.append(file_change)
            
            return file_changes
        except GitHubAPIError as e:
            logging.warning(f"Could not fetch file changes for PR {pr_api_url}: {e}")
            return []
        except Exception as e:
            logging.warning(f"An unexpected error occurred while fetching file changes for PR {pr_api_url}: {e}")
            return []

    def _detect_language_from_filename(self, filename: str) -> str:
        """Detect programming language from file extension."""
        if not filename:
            return 'text'
        
        extension = filename.split('.')[-1].lower() if '.' in filename else ''
        
        language_map = {
            'js': 'javascript',
            'jsx': 'javascript',
            'ts': 'typescript',
            'tsx': 'typescript', 
            'py': 'python',
            'java': 'java',
            'cpp': 'cpp',
            'c': 'c',
            'cs': 'csharp',
            'php': 'php',
            'rb': 'ruby',
            'go': 'go',
            'rs': 'rust',
            'sh': 'bash',
            'sql': 'sql',
            'html': 'html',
            'css': 'css',
            'scss': 'scss',
            'sass': 'sass',
            'json': 'json',
            'xml': 'xml',
            'yaml': 'yaml',
            'yml': 'yaml',
            'md': 'markdown',
            'dockerfile': 'dockerfile'
        }
        
        return language_map.get(extension, 'text')

    def get_commit_file_changes(self, repo_owner: str, repo_name: str, commit_sha: str) -> List[Dict[str, Any]]:
        """Fetch file changes for a specific commit."""
        commit_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{commit_sha}"
        try:
            commit_data = self._make_request(commit_url)
            files = commit_data.get('files', [])
            
            file_changes = []
            for file_info in files:
                file_change = {
                    'filename': file_info.get('filename', ''),
                    'status': file_info.get('status', ''),
                    'additions': file_info.get('additions', 0),
                    'deletions': file_info.get('deletions', 0),
                    'changes': file_info.get('changes', 0),
                    'patch': file_info.get('patch', ''),
                    'language': self._detect_language_from_filename(file_info.get('filename', ''))
                }
                file_changes.append(file_change)
            
            return file_changes
        except GitHubAPIError as e:
            logging.warning(f"Could not fetch file changes for commit {commit_sha}: {e}")
            return []
        except Exception as e:
            logging.warning(f"An unexpected error occurred while fetching file changes for commit {commit_sha}: {e}")
            return []

    def get_user_public_repos(self, username: str) -> List[Dict[str, Any]]:
        logging.info(f"Fetching all repositories for {username}")
        url = f"https://api.github.com/users/{username}/repos?type=all&per_page=100"
        repos = []
        while url:
            try:
                data = self._make_request(url)
                repos.extend(data)
                url = requests.get(url, headers=self.headers).links.get('next', {}).get('url')
            except GitHubAPIError as e:
                logging.error(f"Failed to fetch repositories for {username}: {e}")
                return []
            except Exception as e:
                logging.error(f"An unexpected error occurred while fetching repositories for {username}: {e}")
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

    def search_pull_requests_by_author(self, username: str) -> List[PullRequest]:
        """Search for pull requests authored by a user across all of GitHub."""
        
        # GitHub search API for PRs authored by user
        url = f"https://api.github.com/search/issues?q=type:pr+author:{username}&per_page=100"
        
        all_pull_requests = []
        page_num = 1
        
        logging.info(f"Starting search for PRs authored by {username}")
        
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
                    
                    # Fetch file changes
                    file_changes = self.get_pr_file_changes(pr_url)
                    
                    all_pull_requests.append(PullRequest(
                        id=pr_number,
                        title=pr_details["title"],
                        body=pr_details["body"],
                        url=html_url,
                        created_at=pr_details["created_at"],
                        commit_messages=commit_messages,
                        comments=[],
                        file_changes=file_changes
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


    def search_pull_requests_by_author_filtered(self, username: str, selected_repos: List[Dict[str, Any]]) -> List[PullRequest]:
        """Search for pull requests authored by a user, filtered to specific repositories."""
        
        # Create a set of selected repository names for efficient lookup
        selected_repo_names = {f"{repo['owner']['login']}/{repo['name']}" for repo in selected_repos}
        
        # Build search query with repository filter - GitHub search supports multiple repo: filters
        repo_filters = " ".join([f"repo:{repo['owner']['login']}/{repo['name']}" for repo in selected_repos])
        query = f"type:pr author:{username} {repo_filters}"
        url = f"https://api.github.com/search/issues?q={query}&per_page=100"
        
        all_pull_requests = []
        page_num = 1
        
        logging.info(f"Searching for PRs authored by {username} in {len(selected_repos)} selected repositories")
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
                    
                    # Fetch file changes
                    file_changes = self.get_pr_file_changes(pr_url)
                    
                    all_pull_requests.append(PullRequest(
                        id=pr_number,
                        title=pr_details["title"],
                        body=pr_details["body"],
                        url=html_url,
                        created_at=pr_details["created_at"],
                        commit_messages=commit_messages,
                        comments=[],
                        file_changes=file_changes
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
        
        # 1. Get all personal repositories (public + private)
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
        
        # 3. Convert to list and sort by created_at (newest first)  
        repo_list = list(all_repos.values())
        repo_list.sort(key=lambda r: r.get('created_at', ''), reverse=True)
        
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
        
        return interleaved_repos

    def get_pull_requests(self, username: str) -> List[PullRequest]:
        """Fetch pull requests for a user from all their repositories."""
        all_pull_requests = []

        all_repos = self.get_user_public_repos(username)
        if not all_repos:
            logging.info(f"No repositories found for {username} or failed to fetch them.")
            return []

        for repo in all_repos:
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
                        # Filter by author only
                        if pr_item["user"]["login"] == username:
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

    def get_commits_by_author(self, username: str, selected_repos: List[Dict[str, Any]]) -> List[PullRequest]:
        """Fetch commits authored by a user from selected repositories, grouped as pseudo-PRs."""
        all_commits = []
        
        logging.info(f"Fetching commits authored by {username} from {len(selected_repos)} selected repositories...")
        
        for repo in selected_repos:
            repo_owner = repo['owner']['login']
            repo_name = repo['name']
            repo_full_name = f"{repo_owner}/{repo_name}"
            
            logging.info(f"Fetching commits from {repo_full_name}...")
            
            # GitHub API for listing commits in a repository
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?author={username}&per_page=100"
            
            repo_commits = []
            page_num = 1
            
            while url:
                try:
                    logging.info(f"Fetching page {page_num} of commits from {repo_full_name}...")
                    commits_data = self._make_request(url)
                    
                    if not commits_data:
                        break
                        
                    logging.info(f"Found {len(commits_data)} commits on page {page_num}")
                    
                    for commit in commits_data:
                        # Only include commits where the user is the author
                        if commit.get('author') and commit['author'].get('login') == username:
                            repo_commits.append({
                                'sha': commit['sha'],
                                'message': commit['commit']['message'],
                                'date': commit['commit']['author']['date'],
                                'url': commit['html_url']
                            })
                    
                    # Check for next page
                    response = requests.get(url, headers=self.headers)
                    url = response.links.get('next', {}).get('url')
                    page_num += 1
                    
                except GitHubAPIError as e:
                    logging.error(f"Failed to fetch commits from {repo_full_name}: {e}")
                    break
                except Exception as e:
                    logging.error(f"An unexpected error occurred while fetching commits from {repo_full_name}: {e}")
                    break
            
            if repo_commits:
                # Group commits into a single "pseudo-PR" for each repository
                commit_messages = [commit['message'] for commit in repo_commits]
                latest_commit = repo_commits[0] if repo_commits else None
                
                # Collect file changes from all commits (limited to avoid too much data)
                all_file_changes = []
                for commit in repo_commits[:5]:  # Limit to first 5 commits to avoid huge data
                    commit_file_changes = self.get_commit_file_changes(repo_owner, repo_name, commit['sha'])
                    all_file_changes.extend(commit_file_changes)
                
                # Create a pseudo-PR object representing all commits from this repo
                # Use repo ID + large offset to avoid conflicts with actual PR IDs
                pseudo_pr = PullRequest(
                    id=repo['id'] + 100000000,  # Add 100M to ensure uniqueness
                    title=f"Commits from {repo_full_name} ({len(repo_commits)} commits)",
                    body=f"Collection of {len(repo_commits)} commits from repository {repo_full_name}",
                    url=latest_commit['url'] if latest_commit else f"https://github.com/{repo_full_name}",
                    created_at=latest_commit['date'] if latest_commit else repo.get('created_at', ''),
                    commit_messages=commit_messages,
                    comments=[],
                    file_changes=all_file_changes
                )
                
                all_commits.append(pseudo_pr)
                logging.info(f"Created pseudo-PR for {repo_full_name} with {len(repo_commits)} commits")
        
        logging.info(f"Completed commit fetching. Created {len(all_commits)} pseudo-PRs from commit analysis.")
        return all_commits
