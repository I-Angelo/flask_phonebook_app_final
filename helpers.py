# Helps us with other functions like logging in correctly. Making sure users have access to the API data. Whos allow to see info
from functools import wraps
import secrets
from flask import request, jsonify, json #Json is content that Java is able to parse very easily . Similar to Python on how it works. Json is popualr way to deliver data
import decimal

from models import User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing.'}), 401

        try:
            current_user_token = User.query.filter_by(token = token).first()
            print(token)
            print(current_user_token)
        except:
            owner=User.query.filter_by(token=token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated
# def token_required(our_flask_function): #flask methods. Used every time we want to require a token
#     @wraps(our_flask_function)
#     def decorated(*args, **kwargs):
#         token = None

#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access.token'].split(' ')[1]
#         if not token:
#             return jsonify({'message': 'Token is missing.'}), 401

#         try:
#             current_user_token = User.query.filter_by(token = token).first() #we are checking if the token is in our database, if it is will be stored
#                                                                     #in the variable 'current_user_token'
#             print(token)
#             print(current_user_token)
#         except:
#             owner = User.query.filter_by(token = token).first()

#             if token != owner.token and secrets.compare_digest(token, owner.token):
#                 return jsonify({'message': 'Token is invalid'})
#         return our_flask_function(current_user_token, *args, **kwargs)
#     return decorated


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder,self).default(obj)
