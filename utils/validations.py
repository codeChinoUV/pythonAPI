import bson.errors
from bson import ObjectId


def get_invalid_id_of_list(ids: list) -> str:
    """
    Get invalid ID on the list
    :param ids: The IDs to get the invalid ID
    :return: The invalid id on the list or None if all IDs are valid
    """
    for id in ids:
        try:
            ObjectId(id)
        except bson.errors.InvalidId:
            return id
    return None
