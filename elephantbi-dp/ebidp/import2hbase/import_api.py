from flask import Flask,request
from flask_restful import Api
import uuid
import json

# import ebidp
from ebidp.import2hbase.happy_hbaseutil import createHbaseTable
from ebidp.import2hbase.sqoop_util import sqoop2hbase
from celery import Celery
from ebidp.import2hbase.hdf5_util import readH5
from ebidp.import2hbase.happy_hbaseutil import insertHbase
# from tasks_ import file2hbase_task
# from happy_hbaseutil import createHbaseTable
# from sqoop_util import sqoop2hbase
# from celery import Celery
# from hdf5_util import readH5
# from happy_hbaseutil import insertHbase


app = Flask(__name__)
api = Api(app)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route('/mysql2hbase', methods=['POST'])
# def post():
def mysql2hbase():
    uuid_ = uuid.uuid1()
    data = request.data
    j_data = json.loads(data)
    host_ = j_data["host"]
    port = j_data["port"]
    user = j_data["user"]
    pass_ = j_data["pass_"]
    db_name = j_data["db_name"]
    table_name = j_data["table_name"]
    rowkey = j_data["key"]

    r = mysql2hbase_task.delay(str(uuid_), host_, port, user, pass_, db_name, table_name, rowkey)

    return str(uuid_)


@app.route('/file2hbase', methods=['POST'])
def file2hbase():
    uuid_ = uuid.uuid1()
    data = request.data
    j_data = json.loads(data)
    filePath = j_data["filePath"]
    table_name = j_data["table_name"]
    print('app.name:::'+app.name)
    print('filePath:::'+filePath)
    print('table_name:::'+table_name)
    print('uuid_:::'+str(uuid_))

    r = file2hbase_task.delay(str(filePath), str(table_name), str(uuid_))
    # result = file2hbase_task.apply_async(filePath, table_name, uuid_)
    # print('状态：：：' + r.status())

    return str(uuid_)


# 异步任务
@celery.task()
def mysql2hbase_task(uuid_, host_, port, user, pass_, db_name, table_name, rowkey):

    #  创建hbase表
    createHbaseTable(str(uuid_))

    #  sqoop导入hbase
    sqoop2hbase(str(uuid_), host_, port, user, pass_, db_name, table_name, rowkey)


# 异步任务
@celery.task()
def file2hbase_task(filePath, table_name, uuid_):

    print('file2hbase_task:::')
    #  创建hbase表
    createHbaseTable(str(uuid_))

    #  读取封装数据
    columns = readH5(filePath, table_name)

    #  数据导入hbase
    insertHbase(uuid_, columns)


if __name__ == '__main__':
    app.run(debug=True)
