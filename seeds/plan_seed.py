from flask_seeder import Seeder
from extensions import db
from models.plan_model import Plan
import json
import os
dirname = os.path.dirname(__file__)

# All seeders inherit from Seeder
class PlanSeeder(Seeder):
  
  # run() will be called by Flask-Seeder
  def run(self):
    filename = os.path.join(dirname, './data/plan.json')
    with open(filename) as file:
      data = json.load(file)
    for i in range(0,len(data)):
      plan_data = Plan(data[i]['plan_name'])
      db.session.add(plan_data)
    db.session.commit()