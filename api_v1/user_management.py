from datetime import datetime

from flask import Blueprint, request, jsonify, Response


from extensions import db
from models.auth_model import Auth


user_management_bp = Blueprint('user_management', __name__)


# TODO:
# Implement API key check
@user_management_bp.route('/create/api-key', methods=['POST'])
def create_apikey():
    apikey = Auth('key1','description1',True)
    db.session.add(apikey)
    db.session.flush()
    db.session.commit()
    print('apikey',apikey)
    return {"success":"api key created successfully"}
    

