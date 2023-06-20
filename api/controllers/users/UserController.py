from http import HTTPStatus

from flask import request
from flask.views import MethodView

from api.auth.LoginRequired import LoginRequired
from api.schemas.user.UserEditSchema import UserEditSchema
from api.schemas.user.UserIdSchema import UserIdSchema
from api.schemas.user.UserSchema import UserSchema
from api.schemas.validate_id import validate_id
from entites.user.Roles import Roles
from entites.user.UsersManager import UserManager


class UserController(MethodView):

    @LoginRequired(role=Roles.ADMIN)
    def get(self, id: str):
        """
        Get a user by its ID
        :return: a JSON with the user information
        """
        id = validate_id(UserIdSchema(), id)
        users_manager = UserManager()
        user = users_manager.get_user(id)
        user_serialized = UserSchema().dump(user)
        return user_serialized, HTTPStatus.OK

    @LoginRequired(role=Roles.ADMIN)
    def patch(self, id: str):
        """
        Edit some information of a user
        :param id: The user's ID to update
        :return: A JSON with the updated info of the user
        """
        id = validate_id(UserIdSchema(), id)
        info_to_update = UserEditSchema(id).load(request.json)
        users_manager = UserManager()
        user = users_manager.update_user(id, info_to_update)
        serialized_user = UserSchema().dump(user)
        return serialized_user, HTTPStatus.OK

    @LoginRequired(role=Roles.ADMIN)
    def delete(self, id: str):
        """
        Delete a user
        :param id: The user's ID to delete
        :return: A JSON with the user deleted
        """
        id = validate_id(UserIdSchema(), id)
        users_manager = UserManager()
        user_deleted = users_manager.delete_user(id)
        serialized_user = UserSchema().dump(user_deleted)
        return serialized_user, HTTPStatus.OK
