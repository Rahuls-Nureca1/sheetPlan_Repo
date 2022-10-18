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




qc_plan_management_bp = Blueprint('plan_management', __name__)

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

# Implement get meal plan from plan id and day id
@qc_plan_management_bp.route('/<planId>/<dayId>', methods=['GET'])
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
            
            total_calories = 0
            for recipe in plan['recipes']:
                print('recipe_id', recipe['id'])
                t4 = time.time()
                planned_meal_data = Planned_Meal.query.filter(Planned_Meal.recipe_id == recipe['id'], Planned_Meal.schedule_id == plan['id']).first()
                t5 = time.time()
                meal_data = plan_meal_schema.dump(planned_meal_data)
                t6 = time.time()

                recipe = process_planned_meal_recipe(recipe, meal_data)
                macros = recipe['macros']
                total_calories+= [mac['value'] for mac in macros if mac['key']=='energy'][0]

            data[plan['timing']['timing_label']] = {"no_of_recipes": len(
                plan['recipes']), "total_calories": total_calories, "recipes": plan['recipes']}
            
        t8 = time.time()
        print('Time Processing : ', round(t8-t1, 3))
        return jsonify(data)

      
    except Exception as e:
        print('exception', e)

