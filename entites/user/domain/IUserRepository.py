from abc import ABC, abstractmethod

from entites.shared.PaginatedList import PaginatedList
from entites.user.domain.User import User


class IUserRepository(ABC):

    @abstractmethod
    def create_user(self, user: User) -> User:
        """
        Save a new user in the database
        :param user: The user to create
        :return: The user saved
        """
        pass

    @abstractmethod
    def exists_email(self, email: str) -> bool:
        """
        Validate if exists a user with the email
        :param email: The email to validate
        :return: True if exists or False is not
        """
        pass

    @abstractmethod
    def can_change_email(self, id: str, email: str) -> bool:
        """
        Validate if the user can change of the email
        :param id: The user's ID to change his email
        :param email: The new email
        :return: True if the user can change or false if not
        """
        pass

    @abstractmethod
    def get_users(self, query: str) -> PaginatedList:
        """
        Get all users using a query string
        :param query: The query string to paginate or filter the data
        :return: A Paginated list with the results
        """
        pass

    @abstractmethod
    def exists_user(self, user_id: str) -> bool:
        """
        Validates if user exists by its ID
        :param user_id: The user's ID to validate
        :return: True if exists or False if not
        """
        pass

    @abstractmethod
    def get_user_by_id(self, id: str):
        """
        Get a user by its ID
        :param id: The user ID to get
        :return: The User with the ID
        """
        pass

    @abstractmethod
    def update_user(self, id: str, data_to_update: dict) -> User:
        """
        Update the fields of a user
        :param id: The user's ID to update
        :param data_to_update: The data to update
        :return: The user with the data updated
        """
        pass

    @abstractmethod
    def delete_user(self, id: str) -> User:
        """
        Delete a user by its ID
        :param id: The user's ID to delete
        :return: The deleted user
        """
        pass

    @abstractmethod
    def are_valid_credentials(self, email: str, password: str) -> bool:
        """
        Validate if the user credentials are valid
        :param email: The email to validate
        :param password: The password to validate
        :return: True if the credentials are valid
        """
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        """
        Get a user by its email
        :param email: The email of thr user to get
        :return: The user
        """
        pass
