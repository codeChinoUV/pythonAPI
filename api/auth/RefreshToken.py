from dataclasses import dataclass
from typing import Any


@dataclass
class RefreshToken:
    token: str
    user_id: str
    expiration_time: Any
    id: str = None
