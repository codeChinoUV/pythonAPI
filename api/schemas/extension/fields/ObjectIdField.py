from typing import Any, Mapping

import bson.errors
from flask_babel import gettext as _
from bson import ObjectId
from marshmallow import fields, ValidationError


class ObjectIdField(fields.Field):
    """
    ObjectId path field for validations on the path fields
    """
    default_error_messages = {
        "required": [_("This field is required")],
        "null": [_("This field can't be empty")],
        "validator_failed": [_("Invalid value")],
    }

    def _serialize(self, value: Any, attr: str, obj: Any, **kwargs):
        serialized_value = None
        if value is not None:
            serialized_value = str(value)
        return serialized_value

    def _deserialize(
            self,
            value: Any,
            attr: str,
            data: Mapping[str, Any],
            **kwargs,
    ):
        deserialized_value = None
        if value is not None:
            try:
                deserialized_value = ObjectId(value)
            except bson.errors.InvalidId:
                raise ValidationError(_("The id is not valid"), attr, value)
        return deserialized_value
