from statistics import quantiles
from marshmallow import Schema, fields
from models.plan_schedule_model import Planned_Meal
from schemas.plan_schema import PlanSchema
from schemas.day_schema import DaySchema
from schemas.recipe_schema import RecipeSchema,PlanRecipeSchema
from schemas.timing_schema import TimingSchema
from schemas.ingredient_serving_unit_schema import ServingUnitSchema

class PlannedMealSchema(Schema):
    serving = fields.Nested(ServingUnitSchema, many=False)
    quantity = fields.Float()
    # class Meta:
    #     model = Planned_Meal
    #     fields = [ 'quantity', 'recipe']

 

class PlanScheduleSchema(Schema):
    id = fields.Int()
    plan = fields.Nested(PlanSchema, many=False)
    day = fields.Nested(DaySchema, many=False)
    timing = fields.Nested(TimingSchema, many=False)
    recipes = fields.Nested(RecipeSchema, many=True)
    servings = fields.Nested(ServingUnitSchema, many=True)
    # quantity = fields.Nested(PlannedMealSchema, many=True)




class PlanScheduleWithoutRecipeSchema(Schema):
    id = fields.Int(dump_only=True)
    plan = fields.Nested(PlanSchema, many=False)
    day = fields.Nested(DaySchema, many=False)
    timing = fields.Nested(TimingSchema, many=False)



class DefaultServingPlanScheduleSchema(PlanScheduleSchema):
    recipes = fields.Nested(PlanRecipeSchema, many=True)