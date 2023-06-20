import datetime

from bson import ObjectId
from mongo_queries_manager import mqm

from utils.datetimeutils import time_to_utc
from utils.dictionary import dict_keys_to_camel_case


def replace_diacritic_for_regex_search(search: str) -> str:
    """
    Replace the diacritic letter for its search in regex
    :param search:
    :return:
    """
    search = search.replace('a', '[aá]')
    search = search.replace('e', '[eé]')
    search = search.replace('i', '[ií]')
    search = search.replace('o', '[oó]')
    search = search.replace('u', '[uú]')
    return search


def regex_query(search_string: str):
    """
    Adding a regex search in a filter
    :param search_string: The search string in the regex
    :return: A dict with the information for the regex search
    """
    search_with_diacritic = replace_diacritic_for_regex_search(search_string)
    return {"$regex": search_with_diacritic, "$options": "i"}


def process_list(value):
    """
    Process a list of items
    :param value: The list
    :return: An array with the items
    """
    return value.split(',')


def process_object_id(value):
    """
    Process a mongo ID
    :param value: The ID
    :return: A mongo ObjectId
    """
    try:
        return ObjectId(value)
    except Exception:
        pass


def process_object_id_list(value):
    """
    Process a list of IDs
    :param value: The list of IDs
    :return: An dict with the filter for mongo
    """
    ids = value.split(',')
    return {"$in": list(map(process_object_id, ids))}


def full_day_query(date):
    """
    Create a query to get the full day registers
    :param date: The date to create the full day query
    :return: The full day query
    """
    try:
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        start_date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)
        end_date = datetime.datetime(date.year, date.month, date.day, 23, 59, 59)
        return {
            "$gte": time_to_utc(start_date),
            "$lte": time_to_utc(end_date)
        }
    except Exception as e:
        return {}


def money_range_query(money_range: str):
    split_values = money_range.split(',')
    query = {}

    if len(split_values) != 2:
        return query

    try:
        grater_than = int(split_values[0]) * 100
    except Exception:
        grater_than = None

    try:
        lower_than = int(split_values[1]) * 100
    except Exception:
        lower_than = None

    if grater_than is not None:
        query["$gte"] = grater_than
    if lower_than is not None:
        query["$lte"] = lower_than

    return query


def number_range_query(money_range: str):
    split_values = money_range.split(',')
    query = {}

    if len(split_values) != 2:
        return query

    try:
        grater_than = int(split_values[0])
    except Exception:
        grater_than = None

    try:
        lower_than = int(split_values[1])
    except Exception:
        lower_than = None

    if grater_than is not None:
        query["$gte"] = grater_than
    if lower_than is not None:
        query["$lte"] = lower_than

    return query


def string(value):
    """
    Convert to string a value
    :param value: The value to convert
    :return: The string value
    """
    return str(value)


def mongo_query_manager(query: str, blacklist=None) -> dict:
    """
    Add to the mongo query manager the caster for the regex search
    :param blacklist: The blacklist field for the user query
    :param query: The query string
    :return: A dict with the information to the mongo DB query
    """
    if blacklist is None:
        blacklist = ["deleted"]

    mongo_query = mqm(
        query,
        casters={
            "regex": regex_query,
            "list": process_list,
            "listId": process_object_id_list,
            "objectId": process_object_id_list,
            "fullDay": full_day_query,
            "string": string,
            "moneyRange": money_range_query,
            "range": number_range_query
        },
        blacklist=blacklist
    )
    mongo_query["filter"] = dict_keys_to_camel_case(mongo_query["filter"], ignore_id=False)
    return mongo_query
