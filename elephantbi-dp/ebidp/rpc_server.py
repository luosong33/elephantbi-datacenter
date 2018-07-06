import json
from uuid import uuid1

from ebidp.celery_tasks import (
    mysql_to_hbase_task, mysql_add_to_hbase_task, file_to_hbase_task
)


class RPCServer(object):
    def rpc_test(self):
        return "RPC OK"

    def mysql_to_hbase(self, json_str):
        data_job = json.loads(json_str)
        table_uuid = uuid1().hex
        host_ = data_job["host"]
        port = data_job["port"]
        user = data_job["user"]
        password = data_job["password"]
        db_name = data_job["db_name"]
        table_name = data_job["table_name"]
        key = data_job["key"]

        mysql_to_hbase_task(table_uuid, host_, port, user,
                            password, db_name, table_name, key)

        return table_uuid

    def mysql_add_to_hbase(self, json_str):
        data_job = json.loads(json_str)
        table_uuid = data_job["table_uuid"]
        host_ = data_job["host"]
        port = data_job["port"]
        user = data_job["user"]
        password = data_job["password"]
        db_name = data_job["db_name"]
        table_name = data_job["table_name"]
        key = data_job["key"]
        gmt_modified = data_job["gmt_modified"]

        mysql_add_to_hbase_task(table_uuid, host_, port, user,
                                password, db_name, table_name, key,
                                gmt_modified)

        return table_uuid

    def file_to_hbase(self, json_str):
        data_job = json.loads(json_str)
        file_path = data_job["file_path"]
        table_name = data_job["table_name"]
        table_uuid = uuid1().hex

        file_to_hbase_task(file_path, table_name, table_uuid)

        return str(table_uuid)

    def file_add_to_hbase(self, json_str):
        data_job = json.loads(json_str)
        file_path = data_job["file_path"]
        table_name = data_job["table_name"]
        table_uuid = data_job["table_uuid"]

        file_to_hbase_task(file_path, table_name, table_uuid)

        return str(table_uuid)
