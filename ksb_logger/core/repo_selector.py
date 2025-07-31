#!/usr/bin/env python3

import sys
import os
from typing import List, Dict, Any, Tuple
from rich.console import Console
import inquirer

console = Console()

def determine_default_analysis_type(repo: Dict[str, Any], username: str) -> str:
    """Determine the default analysis type for a repository based on contribution patterns."""
    # Simple heuristic: if it's your repo, default to commits; if it's an org repo, default to PRs
    is_owner = repo['owner']['login'] == username
    
    if is_owner:
        return 'commits'
    else:
        return 'PRs'

class RepoAnalysisChoice:
    """Represents a repository with its analysis method choice."""
    def __init__(self, repo: Dict[str, Any], username: str):
        self.repo = repo
        self.default_method = determine_default_analysis_type(repo, username)
        self.current_method = self.default_method
        self.cycle_state = 0  # 0=unselected, 1=default selected, 2=alt selected
    
    def cycle(self):
        """Cycle through the 3 states."""
        self.cycle_state = (self.cycle_state + 1) % 3
        if self.cycle_state == 2:  # Alternative selected
            self.current_method = 'PRs' if self.default_method == 'commits' else 'commits'
        else:  # Unselected or default selected
            self.current_method = self.default_method
    
    def is_selected(self) -> bool:
        return self.cycle_state in [1, 2]
    
    def get_display_text(self) -> str:
        """Get the display text for this choice."""
        repo_name = f"{self.repo['owner']['login']}/{self.repo['name']}"
        description = self.repo.get('description', '') or 'No description'
        
        # Truncate description if too long
        if len(description) > 40:
            description = description[:37] + "..."
        
        # Choose text based on current method (no icons)
        method_text = "com" if self.current_method == 'commits' else "PRs"
        
        return f"{method_text} • {repo_name} - {description}"

def select_repositories_interactive(repos: List[Dict[str, Any]]) -> List[Tuple[Dict[str, Any], str]]:
    """Interactive repository selection with analysis method choice."""
    if not repos:
        console.print("[yellow]No repositories found.[/yellow]")
        return []
    
    # Get username for determining defaults
    username = None
    for repo in repos:
        if repo.get('repo_type') == 'personal':
            username = repo['owner']['login']
            break
    
    if not username:
        # Fallback: use the first repo owner
        username = repos[0]['owner']['login']
    
    console.print("[bold cyan]Repository Selection[/bold cyan]")
    console.print("[dim]Select repositories. Default analysis method shown (personal repos: com, org repos: PRs)[/dim]\n")
    
    # Create repo choices with default methods
    repo_choices = [RepoAnalysisChoice(repo, username) for repo in repos]
    
    # Create display choices for inquirer
    choices = [(choice.get_display_text(), choice) for choice in repo_choices]
    
    questions = [
        inquirer.Checkbox(
            'selected_choices',
            message="Select repositories",
            choices=choices,
            default=[],
        ),
    ]
    
    # Increase display height
    original_lines = os.environ.get('LINES')
    os.environ['LINES'] = '30'
    
    try:
        answers = inquirer.prompt(questions)
    finally:
        if original_lines:
            os.environ['LINES'] = original_lines
        else:
            os.environ.pop('LINES', None)
    
    if not answers or not answers['selected_choices']:
        console.print("[yellow]No repositories selected. Exiting.[/yellow]")
        return []
    
    selected_choices = answers['selected_choices']
    
    # Show confirmation
    console.print(f"\n[green]✓ Selected {len(selected_choices)} repositories:[/green]")
    for choice in selected_choices:
        method_desc = "commit analysis" if choice.current_method == 'commits' else "PR analysis"
        console.print(f"  • {choice.repo['owner']['login']}/{choice.repo['name']} ({method_desc})")
    console.print()
    
    # Return tuples of (repo, analysis_method)
    return [(choice.repo, choice.current_method) for choice in selected_choices]

if __name__ == "__main__":
    # Test with dummy data
    dummy_repos = [
        {"name": "test-repo-1", "owner": {"login": "user"}, "description": "A test repository"},
        {"name": "test-repo-2", "owner": {"login": "user"}, "description": "Another test repository"},
    ]
    selected = select_repositories_interactive(dummy_repos)
    print(f"Selected: {[r['name'] for r in selected]}")