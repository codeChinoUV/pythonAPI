from dependency_injector.wiring import Provide

from extension.ApplicationContainer import ApplicationContainer


class SecretKey:
    """
    Application secret key
    """

    def __init__(self, secret_key=Provide[ApplicationContainer.config.secretKey]):
        self.secret_key = secret_key
