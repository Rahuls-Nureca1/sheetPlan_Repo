import json
from functools import wraps
from api_v1.api_v1_app import SECRET_KEY

from decouple import config
from flask import Response, request,abort
import jwt

from schemas.auth_schema import AuthSchema
from models.auth_model import Auth


SECRET_KEY = config('SECRET_KEY')

auth_schema = AuthSchema()
auth_schema_list = AuthSchema(many = True)

# def require_api_key():
#     def wrapper(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             auth_header = request.headers.get('Authorization')
#             if auth_header and auth_header == API_KEY:
#                 return f(*args, **kwargs)
#             else:
#                 response = {
#                     "message": "Unauthorized",
#                     "status": "401"
#                 }
#                 return Response(response=json.dumps(response), status=401, mimetype='application/json')
#         return decorated_function
#     return wrapper


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print('request',request.headers)
        current_user = None
        auth_type = "API_KEY"
        if "Authorization" in request.headers:
            print('here', request.headers["Authorization"])
            auth_token = request.headers["Authorization"]
            if auth_token.startswith('Bearer'):
                token = auth_token.split(" ")[1]
                data=jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                current_user = {}
                auth_type = "LOGIN"
            else:
                token = auth_token

                auth = Auth.query.filter(Auth.auth_key == auth_token, Auth.status == True).first()
                print('auth', auth)
                auth_data = auth_schema.dump(auth)
                print('auth', auth_data)
                current_user = {}
            print('token', token)
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            # if not current_user["active"]:
            #     abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500
        print({'current_user':current_user,'auth_type': auth_type})
        return f({'current_user':current_user,'auth_type': auth_type}, *args, **kwargs)

    return decorated