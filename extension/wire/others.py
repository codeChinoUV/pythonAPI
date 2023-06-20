from api.auth.LoginRequired import LoginRequired
from api.controllers.auth.RefreshTokenController import RefreshTokenController
from api.extension.ErrorHandlers import ErrorHandlers
from api.extension.RequestLogger import RequestLogger
from extension.appSettings.MongoSettings import MongoSettings
from extension.appSettings.SecretKey import SecretKey
from extension.appSettings.TokenSettings import TokenSettings
from extension.infrastructure.InitializeDataBase import InitializeDataBase


def wire_others(container):
    """
    Indicate which classes need to inject dependencies
    :param container: The container to wire the classes
    :return: None
    """
    container.wire(packages=[
        # Controllers
        RefreshTokenController,

        # Errors logger
        ErrorHandlers,

        # Request logger
        RequestLogger,

        # Config
        SecretKey,
        TokenSettings,
        MongoSettings,
        InitializeDataBase,

        # Login
        LoginRequired,
    ])
