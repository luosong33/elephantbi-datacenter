import json
from ebidp.utils.happy_hbaseutil import create_hbase_table
from ebidp.utils.phoenixdb_util import (
    insert_metadata, insert_phoenix, create_phoenix_table
)
from ebidp.utils.hdf5_util import read_h5_phoenix_data_list, read_h5_columns
from ebidp.utils.sqoop_util import sqoop_to_hbase
from ebidp.data_proc import data_join_clu


# @celery.task()
def mysql_to_hbase_task(table_uuid, host_, port, user, password,
                        db_name, table_name, key):
    # 创建hbase表
    create_hbase_table(table_uuid)
    # sqoop导入hbase
    sqoop_to_hbase(table_uuid, host_, port, user,
                   password, db_name, table_name, key)


# @celery.task()
def file_to_hbase_task(file_path, table_name, table_uuid):
    #  创建phoenix表
    columns_str = read_h5_columns(file_path, table_name)
    create_table_sql = create_phoenix_table(table_uuid, columns_str)
    #  记录表元数据
    insert_metadata(table_uuid, create_table_sql, columns_str)

    #  读取文件封装数据 phoenix
    data_list = read_h5_phoenix_data_list(file_path, table_name)
    #  数据导入phoenix
    insert_phoenix(table_uuid, columns_str, data_list)


# @celery.task()
def data_join_task(data_str, uuid_):
    #  数据加工
    data_job = json.loads(data_str)
    join_by = data_job["join_by"]  # 行列连接标识
    if join_by == "col":
        meta = data_job["meta"]
        tmp_table = ""
        same_name = ""
        for i in range(len(meta)):
            m = meta[i]
            join_type = m["join_type"]
            join_conf = m["join_conf"]
            conf0 = join_conf[0]
            join_on0 = ""
            if tmp_table == "":
                table_id0 = conf0["table_id"]
                join_on0 = conf0["join_on"]
            else:
                table_id0 = tmp_table
                table_clu_flag = conf0["table_id"]
                if same_name == "" or same_name == "0":  # 结果表无重名，直接取
                    join_on0 = conf0["join_on"]
                elif same_name == "1":  # 结果表有重名，根据标识取
                    if table_clu_flag == "0":
                        join_on0 = '{0}{1}'.format(conf0["join_on"], "_0")
                    elif table_clu_flag == "1":
                        join_on0 = '{0}{1}'.format(conf0["join_on"], "_1")

            conf1 = join_conf[1]
            table_id1 = conf1["table_id"]
            join_on1 = conf1["join_on"]
            if i == (len(meta) - 1):
                tmp_table_and_same_name = data_join_clu(table_id0, table_id1,
                                                        join_on0, join_on1,
                                                        join_type, str(uuid_))
                tn_sn_list = tmp_table_and_same_name.split("^")
                tmp_table = tn_sn_list[0]
                same_name = tn_sn_list[1]
            else:
                tmp_table_and_same_name = data_join_clu(table_id0, table_id1,
                                                        join_on0, join_on1,
                                                        join_type, None)
                tn_sn_list = tmp_table_and_same_name.split("^")
                tmp_table = tn_sn_list[0]
                same_name = tn_sn_list[1]
