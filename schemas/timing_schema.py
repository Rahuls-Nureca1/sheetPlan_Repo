from marshmallow import Schema, fields

class TimingSchema(Schema):
    id = fields.Int(dump_only=True)
    timing_label = fields.Str()
    created_at = fields.DateTime()
   