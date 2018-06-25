from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)

# 可独立启动，而不用flask run
# 也可以使用python /home/luosong/workspace/elephantbi-datacenter/elephantbi-dp/ebidp/learn/restfulhallo.py  运行
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'python restful'}

# 定义url
api.add_resource(HelloWorld, '/hello')

if __name__ == '__main__':
    app.run(debug=True)