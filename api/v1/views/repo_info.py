from flask import render_template, abort
import requests
import cachetools
from markdown2 import markdown
from api.v1.views import app_views

cache = cachetools.TTLCache(maxsize=100, ttl=300)

@app_views.route("/<username>/<repo_name>", methods=["GET"])
def repo_info(username, repo_name):
    cache_key = f"{username}/{repo_name}"
    
    if cache_key in cache:
        repo_info = cache[cache_key]
    else:
        repo_info = fetch_repo_info(username, repo_name)
        if not repo_info:
            abort(404, description="Repository not found")
        cache[cache_key] = repo_info

    return render_template('repo_info.html', repo_info=repo_info)

def fetch_repo_info(username, repo_name):
    base_url = f"https://api.github.com/repos/{username}/{repo_name}"
    headers = {"Accept": "application/vnd.github.v3.raw"}
    
    repo_info = {}
    
    try:
        repo_data = requests.get(base_url).json()
        if "message" in repo_data:
            return None
        
        issues_data = requests.get(f"{base_url}/issues").json()
        pulls_data = requests.get(f"{base_url}/pulls").json()
        contributors_data = requests.get(f"{base_url}/contributors").json()
        readme_data = requests.get(f"{base_url}/readme", headers=headers).text

        readme_html = markdown(readme_data) if readme_data else "<p>No README available.</p>"

        repo_info = {
            'name': repo_data.get('name', 'Unknown Repo'),
            'description': repo_data.get('description', 'No description'),
            'issues': [{'title': issue['title'], 'status': issue['state'], 'labels': [label['name'] for label in issue['labels']]} for issue in issues_data],
            'pulls': [{'title': pr['title'], 'status': pr['state'], 'author': pr['user']['login']} for pr in pulls_data],
            'contributors': [{'login': contributor['login'], 'commits': contributor['contributions']} for contributor in contributors_data],
            'readme': readme_html,
            'user': {'name': username},
            'clone_url': repo_data.get('clone_url', ''),
            'zip_url': repo_data.get('zipball_url', '')
        }
        
    except requests.RequestException as e:
        print(f"Error fetching repository data: {e}")
        return None
    
    return repo_info
