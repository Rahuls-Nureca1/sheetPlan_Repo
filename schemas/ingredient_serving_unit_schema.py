
from marshmallow import Schema, fields


class IngredientServingUnitSchema(Schema):

    id = fields.Int(dump_only = True)
    serving_unit_name = fields.Str()
    serving_unit_othername = fields.Str()
    serving_unit_quantity = fields.Int()
  

        