from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from helpers import token_required, validate_credentials
from datetime import datetime
from functools import wraps
import jwt, bcrypt


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

# Helper Functions

# Helper functions
def validate_credentials(username, password):
    hashed_pw = users.find({"Username": username})[0]["Password"]

    if bcrypt.checkpw(password.encode("utf-8"), hashed_pw):
        login(username, password)
    else:
        return make_response('Unable to verify', 403, {"WWW-Authenticate": 'Basic realm: "Authentication Failed!"' })



def login(username, password):
    token = jwt.encode({
         'user': username,
         'expiration': datetime.utcnow() + timedelta(seconds=120)
         },
         app.config['SECRET_KEY']
         )
    return jsonify({"token": token.decode('utf-8')})

    #TODO try and accept since there are many exceptions


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return {'message': 'Token is required'}
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return {'message': 'Invalid tokem'}
        return decorated

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


@app.route("/pub")
def public():
    return "For all "


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