from extensions import ma
from models.nin_ingredient_model import NIN_Ingredient
from marshmallow import Schema, fields, ValidationError, pre_load


class CourseSchema(Schema):
    type = fields.String()


class CusineSchema(Schema):
    type = fields.String()


class MicrosSchema(Schema):
    type = fields.String()
    unit = fields.String()
    value = fields.Float()

class RecipeSchema(Schema):

    id = fields.Int(dump_only = True)
    recipe_name = fields.Str()
    image_path = fields.Str()
    course = fields.Nested(CourseSchema)
    cusine = fields.Nested(CusineSchema)
    recipe_url = fields.Str()
    website_name = fields.Str()
    serving = fields.Int()
    deleted = fields.Bool()

        