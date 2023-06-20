from datetime import datetime, timezone

from dependency_injector.wiring import Provide
from marshmallow import fields, validates, ValidationError
from pytz import utc

from api.auth.IRefreshTokenRepository import IRefreshTokenRepository
from api.schemas.CommonSchema import CommonSchema
from api.schemas.extension.errors import get_string_error_messages
from extension.ApplicationContainer import ApplicationContainer


class RefreshTokenSchema(CommonSchema):
    __refresh_tokens_repository: IRefreshTokenRepository

    refreshToken = fields.Str(required=True, allow_none=False, error_messages=get_string_error_messages())

    def __init__(self,
                 refresh_tokens_repository=Provide[ApplicationContainer.repositories.refresh_token_repository],
                 *args,
                 **kwargs):
        super().__init__(None, *args, **kwargs)
        self.__refresh_tokens_repository = refresh_tokens_repository

    @validates('refreshToken')
    def validate_refresh_token(self, token):
        refresh_token_info = self.__refresh_tokens_repository.get_token(token)

        if refresh_token_info is None:
            raise ValidationError('El token de re-autenticacion no es valido')

        expiration_date = utc.localize(refresh_token_info.expiration_time)
        current_date = utc.localize(datetime.now())

        if expiration_date <= current_date:
            raise ValidationError('El token a expirado')
