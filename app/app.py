import bcrypt
from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient

#Flask REST API Init
app = Flask(__name__)
app.config['SECRET_KEY']
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

# Helper functions
def validate_credentials(username, password):
    hashed_pw = users.find({"Username": username})[0]["Password"]

    if bcrypt.checkpw(password.encode("utf-8"), hashed_pw):
        return True
    else:
        return False


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


class Signup(Resource):
    pass


class Logout(Resource):
    pass

api.add_resource(Login, '/login')
api.add_resource(Signup, '/login')
api.add_resource(Logout, '/logout')


app.run(debug=True)