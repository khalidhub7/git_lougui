# main.py
#!/usr/bin/python3
from flask import jsonify, render_template
import requests
from api.v1.views import app_views

cache = {}  # Global cache for storing the data

@app_views.route("/homepage", methods=["GET"])
def fetch_github_trending():
    if "trending_data" in cache:  # Check if data is cached
        return cache["trending_data"]  # Return cached data if available
    
    # GitHub API to get the top trending repositories
    url_repos = "https://api.github.com/search/repositories?q=stars:>1&sort=stars&order=desc&per_page=3"
    repos_req = requests.get(url_repos)
    
    if repos_req.status_code == 200:  # Successful API response
        repos_data = repos_req.json().get("items", [])
        
        # Parse repository data and trim descriptions longer than 55 characters
        repos = [{
            "name": repo["name"],
            "description": (repo["description"][:55] + "...") if repo["description"] and len(repo["description"]) > 55 else repo["description"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "language": repo["language"]
        } for repo in repos_data]
        
        # Hardcoded developer data (static)
        developers = [
            {"name": "Linus Torvalds"},
            {"name": "Jake Wharton"},
            {"name": "Evan You"}
        ]
        
        # Render the template with repository and developer data
        rendered_template = render_template("home_page.html", repos=repos, developers=developers)
        cache["trending_data"] = rendered_template  # Cache the rendered template
        return rendered_template
    
    # Return an error message if the GitHub API request fails
    return jsonify({"error": "Failed to fetch data from GitHub"}), 500
