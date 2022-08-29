from marshmallow import Schema, fields
from schemas.plan_schema import PlanSchema
from schemas.day_schema import DaySchema
from schemas.recipe_schema import RecipeSchema
from schemas.timing_schema import TimingSchema


class PlanScheduleSchema(Schema):
    id = fields.Int(dump_only=True)
    plan = fields.Nested(PlanSchema, many=False)
    day = fields.Nested(DaySchema, many=False)
    timing = fields.Nested(TimingSchema, many=False)
    recipes = fields.Nested(RecipeSchema, many=True,  only=('course', 'cusine', 'id','image_path', 'recipe_name','serving','macros', 'micros'))

