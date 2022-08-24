from extensions import ma
from models.nin_ingredient_model import NIN_Ingredient
from marshmallow import Schema, fields, ValidationError, pre_load

class PlanSchema(Schema):
    id = fields.Int(dump_only=True)
    plan_name = fields.Str()
   