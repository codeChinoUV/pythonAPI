from abc import ABC, abstractmethod


class IErrorLoggerRepository(ABC):

    @abstractmethod
    def log_error(self, user_email: str, endpoint: str, method: str, query_params: str, body: str, error_type: str,
                  error_message: str, stack_trace: str):
        """
        Log in the database an error
        :param user_email: The user who made the request which raise the error
        :param endpoint: The endpoint requested
        :param method: The method requested
        :param query_params: The query params in the request
        :param body: The body of the request
        :param error_type: The error type
        :param error_message: The error message
        :param stack_trace: The stack trace
        :return: None
        """
        pass
