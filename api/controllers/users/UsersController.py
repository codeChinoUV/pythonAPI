from http import HTTPStatus

from flask import request, jsonify
from flask.views import MethodView

from api.auth.LoginRequired import LoginRequired
from api.extension.wrappers import query_params
from api.schemas.create_paginated_list_schema import create_paginated_list_schema
from api.schemas.user.UserSchema import UserSchema
from entites.user.Roles import Roles
from entites.user.UsersManager import UserManager


class UsersController(MethodView):
    """
    User controller
    Class for manage the end points for users resource
    """

    @LoginRequired(role=Roles.ADMIN)
    def post(self):
        """
        Create a new user
        :return: JSON with the user created
        """
        user = UserSchema().load(request.json)
        users_managers = UserManager()
        user_created = users_managers.create_user(user)
        user_serialized = UserSchema().dump(user_created)
        return user_serialized, HTTPStatus.CREATED

    @LoginRequired(role=Roles.ADMIN)
    @query_params
    def get(self):
        """
        Get users paginated
        :return: A JSON with users registered
        """
        query = request.query_string.decode()
        users_manager = UserManager()
        results = users_manager.get_users(query)
        users_serialized = create_paginated_list_schema(UserSchema).dump(results)
        return jsonify(users_serialized), HTTPStatus.OK
