from datetime import datetime
from extensions import db

class Day( db.Model):
    __tablename__ = "day"

    id = db.Column(db.Integer, primary_key=True)
    day_week_number = db.Column(db.Integer)
    day = db.Column(db.String(255))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, day_week_number,day ) -> None:
        self.day_week_number = day_week_number
        self.day = day
   