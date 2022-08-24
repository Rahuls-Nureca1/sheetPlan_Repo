from datetime import datetime

from extensions import db
from typing import List

class NIN_Ingredient( db.Model):
    __tablename__ = "nin_ingredient"
    id = db.Column(db.Integer, primary_key=True)
    nin_code = db.Column(db.String(255), index=True, unique=True)
    ingredient_name = db.Column(db.String(255))
    ingredient_description = db.Column(db.String(500))
    macros = db.Column(db.JSON)
    micros = db.Column(db.JSON)
    deleted = db.Column(db.Boolean, default=False)
    updated_by = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, nin_code, ingredient_name, ingredient_description,macros, micros ) -> None:
        self.nin_code = nin_code
        self.ingredient_name = ingredient_name
        self.ingredient_description = ingredient_description
        self.macros = macros
        self.micros = micros

    # def json(self):
    #     return {'nin_code': self.nin_code, 'ingredient_name': self.ingredient_name,'ingredient_description':self.ingredient_description,'macros':self.macros,'micros': self.micros}


    # @classmethod
    # def find_by_name(cls, name) -> "ItemModel":
    #     return cls.query.filter_by(name=name).first()

    # @classmethod
    # def find_by_id(cls, _id) -> "ItemModel":
    #     return cls.query.filter_by(id=_id).first()

    # @classmethod
    # def find_all(cls) -> List["ItemModel"]:
    #     return cls.query.all()

    # def save_to_db(self) -> None:
    #     db.session.add(self)
    #     db.session.commit()

    # def delete_from_db(self) -> None:
    #     db.session.delete(self)
    #     db.session.commit()