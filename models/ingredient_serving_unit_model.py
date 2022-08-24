from datetime import datetime
from email.policy import default

from extensions import db

class IngredientServingUnit( db.Model):
    __tablename__ = "ingredient_serving_unit"
    id = db.Column(db.Integer, primary_key=True)
    serving_unit_name = db.Column(db.String)
    serving_unit_quantity = db.Column(db.Integer)
    updated_by = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, serving_unit_name, serving_unit_quantity,updated_by ) -> None:
        self.serving_unit_name = serving_unit_name
        self.serving_unit_quantity = serving_unit_quantity
        self.updated_by = updated_by
