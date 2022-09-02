from datetime import datetime

from flask import Blueprint, request, jsonify, Response,make_response


from extensions import db
from models.user_model import User
from schemas.user_schema import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash

user_schema = UserSchema()


user_management_bp = Blueprint('user_management', __name__)

def encrypt_password(password):
    """Encrypt password"""
    return generate_password_hash(password)

# TODO:
# Implement create user
@user_management_bp.route('/', methods=['POST'])
def create_user():
    reg_user = User.query.filter(User.email == request.get_json()['email']).first()
    if reg_user != None:
            return make_response({"success":False,"message":"Email already registered"}, 400)
    user = User(request.get_json()['first_name'],request.get_json()['last_name'],request.get_json()['email'],encrypt_password(request.get_json()['password']))
    db.session.add(user)
    db.session.commit()
    return make_response({"success":"User created successfully"}, 201)
    
