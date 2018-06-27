#!/usr/bin/python
from flask import request, Blueprint
from flask_restful import Api, Resource
from uuid import uuid1
import json

from ebidp.asyn_tasks import (
    mysql_to_hbase_task, file_to_hbase_task, data_join_task
)

bp = Blueprint('simple_page', __name__, template_folder='templates')
api = Api(bp)


class Test(Resource):
    def get(self):
        return "OK"


class MysqlToHbase(Resource):
    def post(self):
        data = request.data
        table_uuid = uuid1().hex
        j_data = json.loads(data)
        host_ = j_data["host"]
        port = j_data["port"]
        user = j_data["user"]
        pass_ = j_data["pass_"]
        db_name = j_data["db_name"]
        table_name = j_data["table_name"]
        key = j_data["key"]

        # r = mysql2hbase_task.delay(str(uuid_), host_, port, user,
        #                            pass_, db_name, table_name, key)
        mysql_to_hbase_task(table_uuid, host_, port, user, pass_, db_name,
                            table_name, key)
        return table_uuid


class FileToHbase(Resource):
    def post(self):
        data = request.data
        table_uuid = uuid1().hex
        j_data = json.loads(data)
        file_path = j_data["filePath"]
        table_name = j_data["table_name"]

        # r = file2hbase_task.delay(str(filePath), str(table_name), str(uuid_))
        file_to_hbase_task(str(file_path), str(table_name), table_uuid)
        return str(table_uuid)


class DataProcessing(Resource):
    def post(self):
        data_job = request.data
        data_dict = json.loads(data_job)
        data_str = json.dumps(data_dict)
        table_uuid = uuid1().hex
        # r = data_join_task.delay(data_str, str(uuid_))
        data_join_task(data_str, table_uuid)
        return table_uuid


api.add_resource(Test, '/test')
api.add_resource(MysqlToHbase, '/mysql2hbase')
api.add_resource(FileToHbase, '/file2hbase')
api.add_resource(DataProcessing, '/data_processing')