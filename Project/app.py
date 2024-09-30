from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from datetime import timedelta
from flask_smorest import Api
from flask import Flask

from db import db, migrate
import models

from resources.auth import blp as AuthBlueprint

import os

load_dotenv()


def create_app(db_url=None):

    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = 'tu_clave_secreta_muy_segura' 
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=int(os.getenv("TOKEN_VALID_TIME")))
    app.config["PROPAGATE_EXCEPTIONS"]= True
    app.config["API_TITLE"] = "Airbnb REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/documentation"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url or os.environ.get('DATABASE_URI') 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    
    api = Api(app)
    jwt = JWTManager(app)

    with app.app_context():
        db.create_all()


    api.register_blueprint(AuthBlueprint)

    return app


