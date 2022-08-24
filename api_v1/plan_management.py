from flask import Blueprint, request, jsonify, make_response
from extensions import db
from models.plan_schedule_model import Plan_Schedule
from schemas.plan_schedule_schema import PlanScheduleSchema
from time import strftime
from utils import api_logger




plan_management_bp = Blueprint('plan_management', __name__)

plan_schedule_schema = PlanScheduleSchema()
plan_schedule_schema_list = PlanScheduleSchema(many = True)


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
# Implement list Plan schedule
@plan_management_bp.route('/', methods=['GET'])
def list_plan_schedule():
    try:
        plan_schedule_data = Plan_Schedule.query.all()
        print('planSchedule',plan_schedule_data)
        plan_data = plan_schedule_schema_list.dump(plan_schedule_data)
        return make_response({"success":True,"data":plan_data}, 200)
    except Exception as e:
        print('exception', e)


# TODO:
# Implement delete NIN Ingredient
@plan_management_bp.route('/<id>', methods=['DELETE'])
def delete_nin_ingredient(id):
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