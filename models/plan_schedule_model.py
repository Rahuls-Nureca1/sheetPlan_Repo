from datetime import datetime

from extensions import db

planned_meal = db.Table('planned_meal',
                db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
                db.Column('schedule_id', db.Integer, db.ForeignKey('plan_schedule.id'))
                )

class Plan_Schedule( db.Model):
    __tablename__ = "plan_schedule"
    id = db.Column(db.Integer, primary_key=True)
    plan_id = db.Column(db.Integer, db.ForeignKey('plan.id'), nullable=False)
    day_id = db.Column(db.Integer, db.ForeignKey('day.id'), nullable=False)
    time_id = db.Column(db.Integer, db.ForeignKey('timing.id'), nullable=False)
    updated_by = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    plan = db.relationship('Plan', backref='plan_schedule')
    day = db.relationship('Day', backref='plan_schedule')
    timing = db.relationship('Timing', backref='plan_schedule')
    recipes = db.relationship('Recipe', secondary=planned_meal, backref = 'plan_schedule', )

    def __init__(self, plan_id, day_id, time_id, updated_by ) -> None:
        self.plan_id = plan_id
        self.day_id = day_id
        self.time_id = time_id
        self.updated_by = updated_by
