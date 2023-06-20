import bson.errors
from bson import ObjectId


def get_object_id_list(ids: list) -> list:
    """
    Convert a list of string IDs to a list of ObjectId
    :param ids: The ids to convert
    :return: A list of ObjectId
    """
    list_object_ids = []
    for id in ids:
        try:
            object_id = ObjectId(id)
            list_object_ids.append(object_id)
        except bson.errors.InvalidId:
            pass
    return list_object_ids


def get_lists_of_db_dict_key(data: list, field: str):
    """
    Get a list of a dict field on a list of dicts
    :param data: The data to get the list
    :param field: The field of the dict to get the list
    :return: A list with the value of the field
    """
    return map(lambda dictionary: dictionary[field], data)
