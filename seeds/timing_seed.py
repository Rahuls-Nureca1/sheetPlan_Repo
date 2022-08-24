from flask_seeder import Seeder
from extensions import db
from models.timing_model import Timing

# All seeders inherit from Seeder
class TimingSeeder(Seeder):
  
  # run() will be called by Flask-Seeder
 
  def run(self):
    timing = ['Early Morning', 'Breakfast', 'Mid Morning', 'Lunch', 'Evening Tea', 'Dinner']
   
    for i in range(0,6):
      timings = Timing(timing[i])
      db.session.add(timings)
      db.session.commit()