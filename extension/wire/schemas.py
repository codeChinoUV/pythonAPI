from api.schemas.auth.RefreshTokenSchema import RefreshTokenSchema
from api.schemas.user.UserEditSchema import UserEditSchema
from api.schemas.user.UserIdSchema import UserIdSchema
from api.schemas.user.UserSchema import UserSchema


def wire_schemas(container):
    """
    Indicate which classes need to inject dependencies
    :param container: The container to wire the classes
    :return: None
    """
    container.wire(packages=[
        # User
        UserSchema,
        UserEditSchema,
        UserIdSchema,

        # Auth
        RefreshTokenSchema,
    ])
