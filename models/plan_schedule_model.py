from datetime import datetime

from extensions import db

class Plan_Schedule( db.Model):
    __tablename__ = "plan_schedule"
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    time_id = db.Column(db.Integer, db.ForeignKey('timing.id'), nullable=False)
    updated_by = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    plan = db.relationship('Plan', backref='plans')
    day = db.relationship('Day', backref='days')
    timing = db.relationship('Timing', backref='timings')

    def __init__(self, plan_id, day_id, time_id, updated_by ) -> None:
        self.plan_id = plan_id
        self.day_id = day_id
        self.time_id = time_id
        self.updated_by = updated_by
