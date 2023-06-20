from dependency_injector.wiring import Provide
from flask import Flask, request, g

from entites.shared.logger.ILoggerRepository import ILoggerRepository
from extension.ApplicationContainer import ApplicationContainer


class RequestLogger:
    """
    Register the loggers for the API request
    """
    _app: Flask
    _logger_repository: ILoggerRepository

    def __init__(self, app: Flask, logger_repository=Provide[ApplicationContainer.repositories.logs_repository]):
        self._app = app
        self._logger_repository = logger_repository

        @self._app.after_request
        def _log_before_request(response):
            """
            Log the information of the request after have been called
            :param response: The response of the request
            :return: None
            """
            endpoint = request.path
            query_params = request.query_string.decode()
            body = request.data.decode()
            method = request.method

            if method != "OPTIONS":
                status = response.status if response is not None else None
                user = 'Unknown'
                if 'user' in g.__dict__.keys():
                    user = g.user.email

                from app import executor
                executor.submit(logger_repository.log, user, endpoint, query_params, body, method, status)
            return response

        self.log_after_request = _log_before_request
