from dataclasses import field
from extensions import ma
from models.nin_ingredient_model import NIN_Ingredient
from marshmallow import Schema, fields, ValidationError, pre_load

class DaySchema(Schema):
    id = fields.Int(dump_only=True)
    day = fields.Str()
    day_week_number = fields.Int()
   