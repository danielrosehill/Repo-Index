Your task is to generate a script which will be used to generate and update a Github repository which will serve as a chronological list of (public) Github repositories that I have created (starting with the newest ones and continuing to the oldest ones).

The script should be designed with the assumption that it will be run repetitively in order to update the index without creating duplicate or redundant data. The script can use a GitHub token which will be provided as a .env value GITHUB_PAT. 

It should write its data to the markdown file in this format. The values describe the entries for each repository. There should be an empty line between repositories.

## 22 Feb 2025

Repository 1 Name
Repository Description
Github view repo badge linking to repo


## Other Instructions

- Dates are only added if repositories were created on that day. 
- Only public repositories are included in the index. 
- The list of repositories is large > 800 so so pagination method may be necessary when working with the github api