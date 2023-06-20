from datetime import datetime, timezone, timedelta
from http import HTTPStatus

import jwt
from flask import request
from flask.views import MethodView

from api.models.Login import Login
from api.schemas.auth.LoginDumpSchema import LoginDumpSchema
from api.schemas.auth.LoginSchema import LoginSchema
from entites.shared.exceptions.ValidationModelError import ValidationModelError
from entites.user.UserAuthManager import UserAuthManager
from extension.appSettings.SecretKey import SecretKey
from extension.appSettings.TokenSettings import TokenSettings


class LoginController(MethodView):

    @classmethod
    def create_access_token(cls, user_id: str):
        app_secret_key = SecretKey()
        token_settings = TokenSettings()

        expiration_date = datetime.now(tz=timezone.utc) + timedelta(hours=token_settings.hours_expire)
        token = jwt.encode({"id": user_id, "exp": expiration_date}, app_secret_key.secret_key)

        return token

    def post(self):
        """
        Login a user into the app
        :return: A JSON with the login info
        """
        credentials = LoginSchema().load(request.json)

        user_auth_manager = UserAuthManager()
        user = user_auth_manager.validate_user_credentials(credentials["email"], credentials["password"])

        if user is None:
            raise ValidationModelError("Usuario o contraseña invalidos")

        access_token = self.create_access_token(str(user.id))
        refresh_token = user_auth_manager.create_refresh_token(user.id)

        login = Login(access_token, refresh_token, user)
        login_serialized = LoginDumpSchema().dump(login)

        return login_serialized, HTTPStatus.CREATED
