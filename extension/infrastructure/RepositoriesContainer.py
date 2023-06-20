from dependency_injector import containers, providers
from pymongo import MongoClient

from infrastructure.repositories.ErrorLoggerRepository import ErrorLoggerRepository
from infrastructure.repositories.LoggerRepository import LoggerRepository
from infrastructure.repositories.RefreshTokenRepository import RefreshTokenRepository
from infrastructure.repositories.RoleRepository import RoleRepository
from infrastructure.repositories.UserRepository import UserRepository


class RepositoriesContainer(containers.DeclarativeContainer):
    """
    Container to inject the repositories dependencies
    """
    config = providers.Configuration()

    mongo_instance = providers.Factory(
        MongoClient,
        host=config.mongodb.connectionString
    )

    users_repository = providers.Factory(
        UserRepository,
        mongo_instance=mongo_instance,
        database_name=config.mongodb.databaseName
    )

    roles_repository = providers.Factory(
        RoleRepository,
        mongo_instance=mongo_instance,
        database_name=config.mongodb.databaseName
    )

    errors_logger_repository = providers.Factory(
        ErrorLoggerRepository,
        mongo_instance=mongo_instance,
        database_name=config.mongodb.databaseName
    )

    logs_repository = providers.Factory(
        LoggerRepository,
        mongo_instance=mongo_instance,
        database_name=config.mongodb.databaseName
    )

    refresh_token_repository = providers.Factory(
        RefreshTokenRepository,
        mongo_instance=mongo_instance,
        database_name=config.mongodb.databaseName
    )
