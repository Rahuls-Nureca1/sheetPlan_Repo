
from marshmallow import Schema, fields

class NININgredientSchema(Schema):
    id = fields.Int(dump_only=True)
    nin_code = fields.Str()
    ingredient_name = fields.Str()
    ingredient_description = fields.Str()
    macros = fields.Raw()
    micros = fields.Raw()

    # formatted_name = fields.Method("format_name", dump_only=True)

    # def format_name(self, author):
    #     return f"{author.last}, {author.first}"

    # class Meta:
    #     model = NIN_Ingredient
    #     load_instance = True
    #     load_only = ("store",)
    #     include_fk= True

        