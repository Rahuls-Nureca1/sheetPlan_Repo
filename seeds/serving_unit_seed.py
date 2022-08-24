from flask_seeder import Seeder
from extensions import db
from models.ingredient_serving_unit_model import IngredientServingUnit

# All seeders inherit from Seeder
class IngredientServingUnitSeeder(Seeder):
  
  # run() will be called by Flask-Seeder
 
  def run(self):
    serving = [
      {"serving_unit_name":'Small Bowl',"serving_unit_quantity": 150},
        {"serving_unit_name":'Katori',"serving_unit_quantity": 150},
        {"serving_unit_name":'Bowl',"serving_unit_quantity": 350},
        {"serving_unit_name":'Cup',"serving_unit_quantity": 180},
        {"serving_unit_name":'Soup Bowl',"serving_unit_quantity": 180},
        {"serving_unit_name":'Big Katori',"serving_unit_quantity": 180},
        {"serving_unit_name":'mug',"serving_unit_quantity": 250},
        {"serving_unit_name":'Large glass',"serving_unit_quantity": 350},
        {"serving_unit_name":'Table spoon',"serving_unit_quantity": 15},
        {"serving_unit_name":'Tea spoon',"serving_unit_quantity": 5},
        {"serving_unit_name":'gram',"serving_unit_quantity": 1},
        {"serving_unit_name":'ml',"serving_unit_quantity": 1},
        {"serving_unit_name":'Pieces',"serving_unit_quantity": 20},
        {"serving_unit_name":'Small',"serving_unit_quantity": 35},
        {"serving_unit_name":'Medium',"serving_unit_quantity": 60},
        {"serving_unit_name":'Large',"serving_unit_quantity": 100},
        {"serving_unit_name":'Slice',"serving_unit_quantity": 20},
        {"serving_unit_name":'Whole fruit',"serving_unit_quantity": 120},
        {"serving_unit_name":'Fist',"serving_unit_quantity": 30},
        {"serving_unit_name":'Scoop',"serving_unit_quantity": 30},
        {"serving_unit_name":'Pint',"serving_unit_quantity": 250},
        {"serving_unit_name":'Bottel',"serving_unit_quantity": 1000},
        {"serving_unit_name":'Sachet',"serving_unit_quantity": 5},
        {"serving_unit_name":'Can',"serving_unit_quantity": 300},
        {"serving_unit_name":'Ounce',"serving_unit_quantity": 28},
        {"serving_unit_name":'Liter',"serving_unit_quantity": 1000},
        {"serving_unit_name":'Pack',"serving_unit_quantity": 100},
        {"serving_unit_name":'Pinch',"serving_unit_quantity": 1},

      
      ]
 
    for i in range(0,28):
      serving_unit = IngredientServingUnit(serving[i]['serving_unit_name'],serving[i]['serving_unit_quantity'],None)
      db.session.add(serving_unit)
      db.session.commit()