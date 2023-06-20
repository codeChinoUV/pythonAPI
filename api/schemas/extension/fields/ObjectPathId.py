from typing import Any, Mapping

import bson.errors
from bson import ObjectId
from marshmallow import fields

from entites.shared.exceptions.ValidationPathError import ValidationPathError


class ObjectIdPath(fields.Field):
    """
    ObjectId path field for validations on the path fields
    """
    default_error_messages = {
        'required': ['Este campo es requerido'],
        'null': ['Este campo no puede ser vacio'],
        'validator_failed': ['Valor invalido'],
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
                error = 'El id no es valido'
                raise ValidationPathError(error, attr, value)
        return deserialized_value
