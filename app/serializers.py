from marshmallow import Schema, fields

class BlogPostSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    body = fields.Str(required=True)
    timestamp = fields.DateTime(dump_only=True)
    user_id = fields.Int(dump_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
