from marshmallow import fields, validate

from api.schemas.CommonSchema import CommonSchema
from api.schemas.extension.errors import get_invalid_email_error_message, get_string_error_messages


class LoginSchema(CommonSchema):
    """
    Login user schema
    """

    email = fields.Str(
        required=True,
        allow_none=False,
        validate=validate.Email(error=get_invalid_email_error_message()),
        error_messages=get_string_error_messages()
    )
    password = fields.Str(
        required=True,
        allow_none=False,
        error_messages=get_string_error_messages()
    )
