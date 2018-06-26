#!/usr/bin/python
from flask import request, Blueprint
from flask_restful import Api
import uuid
import json

from ebidp.import2hbase.data_proc import data_join_clu
from ebidp.import2hbase.happy_hbaseutil import createHbaseTable
from ebidp.import2hbase.phoenixdb_util import create_phoenix_table, insert_metadata, insert_phoenix
from ebidp.import2hbase.sqoop_util import sqoop2hbase
from ebidp.import2hbase.hdf5_util import redaH5_clumns, readH5_phoenix_datas

bp = Blueprint(__name__)
api = Api(bp)


@bp.route('/test', methods=['GET'])
def test():
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


# 异步任务
@celery.task()
def mysql2hbase_task(uuid_, host_, port, user, pass_, db_name, table_name, rowkey):
    # 创建hbase表
    createHbaseTable(str(uuid_))
    # sqoop导入hbase
    sqoop2hbase(str(uuid_), host_, port, user, pass_, db_name, table_name, rowkey)


@celery.task()
def file2hbase_task(filePath, table_name, uuid_):

    #  创建phoenix表
    clumns_str = redaH5_clumns(filePath, table_name)
    create_table_sql = create_phoenix_table(str(uuid_), clumns_str)
    #  记录表元数据
    insert_metadata(str(uuid_), create_table_sql, clumns_str)

    #  读取文件封装数据 phoenix
    datas = readH5_phoenix_datas(filePath, table_name)
    #  数据导入phoenix
    insert_phoenix(str(uuid_), clumns_str, datas)


@celery.task()
def data_join_task(data_str, uuid_):

    #  数据加工
    data_job = json.loads(data_str)
    join_by = data_job["join_by"]  # 行列连接标识
    if join_by == "col":
        meta = data_job["meta"]
        tmptable = ""
        samename = ""
        for i in range(len(meta)):
            m = meta[i]
            join_type = m["join_type"]
            join_conf = m["join_conf"]
            conf0 = join_conf[0]
            # table_id0 = ""
            join_on0 = ""
            if tmptable == "":
                table_id0 = conf0["table_id"]
                join_on0 = conf0["join_on"]
            else:
                table_id0 = tmptable
                table_clu_flag = conf0["table_id"]
                if samename == "" or samename == "0": # 结果表无重名，直接取
                    join_on0 = conf0["join_on"]
                elif samename == "1": # 结果表有重名，根据标识取
                    if table_clu_flag == "0":
                        join_on0 = '{0}{1}'.format(conf0["join_on"], "_0")
                    elif table_clu_flag == "1":
                        join_on0 = '{0}{1}'.format(conf0["join_on"], "_1")

            conf1 = join_conf[1]
            table_id1 = conf1["table_id"]
            join_on1 = conf1["join_on"]
            if i == (len(meta) - 1):
                tmptable_and_samename = data_join_clu(table_id0, table_id1, join_on0, join_on1, join_type, str(uuid_))
                tn_sn_list = tmptable_and_samename.split("^")
                tmptable = tn_sn_list[0]
                samename = tn_sn_list[1]
            else:
                tmptable_and_samename = data_join_clu(table_id0, table_id1, join_on0, join_on1, join_type, None)
                tn_sn_list = tmptable_and_samename.split("^")
                tmptable = tn_sn_list[0]
                samename = tn_sn_list[1]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # 网络接口
