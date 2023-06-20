from datetime import datetime

from pymongo import MongoClient
from pymongo.collection import Collection

from entites.shared.logger.ILoggerRepository import ILoggerRepository
from utils.datetimeutils import time_to_utc


class LoggerRepository(ILoggerRepository):
    __COLLECTION_NAME = 'requests_logs'
    __logs_collection: Collection

    def __init__(self, mongo_instance: MongoClient, database_name: str):
        mongo = mongo_instance.get_database(database_name)
        self.__logs_collection = mongo[self.__COLLECTION_NAME]

    def log(self, user_email: str, endpoint: str, query_params: str, body: str, method: str, response_code_status):
        """
        Log a request in the database
        :param user_email: The user who made the request
        :param endpoint: The endpoint requested
        :param query_params: The query params in the request
        :param body: The body of the request
        :param method: The method requested
        :param response_code_status: The code status of the response
        :return: None
        """

        current_date = datetime.now()
        now_utc = time_to_utc(current_date)

        log_dict = {
            "created_date": str(now_utc)[:19],
            "user": user_email,
            "endpoint": endpoint,
            "query_params": query_params,
            "body": body,
            "method": method,
            "response_code_status": response_code_status
        }

        self.__logs_collection.insert_one(log_dict)
