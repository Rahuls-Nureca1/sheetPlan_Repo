from extensions import ma
from models.nin_ingredient_model import NIN_Ingredient
from marshmallow import Schema, fields, ValidationError, pre_load

class MacrosSchema(Schema):
    type = fields.String()
    unit = fields.String()
    value = fields.Float()

class MicrosSchema(Schema):
    type = fields.String()
    unit = fields.String()
    value = fields.Float()

class NININgredientSchema(Schema):
    id = fields.Int(dump_only=True)
    nin_code = fields.Str()
    ingredient_name = fields.Str()
    ingredient_description = fields.Str()
    macros = fields.Nested(MacrosSchema)
    micros = fields.Nested(MicrosSchema)

    # formatted_name = fields.Method("format_name", dump_only=True)

    # def format_name(self, author):
    #     return f"{author.last}, {author.first}"

    # class Meta:
    #     model = NIN_Ingredient
    #     load_instance = True
    #     load_only = ("store",)
    #     include_fk= True

        