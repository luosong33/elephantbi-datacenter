from flask import Flask



def create_app():
    __name__ = "ebidp/learn"
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    ctx = app.app_context()
    ctx.push()

    from .home import home
    app.register_blueprint(home)
    return app