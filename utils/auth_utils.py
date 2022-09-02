import json
from functools import wraps
from api_v1.api_v1_app import SECRET_KEY

from decouple import config
from flask import Response, request,abort
import jwt
from models.user_model import User

from schemas.auth_schema import AuthSchema
from models.auth_model import Auth
from schemas.user_schema import UserSchema


SECRET_KEY = config('SECRET_KEY')

auth_schema = AuthSchema()
auth_schema_list = AuthSchema(many = True)

user_schema = UserSchema()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # print('request',request.headers)
        current_user = None
        auth_type = "API_KEY"
        if "Authorization" in request.headers:
            # print('here', request.headers["Authorization"])
            auth_token = request.headers["Authorization"]
            if auth_token.startswith('Bearer'):
                token = auth_token.split(" ")[1]
                try:
                    data=jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                    # print('data', data)
                    user = User.query.filter(User.id == data['user_id']).first()
                    # print('user', user)
                    if user == None:
                        return {
                            "message": "Invalid Authentication token!",
                            "data": None,
                            "error": "Unauthorized",
                            "success": False
                        }, 401
                    current_user = user_schema.dump(user)
                    auth_type = "LOGIN"
                except jwt.ExpiredSignatureError:
                    print("Token expired. Get new one")
                    return {
                            "message": "Token expired",
                            "data": None,
                            "error": "Unauthorized",
                            "success": False
                        }, 401
                except jwt.InvalidTokenError:
                    return {
                            "message": "Invalid Authentication token!",
                            "data": None,
                            "error": "Unauthorized",
                            "success": False
                        }, 401
               
            else:
                token = auth_token

                auth = Auth.query.filter(Auth.auth_key == auth_token, Auth.status == True).first()
                # print('auth', auth)
                if auth == None:
                    current_user = None 
                else:      
                    current_user = auth_schema.dump(auth)
            # print('token', token)
            # print('curren_user', current_user)
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized",
                "success": False
            }, 401
        try:
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized",
                "success": False
            }, 401
            # if not current_user["active"]:
            #     abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500
        # print({'current_user':current_user,'auth_type': auth_type})
        return f({'current_user':current_user,'auth_type': auth_type}, *args, **kwargs)

    return decorated