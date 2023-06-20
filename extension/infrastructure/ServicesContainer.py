from dependency_injector import containers, providers

from infrastructure.services.encryption.EncryptionService import EncryptionService


class ServicesContainer(containers.DeclarativeContainer):
    """
    Container to inject the services dependencies
    """
    config = providers.Configuration()

    encryption_service = providers.Factory(
        EncryptionService
    )
