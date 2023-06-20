from dependency_injector.wiring import Provide

from entites.shared.PaginatedList import PaginatedList
from entites.shared.encryption.IEncriptionService import IEncryptionService
from entites.user.domain.IUserRepository import IUserRepository
from entites.user.domain.User import User
from extension.ApplicationContainer import ApplicationContainer


class UserManager:
    __user_repository: IUserRepository
    __encryption_service: IEncryptionService

    def __init__(self,
                 user_repository=Provide[ApplicationContainer.repositories.users_repository],
                 encryption_service=Provide[ApplicationContainer.services.encryption_service]):
        self.__user_repository = user_repository
        self.__encryption_service = encryption_service

    def create_user(self, user: User) -> User:
        """
        Create a new user
        :param user: The user to create
        :return: The created user
        """
        user.password = self.__encryption_service.encrypt(user.password)
        return self.__user_repository.create_user(user)

    def get_users(self, query='') -> PaginatedList:
        """
        Get the saved users using a query
        :param query: The query to filter, sort or paginate the users
        :return: The saved users
        """
        return self.__user_repository.get_users(query)

    def get_user(self, user_id: str) -> User:
        """
        Get a user by its ID
        :param user_id: The user's ID to get
        :return: A User
        """
        return self.__user_repository.get_user_by_id(user_id)

    def update_user(self, user_id: str, fields_to_update: dict) -> User:
        """
        Update a user by its ID
        :param user_id: The user's ID to update
        :param fields_to_update: The fields with the info to update
        :return: The user updated
        """
        if "password" in fields_to_update.keys():
            fields_to_update["password"] = self.__encryption_service.encrypt(fields_to_update["password"])

        return self.__user_repository.update_user(user_id, fields_to_update)

    def delete_user(self, user_id: str) -> User:
        """
        Delete a user by its ID
        :param user_id: The user's ID to delete
        :return: A user
        """
        return self.__user_repository.delete_user(user_id)
