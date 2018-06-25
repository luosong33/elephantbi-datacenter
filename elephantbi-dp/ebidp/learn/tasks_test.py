import time
from flask import Flask
from flask_restful import Api
from ebidp.learn.tasks import add
app = Flask(__name__)
api = Api(app)

r = add.delay(4, 4) #不要直接 add(4, 4)，这里需要用 celery 提供的接口 delay 进行调用
while not r.ready():
    time.sleep(1)
print('task done: {0}'.format(r.get()))

if __name__ == '__main__':
    app.run(debug=True)