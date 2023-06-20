from dataclasses import asdict

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection

from entites.shared.PaginatedList import PaginatedList
from entites.user.domain.IUserRepository import IUserRepository
from entites.user.domain.User import User
from infrastructure.services.mongo_query_manager import mongo_query_manager
from utils.dictionary import dict_keys_to_camel_case, dict_keys_to_snake_case


class UserRepository(IUserRepository):
    __GET_BLACK_LIST = ["deleted", "password"]
    __COLLECTION_NAME = "users"
    __users_collection: Collection

    def __init__(self, mongo_instance: MongoClient, database_name: str):
        database = mongo_instance.get_database(database_name)
        self.__users_collection = database[self.__COLLECTION_NAME]

    def create_user(self, user: User) -> User:
        """
        Save a new user on the database
        :param user: The user to save
        :return: The saved user
        """
        user_dict = asdict(user)
        user_to_save = dict_keys_to_camel_case(user_dict)
        user_to_save.pop('id')
        user_created_db = self.__users_collection.insert_one(user_to_save)
        user_to_save['id'] = user_created_db.inserted_id
        user_created = self.__get_user_from_db_dict(user_to_save)
        return user_created

    def exists_email(self, email: str) -> bool:
        """
        Validate if exists a user with the email
        :param email: The email to validate
        :return: True if exists or False is not
        """
        registers_quantity = self.__users_collection.count_documents({"email": email})
        return registers_quantity > 0

    def exists_user(self, user_id: str) -> bool:
        """
        Validates if user exists by its ID
        :param user_id: The user's ID to validate
        :return: True if exists or False if not
        """
        registers_quantity = self.__users_collection.count_documents({"_id": ObjectId(user_id), "deleted": False})
        return registers_quantity > 0

    def get_users(self, query: str) -> PaginatedList:
        """
        Get all users by a custom query
        :param query: The query string to paginate or filter the data
        :return: A Paginated list with the results
        """
        filters = mongo_query_manager(query, blacklist=self.__GET_BLACK_LIST)
        filters['filter']['deleted'] = False
        users_from_db = list(self.__users_collection.find(**filters))
        total_users = self.__users_collection.count_documents(filters["filter"])
        users = self.__get_users_from_db_list(users_from_db)
        paginated_list = PaginatedList(total_users, filters["skip"], filters["limit"], users)
        return paginated_list

    def get_user_by_id(self, id: str):
        """
        Get a user by its ID
        :param id: The user ID to get
        :return: The User with the ID
        """
        user_from_db = self.__users_collection.find_one({"_id": ObjectId(id), "deleted": False})
        return self.__get_user_from_db_dict(user_from_db)

    def get_user_by_email(self, email: str) -> User:
        """
        Get a user by its email
        :param email: The email of thr user to get
        :return: The user
        """
        user_db = self.__users_collection.find_one({"email": email})
        return self.__get_user_from_db_dict(user_db)

    def update_user(self, id: str, data_to_update: dict) -> User:
        """
        Update the fields of a user
        :param id: The user's ID to update
        :param data_to_update: The data to update
        :return: The user with the data updated
        """
        data_to_update = dict_keys_to_camel_case(data_to_update)
        update_query = {"$set": data_to_update}
        self.__users_collection.update_one({"_id": ObjectId(id)}, update_query)
        user = self.get_user_by_id(id)
        return user

    def can_change_email(self, id: str, email: str) -> bool:
        """
        Validate if the user can change of the email
        :param id: The user's ID to change his email
        :param email: The new email
        :return: True if the user can change or false if not
        """
        current_user = self.__users_collection.find_one({"_id": ObjectId(id)})
        if current_user and current_user["email"] == email:
            return True
        return not self.exists_email(email)

    def delete_user(self, id: str) -> User:
        """
        Delete a user by its ID
        :param id: The user's ID to delete
        :return: The deleted user
        """
        delete_query = {"$set": {"deleted": True}}
        self.__users_collection.update_one({"_id": ObjectId(id)}, delete_query)
        user_deleted = self.__users_collection.find_one({"_id": ObjectId(id)})
        return self.__get_user_from_db_dict(user_deleted)

    def are_valid_credentials(self, email: str, password: str) -> bool:
        """
        Validate if the user credentials are valid
        :param email: The email to validate
        :param password: The password to validate
        :return: True if the credentials are valid
        """

    @classmethod
    def __get_user_from_db_dict(cls, user_db_dict: dict) -> User:
        """
        Create a user instance from dict got from the db
        :param user_db_dict:
        :return: An user instance
        """
        if '_id' in user_db_dict:
            user_db_dict['id'] = user_db_dict['_id']
            user_db_dict.pop('_id')
        if '__v' in user_db_dict:
            user_db_dict.pop('__v')
        if 'avatar' in user_db_dict:
            user_db_dict.pop('avatar')

        user_dict = dict_keys_to_snake_case(user_db_dict)

        return User(**user_dict)

    @classmethod
    def __get_users_from_db_list(cls, users_from_db: list) -> list:
        """
        Get a list of users from db list objects
        :param users_from_db: The users from the db
        :return: A list with the objects
        """
        users = []
        for user in users_from_db:
            users.append(cls.__get_user_from_db_dict(user))
        return users
