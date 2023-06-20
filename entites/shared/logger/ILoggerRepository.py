from abc import ABC


class ILoggerRepository(ABC):

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
        pass
