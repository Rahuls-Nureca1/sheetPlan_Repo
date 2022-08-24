from datetime import datetime
from extensions import db

class Plan( db.Model):
    __tablename__ = "plan"

    id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String(255))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, plan_name ) -> None:
        self.plan_name = plan_name
   