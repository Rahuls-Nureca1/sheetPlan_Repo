
from marshmallow import Schema, fields


class IngredientServingUnitSchema(Schema):

    id = fields.Int(dump_only = True)
    serving_unit_name = fields.Str()
    serving_unit_othername = fields.Str()
    serving_unit_quantity = fields.Int()
  

        
class ServingUnitSchema(Schema):
    # id = fields.Int(dump_only = True)
    # serving_unit_othername = fields.Str()
    unit = fields.Str(attribute="serving_unit_name")
    size = fields.Int(attribute="serving_unit_quantity")
  

        