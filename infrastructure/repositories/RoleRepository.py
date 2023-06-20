from pymongo import MongoClient
from pymongo.collection import Collection

from entites.user.domain.IRoleRepository import IRoleRepository
from entites.user.domain.Role import Role
from utils.dictionary import dict_keys_to_snake_case


class RoleRepository(IRoleRepository):
    __COLLECTION_NAME = 'roles'
    __roles_collection: Collection

    def __init__(self, mongo_instance: MongoClient, database_name: str):
        database = mongo_instance.get_database(database_name)
        self.__roles_collection = database[self.__COLLECTION_NAME]

    def find_by_name(self, name: str) -> Role:
        """
        Find a role by its name
        :param name: The role's name
        :return: The role if exits or None if not
        """
        role = self.__roles_collection.find_one({"role": name})
        if role is not None:
            return self.__get_role_from_db_dict(role)

    @classmethod
    def __get_role_from_db_dict(cls, db_dict):
        """
        Get a role instance from database response
        :param db_dict: The database dict response
        :return:
        """
        role_dict = dict_keys_to_snake_case(db_dict)
        role_dict['id'] = role_dict['_id']

        if '__v' in db_dict:
            role_dict.pop('__v')

        role_dict.pop('_id')

        return Role(**role_dict)
