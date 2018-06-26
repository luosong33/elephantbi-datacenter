from flask import Blueprint, current_app
from ebidp.learn.tasks_ import add


home = Blueprint('home', __name__)


@home.route('/')
def helle():
    add.delay(1, 1)
    return 'hello home '+current_app.config['TEST']