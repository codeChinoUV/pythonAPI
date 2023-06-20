from flask import Flask
from flask_cors import CORS
from flask_executor import Executor

from api.extension.ErrorHandlers import ErrorHandlers
from api.extension.RequestLogger import RequestLogger
from api.routes.AppRouter import AppRouter
from extension.ApplicationContainer import ApplicationContainer
from extension.wire.wire import wire

# Containers initialization
container = ApplicationContainer()
wire(container)
container.config.from_json('./config.json')

app = Flask(__name__)

# Thread pool
executor = Executor()
executor.init_app(app)
app.config["EXECUTOR_TYPE"] = "thread"
app.config["EXECUTOR_MAX_WORKERS"] = 2


CORS(app)
app.container = container

# Register routes
AppRouter(app)

# Register error handlers
ErrorHandlers(app)

# Register request logger
RequestLogger(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005)
