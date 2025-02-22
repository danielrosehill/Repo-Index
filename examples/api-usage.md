# API Usage Examples

The repository data is available as JSON at:
`https://danielrosehill.github.io/Github-Timeline/data/exports/repo-index.json`

## Example: Fetch using curl
```bash
curl https://danielrosehill.github.io/Github-Timeline/data/exports/repo-index.json
```

## Example: Fetch using JavaScript
```javascript
// Using fetch
fetch('https://danielrosehill.github.io/Github-Timeline/data/exports/repo-index.json')
  .then(response => response.json())
  .then(data => console.log(data));

// Using axios
axios.get('https://danielrosehill.github.io/Github-Timeline/data/exports/repo-index.json')
  .then(response => console.log(response.data));
```

## Example: Fetch using Python
```python
import requests

# Fetch the repository data
response = requests.get('https://danielrosehill.github.io/Github-Timeline/data/exports/repo-index.json')
repos = response.json()

# Example: Print all non-fork repositories
for repo in repos:
    if not repo['is_fork']:
        print(f"Name: {repo['name']}")
        print(f"Description: {repo['description']}")
        print(f"URL: {repo['url']}")
        print("---")
```

## Data Structure

Each repository entry contains:
```json
{
  "name": "repo-name",
  "pretty_name": "Repository Name",
  "description": "Repository description",
  "url": "https://github.com/username/repo-name",
  "is_fork": false,
  "created_at": "2024-01-01T00:00:00Z"
}
```

## Categories

The repository data is also organized by categories. Each category's repositories can be accessed at:
`https://danielrosehill.github.io/Github-Timeline/lists/categories/{category-name}.txt`

Available categories:
- assistants
- backups
- context-rag
- data
- documentation
- emissions
- experiments
- forks
- home-assistant
- ideas
- indexes
- israel
- linux
- lists
- llm
- obsidian
- opensuse
- prompt-libraries
- templates
- utilities
- voice