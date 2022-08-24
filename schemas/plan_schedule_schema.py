from dataclasses import field
from extensions import ma
from models.nin_ingredient_model import NIN_Ingredient
from marshmallow import Schema, fields, ValidationError, pre_load

from schemas.plan_schema import PlanSchema
from schemas.day_schema import DaySchema
from schemas.timing_schema import TimingSchema


class PlanScheduleSchema(Schema):
    id = fields.Int(dump_only=True)
    # plan_id = fields.Int()
    # day_id = fields.Int()
    # time_id = fields.Int()
    plan = fields.Nested(PlanSchema, many=False)
    day = fields.Nested(DaySchema, many=False)
    timing = fields.Nested(TimingSchema, many=False)
    # updated_by = fields.Date()

