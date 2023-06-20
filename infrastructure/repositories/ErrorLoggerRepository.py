from datetime import datetime

from pymongo import MongoClient
from pymongo.collection import Collection

from entites.shared.logger.IErrorLoggerRepository import IErrorLoggerRepository
from utils.datetimeutils import time_to_utc


class ErrorLoggerRepository(IErrorLoggerRepository):
    __COLLECTION_NAME = 'errors'
    __errors_collection: Collection

    def __init__(self, mongo_instance: MongoClient, database_name: str):
        mongo = mongo_instance.get_database(database_name)
        self.__errors_collection = mongo[self.__COLLECTION_NAME]

    def log_error(self, user_email: str, endpoint: str, method: str, query_params: str, body: str, error_type: str,
                  error_message: str, stack_trace: str):

        current_date = datetime.now()
        now_utc = time_to_utc(current_date)

        error_dict = {
            "created_date": str(now_utc)[:19],
            "user": user_email,
            "endpoint": endpoint,
            "method": method,
            "query_params": query_params,
            "body": body,
            "error_type": error_type,
            "error_message": error_message,
            "stack_trace": stack_trace,
        }

        error = self.__errors_collection.insert_one(error_dict)
        return error.inserted_id
