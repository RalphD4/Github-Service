
from flask import Blueprint, jsonify, request
from backend.helpers.validator import validate_issue
from backend.services.github_service import github_create_issue


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
        github_response = response.json()
        issue = {
            "number": github_response["number"],
            "htlml_url": github_response["html_url"],
            "state": github_response["state"],
            "title": github_response["title"],
            "body": github_response["body"],
            "labels": github_response["labels"],
            "created_at": github_response["created_at"],
            "updated_at": github_response["updated_at"]
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
    return "list of issues"


#add other related routes below