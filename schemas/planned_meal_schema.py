from marshmallow import Schema, fields
from schemas.recipe_schema import RecipeSchema
from schemas.plan_schedule_schema import PlanScheduleSchema


class PlannedMealSchema(Schema):
    id = fields.Int(dump_only=True)
    # recipeId = fields.Nested(RecipeSchema, many=False)
    # schedule_id = fields.Nested(PlanScheduleSchema, many=False)
    planned_by = fields.Int()
    recipe = fields.Nested(RecipeSchema, many=False)
    plan_schedule = fields.Nested(PlanScheduleSchema, many=False)
    
    # updated_by = fields.Date()

