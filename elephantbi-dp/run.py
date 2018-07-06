import os

from ebidp import create_app
from ebidp.configuration import get_config

app_env = os.getenv('APP_ENV')
app = create_app(get_config(app_env))

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80, debug=True)
