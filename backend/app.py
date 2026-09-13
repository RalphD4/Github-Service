from flask import Flask, Blueprint
from flask_cors import CORS

from backend.routes.issues_home import issues_api

#app start-up
app = Flask(__name__)
CORS(app)


#registering blue prints
app.register_blueprint(issues_api)

@app.route("/")
def home():
    return "Home Page"


#start the app, change to port listed on assignment later
if __name__ == "__main__":
    app.run()

