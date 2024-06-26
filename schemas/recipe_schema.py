from marshmallow import Schema, fields,  validates, ValidationError
import datetime
from models.plan_schedule_model import Planned_Meal
from schemas.ingredient_schema import IngredientSchema
from schemas.ingredient_serving_unit_schema import DefaultServingUnitSchema
import collections
import functools
import operator




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
    ingredients = fields.Nested(IngredientSchema, many=True)
    macros = fields.Method("calculate_macros")
    micros= fields.Method("calculate_micros")
    per_serving = fields.Method("calculate_per_serving")
    plan_Schedule = fields.Nested(Planned_Meal,many=True)

    def calculate_macros(self, obj):
        macros = []
        
        for i in obj.ingredients:
            for key in i.macros:
                macros.append({key: i.macros[key]})
          
        #     macros.append(i.macros)
        counter = collections.Counter()
        for d in macros:
            counter.update(d)

        res = dict(counter)
        formated_macros=[]
        for key in res:
            formated_macros.append({
                'key': key,
                'value': float(res[key]),
                'unit': 'g' if key != 'energy' else 'kcal'
            })

        return formated_macros

    def calculate_micros(self, obj):
        micros = []
        
        for i in obj.ingredients:
            for key in i.micros:
                micros.append({key: i.micros[key]})
          
        #     macros.append(i.macros)
        counter = collections.Counter()
        for d in micros:
            counter.update(d)

        res = dict(counter)
        formated_micros=[]
        for key in res:
            formated_micros.append({
                'key': key,
                'value': res[key],
                'unit': 'g'
            })

        return formated_micros
   
    def calculate_per_serving(self, obj):
        per_serving = 0
        
        for i in obj.ingredients:
            if i.quantity_in_gram != None:
                per_serving += i.quantity_in_gram
          
        per_serving = per_serving / obj.serving

        return per_serving
   



class CreateIngredientSchema(Schema):
    ingredient_name = fields.Str(required=True, allow_none=False)
    ingredient_standard_name = fields.Str(required=True,allow_none=False)
    ingredient_desc = fields.Str(required=True,allow_none=False)
    quantity = fields.Int(required=True,allow_none=False)
    quantity_in_gram = fields.Int(required=True,allow_none=True)
    serving_unit = fields.Str(required=True,allow_none=False)
    nin_id = fields.Int(required=True,allow_none=True)


class PlanRecipeSchema(RecipeSchema):
    default_serving_unit = fields.Nested(DefaultServingUnitSchema,many=False)