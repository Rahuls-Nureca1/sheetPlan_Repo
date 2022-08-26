from flask_seeder import Seeder
from extensions import db
from models.nin_ingredient_model import NIN_Ingredient
import json
import os
dirname = os.path.dirname(__file__)

# All seeders inherit from Seeder
class NinSeeder(Seeder):
  
  # run() will be called by Flask-Seeder
  def run(self):
    filename = os.path.join(dirname, './data/nutrition.json')
    with open(filename) as file:
      data = json.load(file)
    for i in range(0,len(data)):
      nin_data = NIN_Ingredient(data[i]['code'],data[i]['main_name'], data[i]['name'],data[i]['macros'],data[i]['micros'])
      db.session.add(nin_data)
    db.session.commit()