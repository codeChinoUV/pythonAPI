from functools import wraps

from flask import request
from werkzeug.datastructures import ImmutableMultiDict

from api.helpers.query_params import add_default_pagination_to_query_params, get_snake_case_query_params_keys, \
    get_snake_case_dict_from_query_params, add_default_pagination_to_dict


def query_params(_func=None, *, limit=20):
    """
    Convert the query params to snake case
    :return:
    """

    def query_params_inner(func):
        @wraps(func)
        def wrapper_query_params(*args, **kwargs):
            query_params = request.query_string.decode()
            # Get snake case dict from query params
            snake_case_query_params = get_snake_case_query_params_keys(query_params)
            snake_case_query_params = add_default_pagination_to_query_params(snake_case_query_params)
            # Get snake case query params
            snake_case_query_params_dict = get_snake_case_dict_from_query_params(query_params)
            snake_case_query_params_dict = add_default_pagination_to_dict(snake_case_query_params_dict)

            # Override query params in the request
            request.query_string = snake_case_query_params.encode()
            request.args = ImmutableMultiDict(snake_case_query_params_dict)
            return func(*args, **kwargs)

        return wrapper_query_params

    if _func is None:
        return query_params_inner
    else:
        return query_params_inner(_func)
