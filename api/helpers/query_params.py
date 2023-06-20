import urllib

from api.helpers.PaginationConfiguration import PaginationConfiguration
from utils.strings import camel_case_to_snake_case


def _find_separator_value_for_param(query_param: str) -> str:
    """
    Find the separator for a param string
    :param query_param: The param to find the separator
    :return: The separator or None
    """
    separator_values = ['<', '>', '>=', '<=', '!=', '=']

    for separator_value in separator_values:
        if query_param.find(separator_value) != -1:
            separator_for_param = separator_value
            return separator_for_param


def _get_dict_from_query_param(query_param: str) -> dict:
    """
    Get a dict with the key, value and separator for the query_param
    :param query_param:
    :return:
    """
    separator = _find_separator_value_for_param(query_param)

    if separator is not None:
        query_param_values = query_param.split(separator)
        key = query_param_values[0]
        value = query_param_values[1]
    else:
        key = query_param
        value = None

    return {"key": key, "value": value, "separator": separator}


def get_dict_from_query_params(query_params: str) -> list:
    """
    Convert a query params string into a dictionary
    :param query_params: The string with the query params
    :return: A dict with the key (param) value(param value)
    """
    query_params_split = []
    query_params = query_params.split('&')
    # Visit every query param
    for param in query_params:
        decode_param = urllib.parse.unquote(param)
        query_param_dict = _get_dict_from_query_param(decode_param)
        query_params_split.append(query_param_dict)

    return query_params_split


def get_snake_case_dict_from_query_params(query_params: str) -> dict:
    """
    Convert the query params string to a dictionary with the keys on snake case
    :param query_params: The query params to convert
    :return: S dict with the key in snake case (param) and the param value
    """
    snake_case_dict = {}
    query_params_dict = get_dict_from_query_params(query_params)
    for query_param_dict in query_params_dict:
        if query_param_dict["key"] == "id":
            key = "_id"
        else:
            key = camel_case_to_snake_case(query_param_dict["key"])
        recreated_query_param = key
        if query_param_dict["separator"] is not None:
            recreated_query_param += query_param_dict["separator"]
        if query_param_dict["value"] is not None:
            recreated_query_param += query_param_dict["value"]

        split_query_params = recreated_query_param.split("=")
        key = split_query_params[0]
        value = split_query_params[1] if len(split_query_params) > 1 else None
        snake_case_dict[key] = value

    return snake_case_dict


def get_snake_case_query_params_keys(query_params: str) -> str:
    """
    Get the query params string with the keys in snake case
    :param query_params: The query params to transform
    :return: A string with the query params keys on snake case
    """
    snake_case_query_params = []
    query_params_dict = get_dict_from_query_params(query_params)
    for query_param_dict in query_params_dict:
        if query_param_dict["key"] == "id":
            key = "_id"
        else:
            key = camel_case_to_snake_case(query_param_dict["key"])
        recreated_query_param = key
        if query_param_dict["separator"] is not None:
            recreated_query_param += query_param_dict["separator"]
        if query_param_dict["value"] is not None:
            recreated_query_param += query_param_dict["value"]

        snake_case_query_params.append(recreated_query_param)
    return "&".join(snake_case_query_params)


def add_default_pagination_to_dict(query_params: dict) -> dict:
    """
    Add the default pagination params to the query params dict
    :param query_params: The dict to add the default values
    :return:
    """
    pagination_configuration = PaginationConfiguration()

    # Limit
    if "limit" not in query_params:
        query_params["limit"] = pagination_configuration.default_page_size
    else:
        if query_params["limit"].isdigit() and int(query_params["limit"]) >= 0:
            query_params["limit"] = int(query_params["limit"])
        else:
            query_params["limit"] = pagination_configuration.default_page_size

    # Skip
    if "skip" not in query_params:
        query_params["skip"] = pagination_configuration.default_page_size * pagination_configuration.default_page
    else:
        if query_params["skip"].isdigit() and int(query_params["skip"]) >= 0:
            query_params["skip"] = int(query_params["skip"])
        else:
            query_params["skip"] = pagination_configuration.default_page_size * pagination_configuration.default_page

    return query_params


def add_default_pagination_to_query_params(query_params: str) -> str:
    """
    Add the default pagination to a query params
    :param query_params: The query params to add the deault pagination
    :return:
    """
    updated_query_params = query_params
    query_params_dict = get_snake_case_dict_from_query_params(query_params)

    pagination_configuration = PaginationConfiguration()

    # Limit
    if "limit" not in query_params_dict:
        updated_query_params += f"&limit={pagination_configuration.default_page_size}"
    else:
        if not query_params_dict["limit"].isdigit() or int(query_params_dict["limit"]) < 0:
            updated_query_params = updated_query_params.replace(
                f"limit={query_params_dict['limit']}",
                f"limit={pagination_configuration.default_page_size}")

    # Skip
    skip = pagination_configuration.default_page_size * pagination_configuration.default_page
    if "skip" not in query_params_dict:
        updated_query_params += f"&skip={skip}"
    else:
        if not query_params_dict["skip"].isdigit() or int(query_params_dict["skip"]) < 0:
            updated_query_params = updated_query_params.replace(f"skip={query_params_dict['skip']}", f"skip={skip}")

    return updated_query_params
