from utils.strings import snake_case_to_camel_case, camel_case_to_snake_case


def dict_keys_to_camel_case(original_dict: dict, ignore_id=True) -> dict:
    """
    Convert the dict keys to camel case
    :param original_dict: The original dict to change its keys
    :param ignore_id: Indicates if no convert the id
    :return: The converted dict
    """
    new_dict = {}
    for key in original_dict:
        if (key == "_id" or key == "id") and not ignore_id:
            new_dict["_id"] = original_dict[key]
        else:
            key_snake_case = snake_case_to_camel_case(key)
            new_dict[key_snake_case] = original_dict[key]
    return new_dict


def dict_keys_to_snake_case(original_dict: dict) -> dict:
    """
    Convert the dict keys to snake case
    :param original_dict: The original dict to change its keys
    :return: The converted dict
    """
    new_dict = {}
    for key in original_dict:
        key_snake_case = camel_case_to_snake_case(key)
        new_dict[key_snake_case] = original_dict[key]
    return new_dict
