
from flask import current_app
import requests

def github_create_issue(data):
    #github configurations
    token = current_app.config["GITHUB_TOKEN"]
    owner = current_app.config["GITHUB_OWNER"]
    repo = current_app.config["GITHUB_REPO"]
    

    #construct the url
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    #headers
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2026-03-10"
    }


    # POST request to github
    response = requests.post(url, headers=headers, json=data)

    return response

    