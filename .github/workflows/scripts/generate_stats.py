#!/usr/bin/env python3
"""
GitHub Stats Generator
Fetches and updates GitHub statistics in README
"""

import requests
import json
from datetime import datetime
import os
import re

USERNAME = "Anujkumar1407"
GITHUB_API = "https://api.github.com"
README_FILE = "README.md"

def get_user_stats(username):
    """Fetch user statistics from GitHub API"""
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    # Get user info
    user_response = requests.get(f"{GITHUB_API}/users/{username}", headers=headers)
    user_data = user_response.json()
    
    # Get repositories
    repos_response = requests.get(f"{GITHUB_API}/users/{username}/repos?per_page=100", headers=headers)
    repos_data = repos_response.json()
    
    # Calculate stats
    total_repos = len(repos_data)
    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
    
    # Get language breakdown
    languages = {}
    for repo in repos_data:
        if repo.get("language"):
            languages[repo["language"]] = languages.get(repo["language"], 0) + 1
    
    return {
        "followers": user_data.get("followers", 0),
        "public_repos": user_data.get("public_repos", 0),
        "total_stars": total_stars,
        "languages": languages,
        "bio": user_data.get("bio", ""),
        "location": user_data.get("location", "")
    }

def generate_stats_section(stats):
    """Generate markdown stats section"""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    
    # Generate language breakdown
    lang_breakdown = ""
    if stats["languages"]:
        total_lang_repos = sum(stats["languages"].values())
        for lang, count in sorted(stats["languages"].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_lang_repos) * 100
            lang_breakdown += f"- **{lang}** - {percentage:.1f}%\n"
    
    stats_section = f"""## 📊 GitHub Stats & Language Usage

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=Anujkumar1407&theme=tokyonight&show_icons=true&hide_border=true&count_private=true&bg_color=1a1b26)

![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=Anujkumar1407&theme=tokyonight&layout=pie&hide_border=true&bg_color=1a1b26)

### GitHub Statistics
- 👥 **Followers:** {stats['followers']}
- 📦 **Public Repositories:** {stats['public_repos']}
- ⭐ **Total Stars:** {stats['total_stars']}

### Language Breakdown
{lang_breakdown}
*Last updated: {timestamp}*
"""
    return stats_section

def update_readme(stats_section):
    """Update README.md with new stats section"""
    if not os.path.exists(README_FILE):
        print(f"Error: {README_FILE} not found")
        return False
    
    with open(README_FILE, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Replace the stats section
    pattern = r'## 📊 GitHub Stats & Language Usage.*?(?=\n---\n|\n## |$)'
    
    new_readme = re.sub(pattern, stats_section.rstrip(), readme_content, flags=re.DOTALL)
    
    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.write(new_readme)
    
    print(f"✅ Updated {README_FILE} with new stats")
    return True

if __name__ == "__main__":
    print(f"Fetching stats for {USERNAME}...")
    try:
        stats = get_user_stats(USERNAME)
        
        print("\n=== GitHub Statistics ===")
        print(f"Followers: {stats['followers']}")
        print(f"Public Repos: {stats['public_repos']}")
        print(f"Total Stars: {stats['total_stars']}")
        print(f"Languages: {stats['languages']}")
        
        # Generate and update stats section
        stats_section = generate_stats_section(stats)
        update_readme(stats_section)
        
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
