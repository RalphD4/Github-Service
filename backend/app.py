from flask import Flask, Blueprint
from flask_cors import CORS
import os
from dotenv import load_dotenv



from backend.routes.issues_home import issues_api
from backend.routes.webhook import webhook_api

load_dotenv()

#app start-up
app = Flask(__name__)
CORS(app)
app.config['GITHUB_TOKEN'] = os.getenv("GITHUB_TOKEN")
app.config['GITHUB_OWNER'] = os.getenv("GITHUB_OWNER")
app.config['GITHUB_REPO'] = os.getenv("GITHUB_REPO")

#registering blue prints
app.register_blueprint(issues_api)
app.register_blueprint(webhook_api)

@app.route("/")
def home():
    return "Home Page"


#start the app, change to port listed on assignment later
if __name__ == "__main__":
    app.run(port=8000)

