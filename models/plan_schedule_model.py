from datetime import datetime

from extensions import db

# planned_meal = db.Table('planned_meal',
#                 db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
#                 db.Column('schedule_id', db.Integer, db.ForeignKey('plan_schedule.id')),
#                 db.Column('serving_unit_id', db.Integer, db.ForeignKey('ingredient_serving_unit.id'))
#                 )

class Planned_Meal(db.Model):
    __tablename__ = "planned_meal"
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer,db.ForeignKey("recipe.id"))
    recipe = db.relationship('Recipe', backref= 'planned_meal')
    schedule_id = db.Column(db.Integer,db.ForeignKey("plan_schedule.id"))
    plan_schedule = db.relationship('Plan_Schedule', backref = 'planned_meal')
    serving_unit_id = db.Column(db.Integer,db.ForeignKey("ingredient_serving_unit.id"))
    serving = db.relationship('IngredientServingUnit', backref = 'planned_meal')
    quantity = db.Column(db.Float)
    
    def __init__(self, recipe_id, schedule_id,serving_unit_id, quantity ) -> None:
        self.recipe_id = recipe_id
        self.schedule_id = schedule_id
        self.quantity = quantity
        self.serving_unit_id = serving_unit_id

class Plan_Schedule( db.Model):
    __tablename__ = "plan_schedule"
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    time_id = db.Column(db.Integer, db.ForeignKey('timing.id'), nullable=False)
    updated_by = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    plan = db.relationship('Plan', backref='plan_schedule')
    day = db.relationship('Day', backref='plan_schedule')
    timing = db.relationship('Timing', backref='plan_schedule')
    recipes = db.relationship('Recipe',secondary='planned_meal', backref = 'plan_schedule')
    servings = db.relationship('IngredientServingUnit', secondary='planned_meal', backref = 'plan_schedule', )


    def __init__(self, plan_id, day_id, time_id, updated_by ) -> None:
        self.plan_id = plan_id
        self.day_id = day_id
        self.time_id = time_id
        self.updated_by = updated_by



class Recipe( db.Model):
    __tablename__ = "recipe"
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String)
    image_path = db.Column(db.String)
    course = db.Column(db.JSON)
    cusine = db.Column(db.JSON)
    recipe_url = db.Column(db.String)
    website_name = db.Column(db.String)
    serving = db.Column(db.Integer)
    ingredients = db.relationship('Ingredient', backref='recipe')
   
    deleted = db.Column(db.Boolean, default = False)
    updated_by = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, recipe_name, image_path, course, cusine, recipe_url, website_name, serving, updated_by ) -> None:
        self.recipe_name = recipe_name
        self.image_path = image_path
        self.course = course
        self.cusine = cusine
        self.recipe_url = recipe_url
        self. website_name = website_name
        self.serving = serving
        self.updated_by = updated_by
