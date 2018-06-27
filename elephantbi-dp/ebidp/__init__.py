from flask import Flask


def create_app(config):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config)
    ctx = app.app_context()
    ctx.push()

    from ebidp.import_api import bp
    app.register_blueprint(bp)

    return app
