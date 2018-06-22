from flasgger import Swagger
from flask import Flask
from flask_babel import Babel
from flask_cors import CORS
from flask_jwt import JWT
from flask_mail import Mail
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Flask extensions
cors = CORS()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
mail = Mail()
babel = Babel()
swagger = Swagger()


def create_app(config):
    app = Flask(__name__)

    # Config app
    app.config.from_object(config)

    # Flask-Cors
    cors.init_app(app)

    # Initialize database connection
    db.init_app(app)

    # Flask-Marshmallow
    ma.init_app(app)

    # Flask-Migrate
    migrate.init_app(app, db)

    # Email
    mail.init_app(app)

    # Flask-Babel
    babel.init_app(app)

    # flasgger
    swagger.init_app(app)


    return app
