from marshmallow import Schema, fields
import datetime
from schemas.ingredient_schema import IngredientSchema
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
                'value': int(res[key]),
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
          
       

        return per_serving
   


        