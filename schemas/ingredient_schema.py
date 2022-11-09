from marshmallow import Schema, fields
from schemas.ingredient_serving_unit_schema import DefaultServingUnitSchema
from schemas.nin_ingredient_schema import NININgredientSchema

class IngredientSchema(Schema):

    id = fields.Int(dump_only = True)
    recipe_id = fields.Int()
    nin_id = fields.Int()
    ingredient_name = fields.Str()
    ingredient_desc = fields.Str()
    ingredient_standard_name = fields.Str()
    quantity = fields.Float()
    quantity_in_gram = fields.Int()
    serving_unit_id = fields.Int()
    serving_unit = fields.Str()
    macros = fields.Raw()
    micros = fields.Raw()

class IngredientDetailsUpdateSchema(IngredientSchema):
    serving_unit_details = fields.Nested(DefaultServingUnitSchema,many=False)
    nin_details = fields.Nested(NININgredientSchema,many=False)
        