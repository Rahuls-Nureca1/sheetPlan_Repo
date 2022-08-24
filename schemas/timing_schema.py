from dataclasses import field
from extensions import ma
from models.nin_ingredient_model import NIN_Ingredient
from marshmallow import Schema, fields, ValidationError, pre_load

class TimingSchema(Schema):
    id = fields.Int(dump_only=True)
    timing_label = fields.Str()
    created_at = fields.DateTime()
   