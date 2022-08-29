from marshmallow import Schema, fields

from schemas.ingredient_schema import IngredientSchema


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
    micros = fields.Nested(MicrosSchema)
    recipe_url = fields.Str()
    website_name = fields.Str()
    serving = fields.Int()
    ingredients = fields.Nested(IngredientSchema)
    # deleted = fields.Bool()


        