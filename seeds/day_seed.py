from flask_seeder import Seeder
from extensions import db
from models.day_model import Day

# All seeders inherit from Seeder
class DaySeeder(Seeder):
  
  # run() will be called by Flask-Seeder
 
  def run(self):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    # # data_gen = (y for y in days)
    # faker = Faker(
    #   cls=days_model.Days,
    #   init={
    #     "day_week_number":  generator.Sequence() ,
    #     "day":  next(days),
    #   }
    # )

    # Create 7 days
    for i in range(0,7):
      day = Day(i+1,days[i])
      db.session.add(day)
      db.session.commit()