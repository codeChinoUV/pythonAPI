from dependency_injector.wiring import Provide

from entites.user.UsersManager import UserManager
from entites.user.domain.User import User
from extension.ApplicationContainer import ApplicationContainer
from extension.appSettings.MongoSettings import MongoSettings


class InitializeDataBase:

    def __init__(self, mongo_client=Provide[ApplicationContainer.repositories.mongo_instance]):
        mongo_settings = MongoSettings()
        self.__mongo_instance = mongo_client.get_database(mongo_settings.database_name)

    def __create_users_indexes(self):
        users_collection = self.__mongo_instance['users']
        users_collection.create_index('email')
        users_collection.create_index('deleted')

    def __create_indexes(self):
        self.__create_users_indexes()

    def __initialize_roles(self):
        roles_collection = self.__mongo_instance['roles']
        if roles_collection.count_documents({}) == 0:
            roles_collection.insert_many([
                {"role": "NORMAL"},
                {"role": "ADMIN"}
            ])

    def __initialize_users(self):
        users_collection = self.__mongo_instance['users']
        if users_collection.count_documents({}) == 0:

            users_manager = UserManager()
            user = User(id=None, name="Jose Miguel", last_name="Quiroz", email="miguel@admin.com", password="hola9011",
                        role="ADMIN")
            users_manager.create_user(user)

    def initialize_database(self):
        self.__create_indexes()
        self.__initialize_roles()
        self.__initialize_users()

