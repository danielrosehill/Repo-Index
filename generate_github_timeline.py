import os
import requests
from dotenv import load_dotenv
from datetime import datetime

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

    all_repos = get_all_repos(username, github_token)
    if not all_repos:
        return

    timeline_content = "\n"  # Start with a newline for clean formatting
    last_date = None
    for repo in all_repos:
        if repo["private"]:
            continue  # Skip private repositories

        repo_name = repo["name"]
        repo_description = repo["description"] or "No description provided"
        repo_url = repo["html_url"]
        created_at = datetime.strptime(repo["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        date_str = created_at.strftime("%d %b %Y")

        # Write date if it's a new date
        if date_str != last_date:
            timeline_content += f"## {date_str}\n\n"
        last_date = date_str

        # Write repository information with badge on a new line after description
        timeline_content += f"### {repo_name}\n"
        timeline_content += f"{repo_description}\n\n"  # Add extra newline here
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
    updated_readme_content = readme_content[:start_index + 1]
    updated_readme_content.append(timeline_content)
    updated_readme_content.extend(readme_content[end_index:])

    # Write the updated content back to README.md
    with open(markdown_file, "w") as f:
        f.writelines(updated_readme_content)

if __name__ == "__main__":
    generate_timeline()