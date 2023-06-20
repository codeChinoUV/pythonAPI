from dependency_injector.wiring import Provide

from extension.ApplicationContainer import ApplicationContainer


class TokenSettings:
    """
    JWT Application settings
    """

    def __init__(self,
                 hours_expire=Provide[ApplicationContainer.config.jwt.hoursExpire],
                 refresh_token_expiration=Provide[ApplicationContainer.config.jwt.refreshTokenHoursExpire]):
        self.hours_expire = hours_expire
        self.refresh_token_hours_expire = refresh_token_expiration
