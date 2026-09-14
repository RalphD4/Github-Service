
from flask import Blueprint, jsonify, request
from backend.helpers.validator import validate_issue
from backend.services.github_service import github_create_issue, github_get_issues



#Blue print for routes
issues_api = Blueprint("issues", __name__)

#processing an issue created
@issues_api.route("/issues", methods=["POST"])
def create_issue():

    #receive the data
    data = request.get_json()
    

    #check data format
    if not validate_issue(data):
        print("invalid json")
        return jsonify({"error": "Invalid payload"}), 400

    response = github_create_issue(data)

    #extract fields if correct status code
    if response.status_code == 201:
        github_issue = response.json()
        issue = {
            "number": github_issue["number"],
            "htlm_url": github_issue["html_url"],
            "state": github_issue["state"],
            "title": github_issue["title"],
            "body": github_issue["body"],
            "labels": github_issue["labels"],
            "created_at": github_issue["created_at"],
            "updated_at": github_issue["updated_at"]
        }
        return jsonify(issue), 201, {
            "Location": f"/issues/{issue['number']}"
        }
    
    elif response.status_code == 201:
        return jsonify({"error": "Invalid Token"}), 401
    
    else:
        return jsonify({"error": "Github request failed"}), response.status_code
        


    
#list of issues
@issues_api.route("/issues", methods=["GET"])
def list_issues():
    #get the parameters of the request
    state = request.args.get("state")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 30, type=int)

    #build the params
    params = {
        "state": state,
        "page": page,
        "per_page": per_page
    }

    #get the issues using service function
    github_issues, status_code = github_get_issues(params)

    #if valid, for each issue, build the dictionary format and add to final array
    if status_code == 200:
        
        issues = []
        for github_issue in github_issues:
            issue = {
                "number": github_issue ["number"],
                "htlml_url": github_issue["html_url"],
                "state": github_issue["state"],
                "title": github_issue["title"],
                "body": github_issue["body"],
                "labels": github_issue["labels"],
                "created_at": github_issue["created_at"],
                "updated_at": github_issue["updated_at"]
            }
            issues.append(issue)



        return jsonify(issues), 200
    else:
        return jsonify({"error": "Couldnt retrieve issues"}), status_code



#add other related routes below