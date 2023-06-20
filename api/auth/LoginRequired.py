from datetime import datetime, timezone

import jwt
from flask import request, g
from pymongo import MongoClient

from api.auth.exceptions.InvalidTokenException import InvalidTokenException
from api.auth.exceptions.RoleNotAllowedException import RoleNotAllowedException
from api.auth.exceptions.TokenExpiredException import TokenExpiredException
from entites.user.Roles import Roles
from extension.appSettings.MongoSettings import MongoSettings

from extension.appSettings.SecretKey import SecretKey
from infrastructure.repositories.UserRepository import UserRepository


class LoginRequired:
    """
    Decorator class to validate the authentication on a endpoint method
    """

    def __init__(self, role: Roles = Roles.NORMAL):
        self.role = role

    @classmethod
    def __get_token_info(cls, token):
        """
        Decode the token and retrieve the user information
        :param token: The token to decode
        """
        if token is None:
            raise InvalidTokenException()
        try:
            secret_key = SecretKey()
            data = jwt.decode(token, secret_key.secret_key, algorithms=["HS256"])
            return data
        except Exception as err:
            raise InvalidTokenException(err)

    @classmethod
    def validate_role(cls, method_allowed_role, user_role):
        """
        Validate if the user has the role to access to the route
        :param role: The role to validate if the user has access
        """
        if user_role is not None:
            allowed_roles = Roles.get_allowed_roles_per_role(user_role)
            if method_allowed_role not in allowed_roles:
                raise RoleNotAllowedException()

    @classmethod
    def validate_token_is_not_expired(cls, expiration_date: int):
        """
        Validate if the user token is not expired
        :param expiration_date: The token's expiration date
        """
        try:
            expiration_date = datetime.fromtimestamp(expiration_date, tz=timezone.utc)
        except Exception as error:
            raise InvalidTokenException(error)

        now = datetime.now(expiration_date.tzinfo)

        if now > expiration_date:
            raise TokenExpiredException()

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authentication')
            token_info = self.__get_token_info(token)
            self.validate_token_is_not_expired(token_info['exp'])

            db_config = MongoSettings()
            users_repository = UserRepository(mongo_instance=MongoClient(host=db_config.connection_string),
                                              database_name=db_config.database_name)

            user = users_repository.get_user_by_id(token_info['id'])
            self.validate_role(self.role, user.role)
            g.user = user
            return function(*args, **kwargs)

        return wrapper
