from datetime import datetime

from sqlalchemy import ForeignKey
from extensions import db

class Timing( db.Model):
    __tablename__ = "timing"

    id = db.Column(db.Integer, primary_key=True)
    timing_label = db.Column(db.String(255))
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, timing_label ) -> None:
        self.timing_label = timing_label
   