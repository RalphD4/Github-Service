
from flask import Blueprint, jsonify, request
from backend.helpers.validator import validate_issue
from backend.services.github_service import github_create_issue, github_get_issues, github_get_one_issue, github_add_issue_comment



#Blue print for routes
issues_api = Blueprint("issues", __name__)

#processing an issue created
@issues_api.route("/issues", methods=["POST"])
def create_issue():

    #receive the data
    issue_data = request.get_json()
    

    #check data format
    if not validate_issue(issue_data):
        print("invalid json")
        return jsonify({"error": "Invalid payload"}), 400

    new_github_issue, status_code = github_create_issue(issue_data)

    #extract fields if correct status code
    if status_code == 201:
        
        issue = {
            "number": new_github_issue["number"],
            "html_url": new_github_issue["html_url"],
            "state": new_github_issue["state"],
            "title": new_github_issue["title"],
            "body": new_github_issue["body"],
            "labels": new_github_issue["labels"],
            "created_at": new_github_issue["created_at"],
            "updated_at": new_github_issue["updated_at"]
        }
        return jsonify(issue), 201, {
            "Location": f"/issues/{issue['number']}"
        }
    
    else:
        return jsonify({"error": "Github request failed"}), status_code
        


    
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
        for new_github_issue in github_issues:
            issue = {
                "number": new_github_issue ["number"],
                "htlml_url": new_github_issue["html_url"],
                "state": new_github_issue["state"],
                "title": new_github_issue["title"],
                "body": new_github_issue["body"],
                "labels": new_github_issue["labels"],
                "created_at": new_github_issue["created_at"],
                "updated_at": new_github_issue["updated_at"]
            }
            issues.append(issue)


        return jsonify(issues), 200
    else:
        return jsonify({"error": "Couldnt retrieve issues"}), status_code




#get a specific issue
@issues_api.route("/issues/<int:number>", methods=["GET"])
def get_one_issue(number):
    #get the issue
    new_github_issue, status_code = github_get_one_issue(number)

    #behavior based on status code
    if status_code == 200:

        #build response 
        issue = {
            "number": new_github_issue ["number"],
            "htlml_url": new_github_issue["html_url"],
            "state": new_github_issue["state"],
            "title": new_github_issue["title"],
            "body": new_github_issue["body"],
            "labels": new_github_issue["labels"],
            "created_at": new_github_issue["created_at"],
            "updated_at": new_github_issue["updated_at"]
        }
        return jsonify(issue), 200

    #errors
    elif status_code == 404:
        return jsonify({"error": "issue not found"}), status_code
    else:
        return jsonify({"error: Couldn't retrieve issue"})


#adding a commenent to an issue
@issues_api.route("/issues/<int:number>/comments", methods=["POST"])
def add_issue_comment(number):

    #receive the comment
    comment_data = request.get_json()

    #response from github
    new_comment, status_code = github_add_issue_comment(number, comment_data)

    #id, body, user, created_at, html_url }
    if status_code == 201:
        #build comment
        comment = {
            "id": new_comment["id"],
            "body": new_comment["body"],
            "user": new_comment["user"],
            "created_at": new_comment["created_at"],
            "html_url": new_comment["html_url"],
        }
        return jsonify(comment), 201
    
    else:
        return jsonify({"error": "Error or comment creation"}), status_code




        

    
#ROUTES NOT COMPLETE


#edit a specific issue  
@issues_api.route("/issues/<int:number>", methods=["PATCH"])
def edit_one_issue(number):
    return 


#optional /events route