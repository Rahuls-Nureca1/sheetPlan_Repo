from marshmallow import Schema, fields

class PlanSchema(Schema):
    id = fields.Int(dump_only=True)
    plan_name = fields.Str()
   