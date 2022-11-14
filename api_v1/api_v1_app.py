from datetime import  timezone
import datetime
from flask import Blueprint, request, jsonify, Response, make_response
import uuid
import jwt

from extensions import db
from models.auth_model import Auth
from decouple import config
from schemas.auth_schema import AuthSchema
from models.user_model import User
from schemas.user_schema import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash


user_schema = UserSchema()


SECRET_KEY = config('SECRET_KEY')

auth_schema = AuthSchema()
auth_schema_list = AuthSchema(many = True)

api_v1_bp = Blueprint('api_v1', __name__)


# TODO:
# Implement create api
@api_v1_bp.route('/api_management/api-key', methods=['POST'])
def create_apikey():
    description = request.get_json()['description']
    token = jwt.encode({"user_id": uuid.uuid4().hex},SECRET_KEY,algorithm="HS256")
    auth = Auth(token,description,True)
    db.session.add(auth)
    db.session.commit()
    return {"success": True,"message":"api key created successfully", "api_key":token}
    
# TODO:
# Implement Update api key
@api_v1_bp.route('/api_management/api-key/<id>', methods=['PUT'])
def update_apikey(id):
    description = request.get_json()['description']
    status = request.get_json()['status']

    auth = Auth.query.filter(Auth.id == id).update({Auth.auth_description : description, Auth.status: status})
    if auth == 0:
        return make_response({"success":False,"message":"Invalid api key id"}, 404)
    db.session.commit()
    return {"success":"api key updated successfully"}

# TODO:
# Implement List api key
@api_v1_bp.route('/api_management/api-key/', methods=['GET'])
def get_api_keys():
    try:
        apis = Auth.query.order_by(Auth.create_at.desc()).all()
        data = auth_schema_list.dump(apis)
        print(data)
        return jsonify(data)    
    except Exception as e:
        print('exception', e)



# TODO:
# Implement login
@api_v1_bp.route('/auth/login', methods=['POST'])
def create_user():
    reg_user = User.query.filter(User.email == request.get_json()['email']).first()
    if reg_user == None:
            return make_response({"success":False,"message":"User not registered"}, 404)

    if not check_password_hash(reg_user.password, request.get_json()['password']):
            return make_response({"success":False,"message":"Invalid email or password"}, 400)
   
    print('reg user', reg_user)
    token = jwt.encode({"user_id": reg_user.id, "email": reg_user.email,"exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=1)},SECRET_KEY,algorithm="HS256")
    return make_response({"success":True,"message":"User created successfully", "auth":{"token":token, "type": "Bearer"}}, 200)
    