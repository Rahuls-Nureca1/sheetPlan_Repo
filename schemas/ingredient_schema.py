from dataclasses import field
from extensions import ma
from models.nin_ingredient_model import NIN_Ingredient
from marshmallow import Schema, fields, ValidationError, pre_load

class IngredientSchema(Schema):

    id = fields.Int(dump_only = True)
    recipe_id = fields.Int()
    nin_id = fields.Int()
    ingredient_name = fields.Str()
    ingredient_desc = fields.Str()
    quantity = fields.Float()
    quantity_in_gram = fields.Int()
    serving_unit_id = fields.Int()
    serving_unit = fields.Str()
 
        