from cmath import log
import json
from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.nin_ingredient_model import NIN_Ingredient
from models.plan_schedule_model import Recipe
from models.ingredient_serving_unit_model import IngredientServingUnit
from models.ingredient_model import Ingredient
from schemas.nin_ingredient_schema import NININgredientSchema
from schemas.recipe_schema import RecipeSchema
from schemas.ingredient_schema import IngredientSchema
from schemas.ingredient_serving_unit_schema import IngredientServingUnitSchema
from time import strftime
from utils import api_logger, nin_mapping
import os
from models.plan_schedule_model import Planned_Meal
from sqlalchemy import func

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

        recipe = Recipe.query.filter(func.lower(Recipe.recipe_name) == func.lower(req_body['recipe_name'])).all()
        if len(recipe) > 0:
            return make_response({"success":False,"message":"Recipe already exist"}, 400)

        recipe_data = Recipe(req_body['recipe_name'],req_body['image_path'],req_body['course'],req_body['cusine'],req_body['recipe_url'],req_body['website_name'],req_body['serving'], 1)
        ingredients = req_body['ingredients']
        ingredient_list = []
        nutrition_data = []
        try:
            # db.session.add(recipe_data)
            # db.session.flush()
            for i in ingredients:
                # i['recipe_id'] = recipe_data.id
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


                if i['quantity_in_gram'] != None:
                    serving_size = i['quantity_in_gram']
               
                quantity_in_gram = serving_size * i['quantity']
                

               

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
                        macros[key] = round(float(macros[key]) * multiplication_factor, 2)
                    for key in micros:
                        micros[key] =  round(float(micros[key]) * multiplication_factor,3)
                        
                    
                    # ingredient_nutrition_data =  IngredientNutrition(ingredient_data.id,macros,micros)
                else:
                    # if there is no match found insert default data with 0 value
                    filename = os.path.join(dirname, '../seeds/data/nutrition_blueprint.json')
                    with open(filename) as file:
                            data = json.load(file)
                            macros = data['macros']
                            micros = data['micros']
                            # ingredient_nutrition_data =  IngredientNutrition(ingredient_data.id,data['macros'],data['micros'])

                ingredient_data = Ingredient(recipe = recipe_data, nin_id = nin_id,ingredient_name=i['ingredient_name'],ingredient_standard_name=i['ingredient_standard_name'],ingredient_desc= i['ingredient_desc'],quantity= i['quantity'],quantity_in_gram=  quantity_in_gram,serving_unit_id = serving_unit_id,serving_unit = i['serving_unit'], macros =macros, micros =micros)

                # ingredient_data = Ingredient(i['recipe_id'],nin_id, i['ingredient_name'],i['ingredient_standard_name'], i['ingredient_desc'], i['quantity'], quantity_in_gram,serving_unit_id,i['serving_unit'], macros =macros, micros =micros)

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
# Implement create multiple recipe
@recipe_management_bp.route('/multiple-recipe', methods=['POST'])
def create_multiple_recipe():
    try:
        serving_data = IngredientServingUnit.query.all()
        serving_unit_list = serving_unit_schema_list.dump(serving_data)

        req_body = request.get_json()

        for recipe in req_body:
            ingredient_list = []    
            print('recipe %s started' % recipe['recipe_name'])
            recipe_list = Recipe.query.filter(func.lower(Recipe.recipe_name) == func.lower(recipe['recipe_name'])).all()
            
            if len(recipe_list) > 0:
                return make_response({"success":False,"message":"Recipe %s already exist" % recipe['recipe_name']}, 400)
            recipe_data = Recipe(recipe['recipe_name'],recipe['image_path'],recipe['course'],recipe['cusine'],recipe['recipe_url'],recipe['website_name'],recipe['serving'], 1)
            ingredients = recipe['ingredients']
            try:
                for i in ingredients:
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


                    if i['quantity_in_gram'] != None:
                        serving_size = i['quantity_in_gram']
                
                    quantity_in_gram = serving_size * i['quantity']
                    

                

                    # ingredient_list.append(Ingredient(i['recipe_id'],None, i['ingredient_name'],i['ingredient_standard_name'], i['ingredient_desc'], i['quantity'], quantity_in_gram,serving_unit_id,i['serving_unit']))
                    
                    #find maping from nin table
                    suggested_nin_list = nin_mapping.map_ingredient(i['ingredient_standard_name'])

                    nin_id = suggested_nin_list[0]['id'] if len(suggested_nin_list) else None

                

                    # map ingredient with NIN table based on standardname
                    if len(suggested_nin_list):
                        # if there is more than one match take the best match
                        macros = suggested_nin_list[0]['macros']
                        micros = suggested_nin_list[0]['micros']
                        print('macros', macros)
                        print('micros', micros)
                        multiplication_factor = quantity_in_gram/100
                        for key in macros:
                            if macros[key] == '':
                                macros[key] = 0
                            macros[key] = round(float(macros[key]) * multiplication_factor, 2)
                        for key in micros:
                            if micros[key] == '':
                                micros[key] = 0
                            micros[key] =  round(float(micros[key]) * multiplication_factor,3)
                            
                        
                        # ingredient_nutrition_data =  IngredientNutrition(ingredient_data.id,macros,micros)
                    else:
                        # if there is no match found insert default data with 0 value
                        filename = os.path.join(dirname, '../seeds/data/nutrition_blueprint.json')
                        with open(filename) as file:
                                data = json.load(file)
                                macros = data['macros']
                                micros = data['micros']
                                # ingredient_nutrition_data =  IngredientNutrition(ingredient_data.id,data['macros'],data['micros'])

                    ingredient_data = Ingredient(recipe = recipe_data, nin_id = nin_id,ingredient_name=i['ingredient_name'],ingredient_standard_name=i['ingredient_standard_name'],ingredient_desc= i['ingredient_desc'],quantity= i['quantity'],quantity_in_gram=  quantity_in_gram,serving_unit_id = serving_unit_id,serving_unit = i['serving_unit'], macros =macros, micros =micros)

                    # ingredient_data = Ingredient(i['recipe_id'],nin_id, i['ingredient_name'],i['ingredient_standard_name'], i['ingredient_desc'], i['quantity'], quantity_in_gram,serving_unit_id,i['serving_unit'], macros =macros, micros =micros)
                    ingredient_list.append(ingredient_data)

                db.session.add_all(ingredient_list)
               
                print('recipe %s created' % recipe['recipe_name'])
                
            except Exception as e:
                print('exceptions', e)
                db.session.rollback()  
                return make_response({"success":False,"message":"invalid payload"}, 400)

        db.session.flush()
        db.session.commit()
      
        return make_response({"success":True,"message":"Recipe created successfully"}, 201)
    except Exception as e:
        print('in catch', e)   
        db.session.rollback()
        return make_response({"success":False,"message":"invalid payload","err":jsonify(str(e))}, 400)



# TODO:
# Implement create nin recipe
@recipe_management_bp.route('/nin_recipe', methods=['POST'])
def create_nin_recipe():
    try:
        serving_data = IngredientServingUnit.query.all()
        serving_unit_list = serving_unit_schema_list.dump(serving_data)

        req_body = request.get_json()

        print(req_body)
        try:
            for item in req_body:
                recipe_data = Recipe(item['recipe_name'],item['image_path'],[],[],'','NIN',item['serving'], 1)
                ingredient_serving_unit = item['serving_unit'].lower()
            
                matched_serving_unit = None

                for serving_unit in serving_unit_list:
                    if ingredient_serving_unit == serving_unit['serving_unit_name'].lower() or ingredient_serving_unit in serving_unit['serving_unit_othername']:
                        matched_serving_unit = serving_unit
                        break
                quantity_in_gram = 0  
                if matched_serving_unit != None:
                    serving_unit_id = matched_serving_unit['id']
                    serving_size = matched_serving_unit['serving_unit_quantity']

               
                if item['quantity_in_gram'] != None:
                    serving_size = item['quantity_in_gram']
                quantity_in_gram =  serving_size * item['serving']


                #find maping from nin table - nin_code is blank
                if item['nin_code'] == "":

                    suggested_nin_list = nin_mapping.map_ingredient(item['recipe_name'])

                    nin_id = suggested_nin_list[0]['id'] if len(suggested_nin_list) else None

                else:
                    nin =  NIN_Ingredient.query.filter(NIN_Ingredient.nin_code == item['nin_code']).first()
                    print('nin', nin)
                    nin_data = nin_ingredient_schema.dump(nin)
                    print('nindata', nin.id)
                    nin_id = nin.id
                    suggested_nin_list  = []
                    suggested_nin_list.append(nin_data)


                # map ingredient with NIN table based on standardname
                if len(suggested_nin_list):
                    # if there is more than one match take the best match
                    macros = suggested_nin_list[0]['macros']
                    micros = suggested_nin_list[0]['micros']
                    multiplication_factor = quantity_in_gram/100
                    for key in macros:
                        macros[key] =  round(float(macros[key]) * multiplication_factor,2)
                    for key in micros:
                        micros[key] = round(float(micros[key]) * multiplication_factor,3)
                
            
                # ingredient_nutrition_data =  IngredientNutrition(ingredient_data.id,macros,micros)
                else:
                    # if there is no match found insert default data with 0 value
                    filename = os.path.join(dirname, '../seeds/data/nutrition_blueprint.json')
                    with open(filename) as file:
                            data = json.load(file)
                            macros = data['macros']
                            micros = data['micros']
                    # ingredient_nutrition_data =  IngredientNutrition(ingredient_data.id,data['macros'],data['micros'])

                ingredient_data = Ingredient(recipe = recipe_data, nin_id = nin_id,ingredient_name=item['recipe_name'],ingredient_standard_name=item['recipe_name'],ingredient_desc= "",quantity= item['serving'],quantity_in_gram=  quantity_in_gram,serving_unit_id = serving_unit_id,serving_unit = item['serving_unit'], macros =macros, micros =micros)

                # ingredient_data = Ingredient(i['recipe_id'],nin_id, i['ingredient_name'],i['ingredient_standard_name'], i['ingredient_desc'], i['quantity'], quantity_in_gram,serving_unit_id,i['serving_unit'], macros =macros, micros =micros)

                print(ingredient_data)
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
# Implement update recipe
@recipe_management_bp.route('/<recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    try:
        
        req_body = request.get_json()
        recipe = Recipe.query.filter(Recipe.id == recipe_id).update({Recipe.recipe_name : req_body['recipe_name'], Recipe.image_path:req_body['image_path'] , Recipe.course:req_body['course'],Recipe.cusine: req_body['cusine'],Recipe.recipe_url: req_body['recipe_url'],Recipe.website_name: req_body['website_name'],Recipe.serving: req_body['serving'], Recipe.updated_by: 1  })
        if recipe == 0:
            return make_response({"success":False,"message":"recipe Id not found"}, 404)
        
        db.session.commit()
      
        return make_response({"success":"Recipe updted successfully"}, 200)
    except Exception as e:
        print('in catch', e)
        return jsonify(str(e))


# TODO:
# Implement list recipe with pagination
@recipe_management_bp.route('/<offset>/<limit>', methods=['GET'])
def recipe_list(offset,limit):
    try:

        print('ofset', offset)
        recipe = Recipe.query.filter(Recipe.deleted == False).order_by(Recipe.create_at.desc()).paginate(page=int(offset),error_out=False, per_page=int(limit))
        print('recipe', recipe.items)
        if recipe == None:
            return make_response({"success":True,"data":[]}, 200)

        recipe_data = recipe_schema_list.dump(recipe.items)

        return make_response({"success":True,"data":recipe_data}, 200)
    except Exception as e:
        print('exception', e)



# TODO:
# Implement search recipe with pagination
@recipe_management_bp.route('/<offset>/<limit>/<recipe_name>', methods=['GET'])
def recipe_list_search(offset,limit, recipe_name):
    try:

        print('ofset', offset)
        recipe = Recipe.query.filter(Recipe.deleted == False, Recipe.recipe_name.ilike(recipe_name)).order_by(Recipe.create_at.desc()).paginate(page=int(offset),error_out=False, per_page=int(limit))
        print('recipe', recipe.items)
        if recipe == None:
            return make_response({"success":True,"data":[]}, 200)

        recipe_data = recipe_schema_list.dump(recipe.items)

        return make_response({"success":True,"data":recipe_data}, 200)
    except Exception as e:
        print('exception', e)



# TODO:
# Implement delete recipe 
@recipe_management_bp.route('/<id>', methods=['DELETE'])
def delete_recipe(id):
    try:
        recipe = Recipe.query.filter(Recipe.id == id).update({Recipe.deleted : True})
        if recipe == 0:
            return make_response({"success":False,"message":"Recipe Id not found"}, 404)

        db.session.commit()
        return make_response({"success":True,"message":"Recipe deleted successfully"}, 200)

    except Exception as e:
        print('exception', e)
        return jsonify(str(e))




# TODO:
# Implement add recipe Ingredient
@recipe_management_bp.route('/<recipe_id>/ingredient', methods=['POST'])
def add_recipe_ingredient(recipe_id):
    try:
        serving_data = IngredientServingUnit.query.all()
        serving_unit_list = serving_unit_schema_list.dump(serving_data)
        ingredients = request.get_json()
        try:
            recipe_data = Recipe.query.filter_by(id = recipe_id).first()
            for i in ingredients:
                # i['recipe_id'] = recipe_data.id
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
                

                #find maping from nin table if nin_id is passed in payload
                if i['nin_id'] == None or i['nin_id'] == 0:

                    suggested_nin_list = nin_mapping.map_ingredient(i['ingredient_standard_name'])
                    nin_id = suggested_nin_list[0]['id'] if len(suggested_nin_list) else None
                else:
                    nin_id = i['nin_id']
                    data = NIN_Ingredient.query.filter(NIN_Ingredient.id == nin_id).all()
                    if len(data) == 0:
                        suggested_nin_list =  []
                    suggested_nin_list = nin_ingredient_schema_list.dump(data)


            

                # map ingredient with NIN table based on standardname
                if len(suggested_nin_list):
                    # if there is more than one match take the best match
                    macros = suggested_nin_list[0]['macros']
                    micros = suggested_nin_list[0]['micros']
                    multiplication_factor = quantity_in_gram/100
                    for key in macros:
                        macros[key] = round(float(macros[key]) * multiplication_factor,2)
                    for key in micros:
                        micros[key] = round(float(micros[key]) * multiplication_factor,3)
                        
                    
                    # ingredient_nutrition_data =  IngredientNutrition(ingredient_data.id,macros,micros)
                else:
                    # if there is no match found insert default data with 0 value
                    filename = os.path.join(dirname, '../seeds/data/nutrition_blueprint.json')
                    with open(filename) as file:
                            data = json.load(file)
                            macros = data['macros']
                            micros = data['micros']
                            # ingredient_nutrition_data =  IngredientNutrition(ingredient_data.id,data['macros'],data['micros'])

                ingredient_data = Ingredient(recipe = recipe_data, nin_id = nin_id,ingredient_name=i['ingredient_name'],ingredient_standard_name=i['ingredient_standard_name'],ingredient_desc= i['ingredient_desc'],quantity= i['quantity'],quantity_in_gram=  quantity_in_gram,serving_unit_id = serving_unit_id,serving_unit = i['serving_unit'], macros =macros, micros =micros)

                db.session.add(ingredient_data)
                db.session.flush()

            db.session.commit()
        except Exception as e:
            print('exceptions', e)
            db.session.rollback()    
        
        db.session.commit()
      
        
        return make_response({"success":True,"message":"ingredient addded successfully"}, 200)
    except Exception as e:
        print('exception', e)


# TODO:
# Implement update recipe Ingredient
@recipe_management_bp.route('/ingredient/<ingrdient_id>', methods=['POST'])
def update_recipe_ingredient(ingredient_id):
    try:
        serving_data = IngredientServingUnit.query.all()
        serving_unit_list = serving_unit_schema_list.dump(serving_data)
        ingredients = request.get_json()
        try:
            recipe_data = Recipe.query.filter_by(id = recipe_id).first()
            for i in ingredients:
                # i['recipe_id'] = recipe_data.id
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
                

                #find maping from nin table if nin_id is passed in payload
                if i['nin_id'] == None or i['nin_id'] == 0:

                    suggested_nin_list = nin_mapping.map_ingredient(i['ingredient_standard_name'])
                    nin_id = suggested_nin_list[0]['id'] if len(suggested_nin_list) else None
                else:
                    nin_id = i['nin_id']
                    data = NIN_Ingredient.query.filter(NIN_Ingredient.id == nin_id).all()
                    if len(data) == 0:
                        suggested_nin_list =  []
                    suggested_nin_list = nin_ingredient_schema_list.dump(data)


            

                # map ingredient with NIN table based on standardname
                if len(suggested_nin_list):
                    # if there is more than one match take the best match
                    macros = suggested_nin_list[0]['macros']
                    micros = suggested_nin_list[0]['micros']
                    multiplication_factor = quantity_in_gram/100
                    for key in macros:
                        macros[key] = round(float(macros[key]) * multiplication_factor,2)
                    for key in micros:
                        micros[key] = round(float(micros[key]) * multiplication_factor,3)
                        
                    
                    # ingredient_nutrition_data =  IngredientNutrition(ingredient_data.id,macros,micros)
                else:
                    # if there is no match found insert default data with 0 value
                    filename = os.path.join(dirname, '../seeds/data/nutrition_blueprint.json')
                    with open(filename) as file:
                            data = json.load(file)
                            macros = data['macros']
                            micros = data['micros']
                            # ingredient_nutrition_data =  IngredientNutrition(ingredient_data.id,data['macros'],data['micros'])

                ingredient_data = Ingredient(recipe = recipe_data, nin_id = nin_id,ingredient_name=i['ingredient_name'],ingredient_standard_name=i['ingredient_standard_name'],ingredient_desc= i['ingredient_desc'],quantity= i['quantity'],quantity_in_gram=  quantity_in_gram,serving_unit_id = serving_unit_id,serving_unit = i['serving_unit'], macros =macros, micros =micros)

                db.session.add(ingredient_data)
                db.session.flush()

            db.session.commit()
        except Exception as e:
            print('exceptions', e)
            db.session.rollback()    
        
        db.session.commit()
      
        
        return make_response({"success":True,"message":"ingredient addded successfully"}, 200)
    except Exception as e:
        print('exception', e)


# TODO:
# Implement delete recipe ingredient 
@recipe_management_bp.route('/ingredient/<id>', methods=['DELETE'])
def delete_ingredient(id):
    try:
        ingredient = Ingredient.query.filter(Ingredient.id == id).delete()
        if ingredient == 0:
            return make_response({"success":False,"message":"Ingredient Id not found"}, 404)

        db.session.commit()
        return make_response({"success":True,"message":"Ingredient deleted successfully"}, 200)

    except Exception as e:
        print('exception', e)
        return jsonify(str(e))


# # TODO:
# # Implement update recipe Ingredient
# @recipe_management_bp.route('/ingredient/<id>', methods=['PUT'])
# def update_nin_ingredient(id):
#     try:
#         payload = request.get_json()
#         ingredient = Ingredient.query.filter_by(id = id).first()
#         if nin == None:
#             return make_response({"success":False,"message":"NIN Id not found"}, 404)

#         nin.nin_code = payload['nin_code']
#         nin.ingredient_name = payload['ingredient_name']
#         nin.ingredient_description = payload['ingredient_description']
#         nin.macros = payload['macros']
#         nin.micros = payload['micros']
#         nin.deleted = payload['deleted']
#         db.session.commit()
#         return make_response({"success":True,"message":"NIN data updated successfully"}, 200)
#     except Exception as e:
#         print('exception', e)



# # TODO:
# # Implement get recipe by id
# @recipe_management_bp.route('/<item_name>', methods=['GET'])
# def get_recipe_details(item_name):
#     try:
#         mapdata =   nin_mapping.map_ingredient(item_name)
#         return make_response({"success":True, "data" : mapdata}, 200)
#     except Exception as e:
#         print('exception', e)



# TODO:
# Implement nin ingredient maping
@recipe_management_bp.route('/<ingredient_id>/<nin_id>', methods=['PUT'])
def map_ingredient(ingredient_id, nin_id):
    try:
        ingredient = Ingredient.query.filter_by(id = ingredient_id).first()
        nin_ingredient = NIN_Ingredient.query.filter_by(id = nin_id).first()

        if ingredient == None:
            return make_response({"success":False,"message":"ingredient id not found"}, 404)
        if nin_ingredient == None:
            return make_response({"success":False,"message":"nin id not found"}, 404)

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

    
        for ingredient_obj in ingredient_list_data:
            
            multiplication_factor = ingredient_obj['quantity_in_gram']/100
            for key in nin_macros:
            
                macros[key] = round(float(nin_macros[key]) * multiplication_factor,2)
            for key in nin_micros:
                micros[key] = round(float(nin_micros[key]) * multiplication_factor,3)
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