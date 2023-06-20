from entites.user.UserAuthManager import UserAuthManager
from entites.user.UsersManager import UserManager


def wire_use_cases(container):
    """
    Indicate which classes need to inject dependencies
    :param container: The container to wire the classes
    :return: None
    """
    container.wire(packages=[
        # Auth
        UserAuthManager,

        # Users
        UserManager
    ])
