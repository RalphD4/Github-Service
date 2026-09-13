from flask import Blueprint, jsonify, request
from backend.helpers.validator import validate_issue

#Blue print for routes
issues_api = Blueprint("issues", __name__)

#processing an issue created
@issues_api.route("/issues", methods=["POST"])
def create_issue():

    #receive the data
    data = request.get_json()

    #check data format
    validate_issue(data)

    #make request to github repo -> repo -> issues

    return "creating issue"


        
    
    
    

#list of issues 
@issues_api.route("/issues", methods=["GET"])
def list_issues():
    return "list of issues"


#add other related routes below