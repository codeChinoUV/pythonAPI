from bson import ObjectId
from marshmallow import Schema, post_load, pre_dump, EXCLUDE

from utils.dictionary import dict_keys_to_snake_case, dict_keys_to_camel_case


class CommonSchema(Schema):
    """
    Common implementation of the schema with the logic of load and dump models
    """

    class Meta:
        unknown = EXCLUDE

    schema_class_to_map = None

    def __init__(self, schema_class_to_map=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema_class_to_map = schema_class_to_map

    @post_load(pass_many=True)
    def post_load(self, data, many=False, *args, **kwargs):
        """
        Change the camel case keys in the request for snake case and create an instance of the object
        schema_class_to_map
        :param data: The data in the request
        :param many: Indicate if the data contains multiple objects
        :return: A dict or object with the information
        """
        if many is True:
            items = []
            for item in data:
                item_snake_case = dict_keys_to_snake_case(item)
                if self.schema_class_to_map:
                    items.append(self.schema_class_to_map(**item_snake_case))
                else:
                    items.append(item_snake_case)
            return items
        else:
            data_snake_case = dict_keys_to_snake_case(data)
            if self.schema_class_to_map:
                return self.schema_class_to_map(**data_snake_case)
            else:
                return data_snake_case

    @pre_dump(pass_many=True)
    def pre_dump(self, data, many=False, *args, **kwargs):
        """
        Change the keys of the data to serialize to camel case
        :param data: The data to serialize
        :param many: Indicate if contains multiple objects
        :return: A list or a dict with the info
        """
        if many is True:
            list_camel_case = []
            for data_item in data:
                if type(data) is str or type(data) is int or type(data) is bool:
                    return data
                data_dict = data_item.__dict__
                data_camel_case = dict_keys_to_camel_case(data_dict)
                list_camel_case.append(data_camel_case)
            return list_camel_case
        else:
            if type(data) is ObjectId:
                data = str(data)
            if type(data) is str or type(data) is int or type(data) is bool:
                return data
            data_dict = data.__dict__
            data_camel_case = dict_keys_to_camel_case(data_dict)
            return data_camel_case
