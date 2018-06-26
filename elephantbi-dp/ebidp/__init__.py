from flask import Flask
from flask import Blueprint


def create_app(config):
    __name__ = "ebidp/"
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py')
    ctx = app.app_context()
    ctx.push()

    from ebidp.import_api import bp
    app.register_blueprint(bp)

    return app
