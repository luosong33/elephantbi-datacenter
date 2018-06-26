#!/usr/bin/python
from flask import request, Blueprint, current_app
from flask_restful import Api, Resource
import uuid
import json

from ebidp.tasks_ import mysql2hbase_task, file2hbase_task, data_join_task

bp = Blueprint('simple_page', __name__, template_folder='templates')
api = Api(bp)


class test(Resource):
    def get(self):
        return "OK"


@bp.route('/mysql2hbase', methods=['POST'])
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
    key = j_data["key"]

    # r = mysql2hbase_task.delay(str(uuid_), host_, port, user, pass_, db_name, table_name, rowkey)
    mysql2hbase_task(str(uuid_), host_, port, user, pass_, db_name, table_name, key)
    return str(uuid_)


@bp.route('/file2hbase', methods=['POST'])
def file2hbase():
    uuid_ = uuid.uuid1()
    data = request.data
    j_data = json.loads(data)
    filePath = j_data["filePath"]
    table_name = j_data["table_name"]

    r = file2hbase_task.delay(str(filePath), str(table_name), str(uuid_))
    return str(uuid_)


@bp.route('/data_processing', methods=['POST'])
def data_processing():
    uuid_ = uuid.uuid1()
    data_job = request.data
    data_dict = json.loads(data_job)
    data_str = json.dumps(data_dict)
    r = data_join_task.delay(data_str, str(uuid_))
    return str(uuid_)


api.add_resource(test, '/test')