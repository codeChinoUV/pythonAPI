from dependency_injector.wiring import Provide

from extension.ApplicationContainer import ApplicationContainer


class MongoSettings:
    """
    Setting for the mongo database
    """

    def __init__(self,
                 connection_string=Provide[ApplicationContainer.config.mongodb.connectionString],
                 database_name=Provide[ApplicationContainer.config.mongodb.databaseName]):
        self.connection_string = connection_string
        self.database_name = database_name
