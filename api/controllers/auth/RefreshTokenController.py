from http import HTTPStatus

from dependency_injector.wiring import Provide
from flask import request
from flask.views import MethodView

from api.auth.IRefreshTokenRepository import IRefreshTokenRepository
from api.controllers.auth.LoginController import LoginController
from api.models.Login import Login
from api.schemas.auth.LoginDumpSchema import LoginDumpSchema
from api.schemas.auth.RefreshTokenSchema import RefreshTokenSchema
from entites.user.domain.IUserRepository import IUserRepository
from extension.ApplicationContainer import ApplicationContainer


class RefreshTokenController(MethodView):
    __users_repository: IUserRepository
    __refresh_token_repository: IRefreshTokenRepository

    def __init__(self,
                 users_repository=Provide[ApplicationContainer.repositories.users_repository],
                 refresh_token_repository=Provide[ApplicationContainer.repositories.refresh_token_repository]):
        self.__users_repository = users_repository
        self.__refresh_token_repository = refresh_token_repository

    def post(self):
        """
        Refresh a user token using a refresh token
        :return: A JSON with the updated token
        """
        refresh_token = RefreshTokenSchema().load(request.json)
        refresh_token = refresh_token['refresh_token']

        token_info = self.__refresh_token_repository.get_token(refresh_token)
        user = self.__users_repository.get_user_by_id(token_info.user_id)

        access_token = LoginController.create_access_token(str(user.id))
        login = Login(access_token, refresh_token, user)

        login_serialized = LoginDumpSchema().dump(login)
        return login_serialized, HTTPStatus.CREATED
