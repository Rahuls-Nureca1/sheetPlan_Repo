from datetime import datetime
from email.policy import default

from extensions import db, login_manager

class Auth( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_key = db.Column(db.String(255), index=True, unique=True)
    auth_description = db.Column(db.String(500))
    status = db.Column(db.Boolean, default=True)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, auth_key, auth_description, status) -> None:
        self.auth_key = auth_key
        self.auth_description = auth_description
        self.status = status

   