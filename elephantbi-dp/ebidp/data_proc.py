#!/usr/bin/python
import uuid
import phoenixdb.cursor
from flask import current_app
from ebidp.phoenixdb_util import (
    query_metadata, create_phoenix_table, insert_metadata
)
from ebidp.sql_config import join_query_sql


def data_join_clu(table0, table1, join_column0, join_column1, join_type, _uuid):

    if _uuid is None:
        tmp_uuid = uuid.uuid1()
    else:
        tmp_uuid = _uuid
    database_url = current_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)

    # 封装join后表结构并建表
    table0_metadata = query_metadata("meta_table", "id", table0)
    table0_columns = table0_metadata[2]
    table1_metadata = query_metadata("meta_table", "id", table1)
    table1_columns = table1_metadata[2]
    columns_str = '{0}^{1}'.format(table0_columns, table1_columns)
    # 处理重名字段
    same_name_flag = ""  # 是否重名标识 0不重 1重名
    columns_list = columns_str.split("^")
    for clu in set(columns_list):
        count = columns_list.count(clu)
        if count >= 2:
            same_name_flag = "1"
            first_pos = 0  # 最新一次出现的角标
            for i in range(count):
                new_list = columns_list[first_pos:]  # 最新一次出现往后的剩余数据集
                next_pos = new_list.index(clu) + 1  # 剩余数据集中出现的角标
                columns_list[first_pos + new_list.index(clu)] = '{0}_{1}'\
                    .format(clu, str(i))  # 将其添加后缀
                first_pos += next_pos  # 更新角标
        else:
            same_name_flag = "0"
    columns_str = "^".join(columns_list)
    columns_str_meta = 'ROW^{0}'.format(columns_str)

    create_table_sql = create_phoenix_table(str(tmp_uuid), columns_str_meta)
    insert_metadata(str(tmp_uuid), create_table_sql, columns_str)

    # 查询join数据并插入
    cursor = conn.cursor()
    join_str = ""
    if join_type == "left":
        join_str = "left join"
    elif join_type == "right":
        join_str = "right join"
    elif join_type == "inner":
        join_str = "inner join"
    elif join_type == "full":
        join_str = "full join"
    query_sql = join_query_sql % (table0, join_str, table1,
                                      join_column0, join_column1)
    cursor.execute(query_sql)
    fetchall = cursor.fetchall()

    # 插入
    sql = 'UPSERT INTO "{0}" VALUES (?'.format(str(tmp_uuid))
    size = len(columns_str_meta.split("^"))
    for i in range(size - 1):
        sql = '{0}, ?'.format(sql)
    sql = '{0})'.format(sql)
    for fetchone in fetchall:
        fetchone.insert(0, str(uuid.uuid1()))
        cursor.execute(sql, fetchone)

    return '{0}^{1}'.format(str(tmp_uuid), same_name_flag)
