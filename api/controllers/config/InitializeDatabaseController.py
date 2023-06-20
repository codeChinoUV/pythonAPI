from http import HTTPStatus

from flask.views import MethodView

from extension.infrastructure.InitializeDataBase import InitializeDataBase


class InitializeDatabaseController(MethodView):

    def post(self):
        """
        Initialize the database
        :return: None
        """
        initialize_database = InitializeDataBase()
        initialize_database.initialize_database()
        return {}, HTTPStatus.NO_CONTENT
