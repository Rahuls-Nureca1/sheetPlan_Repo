from datetime import datetime
from email.policy import default

from extensions import db, login_manager

class User( db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(500))
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, first_name, last_name, email, password) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

   