### Base Python API

The base for create a flask API, this base include:
- Routes configuration
- Schemas load and dump configuration
- request and responses logger
- Error logger
- JWT authentication
- Dependency injection
- Thread pools
- Docker configuration

* * *

#### Setup docker compose
To set up the docker compose perform the next actions:
1. Create a .envDB file using the .envDB.example file like template
2. Create a config.json file using the config.json.example file like template
3. Run the command ```docker-compose build```
4. Run the command ```docker-compose up```
5. The development server is listening on the port **5005**
6. The production server using nginx is listening on the port **8082**
7. To set up the database and seed the initial user perform an POST request to the endpoint **/api/config/init-db**