from dependency_injector.wiring import Provide
from marshmallow import validates

from api.schemas.CommonSchema import CommonSchema
from api.schemas.extension.fields.ObjectPathId import ObjectIdPath
from entites.shared.exceptions.NotFoundError import NotFoundError
from entites.user.domain.IUserRepository import IUserRepository
from extension.ApplicationContainer import ApplicationContainer


class UserIdSchema(CommonSchema):
    """
    Necessary validations for the user id
    """

    __users_repository: IUserRepository

    id = ObjectIdPath()

    def __init__(self,
                 users_repository=Provide[ApplicationContainer.repositories.users_repository],
                 *args,
                 **kwargs):
        super().__init__(None, *args, **kwargs)
        self.__users_repository = users_repository

    @validates('id')
    def validate_exists_user(self, user_id: str):
        if user_id is not None:
            if not self.__users_repository.exists_user(user_id):
                raise NotFoundError(str(user_id), "usuarios")
