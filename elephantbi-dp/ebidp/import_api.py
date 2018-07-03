#!/usr/bin/python
from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from uuid import uuid1
import json
from ast import literal_eval

from ebidp.celery_tasks import (
    mysql_to_hbase_task, file_to_hbase_task, data_join_task
)
from ebidp.utils.phoenixdb_util import query_metadata

bp = Blueprint('simple_page', __name__)
api = Api(bp)


class Test(Resource):
    def get(self):
        return "OK"


# mysql导入phoenix
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

        r = mysql_to_hbase_task.delay(table_uuid, host_, port, user,
                                   password, db_name, table_name, key)
        return table_uuid


# h5 file导入phoenix
file_to_hbase_parser_post = reqparse.RequestParser()
file_to_hbase_parser_post.add_argument('file_path', type=str, required=True)
file_to_hbase_parser_post.add_argument('table_name', type=str, required=True)
class FileToHbase(Resource):
    def post(self):
        data_job = file_to_hbase_parser_post.parse_args()
        file_path = data_job["file_path"]
        table_name = data_job["table_name"]
        table_uuid = uuid1().hex

        r = file_to_hbase_task.delay(file_path, table_name, table_uuid)
        return str(table_uuid)


# h5 增量file导入phoenix
file_inc_to_hbase_parser_post = reqparse.RequestParser()
file_inc_to_hbase_parser_post.add_argument('file_path', type=str, required=True)
file_inc_to_hbase_parser_post.add_argument('table_name', type=str,
                                           required=True)
file_inc_to_hbase_parser_post.add_argument('table_uuid', type=str,
                                           required=True)
class FileAddToHbase(Resource):
    def post(self):
        data_job = file_inc_to_hbase_parser_post.parse_args()
        file_path = data_job["file_path"]
        table_name = data_job["table_name"]
        table_uuid = data_job["table_uuid"]

        r = file_to_hbase_task.delay(file_path, table_name, table_uuid)
        return str(table_uuid)


# 数据加工
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
        r = data_join_task.delay(data_str, table_uuid)
        return table_uuid


# 元数据查询
meta_query_parser_post = reqparse.RequestParser()
meta_query_parser_post.add_argument('id', type=str,
                                    required=True, location='json')
class MetaQuery(Resource):
    def post(self):
        data_job = meta_query_parser_post.parse_args()
        id_value = data_job['id']
        metadata = query_metadata(id_value)
        return metadata


# 状态查询
task_status_query_parser_post = reqparse.RequestParser()
task_status_query_parser_post.add_argument('id', type=str,
                                           required=True, location='json')
class TaskStatusQuery(Resource):
    def post(self):
        data_job = task_status_query_parser_post.parse_args()
        task_id = data_job['taskid']
        query_metadata(task_id)


api.add_resource(Test, '/test')
api.add_resource(MysqlToHbase, '/mysql_to_hbase')
api.add_resource(FileToHbase, '/file_to_hbase')
api.add_resource(FileAddToHbase, '/file_add_to_hbase')
api.add_resource(DataProcessing, '/data_to_processing')
api.add_resource(MetaQuery, '/meta_query')
