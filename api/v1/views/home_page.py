# main.py
#!/usr/bin/python3
from flask import jsonify, render_template
import requests
from api.v1.views import app_views
cache = {}  # Global cache for storing the data

@app_views.route("/", methods=["GET"])
def landing():
    return render_template("landing.html")

@app_views.route("/homepage", methods=["GET"])
def fetch_github_trending():
    if "trending_data" in cache:
        return cache["trending_data"]  # Return cached data if available
    url_repos = "https://api.github.com/search/repositories?q=stars:>1&sort=stars&order=desc&per_page=3"
    repos_req = requests.get(url_repos)
    if repos_req.status_code == 200:
        repos_data = repos_req.json().get("items", [])
        repos = [{
            "name": repo["name"],
            "description": (repo["description"][:55] + "...") if repo["description"] and len(repo["description"]) > 55 else repo["description"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "language": repo["language"]
        } for repo in repos_data]
        developers = [
            {"name": "Linus Torvalds"},
            {"name": "Jake Wharton"},
            {"name": "Evan You"}
        ]
        rendered_template = render_template("home_page.html", repos=repos, developers=developers)
        cache["trending_data"] = rendered_template
        return rendered_template
    return jsonify({"error": "Failed to fetch data from GitHub"}), 500
