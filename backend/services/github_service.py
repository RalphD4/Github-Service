
from flask import current_app
import requests, os


#github configurations
TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = os.getenv("GITHUB_OWNER")
REPO = os.getenv("GITHUB_REPO")



def github_create_issue(data):
    
    #construct the url
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"

    #headers
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2026-03-10"
    }


    # POST request to github
    response = requests.post(url, headers=headers, json=data)

    return response.json(), response.status_code


def github_get_issues(params=None):
    #construct the url
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2026-03-10"
    }
    #request data
    response = requests.get(url, headers=headers, params=params)

    return response.json(), response.status_code



def github_get_one_issue(number):
    #url
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{number}"

    #headers
    headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "X-GitHub-Api-Version": "2026-03-10"
        }
    
    response = requests.get(url, headers=headers)
    return response.json(), response.status_code


def github_add_issue_comment(number, comment):
    #construct the url
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{number}/comments"

    #headers
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    # POST request to github
    response = requests.post(url, headers=headers, json=comment)


    return response.json(), response.status_code


def github_update_issue(number, data): 
    #construct the url
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues/{number}"

    #headers
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {TOKEN}",
        "X-GitHub-Api-Version": "2026-03-10"
    }

    # Patch request to github
    response = requests.patch(url, headers=headers, json=data) 


    return response.json(), response.status_code

    