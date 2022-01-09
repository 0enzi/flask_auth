from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from helpers import token_required, validate_credentials


#Flask REST API Init
app = Flask(__name__)
app.config['SECRET_KEY'] = "409e092b3e8d42698f341f4fe4d74be5"

"""
import os
os.url

or

import uuid
uuid.uuid4().hex


"""
api = Api(app)


# Init DB connection
client = MongoClient("mongodb://db:27017")

# create a new DB named as aNewDB
db = client.DocumentsDB                 
users = db['Users']


# Objectives
"""
Objectives

***Login 
* Get Username, Password
* Make sure both are given
* Check if user exists, Check if username and password match

* create a user token

***Register
* Get username, password, email, password

"""


# Routes [NON API]
@app.route("/")
def home():
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return "You're are logged in!"

@app.route("/public")
def public():
    return "For public"


@app.route("/auth")
@token_required
def auth():
    return "You are logged in"


class Login(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data["username"]
        password = posted_data["password"]

        # Validate
        if request.get_json()['username'] and request.get_json()['password']:
            validate_credentials(username, password)
        else:
            return {"message": "Please enter all required!"}


api.add_resource(Login, '/login')

app.run(debug=True)