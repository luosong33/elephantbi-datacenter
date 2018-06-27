#!/usr/bin/python
import os

from ebidp.configuration import get_config
from ebidp import create_app

# app = create_app(get_config(os.getenv('ENV')))
app = create_app(get_config('develop'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)