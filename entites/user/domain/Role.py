from dataclasses import dataclass


@dataclass
class Role:
    """
    Represent a user's role
    """
    id: str = None
    role: str = None
