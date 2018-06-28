#!/usr/bin/python
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from uuid import uuid1
import json
from ast import literal_eval

from ebidp.asyn_tasks import (
    mysql_to_hbase_task, file_to_hbase_task, data_join_task
)

bp = Blueprint('simple_page', __name__)
api = Api(bp)


class Test(Resource):
    def get(self):
        return "OK"


mysql_to_hbase_parser_post = reqparse.RequestParser()
mysql_to_hbase_parser_post.add_argument('host', type=str, required=True)
mysql_to_hbase_parser_post.add_argument('port', type=str, required=True)
mysql_to_hbase_parser_post.add_argument('user', type=str, required=True)
mysql_to_hbase_parser_post.add_argument('password', type=str, required=True)
mysql_to_hbase_parser_post.add_argument('db_name', type=str, required=True)
mysql_to_hbase_parser_post.add_argument('table_name', type=str, required=True)
mysql_to_hbase_parser_post.add_argument('key', type=str, required=True)
class MysqlToHbase(Resource):
    def post(self):
        data_job = mysql_to_hbase_parser_post.parse_args()
        table_uuid = uuid1().hex
        host_ = data_job["host"]
        port = data_job["port"]
        user = data_job["user"]
        password = data_job["password"]
        db_name = data_job["db_name"]
        table_name = data_job["table_name"]
        key = data_job["key"]

        # r = mysql2hbase_task.delay(str(uuid_), host_, port, user,
        #                            pass_, db_name, table_name, key)
        mysql_to_hbase_task(table_uuid, host_, port, user, password, db_name,
                            table_name, key)
        return table_uuid


file_to_hbase_parser_post = reqparse.RequestParser()
file_to_hbase_parser_post.add_argument('file_path', type=str, required=True)
file_to_hbase_parser_post.add_argument('table_name', type=str, required=True)
class FileToHbase(Resource):
    def post(self):
        data_job = file_to_hbase_parser_post.parse_args()
        table_uuid = uuid1().hex
        file_path = data_job["file_path"]
        table_name = data_job["table_name"]

        # r = file2hbase_task.delay(str(filePath), str(table_name), str(uuid_))
        file_to_hbase_task(str(file_path), str(table_name), table_uuid)
        return str(table_uuid)


data_processing_parser_post = reqparse.RequestParser()
data_processing_parser_post.add_argument('join_by', type=str,
                                         required=True, location='json')
data_processing_parser_post.add_argument('meta', type=str, required=True,
                                         location='json', action='append')
class DataProcessing(Resource):
    def post(self):
        data_job = data_processing_parser_post.parse_args()
        join_by = data_job['join_by']
        meta_list = data_job['meta']
        meta = list(map(literal_eval, meta_list))

        new_data_job = {
            'meta': meta,
            'join_by': join_by
        }

        data_str = json.dumps(new_data_job)
        table_uuid = uuid1().hex
        # r = data_join_task.delay(data_str, str(uuid_))
        data_join_task(data_str, table_uuid)
        return table_uuid


api.add_resource(Test, '/test')
api.add_resource(MysqlToHbase, '/mysql2hbase')
api.add_resource(FileToHbase, '/file2hbase')
api.add_resource(DataProcessing, '/data_processing')
