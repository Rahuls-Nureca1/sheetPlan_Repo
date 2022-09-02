from dataclasses import field
from extensions import ma
from models.nin_ingredient_model import NIN_Ingredient
from marshmallow import Schema, fields, ValidationError, pre_load

class AuthSchema(Schema):
    id = fields.Int(dump_only=True)
    auth_key = fields.Str()
    auth_description = fields.Str()
    status = fields.Bool()
    
 