from marshmallow import fields

from api.schemas.CommonSchema import CommonSchema


def create_paginated_list_schema(results_schema: CommonSchema):
    """
    Create a custom paginated schema for the type of the results
    :param results_schema: The Schema class to map the results
    :return: An instance of the custom paginated list schema
    """

    class PaginationSchema(CommonSchema):
        total = fields.Int()
        skip = fields.Int()
        limit = fields.Int()

    # For create the custom class we are using metaprogramming
    PaginatedListSchema = type('PaginatedListSchema', (CommonSchema,), {
        'pagination': fields.Nested(PaginationSchema),
        'results': fields.List(fields.Nested(lambda: results_schema()))
    })

    return PaginatedListSchema()
