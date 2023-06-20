import traceback
from http import HTTPStatus
from typing import List, Any

from dependency_injector.wiring import Provide
from flask import Flask, Request, request, jsonify, g
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest, NotFound

from api.auth.exceptions.InvalidTokenException import InvalidTokenException
from api.auth.exceptions.RoleNotAllowedException import RoleNotAllowedException
from api.auth.exceptions.TokenExpiredException import TokenExpiredException
from entites.shared.exceptions.NotFoundError import NotFoundError
from entites.shared.exceptions.ValidationModelError import ValidationModelError
from entites.shared.exceptions.ValidationPathError import ValidationPathError
from entites.shared.logger.IErrorLoggerRepository import IErrorLoggerRepository
from extension.ApplicationContainer import ApplicationContainer


class ErrorHandlers:
    """
    Register the error handlers for the application
    """

    app: Flask

    _error_logger_repository: IErrorLoggerRepository

    def __init__(self, app: Flask,
                 error_logger_repository=Provide[ApplicationContainer.repositories.errors_logger_repository]):
        self._app = app
        self._error_logger_repository = error_logger_repository
        self._register_error_handlers()

    @classmethod
    def __get_current_user(cls):
        """
        Get the current user
        :return: The current user
        """
        user = 'Unknown'
        if 'user' in g.__dict__.keys():
            user = g.user.email

        return user

    @classmethod
    def _get_request_information(cls, request_information: Request) -> dict:
        """
        Get basic information of the request
        :param request_information: The full request information
        :return: A dict with the details of the request
        """
        query_params = request_information.query_string.decode()
        body = request_information.data.decode()
        method = request_information.method
        endpoint = request_information.path

        return {"query_params": query_params, "body": body, "endpoint": endpoint, "method": method}

    @classmethod
    def __create_validation_error_detail(cls, field: str, error: str, value: Any):
        """
        Create an error detail dict
        :param field: The field where the error
        :param error: The error
        :param value: The current value for the field
        :return:
        """
        return {
            "field": field,
            "location": "body",
            "error": error,
            "value": value
        }

    @classmethod
    def __create_validation_errors_from_dict(cls, field: str, errors: dict, data: dict):
        """
        Create the validation error messages for a schema list validations
        :param field: The field where the error was raised
        :param errors: The errors on the validation
        :param data: The data validated
        :return: A list with dicts with the details
        """
        validation_errors = []

        for item_in_list in errors:
            if type(item_in_list) is int:
                if type(errors[item_in_list]) is not dict:
                    for error in errors[item_in_list]:
                        validation_error = cls.__create_validation_error_detail(
                            f"{field}[{item_in_list}]", error, data[field][item_in_list]
                        )
                        validation_errors.append(validation_error)
                else:
                    dict_errors = errors[item_in_list]
                    for error_key in dict_errors:
                        error_messages = dict_errors[error_key]
                        for error_message in error_messages:
                            field_representation = f"{field}[{item_in_list}]"
                            value = data[field][item_in_list]

                            if error_key != "_schema":
                                value = value[error_key]
                                field_representation += f".{error_key}"

                            validation_error = cls.__create_validation_error_detail(
                                field_representation, error_message, value)

                            validation_errors.append(validation_error)
            else:
                # For many validations
                for field_error in errors[item_in_list]:
                    if type(errors[item_in_list] is not dict):
                        error_messages = errors[item_in_list]
                        for error_message in error_messages:
                            if type(error_messages) is dict:
                                messages = error_messages[error_message]
                                if type(messages) is list:
                                    for item in messages:
                                        validation_error = cls.__create_validation_error_detail(
                                            f"{field}[{item_in_list}]", item, data[field]
                                        )
                                        validation_errors.append(validation_error)
                                else:
                                    validation_error = cls.__create_validation_error_detail(
                                        f"[{field}]", error_message, data[field]
                                    )
                                    validation_errors.append(validation_error)
                            else:
                                validation_error = cls.__create_validation_error_detail(
                                    f"[{field}]", error_message, data[field]
                                )
                                validation_errors.append(validation_error)
                    else:
                        # For nested list
                        error_messages = errors[item_in_list][field_error]
                        for error_message in error_messages:
                            field_representation = f"{field}[{item_in_list}]"

                            if field_error != '_schema':
                                value = data[field][item_in_list][field_error]
                                field_representation += f".{field_error}"
                            else:
                                value = data[field][item_in_list]

                            validation_error = cls.__create_validation_error_detail(
                                field_representation, error_message, value
                            )
                            validation_errors.append(validation_error)
        return validation_errors

    def _get_validation_errors(self, validation_errors: ValidationError) -> List:
        """
        Create a List with the error details in the validation error
        :param validation_errors: to create the error details
        :return: A list with the error details
        """
        errors_details = []

        error_messages = validation_errors.messages
        data = validation_errors.data
        for field in error_messages:
            if type(error_messages[field]) is dict:
                details = self.__create_validation_errors_from_dict(field, error_messages[field], data)
                errors_details.extend(details)
            else:
                for error in error_messages[field]:
                    if field == '_schema':
                        errors_details.append(
                            self.__create_validation_error_detail('_schema', error, data)
                        )
                    else:
                        errors_details.append(
                            self.__create_validation_error_detail(field, error, getattr(data, field, None))
                        )
        return errors_details

    def _handle_common_error(self, exception, request_information: Request, error_type: str, error_message):
        """
        Create common error response
        :param exception: Exception to log
        :param request_information: The information of the request which raise the exception
        :param error_type: The error type
        :param error_message: The descriptive message for the error
        :return: A dict with the error info
        """
        request_information = self._get_request_information(request_information)
        try:

            debug_id = self._error_logger_repository.log_error(
                self.__get_current_user(),
                request_information['endpoint'],
                request_information['method'],
                request_information['query_params'],
                request_information['body'],
                error_type,
                exception.__repr__(),
                traceback.format_exc()
            )
        except Exception:
            debug_id = 'DB_ERROR'

        error = {
            "errorType": error_type,
            "debugId": str(debug_id),
            "message": error_message
        }
        return error

    def handle_validation_errors(self, e: ValidationError):
        """
        Handle validation errors of Marshmallow library
        :param e: The error to handle
        :return: The errors in the request
        """
        request_information = self._get_request_information(request)
        try:
            debug_id = self._error_logger_repository.log_error(
                self.__get_current_user(),
                request_information['endpoint'],
                request_information['method'],
                request_information['query_params'],
                request_information['body'],
                "validationError",
                e.__repr__(),
                traceback.format_exc()
            )
        except Exception:
            debug_id = 'DB_ERROR'

        error = {
            "errorType": "validationError",
            "errors": self._get_validation_errors(e),
            "debugId": str(debug_id),
            "message": "Existen errores de validación"
        }
        return jsonify(error), HTTPStatus.BAD_REQUEST

    def handle_validation_model_errors(self, e: ValidationModelError):
        """
        Handle validation errors of model
        :param e: The error to handle
        :return: The errors in the request
        """
        request_information = self._get_request_information(request)
        try:
            debug_id = self._error_logger_repository.log_error(
                self.__get_current_user(),
                request_information['endpoint'],
                request_information['method'],
                request_information['query_params'],
                request_information['body'],
                "validationError",
                e.__repr__(),
                traceback.format_exc()
            )
        except Exception:
            debug_id = 'DB_ERROR'

        error = {
            "errorType": "validationError",
            "errors": [self.__create_validation_error_detail(e.field, e.message, e.value)],
            "debugId": str(debug_id),
            "message": "Existen errores de validación"
        }
        return jsonify(error), HTTPStatus.BAD_REQUEST

    def handle_validation_path_error(self, validation_path_error: ValidationPathError):
        """
        Handle validation path error
        :param validation_path_error: The validation path error to handle
        :return: The errors in the request
        """
        request_information = self._get_request_information(request)
        validation_errors = [{
            "field": validation_path_error.field,
            "location": "path",
            "value": validation_path_error.value,
            "error": validation_path_error.message
        }]
        debug_id = self._error_logger_repository.log_error(
            self.__get_current_user(),
            request_information['endpoint'],
            request_information['method'],
            request_information['query_params'],
            request_information['body'],
            "validationError",
            validation_path_error.__repr__(),
            traceback.format_exc()
        )
        error = {
            "errorType": "validationError",
            "errors": validation_errors,
            "debugId": str(debug_id),
            "message": "Existen errores de validación en la ruta del recurso"
        }
        return jsonify(error), HTTPStatus.NOT_FOUND

    def handle_not_found_exception(self, not_found_exception: NotFoundError):
        """
        Handle custom exception not found
        :param not_found_exception: The error to handle
        :return: The errors in the request
        """
        request_information = self._get_request_information(request)

        full_error_message = f'El item con el {not_found_exception.item_id} no se encuentra'

        validation_errors = [{
            "field": "id",
            "location": "path",
            "value": not_found_exception.item_id,
            "error": full_error_message
        }]

        debug_id = self._error_logger_repository.log_error(
            self.__get_current_user(),
            request_information['endpoint'],
            request_information['method'],
            request_information['query_params'],
            request_information['body'],
            "notFoundError",
            not_found_exception.__repr__(),
            traceback.format_exc()
        )

        error = {
            "errorType": "notFoundError",
            "errors": validation_errors,
            "debugId": str(debug_id),
            "message": "El recurso no fue encontrado"
        }
        return jsonify(error), HTTPStatus.NOT_FOUND

    def handle_method_not_allowed(self, e):
        """
        Handle method not allowed exception
        :param e: The exception
        :return: A JSON response with the error details
        """
        error = self._handle_common_error(e, request, "MethodNotAllowed", "Metodo no permitido")
        return jsonify(error), HTTPStatus.METHOD_NOT_ALLOWED

    def handle_general_exceptions(self, e):
        """
        Handle server error exceptions
        :param e: The exception
        :return: A JSON response with the error details
        """
        error = self._handle_common_error(e, request, "unknown", "Un error desconocido ocurrio en el servidor")
        return jsonify(error), HTTPStatus.INTERNAL_SERVER_ERROR

    def handle_bad_request_error(self, error: BadRequest):
        request_information = self._get_request_information(request)
        debug_id = self._error_logger_repository.log_error(
            self.__get_current_user(),
            request_information['endpoint'],
            request_information['method'],
            request_information['query_params'],
            request_information['body'],
            "validationError",
            error.__repr__(),
            traceback.format_exc()
        )

        message = "Existen errores de validacion"

        if request.content_type != 'application/json':
            message = "The request should have a JSON body"

        error = {
            "errorType": "validationError",
            "message:": message,
            "debugId": str(debug_id)
        }
        return jsonify(error), HTTPStatus.BAD_REQUEST

    def handle_invalid_token_error(self, e: InvalidTokenException):
        """
        Handle all invalid token exceptions
        :param e: The exception to handle
        """
        error_message = "El token de autenticacion no se encuentra en la cabecera de la solicitud"
        error_code = "invalidToken"
        error = self._handle_common_error(e, request, error_code, error_message)
        return jsonify(error), HTTPStatus.UNAUTHORIZED

    def handle_invalid_role_exception(self, e: RoleNotAllowedException):
        """
        Handle all role not allowed exceptions
        :param e: The exception to handle
        """
        error_message = "No tienes permiso para acceder a este recurso"
        error_code = "forbidden"
        error = self._handle_common_error(e, request, error_code, error_message)
        return jsonify(error), HTTPStatus.FORBIDDEN

    def handle_expired_token_exception(self, e: TokenExpiredException):
        """
        Handle token expired exceptions
        :param e: The exception to handle
        """
        error_message = "Tu token a expirado"
        error_code = "tokenExpired"
        error = self._handle_common_error(e, request, error_code, error_message)
        return jsonify(error), HTTPStatus.UNAUTHORIZED

    def _register_error_handlers(self) -> None:
        """
        Register all handlers in the app
        :return: None
        """
        self._app.register_error_handler(ValidationError, self.handle_validation_errors)
        self._app.register_error_handler(ValidationModelError, self.handle_validation_model_errors)
        self._app.register_error_handler(ValidationPathError, self.handle_validation_path_error)
        self._app.register_error_handler(NotFoundError, self.handle_not_found_exception)
        self._app.register_error_handler(NotFound, self.handle_method_not_allowed)
        self._app.register_error_handler(BadRequest, self.handle_bad_request_error)
        self._app.register_error_handler(InvalidTokenException, self.handle_invalid_token_error)
        self._app.register_error_handler(RoleNotAllowedException, self.handle_invalid_role_exception)
        self._app.register_error_handler(TokenExpiredException, self.handle_expired_token_exception)
        self._app.register_error_handler(Exception, self.handle_general_exceptions)
