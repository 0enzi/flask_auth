import jwt, bcrypt
from datetime import datetime
from functools import wraps
from flask import request
from app import users

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