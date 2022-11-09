from models.ingredient_model import Ingredient
from schemas.ingredient_schema import IngredientDetailsUpdateSchema
from extensions import db
from marshmallow import ValidationError

ingredient_schema_list = IngredientDetailsUpdateSchema(many=True)

def update_ingredient_weight(nin_id, serving_size, ingredient_serving_unit):
    try:
        data = Ingredient.query.filter(Ingredient.nin_id == nin_id).all()
        ingredient_list = ingredient_schema_list.dump(data)
        print(ingredient_list)
        if len(ingredient_list):
            for ingredient in ingredient_list:
                
                serving_unit_ratio = ingredient['serving_unit_details']['serving_unit_quantity']/ingredient_serving_unit

                quantity_in_gram = ingredient['quantity']*serving_unit_ratio*serving_size
                
                updated_ingredient = Ingredient.query.filter_by(id=ingredient['id']).update(
                    {
                        'quantity_in_gram': quantity_in_gram,
                        'macros': update_macros_per_weight(ingredient['nin_details']['macros']),
                        'micros': update_micros_per_weight(ingredient['nin_details']['micros'])
                    }
                )

                if updated_ingredient:
                    db.session.commit()
                    print(ingredient)
                    print(updated_ingredient)
                else:
                    print("ingredient update failed")

    except ValidationError as err:
        print(err.messages)
        print(err.valid_data)
        
    except Exception as e:
        print('exception', e)
        db.session.rollback()
            

def update_macros_per_weight(macros,quantity_in_gram):
    multiplication_factor = quantity_in_gram/100
    for key in macros:
        if macros[key] == '':
            macros[key] = 0
        macros[key] = round(float(macros[key]) * multiplication_factor, 2)
    
    return macros

def update_micros_per_weight(micros, quantity_in_gram):
    multiplication_factor = quantity_in_gram/100
    for key in micros:
        if micros[key] == '':
            micros[key] = 0
        micros[key] = round(float(micros[key]) * multiplication_factor, 3)
    
    return micros