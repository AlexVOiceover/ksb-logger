#!/usr/bin/env python3

import sys
from typing import List, Dict, Any
import inquirer
from rich.console import Console
from rich import print as rprint

console = Console()

def select_repositories_interactive(repos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Interactive repository selection using arrow keys and spacebar (like Vite)."""
    if not repos:
        console.print("[yellow]No repositories found.[/yellow]")
        return []
    
    # Prepare choices for inquirer
    choices = []
    for repo in repos:
        repo_name = f"{repo['owner']['login']}/{repo['name']}"
        description = repo.get('description', '') or 'No description'
        
        # Truncate description if too long
        if len(description) > 50:
            description = description[:47] + "..."
        
        # Format: "owner/repo - description"
        display_name = f"{repo_name} - {description}"
        choices.append((display_name, repo))
    
    try:
        # Show interactive checkbox selection
        console.print("[bold cyan]Select repositories to include in portfolio[/bold cyan]")
        console.print("[dim]Use ↑↓ to navigate, SPACE to toggle, ENTER to confirm[/dim]\n")
        
        questions = [
            inquirer.Checkbox(
                'selected_repos',
                message="Select repositories",
                choices=choices,
                default=[],  # None selected by default
            ),
        ]
        
        answers = inquirer.prompt(questions)
        
        if not answers or not answers['selected_repos']:
            console.print("[yellow]No repositories selected. Exiting.[/yellow]")
            sys.exit(0)
        
        selected_repos = answers['selected_repos']
        
        # Show confirmation
        console.print(f"\n[green]✓ Selected {len(selected_repos)} repositories:[/green]")
        for repo in selected_repos:
            console.print(f"  • {repo['owner']['login']}/{repo['name']}")
        console.print()
        
        return selected_repos
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Selection cancelled.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error during selection: {e}[/red]")
        console.print("[yellow]Falling back to all repositories.[/yellow]")
        return repos

if __name__ == "__main__":
    # Test with dummy data
    dummy_repos = [
        {"name": "test-repo-1", "owner": {"login": "user"}, "description": "A test repository"},
        {"name": "test-repo-2", "owner": {"login": "user"}, "description": "Another test repository"},
    ]
    selected = select_repositories_interactive(dummy_repos)
    print(f"Selected: {[r['name'] for r in selected]}")