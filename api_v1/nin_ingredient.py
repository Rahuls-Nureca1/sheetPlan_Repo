from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.nin_ingredient_model import NIN_Ingredient
from schemas.nin_ingredient_schema import NININgredientSchema
from utils import api_logger
from utils.auth_utils import token_required

nin_ingredient_bp = Blueprint('nin_ingredient', __name__)

nin_schema = NININgredientSchema()
nin_schema_list = NININgredientSchema(many = True)


# TODO:
# Implement create NIN Ingredient
@nin_ingredient_bp.route('/', methods=[''])
@token_required
def create_nin_ingredient(auth_data):
    try:
        req_body = request.get_json()
        nin = NIN_Ingredient.query.filter_by(nin_code = req_body['nin_code']).first()
        if nin != None:
            return make_response({"success":False,"message":"Duplicate NIN code"}, 400)
        nin_data = NIN_Ingredient(req_body['nin_code'],req_body['ingredient_name'],req_body['ingredient_description'], req_body['macros'], req_body['micros'])
        db.session.add(nin_data)
        db.session.flush()
        db.session.commit()
        return make_response({"success":"NIN data created successfully"}, 201)
    except Exception as e:
        return jsonify(str(e))


# TODO:
# Implement delete NIN Ingredient
@nin_ingredient_bp.route('/<id>', methods=[''])
@token_required
def delete_nin_ingredient(auth_data,id):
    try:
        nin = NIN_Ingredient.query.filter_by(id = id).first()
        if nin == None:
            return make_response({"success":False,"message":"NIN Id not found"}, 404)

        nin.deleted = True
        db.session.commit()
        return make_response({"success":True,"message":"NIN data deleted successfully"}, 200)

    except Exception as e:
        print('exception', e)
        return jsonify(str(e))

    
# TODO:
# Implement update NIN Ingredient
@nin_ingredient_bp.route('/<id>', methods=[''])
@token_required
def update_nin_ingredient(auth_data,id):
    try:
        payload = request.get_json()
        nin = NIN_Ingredient.query.filter_by(id = id).first()
        if nin == None:
            return make_response({"success":False,"message":"NIN Id not found"}, 404)

        nin.nin_code = payload['nin_code']
        nin.ingredient_name = payload['ingredient_name']
        nin.ingredient_description = payload['ingredient_description']
        nin.macros = payload['macros']
        nin.micros = payload['micros']
        nin.deleted = payload['deleted']
        db.session.commit()
        return make_response({"success":True,"message":"NIN data updated successfully"}, 200)
    except Exception as e:
        print('exception', e)


# TODO:
# Implement list NIN Ingredient
@nin_ingredient_bp.route('/', methods=['GET'])
@token_required
def list_nin_ingredient(auth_data):
    try:
        nin = NIN_Ingredient.query.filter_by(deleted = False).all()
        return make_response({"success":True,"data":nin_schema_list.dump(nin)}, 200)
    except Exception as e:
        print('exception', e)

# TODO:
# Implement get NIN Ingredient by id
@nin_ingredient_bp.route('/<id>', methods=['GET'])
@token_required
def nin_ingredient_by_id(auth_data,id):
    try:
        nin = NIN_Ingredient.query.filter_by(deleted = False,id = id).first()
        if nin == None:
            return make_response({"success":False,"message":"NIN Id not found"}, 404)
        else:
            return make_response({"success":True,"data":nin_schema.dump(nin)}, 200)
    except Exception as e:
        print('exception', e)



#for logging all the requests

@nin_ingredient_bp.after_request
def after_request_cal(response):
    api_logger.after_request(request,response)
    return response
    

@nin_ingredient_bp.errorhandler(Exception)
def exceptions(e):
    api_logger.exceptions(request,e)
    return e.status_code