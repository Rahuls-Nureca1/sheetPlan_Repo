from datetime import datetime

from flask import Blueprint, request, jsonify, Response


from extensions import db
from models.auth_model import Auth


api_v1_bp = Blueprint('api_v1', __name__)


# TODO:
# Implement API key check
@api_v1_bp.route('/create/api-key', methods=['POST'])
def create_apikey():
    apikey = Auth('key1','description1',True)
    db.session.add(apikey)
    db.session.flush()
    db.session.commit()
    print('apikey',apikey)
    return {"success":"api key created successfully"}
    

@api_v1_bp.route('/update/<id>', methods=['PUT'])
def update_apikey(id):
    description = request.get_json()['description']
    apikey = Auth.query.filter_by(id = id).first_or_404()
    apikey.auth_description = description
    db.session.commit()
    return {"success":"api key updated successfully"}
