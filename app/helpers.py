import jwt
from datetime import datetime
from functools import wraps


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
        token = request/args.get('token')
        if not token:
            return {'message': 'Token is required'}
        
        try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return {'message': 'Invalid t'}