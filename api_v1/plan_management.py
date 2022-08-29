from cmath import log
from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.plan_schedule_model import Plan_Schedule
from schemas.plan_schedule_schema import PlanScheduleSchema

from models.day_model import Day
from schemas.day_schema import DaySchema
from models.timing_model import Timing
from schemas.timing_schema import TimingSchema

from models.plan_model import Plan
from schemas.plan_schema import PlanSchema



# from models.planed_meal_model import PlannedMeal
# from schemas.planned_meal_schema import PlannedMealSchema


from models.recipe_model import Recipe
from schemas.recipe_schema import RecipeSchema

from time import strftime
from utils import api_logger




plan_management_bp = Blueprint('plan_management', __name__)

plan_schedule_schema = PlanScheduleSchema()
plan_schedule_schema_list = PlanScheduleSchema(many = True)

day_schema = DaySchema()
day_schema_list = DaySchema(many = True)

timing_schema = TimingSchema()
timing_schema_list = TimingSchema(many = True)

plan_schema = PlanSchema()
plan_schema_list = PlanSchema(many = True)


# TODO:
# Implement create plan schedule ie. createing plans
@plan_management_bp.route('/', methods=['POST'])
def create_plan_schedule():
    try:
        req_body = request.get_json()
        plan_schedule_data = Plan_Schedule(req_body['plan_id'],req_body['day_id'],req_body['time_id'], 1)
        db.session.add(plan_schedule_data)
        db.session.flush()
        db.session.commit()
        return make_response({"success":"Plan schedule created successfully"}, 201)
    except Exception as e:
        return jsonify(str(e))
        

# TODO:
# Implement create a meal plan
@plan_management_bp.route('/planMeal', methods=['POST'])
def create_meal_plan():
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
        plan_schedule.recipes.append(recipe)
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



# TODO:
# Implement get meal plan from plan id and day id
@plan_management_bp.route('/<planId>/<dayId>', methods=['GET'])
def list_meal_plan_schedule(planId, dayId):
    try:
        
        plan_schedule_data = Plan_Schedule.query.filter_by(plan_id = planId, day_id = dayId).all()
        plan_data = plan_schedule_schema_list.dump(plan_schedule_data)

        if len(plan_data) == 0:
           return make_response({"success":False,"message":"Invalid plan id or day id"}, 200)

        # print(plan_data)
        data = {}
        if len(plan_data):
             data["success"] = True
             data["Id"] = plan_data[0]['plan']['id']
             data["plan_id"] = planId
             data["plan_name"] = plan_data[0]['plan']['plan_name']
             data["day"] = dayId
             data["day_name"] = plan_data[0]["day"]['day']

        for plan in plan_data:
            # plan['recipes']['macros'] = {}
            # plan['recipes']['micros'] = {}
            data[plan['timing']['timing_label']] = plan['recipes']
            print('plan', plan)

        print("data",data)
        


        return make_response(data, 200)
    except Exception as e:
        print('exception', e)




# TODO:
# Implement list Plan schedule
@plan_management_bp.route('/', methods=['GET'])
def list_plan_schedule():
    try:
        plan_schedule_data = Plan_Schedule.query.all()
        plan_data = plan_schedule_schema_list.dump(plan_schedule_data)
        return make_response({"success":True,"data":plan_data}, 200)
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
# Implement update plan schedule
@plan_management_bp.route('/<id>', methods=['PUT'])
def update_plan_schedule(id):
    try:
        payload = request.get_json()
        plan_schedule = Plan_Schedule.query.filter_by(id = id).first()
        if plan_schedule == None:
            return make_response({"success":False,"message":"Plan Schedule Id not found"}, 404)

        plan_schedule.plan_id = payload['plan_id']
        plan_schedule.day_id = payload['day_id']
        plan_schedule.time_id = payload['time_id']
        db.session.commit()
        return make_response({"success":True,"message":"Plan Schedule updated successfully"}, 200)
    except Exception as e:
        print('exception', e)



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