import json
from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.nin_ingredient_model import NIN_Ingredient
from models.recipe_model import Recipe
from models.ingredient_serving_unit_model import IngredientServingUnit
from models.ingredient_model import Ingredient
from schemas.nin_ingredient_schema import NININgredientSchema
from schemas.recipe_schema import RecipeSchema
from schemas.ingredient_schema import IngredientSchema
from schemas.ingredient_serving_unit_schema import IngredientServingUnitSchema
from time import strftime
from utils import api_logger, nin_mapping
import os
dirname = os.path.dirname(__file__)

recipe_management_bp = Blueprint('recipe_management', __name__)

recipe_schema = RecipeSchema()
recipe_schema_list = RecipeSchema(many = True)

serving_unit_schema = IngredientServingUnitSchema()
serving_unit_schema_list = IngredientServingUnitSchema(many = True)

ingredient_schema = IngredientSchema()
ingredient_schema_list = IngredientSchema(many = True)

nin_ingredient_schema = NININgredientSchema()
nin_ingredient_schema_list = NININgredientSchema(many = True)

# TODO:
# Implement create recipe
@recipe_management_bp.route('/', methods=['POST'])
def create_recipe():
    try:
        serving_data = IngredientServingUnit.query.all()
        serving_unit_list = serving_unit_schema_list.dump(serving_data)

        req_body = request.get_json()
        recipe_data = Recipe(req_body['recipe_name'],req_body['image_path'],req_body['course'],req_body['cusine'],req_body['recipe_url'],req_body['website_name'],req_body['serving'], 1)
        ingredients = req_body['ingredients']
        ingredient_list = []
        nutrition_data = []
        try:
            db.session.add(recipe_data)
            db.session.flush()
            for i in ingredients:
                i['recipe_id'] = recipe_data.id
                i['created_by'] = 1

                # find serving_unit_id and calculate quantity_in_gram from ingredient_serving_unit table
                ingredient_serving_unit = i['serving_unit'].lower()
                matched_serving_unit = None
                serving_unit_id = None
                serving_size = 0

                for serving_unit in serving_unit_list:
                    if ingredient_serving_unit == serving_unit['serving_unit_name'].lower() or ingredient_serving_unit in serving_unit['serving_unit_othername']:
                        matched_serving_unit = serving_unit
                        break
                if matched_serving_unit != None:
                    serving_unit_id = matched_serving_unit['id']
                    serving_size = matched_serving_unit['serving_unit_quantity']
                quantity_in_gram = i['quantity_in_gram'] if i['quantity_in_gram'] != None else serving_size * i['quantity']
                
               

                # ingredient_list.append(Ingredient(i['recipe_id'],None, i['ingredient_name'],i['ingredient_standard_name'], i['ingredient_desc'], i['quantity'], quantity_in_gram,serving_unit_id,i['serving_unit']))
                
                #find maping from nin table
                suggested_nin_list = nin_mapping.map_ingredient(i['ingredient_standard_name'])

                nin_id = suggested_nin_list[0]['id'] if len(suggested_nin_list) else None

            

                # map ingredient with NIN table based on standardname
                if len(suggested_nin_list):
                    # if there is more than one match take the best match
                    macros = suggested_nin_list[0]['macros']
                    micros = suggested_nin_list[0]['micros']
                    multiplication_factor = quantity_in_gram/100
                    for key in macros:
                        macros[key] = float(macros[key]) * multiplication_factor
                    for key in micros:
                        micros[key] = float(micros[key]) * multiplication_factor
                        
                    
                    # ingredient_nutrition_data =  IngredientNutrition(ingredient_data.id,macros,micros)
                else:
                    # if there is no match found insert default data with 0 value
                    filename = os.path.join(dirname, '../seeds/data/nutrition_blueprint.json')
                    with open(filename) as file:
                            data = json.load(file)
                            macros = data['macros']
                            micros = data['micros']
                            # ingredient_nutrition_data =  IngredientNutrition(ingredient_data.id,data['macros'],data['micros'])



                ingredient_data = Ingredient(i['recipe_id'],nin_id, i['ingredient_name'],i['ingredient_standard_name'], i['ingredient_desc'], i['quantity'], quantity_in_gram,serving_unit_id,i['serving_unit'], macros, micros)

                db.session.add(ingredient_data)
                db.session.flush()

            db.session.commit()
        except Exception as e:
            print('exceptions', e)
            db.session.rollback()    
        
        db.session.commit()
      
        return make_response({"success":"Recipe created successfully"}, 201)
    except Exception as e:
        print('in catch', e)
        return jsonify(str(e))

# TODO:
# Implement get recipe by id
@recipe_management_bp.route('/<item_name>', methods=['GET'])
def get_recipe_details(item_name):
    try:
        mapdata =   nin_mapping.map_ingredient(item_name)
        return make_response({"success":True, "data" : mapdata}, 200)
    except Exception as e:
        print('exception', e)



# TODO:
# Implement nin ingredient maping
@recipe_management_bp.route('/<ingredient_id>/<nin_id>', methods=['PUT'])
def map_ingredient(ingredient_id, nin_id):
    try:
        ingredient = Ingredient.query.filter_by(id = ingredient_id).first()
        nin_ingredient = NIN_Ingredient.query.filter_by(id = nin_id).first()

        if ingredient == None or nin_ingredient == None :
            return make_response({"success":False,"message":"ingredient id or nin id not found"}, 404)
        else:
            ingredient.nin_id = nin_id
            # update nutrition info for particular ingredient
            # updated_ingredient = Ingredient.query.filter(Ingredient.ingredient_standard_name == ingredient.ingredient_standard_name).update({Ingredient.nin_id:nin_id })
            
            # update ingredient nutrition table info
            nin_data = nin_ingredient_schema.dump(nin_ingredient)

            ingredient_list = Ingredient.query.filter_by(ingredient_standard_name = ingredient.ingredient_standard_name).all()
            ingredient_list_data = ingredient_schema_list.dump(ingredient_list)
            
            nin_macros = nin_data['macros']
            nin_micros = nin_data['micros']
            
            macros={}
            micros={}

            print('macros before', nin_macros)
            print('macros before', nin_micros)
            for ingredient_obj in ingredient_list_data:
                print('ingredient', ingredient_obj)
                multiplication_factor = ingredient_obj['quantity_in_gram']/100
                for key in nin_macros:
                    print('key', key)
                    macros[key] = float(nin_macros[key]) * multiplication_factor
                for key in nin_micros:
                    micros[key] = float(nin_micros[key]) * multiplication_factor
                Ingredient.query.filter(Ingredient.id == ingredient_obj['id']).update({Ingredient.macros:macros,Ingredient.micros:micros,Ingredient.nin_id:nin_id  })
            
            # ingredient_list_data = ingredient_schema_list.dump(ingredient_list)
            # for inredient_obj in ingredient_list_data:
            #     macros = nin_data['macros']
            #     micros = nin_data['micros']
            #     multiplication_factor = inredient_obj['quantity_in_gram']/100
            #     for key in macros:
            #         macros[key] = float(macros[key]) * multiplication_factor
            #     for key in micros:
            #         micros[key] = float(micros[key]) * multiplication_factor
            #     IngredientNutrition.query.filter(IngredientNutrition.ingredient_id == inredient_obj['id']).update({IngredientNutrition.macros:macros,IngredientNutrition.micros:micros })
                

            db.session.commit()

            return make_response({"success":True,"message":'Ingredient mapped successfully'}, 200)
    except Exception as e:
        print('exception', e)
        db.session.rollback()


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