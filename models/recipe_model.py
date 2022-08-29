from datetime import datetime
from email.policy import default

from extensions import db

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
