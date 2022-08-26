from extensions import db

class IngredientNutrition( db.Model):
    __tablename__ = "ingredient_nutrition"
    id = db.Column(db.Integer, primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), nullable=True)
    macros = db.Column(db.JSON)
    micros = db.Column(db.JSON)
   
   
    ingredient = db.relationship('Ingredient', backref='plans')

    def __init__(self, ingredient_id, macros, micros ) -> None:
        self.ingredient_id = ingredient_id
        self.macros = macros
        self.micros = micros
     
        