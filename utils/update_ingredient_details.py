import copy

from models.ingredient_model import Ingredient
from schemas.ingredient_schema import IngredientDetailsUpdateSchema
from extensions import db
from marshmallow import ValidationError

ingredient_schema_list = IngredientDetailsUpdateSchema(many=True)

def update_ingredient_weight(nin_details, serving_size, ingredient_serving_unit):
    try:
        data = Ingredient.query.filter(Ingredient.nin_id == nin_details['id']).all()
        ingredient_list = ingredient_schema_list.dump(data)
        if len(ingredient_list):
            for ingredient in ingredient_list:
                
                print("NIN_Details: ",nin_details)
                serving_unit_ratio = ingredient['serving_unit_details']['serving_unit_quantity']/ingredient_serving_unit
                quantity_in_gram = ingredient['quantity']*serving_unit_ratio*serving_size

                macros = update_nutrients_per_weight(nin_details['macros'], quantity_in_gram=quantity_in_gram)
                micros = update_nutrients_per_weight(nin_details['micros'], quantity_in_gram=quantity_in_gram)
                
                updated_ingredient = Ingredient.query.filter_by(id=ingredient['id']).update(
                    {
                        'quantity_in_gram': quantity_in_gram,
                        'macros': macros,
                        'micros': micros
                    }
                )

                print("Calculated:",micros, macros)

                if updated_ingredient:
                    db.session.commit()
                    
                else:
                    print("ingredient update failed")

    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        
    except Exception as e:
        print('exception', e)
        db.session.rollback()
            

def update_nutrients_per_weight(values,quantity_in_gram):
    multiplication_factor = quantity_in_gram/100
    values_copy = copy.deepcopy(values)
    for key in values_copy:
        if values_copy[key] == '':
            values_copy[key] = 0
        values_copy[key] = round(float(values[key]) * multiplication_factor, 4)
    
    return values_copy
