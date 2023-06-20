from flask import Flask

from api.controllers.auth.LoginController import LoginController
from api.controllers.auth.RefreshTokenController import RefreshTokenController
from api.controllers.config.InitializeDatabaseController import InitializeDatabaseController
from api.controllers.users.UserController import UserController
from api.controllers.users.UsersController import UsersController
from api.routes.helpers import register_api


class AppRouter:
    """
    Register API routes
    """

    __app: Flask

    def __init__(self, app: Flask):
        self.__app = app
        self.__register_routes()

    def __register_routes(self):
        # Auth
        register_api(self.__app, LoginController, 'auth/login')
        register_api(self.__app, RefreshTokenController, 'auth/refresh-token')

        # Config
        register_api(self.__app, InitializeDatabaseController, 'config/init-db')

        # Users
        register_api(self.__app, UsersController, 'users')
        register_api(self.__app, UserController, 'users/<string:id>')
