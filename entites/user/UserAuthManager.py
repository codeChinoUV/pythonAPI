import uuid
from datetime import datetime, timezone, timedelta

from dependency_injector.wiring import Provide

from api.auth.IRefreshTokenRepository import IRefreshTokenRepository
from api.auth.RefreshToken import RefreshToken
from entites.shared.encryption.IEncriptionService import IEncryptionService
from entites.user.domain.IUserRepository import IUserRepository
from entites.user.domain.User import User
from extension.ApplicationContainer import ApplicationContainer
from extension.appSettings.TokenSettings import TokenSettings


class UserAuthManager:
    __user_repository: IUserRepository
    __refresh_token_repository: IRefreshTokenRepository
    __encryption_service: IEncryptionService

    def __init__(self,
                 user_repository=Provide[ApplicationContainer.repositories.users_repository],
                 refresh_token_repository=Provide[ApplicationContainer.repositories.refresh_token_repository],
                 encryption_service=Provide[ApplicationContainer.services.encryption_service]):
        self.__user_repository = user_repository
        self.__refresh_token_repository = refresh_token_repository
        self.__encryption_service = encryption_service

    def validate_user_credentials(self, email: str, password: str) -> User:
        """
        Validate if the user credentials are valid
        :param email: The user's email
        :param password: The user's password
        :return: The user if the credentials are valid, None if not
        """
        user = self.__user_repository.get_user_by_email(email)

        if user is None or not self.__encryption_service.check_encrypted_value(user.password, password):
            return None

        return user

    def create_refresh_token(self, user_id: str):
        token_settings = TokenSettings()
        expiration_time = datetime.now(tz=timezone.utc) + timedelta(hours=token_settings.refresh_token_hours_expire)
        token = uuid.uuid4()

        refresh_token = RefreshToken(str(token), user_id, expiration_time)
        saved_token = self.__refresh_token_repository.save_refresh_token(refresh_token)

        return saved_token.token
