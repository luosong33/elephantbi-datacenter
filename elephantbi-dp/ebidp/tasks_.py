import json
from ebidp.celery_ import celery
from ebidp.happy_hbaseutil import createHbaseTable
from ebidp.phoenixdb_util import insert_metadata, insert_phoenix, create_phoenix_table
from ebidp.hdf5_util import readH5_phoenix_datas, redaH5_clumns
from ebidp.sqoop_util import sqoop2hbase
from ebidp.data_proc import data_join_clu


# 异步任务
# @celery.task()
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
