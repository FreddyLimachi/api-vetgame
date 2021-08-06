
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from datetime import timedelta

# Importaciones para documentar con swagger
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

from dotenv import load_dotenv
import os


class Settings: # Configuraciones para Flask

    load_dotenv() # Inicializando el entorno de variables

    DEBUG = True

    ENV = "development"

    SECRET_KEY = os.getenv('SECRET_KEY')

    HOST = "0.0.0.0"

    PORT = 5000
    
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_HEADERS = ['Content-Type','Authorization']

    JWT_AUTH_URL_RULE = '/auth'

    JWT_EXPIRATION_DELTA = timedelta(days=30)

    APISPEC_SWAGGER_URL = '/swagger/' # URI para acceder al API Doc JSON 
     
    APISPEC_SWAGGER_UI_URL = '/swagger-ui'  # URI para acceder a la interfaz de usuario de API Doc

    APISPEC_SPEC = APISpec ( 
        title = 'Veterinaria game' , 
        version = 'v1' , 
        plugins = [MarshmallowPlugin () ], 
        openapi_version = '2.0.0'
     )


# Iniciar Flask
app = Flask(__name__)
app.config.from_object(Settings)


# Iniciar modulos
db = SQLAlchemy()
api = Api(app)
ma = Marshmallow(app)
cors = CORS(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
docs = FlaskApiSpec(app)
