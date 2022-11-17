import json,copy
from difflib import get_close_matches,SequenceMatcher

from sqlalchemy import Unicode, and_
from models.nin_ingredient_model import NIN_Ingredient
from schemas.nin_ingredient_schema import NININgredientSchema


nin_schema_list = NININgredientSchema(many=True)

def map_ingredient(item_name):
    data = NIN_Ingredient.query.filter(NIN_Ingredient.ingredient_description.ilike(f'%{item_name}%')| NIN_Ingredient.ingredient_name.ilike(f'%{item_name}%') ).all()
    if not len(data):
        return []
    final_data = nin_schema_list.dump(data)
    L= []
    for i,ingredient in enumerate(final_data):
        word_list = []
        word_list.extend(json.loads(ingredient["ingredient_description"]))
        word_list.append(ingredient["ingredient_name"])
        word_list =[x.lower() for x in word_list]

        data = {
            "id": i,
            "word_list": word_list
        }

        L.append(data)
    best_match_index,_ = string_matching(L, item_name.lower())
    if best_match_index is not None:
        return [final_data[best_match_index]]
    # No match found
    return final_data

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def string_matching(items_with_keys, item_name):
    
    max = -1
    id_value = None
    best_match_string = None
    for item in items_with_keys:
        match = get_close_matches(item_name, item["word_list"], n=1)
        if len(match):
            if similar(item_name,match[0]) > max:
                max = similar(item_name,match[0])
                id_value = item["id"]
                best_match_string = match[0]

    return id_value,best_match_string

