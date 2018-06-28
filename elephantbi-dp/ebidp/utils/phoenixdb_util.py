#!/usr/bin/python
import phoenixdb
import phoenixdb.cursor
import datetime
from flask import current_app
from ebidp.sql_config import (
    insert_meta_sql, query_meta_sql,
    create_phoenix_prefix, create_phoenix_key,
    create_phoenix_column, create_phoenix_suffix,
    insert_phoenix_prefix, insert_phoenix_column, insert_phoenix_suffix
)


# phoenix生成建表sql语句
def generate_phoenix_table(table_uuid, columns_str):
    create_table_sql = create_phoenix_prefix % table_uuid
    columns_list = columns_str.split("^")
    table_id = columns_list[0]
    create_table_sql = create_phoenix_key % (create_table_sql, table_id)
    columns_list.pop(0)
    for clu in columns_list:
        create_table_sql = create_phoenix_column % (create_table_sql, clu)
    create_table_sql = create_table_sql[:-2]  # 去掉最后一个逗号
    create_table_sql = create_phoenix_suffix % create_table_sql

    return create_table_sql


# phoenix建表
def create_phoenix_table(create_sql):
    database_url = current_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)

    with conn.cursor() as cursor:
        cursor.execute(create_sql)

    conn.close()


# phoenix插入数据
def insert_phoenix(table_name, columns_str, data_list):
    database_url = current_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)

    with conn.cursor() as cursor:
        columns_list = columns_str.split("^")
        insert_sql = insert_phoenix_prefix % table_name
        for i in range(len(columns_list) - 1):
            insert_sql = insert_phoenix_column % insert_sql
        insert_sql = insert_phoenix_suffix % insert_sql

        for clu in data_list:
            try:
                cursor.execute(insert_sql, clu)
            except ValueError as e:
                print(e)

    conn.close()


# phoenix记录元数据
def insert_metadata(table_uuid, create_table_sql, columns,
                    original_table_sql, original_columns):
    database_url = current_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)

    with conn.cursor() as cursor:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(insert_meta_sql, (table_uuid,
                                         create_table_sql, columns,
                                         original_table_sql, original_columns,
                                         now_time, now_time))

    conn.close()


# phoenix查询元数据
def query_metadata(table_name, column, value):
    database_url = current_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)

    with conn.cursor() as cursor:
        query_sql = query_meta_sql % (table_name, column, value)
        cursor.execute(query_sql)
        fetchone = cursor.fetchone()
    conn.close()

    return fetchone


# phoenix查询数据
def query_dp_data(query_sql):
    database_url = current_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)
    with conn.cursor() as cursor:
        cursor.execute(query_sql)
        fetchall = cursor.fetchall()
    conn.close()

    return fetchall
