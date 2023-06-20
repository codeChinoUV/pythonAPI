from marshmallow import Schema


def validate_id(validation_schema: Schema, id: str):
    """
    Validate an ID
    :param validation_schema: The Schema class to perform the validations
    :param id: The id to validate
    :return: The id
    """
    validation_schema.load({'id': id})
    return str(id)
