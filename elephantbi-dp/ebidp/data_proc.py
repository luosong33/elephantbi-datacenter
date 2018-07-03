from uuid import uuid1

import phoenixdb.cursor

from ebidp import create_app
from ebidp.configuration import get_config
from ebidp.sql_config import join_query_sql
from ebidp.utils.phoenixdb_util import (
    query_metadata, create_phoenix_table, insert_metadata,
    generate_phoenix_table, drop_table, delete_meta_table
)


def data_join_clu(table0, table1, join_column0, join_column1,
                  join_type, final_table_uuid, tmp_table):
    # 判断是否为临时表或最终表
    if final_table_uuid is None:
        tmp_table_uuid = uuid1().hex
    else:
        tmp_table_uuid = final_table_uuid

    # 从元数据表获取join后需要建表的字段
    table0_metadata = query_metadata(table0)
    table0_columns = table0_metadata[4]
    table1_metadata = query_metadata(table1)
    table1_columns = table1_metadata[4]
    original_columns_str = '{0}^{1}'.format(table0_columns, table1_columns)

    # 处理重名字段
    columns_list, columns_str_meta, same_name = handle_same(
        original_columns_str, tmp_table_uuid)

    # 获取phoenix表连接
    data_processing_app = create_app(get_config('develop'))
    data_processing_app.app_context()
    database_url = data_processing_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)

    # 查询join数据
    fetchall_list = query_join(conn, columns_list, table0, table1,
                               join_column0, join_column1,
                               join_type, table1_columns)

    # 将查询插入
    insert_join_data(columns_str_meta, conn, fetchall_list, tmp_table,
                     tmp_table_uuid)

    conn.close()
    return '{0}^{1}'.format(tmp_table_uuid, same_name)


# 处理重名字段
def handle_same(original_columns_str, tmp_table_uuid):
    same_name = ""  # 上次join有是否有重名的标识 0不重 1重名
    columns_list = original_columns_str.split("^")
    for clu in set(columns_list):
        count = columns_list.count(clu)
        if count >= 2:
            same_name = "1"
            first_pos = 0  # 最新一次出现的角标
            for i in range(count):
                new_list = columns_list[first_pos:]  # 最新一次出现往后的剩余数据集
                next_pos = new_list.index(clu) + 1  # 剩余数据集中出现的角标
                columns_list[first_pos + new_list.index(clu)] = '{0}_{1}' \
                    .format(clu, str(i))  # 将其添加后缀
                first_pos += next_pos  # 更新角标
        else:
            same_name = "0"

    final_columns_str = "^".join(columns_list)
    columns_str_meta = 'ROW^{0}'.format(final_columns_str)
    final_create_table_sql = generate_phoenix_table(tmp_table_uuid,
                                                    columns_str_meta)
    create_phoenix_table(final_create_table_sql)
    original_create_table_sql = generate_phoenix_table(tmp_table_uuid,
                                                       original_columns_str)
    insert_metadata(tmp_table_uuid, final_create_table_sql, final_columns_str,
                    original_create_table_sql, original_columns_str)
    return columns_list, columns_str_meta, same_name


# 将查询插入
def insert_join_data(columns_str_meta, conn, fetchall_list, tmp_table,
                     tmp_table_uuid):
    with conn.cursor() as cursor:
        insert_join_sql = "UPSERT INTO \"" + tmp_table_uuid + "\" VALUES (?"
        size = len(columns_str_meta.split("^"))
        for i in range(size - 1):
            insert_join_sql += ", ?"
        insert_join_sql += ")"
        for fetchone in fetchall_list:
            fetchone.insert(0, uuid1().hex)
            cursor.execute(insert_join_sql, fetchone)
    # 删除临时表及临时元数据
    if tmp_table != "":
        drop_table(tmp_table)
        delete_meta_table(tmp_table)


# 查询join数据
def query_join(conn, columns_list, table0, table1,
               join_column0, join_column1, join_type, table1_columns):
    with conn.cursor() as cursor:
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

        # 删除第一二行的ROW
        fetchall_list = []
        table1_column_list = table1_columns.split("^")
        for fetchone in fetchall:
            size_index = len(columns_list) - len(table1_column_list) + 1
            fetchone.pop(size_index)
            fetchone.pop(0)
            fetchall_list.append(fetchone)

    return fetchall_list
