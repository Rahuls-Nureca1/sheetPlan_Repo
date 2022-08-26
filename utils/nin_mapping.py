import traceback
from time import strftime
import logging

from sqlalchemy import Unicode, and_
from models.nin_ingredient_model import NIN_Ingredient
from schemas.nin_ingredient_schema import NININgredientSchema


nin_schema_list = NININgredientSchema(many=True)

def map_ingredient(item_name):
    data = NIN_Ingredient.query.filter(NIN_Ingredient.ingredient_name.ilike(f'%{item_name}%')).all()
    if len(data) == 0:
        return []
    final_data = nin_schema_list.dump(data)
    return final_data
