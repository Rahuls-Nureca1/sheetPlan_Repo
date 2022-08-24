from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.recipe_model import Recipe
from models.ingredient_serving_unit_model import IngredientServingUnit
from models.ingredient_model import Ingredient
from schemas.recipe_schema import RecipeSchema
from schemas.ingredient_schema import IngredientSchema
from time import strftime
from utils import api_logger


recipe_management_bp = Blueprint('recipe_management', __name__)

recipe_schema = RecipeSchema()
recipe_schema_list = RecipeSchema(many = True)


# TODO:
# Implement create recipe
@recipe_management_bp.route('/', methods=['POST'])
def create_recipe():
    try:
        req_body = request.get_json()
        recipe_data = Recipe(req_body['recipe_name'],req_body['image_path'],req_body['course'],req_body['cusine'],req_body['recipe_url'],req_body['website_name'],req_body['serving'], 1)
        ingredients = req_body['ingredients']
        ingredient_data = []
        try:
            db.session.add(recipe_data)
            db.session.flush()
            for i in ingredients:
                i['recipe_id'] = recipe_data.id
                i['created_by'] = 1
                ingredient_data.append(Ingredient(i['recipe_id'],None, i['ingredient_name'], i['ingredient_desc'], i['quantity'], i['quantity_in_gram'],None,i['serving_unit']))
            db.session.add_all(ingredient_data)
        except Exception as e:
            print('exceptions', e)
            db.session.rollback()    
        
        db.session.commit()
      
        return make_response({"success":"Recipe created successfully"}, 201)
    except Exception as e:
        print('in catch', e)
        return jsonify(str(e))

# # TODO:
# # Implement list Plan schedule
# @recipe_management_bp.route('/', methods=['GET'])
# def list_plan_schedule():
#     try:
#         plan_schedule_data = Plan_Schedule.query.all()
#         print('planSchedule',plan_schedule_data)
#         plan_data = plan_schedule_schema_list.dump(plan_schedule_data)
#         return make_response({"success":True,"data":plan_data}, 200)
#     except Exception as e:
#         print('exception', e)


# # TODO:
# # Implement delete NIN Ingredient
# @recipe_management_bp.route('/<id>', methods=['DELETE'])
# def delete_nin_ingredient(id):
#     try:
#         plan_schedule = Plan_Schedule.query.filter_by(id = id).first()
#         if plan_schedule == None:
#             return make_response({"success":False,"message":"Planed schedule Id not found"}, 404)

#         Plan_Schedule.query.filter_by(id = id).delete()
#         db.session.commit()
#         return make_response({"success":True,"message":"Plan schedule deleted successfully"}, 200)

#     except Exception as e:
#         print('exception', e)
#         return jsonify(str(e))

    
# # TODO:
# # Implement update plan schedule
# @recipe_management_bp.route('/<id>', methods=['PUT'])
# def update_plan_schedule(id):
#     try:
#         payload = request.get_json()
#         plan_schedule = Plan_Schedule.query.filter_by(id = id).first()
#         if plan_schedule == None:
#             return make_response({"success":False,"message":"Plan Schedule Id not found"}, 404)

#         plan_schedule.plan_id = payload['plan_id']
#         plan_schedule.day_id = payload['day_id']
#         plan_schedule.time_id = payload['time_id']
#         db.session.commit()
#         return make_response({"success":True,"message":"Plan Schedule updated successfully"}, 200)
#     except Exception as e:
#         print('exception', e)


# # TODO:
# # Implement get plan schedule by id
# @recipe_management_bp.route('/<id>', methods=['GET'])
# def plan_schedule_by_id(id):
#     try:
#         plan_schedule = Plan_Schedule.query.filter_by(id = id).first()
#         if plan_schedule == None:
#             return make_response({"success":False,"message":"Plan schedule Id not found"}, 404)
#         else:
#             return make_response({"success":True,"data":plan_schedule_schema.dump(plan_schedule)}, 200)
#     except Exception as e:
#         print('exception', e)



#for logging all the requests

@recipe_management_bp.after_request
def after_request_cal(response):
    api_logger.after_request(request,response)
    return response
    

@recipe_management_bp.errorhandler(Exception)
def exceptions(e):
    api_logger.exceptions(request,e)
    return e.status_code