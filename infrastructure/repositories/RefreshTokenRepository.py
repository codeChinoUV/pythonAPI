from dataclasses import asdict

from bson import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection

from api.auth.IRefreshTokenRepository import IRefreshTokenRepository
from api.auth.RefreshToken import RefreshToken
from utils.dictionary import dict_keys_to_camel_case, dict_keys_to_snake_case


class RefreshTokenRepository(IRefreshTokenRepository):
    __COLLECTION_NAME = "refresh_tokens"
    __refresh_token_collection: Collection

    def __init__(self, mongo_instance: MongoClient, database_name: str):
        mongo = mongo_instance.get_database(database_name)
        self.__refresh_token_collection = mongo[self.__COLLECTION_NAME]

    def save_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        """
        Save a refresh token
        :param refresh_token: The token information
        :return: The token saved
        """
        refresh_token.user_id = ObjectId(refresh_token.user_id)
        refresh_token_to_save = asdict(refresh_token)
        refresh_token_to_save = dict_keys_to_camel_case(refresh_token_to_save)
        refresh_token_to_save.pop('id')

        self.__refresh_token_collection.delete_one({"user": refresh_token.user_id})
        saved_token = self.__refresh_token_collection.insert_one(refresh_token_to_save)

        refresh_token_to_save['id'] = saved_token.inserted_id

        return self.__create_refresh_token_from_db_dict(refresh_token_to_save)

    def get_token(self, token: str) -> RefreshToken:
        """
        Get a refresh token by its token
        :param token: The token
        :return: The refresh token
        """
        refresh_token_db = self.__refresh_token_collection.find_one({"token": token})

        if refresh_token_db is not None:
            return self.__create_refresh_token_from_db_dict(refresh_token_db)

    @classmethod
    def __create_refresh_token_from_db_dict(cls, refresh_token_db: dict) -> RefreshToken:
        """
        Create a refresh token instance from db dict
        :param refresh_token_db: The refresh token dict
        :return: The refresh token instance
        """
        if '_id' in refresh_token_db:
            refresh_token_db['id'] = refresh_token_db['_id']
            refresh_token_db.pop('_id')
        if '__v' in refresh_token_db:
            refresh_token_db.pop('__v')

        refresh_token = dict_keys_to_snake_case(refresh_token_db)

        return RefreshToken(**refresh_token)
