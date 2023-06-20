from dataclasses import dataclass

from entites.user.domain.Role import Role


@dataclass
class User:
    """
    Class for user representation
    """
    id: str = None
    name: str = None
    last_name: str = None
    email: str = None
    password: str = None
    role: Role = None
    deleted: bool = False
