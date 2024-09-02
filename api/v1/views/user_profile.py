# main.py
#!/usr/bin/python3
import requests
from flask import jsonify, render_template
from api.v1.views import app_views

cache = {}

@app_views.route("/<username>/stats", methods=["GET"])
def fetch_more_github_stats(username):
    if username in cache:
        return cache[username]
    
    base_url = f"https://api.github.com/users/{username}"
    
    with requests.Session() as session:
        user_req = session.get(base_url)
        repos_req = session.get(f"{base_url}/repos")
        followers_req = session.get(f"{base_url}/followers")
        following_req = session.get(f"{base_url}/following")
        events_req = session.get(f"{base_url}/events")
    
    if user_req.status_code == 200:
        user_data = user_req.json()
        repos_data = repos_req.json() if repos_req.status_code == 200 else []
        followers_data = [follower['login'] for follower in followers_req.json()] if followers_req.status_code == 200 else []
        following_data = [following['login'] for following in following_req.json()] if following_req.status_code == 200 else []
        recent_activities = [
            f"{event['type']} at {event['repo']['name']}" 
            for event in events_req.json()[:10]
        ] if events_req.status_code == 200 else []
        
        repos = [{
            "name": repo["name"],
            "description": repo["description"],
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"]
        } for repo in repos_data]
        
        rendered_template = render_template(
            "user_profile.html",
            user={
                "name": user_data.get("name"),
                "description": user_data.get("bio", "No description provided"),
                "avatar_url": user_data.get("avatar_url"),
                "following": user_data.get("following"),
                "followers": user_data.get("followers"),
                "email": user_data.get("email", "No email provided"),
                "html_url": user_data.get("html_url", "#")
            },
            repos=repos,
            followers=followers_data,
            following_list=following_data,
            recent_activities=recent_activities
        )
        
        cache[username] = rendered_template
        return rendered_template
    else:
        return jsonify({"error": "User not found"}), 404