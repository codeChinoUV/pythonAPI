from abc import ABC, abstractmethod

from entites.user.domain.Role import Role


class IRoleRepository(ABC):

    @abstractmethod
    def find_by_name(self, name: str) -> Role:
        """
        Find a role by its name
        :param name: The role's name
        :return: The role if exits or None if not
        """
        pass
