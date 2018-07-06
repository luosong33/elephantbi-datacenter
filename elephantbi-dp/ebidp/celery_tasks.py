import json

from ebidp.utils.happy_hbaseutil import create_hbase_table
from ebidp.utils.mysql_util import query_table_columns
from ebidp.utils.phoenixdb_util import (
    insert_metadata, insert_phoenix, create_phoenix_table,
    generate_phoenix_table, query_metadata, generate_hbase_phoenix_table
)
from ebidp.utils.hdf5_util import read_h5_phoenix_data_list, read_h5_columns
from ebidp.utils.sqoop_util import (
    sqoop_create_job_to_hbase, insert_sqoop_meta, query_sqoop_meta,
    sqoop_exec_job_to_hbase, sqoop_to_hbase)
from ebidp.data_proc import data_join_clu
from celery import Celery

celery = Celery(__name__, broker="redis://localhost:6379/0")


@celery.task()
def mysql_to_hbase_task(table_uuid, host_, port, user, password,
                        db_name, table_name, key):
    # 创建hbase表
    create_hbase_table(table_uuid)
    # 创建phoenix映射表
    columns_str = query_table_columns(host_, port, user, password,
                                      db_name, table_name)  # 查询mysql表字段
    hbase_phoenix_table = generate_hbase_phoenix_table(table_uuid, columns_str)
    create_phoenix_table(hbase_phoenix_table)
    # 记录表元数据
    insert_metadata(table_uuid, hbase_phoenix_table, columns_str,
                    hbase_phoenix_table, columns_str)
    # sqoop导入hbase
    sqoop_to_hbase(table_uuid, host_, port, user,
                   password, db_name, table_name, key)


@celery.task()
def mysql_add_to_hbase_task(table_uuid, host_, port, user, password,
                            db_name, table_name, key, gmt_modified):
    # 创建hbase表
    create_hbase_table(table_uuid)
    # 创建phoenix映射表
    columns_str = query_table_columns(host_, port, user, password,
                                      db_name, table_name)  # 查询mysql表字段
    hbase_phoenix_table = generate_hbase_phoenix_table(table_uuid, columns_str)
    create_phoenix_table(hbase_phoenix_table)
    # 记录表元数据
    insert_metadata(table_uuid, hbase_phoenix_table, columns_str,
                    hbase_phoenix_table, columns_str)

    # 创建sqoop任务导入hbase
    job_id = '{0}_{1}_{2}'.format(host_, db_name, table_name)
    # 查询元数据判断是否有任务
    fetchone = query_sqoop_meta(job_id)
    if fetchone is None:
        try:
            sqoop_create_job_to_hbase(job_id, table_uuid, host_, port,
                                      user, password, db_name, table_name,
                                      key, gmt_modified)
        except ValueError as e:
            print(e)
        # 记录sqoop任务元数据
        insert_sqoop_meta(job_id)
    # 执行任务
    sqoop_exec_job_to_hbase(job_id, password)


@celery.task()
def file_to_hbase_task(file_path, table_name, table_uuid):
    # 判断是否为全量或增量
    metadata = query_metadata(table_uuid)
    if metadata is None:
        # 创建phoenix表
        original_columns_str = read_h5_columns(file_path, table_name)
        columns_str = 'ROW^{0}'.format(original_columns_str)
        create_table_sql = generate_phoenix_table(table_uuid, columns_str)
        original_table_sql = generate_phoenix_table(table_uuid,
                                                    original_columns_str)
        create_phoenix_table(create_table_sql)
        # 记录表元数据
        insert_metadata(table_uuid, create_table_sql, columns_str,
                        original_table_sql, original_columns_str)
    else:
        columns_str = metadata[2]

    # 读取文件封装数据 phoenix
    data_list = read_h5_phoenix_data_list(file_path, table_name)
    # 数据导入phoenix
    insert_phoenix(table_uuid, columns_str, data_list)


@celery.task()
def data_join_task(data_str, table_uuid):
    # 数据加工
    data_job = json.loads(data_str)
    join_by = data_job["join_by"]  # 行列连接标识
    if join_by == "col":
        meta = data_job["meta"]
        tmp_table_uuid = ""  # 临时表表名
        same_name = ""  # 结果表有无重名标记
        for i in range(len(meta)):
            m = meta[i]
            join_type = m["join_type"]
            join_conf = m["join_conf"]
            conf0 = join_conf[0]
            join_on0 = ""
            if tmp_table_uuid == "":
                table_id0 = conf0["table_id"]
                join_on0 = conf0["join_on"]
            else:
                table_id0 = tmp_table_uuid
                table_clu_flag = conf0["table_id"]
                if same_name == "" or same_name == "0":  # 结果表无重名，直接取
                    join_on0 = conf0["join_on"]
                elif same_name == "1":  # 结果表有重名，根据标识取
                    # join字段只可能出现两次，用0和1既可区分
                    if table_clu_flag == "0":
                        join_on0 = '{0}_0'.format(conf0["join_on"])
                    elif table_clu_flag == "1":
                        join_on0 = '{0}_1'.format(conf0["join_on"])

            conf1 = join_conf[1]
            table_id1 = conf1["table_id"]
            join_on1 = conf1["join_on"]
            if i == (len(meta) - 1):  # 代表到了最后一次join，传递最终表名
                tmp_table_and_same_name = data_join_clu(table_id0, table_id1,
                                                        join_on0, join_on1,
                                                        join_type, table_uuid,
                                                        tmp_table_uuid)
                tn_sn_list = tmp_table_and_same_name.split("^")
                tmp_table_uuid = tn_sn_list[0]
                same_name = tn_sn_list[1]
            else:
                tmp_table_and_same_name = data_join_clu(table_id0, table_id1,
                                                        join_on0, join_on1,
                                                        join_type, None,
                                                        tmp_table_uuid)
                tn_sn_list = tmp_table_and_same_name.split("^")
                tmp_table_uuid = tn_sn_list[0]
                same_name = tn_sn_list[1]
