from marshmallow import fields

from api.schemas.CommonSchema import CommonSchema
from api.schemas.user.UserSchema import UserSchema


class LoginDumpSchema(CommonSchema):
    """
    Schema for login dump
    """
    token = fields.Str(dump_only=True)
    refreshToken = fields.Str(dump_only=True)
    user = fields.Nested(UserSchema(), dump_only=True)
