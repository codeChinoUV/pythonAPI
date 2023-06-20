from dataclasses import dataclass

from entites.user.domain.User import User


@dataclass
class Login:
    """
    Login class for login response model
    """
    token: str
    refresh_token: str
    user: User
