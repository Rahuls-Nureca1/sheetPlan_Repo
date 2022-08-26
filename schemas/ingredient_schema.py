
from marshmallow import Schema, fields

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
 
        