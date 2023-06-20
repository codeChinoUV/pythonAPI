from dependency_injector import containers, providers

from extension.infrastructure.RepositoriesContainer import RepositoriesContainer
from extension.infrastructure.ServicesContainer import ServicesContainer


class ApplicationContainer(containers.DeclarativeContainer):
    """
    Application's container which contain all the dependencies
    """

    config = providers.Configuration()

    repositories = providers.Container(
        RepositoriesContainer,
        config=config
    )

    services = providers.Container(
        ServicesContainer,
        config=config
    )
