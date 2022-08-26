from cmath import log
from flask_seeder import Seeder
from extensions import db
from models.ingredient_serving_unit_model import IngredientServingUnit
import json
import os
dirname = os.path.dirname(__file__)

# All seeders inherit from Seeder
class IngredientServingUnitSeeder(Seeder):
  
  # run() will be called by Flask-Seeder
  def run(self):
    filename = os.path.join(dirname, './data/serving_unit.json')
    with open(filename) as file:
      data = json.load(file)
      serving = data['serving_units']
      print('length', len(serving))
 
    for i in range(0,len(serving)):
      serving_unit = IngredientServingUnit(serving[i]['serving_unit_name'], serving[i]['serving_unit_othername'],serving[i]['serving_unit_quantity'],None)
      db.session.add(serving_unit)
    db.session.commit()