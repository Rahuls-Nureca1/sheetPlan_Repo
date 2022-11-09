from datetime import datetime
from email.policy import default

from extensions import db

class Ingredient( db.Model):
    __tablename__ = "ingredient"
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    nin_id = db.Column(db.Integer, db.ForeignKey('nin_ingredient.id'), nullable=True)
    nin_details = db.relationship('NIN_Ingredient', backref = 'Ingredient')
    ingredient_name = db.Column(db.String)
    ingredient_standard_name = db.Column(db.String)
    ingredient_desc = db.Column(db.String)
    quantity = db.Column(db.Float)
    quantity_in_gram = db.Column(db.Integer)
    serving_unit_id = db.Column(db.Integer, db.ForeignKey('ingredient_serving_unit.id'), nullable=True)
    serving_unit = db.Column(db.String)
    serving_unit_details = db.relationship('IngredientServingUnit', backref = 'Ingredient')
    macros = db.Column(db.JSON, default={})
    micros = db.Column(db.JSON, default = {})
    updated_by = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    

    nin_ingredient = db.relationship('NIN_Ingredient', backref='nin_ingredient')
    # recipe = db.relationship('Recipe', backref='recipe')

    # def __init__(self, recipe_id, nin_id, ingredient_name,ingredient_standard_name, ingredient_desc, quantity, quantity_in_gram, serving_unit_id, serving_unit, macros, micros ) -> None:
    #     self.recipe_id = recipe_id
    #     self.nin_id = nin_id
    #     self.ingredient_name = ingredient_name
    #     self.ingredient_standard_name = ingredient_standard_name
    #     self.ingredient_desc = ingredient_desc
    #     self.quantity = quantity
    #     self. quantity_in_gram = quantity_in_gram
    #     self.serving_unit_id = serving_unit_id
    #     self.serving_unit = serving_unit
    #     self.macros = macros
    #     self.micros = micros
