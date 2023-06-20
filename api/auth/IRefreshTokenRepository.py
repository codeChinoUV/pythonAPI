from abc import ABC

from api.auth.RefreshToken import RefreshToken


class IRefreshTokenRepository(ABC):

    def save_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        """
        Save a refresh token
        :param refresh_token: The token information
        :return: The token saved
        """
        pass

    def get_token(self, token: str) -> RefreshToken:
        """
        Get a refresh token by its token
        :param token: The token
        :return: The refresh token
        """
        pass
