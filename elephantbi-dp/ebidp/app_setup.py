from flask import g, request, abort
from werkzeug.security import check_password_hash


def register_error_handlers(app, exception_error_handlers):
    for exception, error_handler in exception_error_handlers:
        app.register_error_handler(exception, error_handler)


def register_blueprints(app, *blueprints):
    if blueprints is not None:
        for blueprint in blueprints:
            app.register_blueprint(blueprint)
