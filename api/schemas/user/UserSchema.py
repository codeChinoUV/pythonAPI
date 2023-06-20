from dependency_injector.wiring import Provide
from marshmallow import fields, validate, validates, ValidationError

from api.schemas.CommonSchema import CommonSchema
from api.schemas.extension.errors import get_string_error_messages, get_length_error_message, \
    get_invalid_email_error_message, get_one_of_error_message
from entites.user.Roles import Roles

from entites.user.domain.IRoleRepository import IRoleRepository
from entites.user.domain.IUserRepository import IUserRepository
from entites.user.domain.User import User
from extension.ApplicationContainer import ApplicationContainer


class UserSchema(CommonSchema):
    __users_repository: IUserRepository
    __roles_repository: IRoleRepository

    def __init__(self, users_repository=Provide[ApplicationContainer.repositories.users_repository],
                 roles_repository=Provide[ApplicationContainer.repositories.roles_repository], *args, **kwargs):
        super().__init__(schema_class_to_map=User, *args, **kwargs)
        self.__users_repository = users_repository
        self.__roles_repository = roles_repository

    id = fields.Str(dump_only=True)
    name = fields.Str(
        required=True,
        allow_none=False,
        validate=validate.Length(min=2, error=get_length_error_message(2)),
        error_messages=get_string_error_messages()
    )
    lastName = fields.Str(
        required=True,
        allow_none=False,
        validate=validate.Length(min=2, error=get_length_error_message(2)),
        error_messages=get_string_error_messages()
    )
    password = fields.Str(
        load_only=True,
        required=True,
        allow_none=False,
        validate=validate.Length(min=6, error=get_length_error_message(6)),
        error_messages=get_string_error_messages()
    )
    email = fields.Str(
        required=True,
        allow_none=False,
        validate=validate.Email(error=get_invalid_email_error_message()),
        error_messages=get_string_error_messages()
    )
    role = fields.Str(
        required=True,
        allow_none=False,
        validate=validate.OneOf(Roles.get_all_roles(), error=get_one_of_error_message(Roles.get_all_roles())),
        error_messages=get_string_error_messages()
    )

    @validates('email')
    def validate_unique_email(self, email):
        """
        Validate if the email is not in use
        :param email: The email to validate
        :return: None
        """
        if email is not None:
            if self.__users_repository.exists_email(email):
                error_message = f'Ya existe un usuario registrado con el correo {email}'
                raise ValidationError(error_message)

    @validates('role')
    def exists_role(self, role):
        """
        Validate if the role exists
        :param role: The role to validate
        :return: None
        """
        if role is not None:
            if self.__roles_repository.find_by_name(role) is None:
                error_message = f'El rol {role} no existe'
                raise ValidationError(error_message)
