from more_itertools import locate


def find_in_list_by_id(id_to_find: list, list_to_find: list):
    """
    Find and element in a list by its id
    :param id_to_find: The ID to find
    :param list_to_find: The list where search
    :return: The element found or None
    """
    for element in list_to_find:
        if str(id_to_find) == str(element.id):
            return element


def find_indices(list_to_find: list, item_to_find) -> list:
    """
    Find all the occurrences on the list
    :param list_to_find: The list where search
    :param item_to_find: The item to search
    :return: A list with the indices of the occurrences
    """
    indices = locate(list_to_find, lambda item: item == item_to_find)
    return list(indices)
