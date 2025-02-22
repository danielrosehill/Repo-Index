import os
import requests
from dotenv import load_dotenv
from datetime import datetime
from collections import defaultdict

def generate_timeline():
    load_dotenv()
    github_token = os.getenv("GITHUB_PAT")
    if not github_token:
        print("Error: GITHUB_PAT not found in .env file")
        return

    username = "danielrosehill"  # Replace with your GitHub username
    markdown_file = "README.md"
    start_placeholder = "<!-- GITHUB_TIMELINE_START -->"
    end_placeholder = "<!-- GITHUB_TIMELINE_END -->"

    # Dictionary for expanding abbreviations
    abbreviations = {
        "HA": "Home Assistant",
        "LLM": "Large Language Model",
        "GPT": "Generative Pre-trained Transformer",
        "AI": "Artificial Intelligence",
        "STT": "Speech to Text",
        "TTS": "Text to Speech",
        "RAG": "Retrieval Augmented Generation",
    }

    # Dictionary for category emojis
    category_emojis = {
        "AI": "🤖",
        "LLM": "🤖",
        "GPT": "🤖",
        "Home Assistant": "🏠",
        "Docker": "🐳",
        "Linux": "🐧",
        "Documentation": "📚",
        "Template": "📋",
        "Backup": "💾",
        "Script": "📜",
        "Data": "📊",
        "Security": "🔒",
        "API": "🔌",
    }

    def get_category_emoji(name, description):
        """Get relevant emoji based on repository name and description"""
        emojis = set()
        text = f"{name} {description}".lower()
        
        for keyword, emoji in category_emojis.items():
            if keyword.lower() in text:
                emojis.add(emoji)
        
        return " ".join(emojis) + " " if emojis else ""

    def prettify_repo_name(name):
        # Split by hyphens and process each word
        words = name.split('-')
        processed_words = []
        
        for word in words:
            # Check if the word is an abbreviation that needs expansion
            if word.upper() in abbreviations:
                processed_words.append(abbreviations[word.upper()])
            else:
                # Capitalize the word
                processed_words.append(word.capitalize())
        
        return ' '.join(processed_words)

    # Function to fetch all repositories with pagination
    def get_all_repos(username, token):
        repos = []
        page = 1
        while True:
            url = f"https://api.github.com/users/{username}/repos?sort=created&direction=desc&page={page}"
            headers = {"Authorization": f"token {token}"}
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                new_repos = response.json()
                if not new_repos:
                    break  # No more repos to fetch
                repos.extend(new_repos)
                page += 1
            else:
                print(f"Error fetching repos: {response.status_code}")
                return None
        return repos

    # Fetch all current repositories
    all_repos = get_all_repos(username, github_token)
    if not all_repos:
        return

    # Count repositories by year
    repos_by_year = defaultdict(int)
    public_repos = [repo for repo in all_repos if not repo["private"]]
    for repo in public_repos:
        year = datetime.strptime(repo["created_at"], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y")
        repos_by_year[year] += 1

    # Generate table of contents
    timeline_content = "\n### Timeline Overview\n\n"
    timeline_content += f"Total Public Repositories: {len(public_repos)}\n\n"
    timeline_content += "Jump to Year:\n"
    for year in sorted(repos_by_year.keys(), reverse=True):
        timeline_content += f"- [{year}](#{year}) ({repos_by_year[year]} repositories)\n"
    timeline_content += "\n---\n\n"

    # Generate timeline content
    # Note: This completely regenerates the timeline each time,
    # so deleted repositories will automatically be removed
    last_date = None
    last_year = None
    for repo in all_repos:
        if repo["private"]:
            continue  # Skip private repositories

        repo_name = repo["name"]
        pretty_name = prettify_repo_name(repo_name)
        repo_description = repo["description"] or "No description provided"
        repo_url = repo["html_url"]
        is_fork = repo["fork"]
        created_at = datetime.strptime(repo["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        date_str = created_at.strftime("%d %b %Y")
        year = created_at.strftime("%Y")

        # Write year if it's a new year
        if year != last_year:
            if last_year is not None:
                timeline_content += "---\n\n"  # Horizontal line between years
            timeline_content += f"# {year}\n\n"
            last_year = year

        # Write date if it's a new date
        if date_str != last_date:
            timeline_content += f"## {created_at.strftime('%d %b')}\n\n"
        last_date = date_str

        # Get category emoji
        category_emoji = get_category_emoji(repo_name, repo_description)

        # Write repository information with badge on a new line
        timeline_content += f"### {category_emoji}{pretty_name}"
        if is_fork:
            timeline_content += " (Fork)"  # Fork indicator in brackets
        timeline_content += "\n"
        timeline_content += f"{repo_description}\n\n"
        timeline_content += f"[![View on GitHub](https://img.shields.io/badge/View_on-GitHub-blue)]({repo_url})\n\n"

    # Read the existing README.md file
    try:
        with open(markdown_file, "r") as f:
            readme_content = f.readlines()
    except FileNotFoundError:
        print("Error: README.md not found")
        return

    # Find the start and end placeholders
    start_index = -1
    end_index = -1
    for i, line in enumerate(readme_content):
        if start_placeholder in line:
            start_index = i
        if end_placeholder in line:
            end_index = i

    if start_index == -1 or end_index == -1:
        print("Error: Start or end placeholder not found in README.md")
        return

    # Update the README.md content with the new timeline
    # This replaces everything between the placeholders with the new content,
    # effectively removing any repositories that no longer exist
    updated_readme_content = readme_content[:start_index + 1]
    updated_readme_content.append(timeline_content)
    updated_readme_content.extend(readme_content[end_index:])

    # Write the updated content back to README.md
    with open(markdown_file, "w") as f:
        f.writelines(updated_readme_content)

if __name__ == "__main__":
    generate_timeline()