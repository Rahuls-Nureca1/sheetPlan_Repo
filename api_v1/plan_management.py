import time
from cmath import log
import json
from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.plan_schedule_model import Plan_Schedule, Planned_Meal
from schemas.plan_schedule_schema import PlanScheduleSchema, PlannedMealSchema
from schemas.plan_schedule_schema import PlanScheduleWithoutRecipeSchema

from models.day_model import Day
from schemas.day_schema import DaySchema
from models.timing_model import Timing
from schemas.timing_schema import TimingSchema

from models.plan_model import Plan
from schemas.plan_schema import PlanSchema
from sqlalchemy import func

from schemas.ingredient_schema import IngredientSchema
from schemas.ingredient_serving_unit_schema import IngredientServingUnitSchema


from models.ingredient_serving_unit_model import IngredientServingUnit


from models.plan_schedule_model import Recipe
from schemas.recipe_schema import RecipeSchema

from time import strftime
from utils import api_logger
from utils.planned_meal_utils import get_planned_meal_serving_details, process_planned_meal_recipe




plan_management_bp = Blueprint('plan_management', __name__)

plan_schedule_schema = PlanScheduleSchema()
plan_schedule_schema_list = PlanScheduleSchema(many = True)

plan_schedule_without_recipe_schema = PlanScheduleWithoutRecipeSchema()
plan_schedule_without_recipe_schema_list = PlanScheduleWithoutRecipeSchema(many = True)

day_schema = DaySchema()
day_schema_list = DaySchema(many = True)

timing_schema = TimingSchema()
timing_schema_list = TimingSchema(many = True)

plan_schema = PlanSchema()
plan_schema_list = PlanSchema(many = True)

plan_meal_schema = PlannedMealSchema()
plan_meal_schema_list = PlannedMealSchema(many = True)


serving_unit_schema = IngredientServingUnitSchema()
serving_unit_schema_list = IngredientServingUnitSchema(many = True)

recipe_schema = RecipeSchema()
recipe_schema_list = RecipeSchema(many = True)

######## PLAN TYPE #########

# TODO:
# Implement List plan type
@plan_management_bp.route('/plan_list', methods=['GET'])
def get_plan_type():
    try:
        plan = Plan.query.all()
        data = plan_schema_list.dump(plan)
        print('data', data)
        return jsonify(data)
    except Exception as e:
        print('exception', e)

# TODO:
# Implement create plan type
@plan_management_bp.route('/plan_type', methods=['POST'])
def create_plan_type():
    try:
        req_body = request.get_json()
        plan = Plan(req_body['plan_type'])
        db.session.add(plan)
        db.session.commit()
        return make_response({"success":True,"message":"Plan schedule created successfully"}, 201)

    except Exception as e:
        print('exception', e)

# TODO:
# Implement update plan type
@plan_management_bp.route('/plan_type/<id>', methods=['PUT'])
def update_plan_type(id):
    try:
        req_body = request.get_json()
        plan_type = Plan.query.filter(Plan.id == id).update({Plan.plan_name : req_body['plan_type']})
        db.session.commit()
        if plan_type == 0:
            return make_response({"success":False,"message":"Plan type Id not found"}, 404)

        return make_response({"success":True,"message":"Plan type updated successfully"}, 201)

    except Exception as e:
        print('exception', e)

# TODO:
# Implement delete plan type
@plan_management_bp.route('/plan_type/<id>', methods=['DELETE'])
def delete_plan_type(id):
    try:
       
        Plan.query.filter_by(id = id).delete()
        db.session.commit()
        return make_response({"success":True,"message":"Plan type deleted successfully"}, 200)


    except Exception as e:
        print('exception', e)


######## Days #########

# TODO:
# Implement List days
@plan_management_bp.route('/day_list', methods=['GET'])
def get_days():
    try:
        days = Day.query.all()
        data = day_schema_list.dump(days)
        return jsonify(data)    
    except Exception as e:
        print('exception', e)

# TODO:
# Implement create day
@plan_management_bp.route('/day', methods=['POST'])
def create_day():
    try:
        req_body = request.get_json()
        day = Day(req_body['day_week_number'], req_body['day'])
        db.session.add(day)
        db.session.commit()
        return make_response({"success":True,"message":"Day created successfully"}, 201)

    except Exception as e:
        print('exception', e)

# TODO:
# Implement update day
@plan_management_bp.route('/day/<id>', methods=['PUT'])
def update_day(id):
    try:
        req_body = request.get_json()
        day = Day.query.filter(Day.id == id).update({Day.day_week_number : req_body['day_week_number'],Day.day: req_body['day']})
        db.session.commit()
        if day == 0:
            return make_response({"success":False,"message":"Day Id not found"}, 404)

        return make_response({"success":True,"message":"Day updated successfully"}, 201)

    except Exception as e:
        print('exception', e)

# TODO:
# Implement delete day
@plan_management_bp.route('/day/<id>', methods=['DELETE'])
def delete_day(id):
    try:
       
        day = Day.query.filter_by(id = id).delete()
        db.session.commit()
        if day == 0:
            return make_response({"success":False,"message":"Day Id not found"}, 404)

        return make_response({"success":True,"message":"Day deleted successfully"}, 200)


    except Exception as e:
        print('exception', e)


######## Timing #########

# TODO:
# Implement List timimng
@plan_management_bp.route('/timing', methods=['GET'])
def get_timings():
    try:
        timings = Timing.query.all()
        data = timing_schema_list.dump(timings)
        return jsonify(data)
    except Exception as e:
        print('exception', e)

# TODO:
# Implement create timing
@plan_management_bp.route('/timing', methods=['POST'])
def create_timing():
    try:
        req_body = request.get_json()
        timing = Timing(req_body['timing_label'])
        db.session.add(timing)
        db.session.commit()
        return make_response({"success":True,"message":"Timing created successfully"}, 201)

    except Exception as e:
        print('exception', e)

# TODO:
# Implement update timing
@plan_management_bp.route('/timing/<id>', methods=['PUT'])
def update_timing(id):
    try:
        req_body = request.get_json()
        timing = Timing.query.filter(Timing.id == id).update({Timing.timing_label : req_body['timing_label']})
        db.session.commit()
        if timing == 0:
            return make_response({"success":False,"message":"Timing Id not found"}, 404)

        return make_response({"success":True,"message":"Timing updated successfully"}, 201)

    except Exception as e:
        print('exception', e)

# TODO:
# Implement delete timing
@plan_management_bp.route('/timing/<id>', methods=['DELETE'])
def delete_timing(id):
    try:
       
        timing = Timing.query.filter_by(id = id).delete()
        db.session.commit()
        if timing == 0:
            return make_response({"success":False,"message":"Timing Id not found"}, 404)
            
        return make_response({"success":True,"message":"Timing deleted successfully"}, 200)


    except Exception as e:
        print('exception', e)


########## Schedule Plan ##########
# TODO:
# Implement create plan schedule ie. createing plans
@plan_management_bp.route('/', methods=['POST'])
def create_plan_schedule():
    try:
        req_body = request.get_json()
        plan = Plan.query.filter_by(id = req_body['plan_type_id']).first()
        if plan == None:
            return make_response({"success":False,"message":"Plan type Id not found"}, 404)
        
        day = Day.query.filter_by(id = req_body['day_id']).first()
        if day == None:
            return make_response({"success":False,"message":"Day Id not found"}, 404)

        timing = Timing.query.filter_by(id = req_body['time_id']).first()
        if timing == None:
            return make_response({"success":False,"message":"Time Id not found"}, 404)

        plan_schedule_data = Plan_Schedule(req_body['plan_type_id'],req_body['day_id'],req_body['time_id'], 1)
        db.session.add(plan_schedule_data)
        db.session.flush()
        db.session.commit()
        return make_response({"success":True,"message":"Plan schedule created successfully"}, 201)
    except Exception as e:
        return jsonify(str(e))



# TODO:
# Implement list Plan schedule without recipe
@plan_management_bp.route('/plan', methods=['GET'])
def list_plan_schedule():
    try:
        plan_schedule_data = Plan_Schedule.query.all()
        plan_data = plan_schedule_without_recipe_schema_list.dump(plan_schedule_data)
        return make_response({"success":True,"data":plan_data}, 200)
    except Exception as e:
        print('exception', e)

    
# TODO:
# Implement update plan schedule
@plan_management_bp.route('/<id>', methods=['PUT'])
def update_plan_schedule(id):
    try:
        payload = request.get_json()
        
        plan = Plan.query.filter_by(id = payload['plan_type_id']).first() 
        if plan == None:
            return make_response({"success":False,"message":"Plan type Id not found"}, 404)
        
        day = Day.query.filter_by(id = payload['day_id']).first()
        if day == None:
            return make_response({"success":False,"message":"Day Id not found"}, 404)

        timing = Timing.query.filter_by(id = payload['time_id']).first()
        if timing == None:
            return make_response({"success":False,"message":"Time Id not found"}, 404)

        plan_schedule = Plan_Schedule.query.filter_by(id = id).first()
        if plan_schedule == None:
            return make_response({"success":False,"message":"Plan Schedule Id not found"}, 404)

        plan_schedule.plan_id = payload['plan_type_id']
        plan_schedule.day_id = payload['day_id']
        plan_schedule.time_id = payload['time_id']
        db.session.commit()
        return make_response({"success":True,"message":"Plan Schedule updated successfully"}, 200)
    except Exception as e:
        print('exception', e)



# TODO:
# Implement delete plan schedule
@plan_management_bp.route('/<id>', methods=['DELETE'])
def delete_plan_management(id):
    try:
        plan_schedule = Plan_Schedule.query.filter_by(id = id).first()
        if plan_schedule == None:
            return make_response({"success":False,"message":"Planed schedule Id not found"}, 404)

        Plan_Schedule.query.filter_by(id = id).delete()
        db.session.commit()
        return make_response({"success":True,"message":"Plan schedule deleted successfully"}, 200)

    except Exception as e:
        print('exception', e)
        return jsonify(str(e))





# TODO:
# Implement create a meal plan
@plan_management_bp.route('/planMeal', methods=['POST'])
def create_meal_plan():
    try:
      
        req_body = request.get_json()

        recipe_id = req_body['recipe_id']
        schedule_id = req_body['schedule_id']
        serving_unit_id = req_body['serving_unit_id']
        quantity = req_body['quantity']

        plan_schedule = Plan_Schedule.query.filter_by(id = schedule_id).first()
        if plan_schedule == None:
            return make_response({"success":False,"message":"Planed schedule Id not found"}, 404)

        recipe = Recipe.query.filter_by(id = recipe_id).first()
        if recipe == None:
            return make_response({"success":False,"message":"recipe Id not found"}, 404)

        serving = IngredientServingUnit.query.filter_by(id = serving_unit_id).first()
        if serving == None:
            return make_response({"success":False,"message":"serving unit Id not found"}, 404)

        print('planed schedule', plan_schedule)
        print('recipe', recipe)
        # plan_schedule.recipes.append(recipe)

        
       
        a = Planned_Meal(recipe_id,schedule_id,serving_unit_id,quantity)
        db.session.add(a)
        # db.session.execute(Planned_Meal.insert(),params={"recipe_id": recipe_id, "serving_unit_id": serving_unit_id, "schedule_id": schedule_id,"quantity":quantity},)         
        db.session.commit()
        return make_response({"success":"Meal planned successfully"}, 201)
    except Exception as e:
        return jsonify(str(e))

# TODO:
# Implement create a meal plan by name
@plan_management_bp.route('/planMealByName', methods=['POST'])
def create_meal_plan_by_name():
    try:
      
        req_body = request.get_json()

        recipe_name = req_body['recipe']
        plan_name = req_body['plan']
        day_name = req_body['day']
        timing = req_body['time']
        quantity = req_body['quantity']
        serving_unit_payload = req_body['serving_unit']

        print('request', req_body)
        plan_object = Plan.query.filter(func.lower(Plan.plan_name) == func.lower(plan_name)).first()
        if plan_object == None:
            return make_response({"success":False,"message":"Planed name not found"}, 404)

        day_object = Day.query.filter(func.lower(Day.day) == func.lower(day_name)).first()
        if day_object == None:
            return make_response({"success":False,"message":"Day not found"}, 404)

        timing_object = Timing.query.filter(func.lower(Timing.timing_label) == func.lower(timing)).first()
        if timing_object == None:
            return make_response({"success":False,"message":"Timing not found"}, 404)

        serving_data = IngredientServingUnit.query.all()
        serving_unit_list = serving_unit_schema_list.dump(serving_data)

        matched_serving_unit = None
        for serving_unit in serving_unit_list:
            print('serving_unit', serving_unit)
            if serving_unit_payload == serving_unit['serving_unit_name'].lower() or serving_unit_payload in serving_unit['serving_unit_othername']:
                matched_serving_unit = serving_unit
                print('serving_unit matched', serving_unit)
                break
        print('matched unit', matched_serving_unit)
        
        if matched_serving_unit == None:
            return make_response({"success":False,"message":"Serving unit not found"}, 404)

        # serving = IngredientServingUnit.query.filter(func.lower(IngredientServingUnit.serving_unit_name) == func.lower(serving_unit)).first()
        # if serving == None:
           


        recipe = Recipe.query.filter(func.lower(Recipe.recipe_name) == func.lower(recipe_name)).first()
        if recipe == None:
            return make_response({"success":False,"message":"recipe not found"}, 404)

        print('planid', plan_object.id)
        print('dayid', day_object.id)
        print('timing', timing_object.id)
        print('recipe', recipe.id)
        print('serving', matched_serving_unit)



        plan_schedule = Plan_Schedule.query.filter(Plan_Schedule.day_id == day_object.id, Plan_Schedule.time_id == timing_object.id, Plan_Schedule.plan_id == plan_object.id).first()
        if plan_schedule == None:
            return make_response({"success":False,"message":"Planed schedule Id not found"}, 404)

       
        print('planed schedule', plan_schedule)
        print('recipe', recipe)
    
       
        a = Planned_Meal(recipe.id,plan_schedule.id,matched_serving_unit['id'],quantity)
        db.session.add(a)
        db.session.commit()
        return make_response({"success":"Meal planned successfully"}, 201)
    except Exception as e:
        return jsonify(str(e))



# TODO:
# Implement create a meal plan
@plan_management_bp.route('/delete-planned-meal', methods=['POST'])
def delete_meal_plan():
    try:
      
        req_body = request.get_json()

        recipe_id = req_body['recipe_id']
        schedule_id = req_body['schedule_id']

        plan_schedule = Plan_Schedule.query.filter_by(id = schedule_id).first()
        if plan_schedule == None:
            return make_response({"success":False,"message":"Planed schedule Id not found"}, 404)

        recipe = Recipe.query.filter_by(id = recipe_id).first()
        if recipe == None:
            return make_response({"success":False,"message":"recipe Id not found"}, 404)

        print('planed schedule', plan_schedule)
        print('recipe', recipe)
        plan_schedule.recipes.remove(recipe)
        db.session.commit()
        return make_response({"success":"Meal plan deleted successfully"}, 201)
    except Exception as e:
        return jsonify(str(e))


# TODO: Update API url to /plan/<plan_id>/day/<day_id>
# Implement get meal plan from plan id and day id
@plan_management_bp.route('/<planId>/<dayId>', methods=['GET'])
def list_meal_plan_schedule(planId, dayId):
    try:
        t1 = time.time()

        plan_schedule_data = Plan_Schedule.query.filter_by(plan_id = planId, day_id = dayId).all()
        print('plan_schedule_data', len(plan_schedule_data[0].recipes))

        t2 = time.time()
        print('Schedule Query Time : ', round(t2 - t1, 3))
        plan_data = plan_schedule_schema_list.dump(plan_schedule_data)

        t3 = time.time()
        print('Schedule Query Dump Time : ', round(t3 - t2, 3))
        if len(plan_data) == 0:
           return make_response({"success":False,"message":"Invalid plan id or day id"}, 200)

        data = {}
        if len(plan_data):
             data["success"] = True
             data["Id"] = plan_data[0]['plan']['id']
             data["plan_id"] = planId
             data["plan_name"] = plan_data[0]['plan']['plan_name']
             data["day"] = dayId
             data["day_name"] = plan_data[0]["day"]['day']

        for plan in plan_data:
           
            for recipe in plan['recipes']:
                print('recipe_id', recipe['id'])
                t4 = time.time()
                planned_meal_data = Planned_Meal.query.filter(Planned_Meal.recipe_id == recipe['id'], Planned_Meal.schedule_id == plan['id']).first()
                t5 = time.time()
                meal_data = plan_meal_schema.dump(planned_meal_data)
                t6 = time.time()

                recipe = process_planned_meal_recipe(recipe, meal_data)
                recipe['per_serving_wt'] = recipe['per_serving']
                del recipe['per_serving']
                recipe['serving']['total_serving_wt'] = recipe['per_serving_wt']*recipe['serving']['quantity']
                del recipe['serving']['size']



            data[plan['timing']['timing_label']] = plan['recipes']
        t8 = time.time()
        print('Time Processing : ', round(t8-t1, 3))
        return jsonify(data)

      
    except Exception as e:
        print('exception', e)


# TODO: Update API url to /plan/<plan_id>/day/<day_id>/new
# Implement get meal plan from plan id and day id
@plan_management_bp.route('/<planId>/<dayId>/new', methods=['GET'])
def list_meal_plan_schedule_new(planId, dayId):
    try:

        t1 = time.time()

        plan_schedule_data = Plan_Schedule.query.filter_by(plan_id=planId, day_id=dayId).all()
        print('plan_schedule_data', len(plan_schedule_data[0].recipes))

        t2 = time.time()
        print('Schedule Query Time : ', round(t2 - t1, 3))

        if len(plan_schedule_data) == 0:
            return make_response({"success": False, "message": "Invalid plan id or day id"}, 200)

        data = {}
        if len(plan_schedule_data):
            data["success"] = True
            # data["Id"] = plan_schedule_data[0]['plan']['id']
            data["Id"] = planId
            data["plan_id"] = planId
            data["plan_name"] = plan_schedule_data[0].plan.plan_name
            data["day"] = dayId
            data["day_name"] = plan_schedule_data[0].day.day

        for plan in plan_schedule_data:
            details = []
            t3 = time.time()
            recipe_objs = recipe_schema_list.dump(plan.recipes)
            t4 = time.time()

            print('Dump Time : ', round(t4 - t3, 3))

            for recipe in recipe_objs:
                print('recipe_id', recipe['id'])
                t5 = time.time()
                planned_meal_data = Planned_Meal.query.filter(Planned_Meal.recipe_id == recipe['id'],
                                                              Planned_Meal.schedule_id == plan.id).first()
                t6 = time.time()
                print('\t plan meal query ',  round(t6 - t5, 3))
                meal_data = {'quantity': planned_meal_data.quantity,
                             'serving':  {'unit': planned_meal_data.serving.serving_unit_name,
                                          'size': planned_meal_data.serving.serving_unit_quantity}}
                print(meal_data)
                # meal_data = plan_meal_schema.dump(planned_meal_data)
                t7 = time.time()
                print('\t plan meal dump ', round(t7 - t6, 3))
                details.append(process_planned_meal_recipe(recipe, meal_data))

            print('schedule ', plan.timing.timing_label)
            data[plan.timing.timing_label] = details
        t8 = time.time()
        print('Time Processing : ', round(t8 - t1, 3))
        return jsonify(data)

    except Exception as e:
        print('exception', e)


@plan_management_bp.route('/plan/search', methods=['GET'])
def search_plan_schedule():
    """
    Search plan schedule by plan name and day

    Query Parameters:
    - `plan_name`: Plan name to search
    - `day`: Day to search

    Returns:
    - `plans`: List of 
    """
    try:
        plan_name = request.args.get('plan_name', None)
        day = request.args.get('day', None)

        if plan_name == None or day == None:
            return make_response({"success":False,"message":"Plan name and day is required"}, 400)

        # Get plan ids for the given plan name
        plans_data = Plan.query.filter(Plan.plan_name.ilike(f'%{plan_name}%')).all()
        plan_ids = [plan.id for plan in plans_data]

        # Get day id for the given day name
        day = Day.query.filter(Day.day.ilike(f'%{day}%')).first()
        if day == None:
            return make_response({"success":False,"message":"Day not found"}, 404)
        
        # Get plan schedules for the given plan ids and day id
        plan_schedule_data = Plan_Schedule.query.filter(Plan_Schedule.plan_id.in_(plan_ids), Plan_Schedule.day_id == day.id).all()
        plan_data = plan_schedule_schema_list.dump(plan_schedule_data)

        # Group plan data
        plans = {}
        # Construct recipe data for each plan_schedule
        for plan in plan_data:
            plan_name = plan['plan']['plan_name']

            # Add plan name to response data if not already present
            if plan_name not in plans.keys():
                plans[plan_name] = {
                    'plan_id': plan['plan']['id'],
                    'plan_name': plan_name,
                    'day': day.day,
                    'day_id': day.id,
                }

            # Construct recipe data for each recipe in the plan
            for recipe in plan['recipes']:
                planned_meal_data = Planned_Meal.query.filter(Planned_Meal.recipe_id == recipe['id'], Planned_Meal.schedule_id == plan['id']).first()
                meal_data = plan_meal_schema.dump(planned_meal_data)

                recipe = process_planned_meal_recipe(recipe, meal_data)

            plans[plan_name][plan['timing']['timing_label']] = plan['recipes']
           
        # Response data
        response_data = {
            "success": True,
            "plans": plans
        }

        return make_response(response_data, 200)

    except Exception as e:
        print('exception', e)
        make_response({"success":False,"message":"Something went wrong"}, 500)


@plan_management_bp.route('/plan/<plan_id>', methods=['GET'])
def get_plan_details(plan_id):
    """
    Get plan details by plan id
    
    - `plan_id`: Plan id to search

    Returns:
    - `plan_details`: Plan details (Recipe list for each day)
    """
    try:
        # Check if plan exists
        found_plan = Plan.query.get(plan_id)
        if found_plan == None:
            return make_response({"success":False,"message":"Plan not found"}, 404)

        #  Get plan schedules for the given plan id
        plan_schedules = Plan_Schedule.query.filter_by(plan_id = plan_id).all()
        plans_data = plan_schedule_schema_list.dump(plan_schedules)

        # Construct plan details
        plan_details = {}
        for plan in plans_data:

            # Skip if there are no recipes for the plan
            if len(plan['recipes']) == 0:
                continue

            day = plan['day']
            timing = plan['timing']

            # Add day to plan details if not already present
            if day['day'] not in plan_details.keys():
                plan_details[day['day']] = {}
            
            # Format recipe data
            recipes = []
            for recipe in plan['recipes']:
                recipe_data = {
                    "recipe_id": recipe['id'],
                    "recipe_name": recipe['recipe_name'],
                    "serving": get_planned_meal_serving_details(recipe['id'], plan['id'])
                }
                recipes.append(recipe_data)

            # Add details for each timing
            plan_details[day['day']][timing['timing_label']] = {
                "schedule_id": plan['id'],
                "total_recipes": len(recipes),
                "recipes": recipes
            }

        # Response data
        response_data = {
            "success": True,
            "plan_id": plan_id,
            "plan_name": found_plan.plan_name,
            "plan_details": plan_details
        }

        return make_response(response_data, 200)

    except Exception as e:
        print('exception', e)
        make_response({"success":False, "message":"Something went wrong"}, 500)


# TODO:
# Implement auto schedule plan
@plan_management_bp.route('/auto-schedule', methods=['GET'])
def auto_plan_schedule():
    try:
       
        plan = Plan.query.all()
        day = Day.query.all()
        timing = Timing.query.all()
        
        plan_list = plan_schema_list.dump(plan)
        day_list = day_schema_list.dump(day)
        timing_list = timing_schema_list.dump(timing)
        print('plan_list', plan_list)
        print('day_list', day_list)
        print('timing_list', timing_list)
        for plan in plan_list:
            try:
                for day in day_list:
                    for timing in timing_list:
                        plan_schedule = Plan_Schedule(plan['id'],day['id'],timing['id'],None)
                        db.session.add(plan_schedule)
                db.session.commit()
            except Exception as e:
                db.session.rollback()


        # db.session.commit()
        return make_response({"success":True,"message":"Plan Scheduled successfully"}, 200)
    except Exception as e:
        print('exception', e)



# TODO:
# Implement get plan schedule by id
@plan_management_bp.route('/<id>', methods=['GET'])
def plan_schedule_by_id(id):
    try:
        plan_schedule = Plan_Schedule.query.filter_by(id = id).first()
        if plan_schedule == None:
            return make_response({"success":False,"message":"Plan schedule Id not found"}, 404)
        else:
            return make_response({"success":True,"data":plan_schedule_schema.dump(plan_schedule)}, 200)
    except Exception as e:
        print('exception', e)




#for logging all the requests

@plan_management_bp.after_request
def after_request_cal(response):
    api_logger.after_request(request,response)
    return response
    

@plan_management_bp.errorhandler(Exception)
def exceptions(e):
    api_logger.exceptions(request,e)
    return e.status_code