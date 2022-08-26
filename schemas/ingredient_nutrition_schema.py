
from marshmallow import Schema, fields

class IngredientNutritionSchema(Schema):

    id = fields.Int(dump_only = True)
    ingredient_id = fields.Int()
    nutrition_type = fields.Str()
    nutrition_name = fields.Str()
    nutrition_value = fields.Str()
   
        