#!/usr/bin/python
from uuid import uuid1
import phoenixdb
import phoenixdb.cursor
import datetime
from ebidp.sql_config import (
    insert_meta_sql, query_meta_sql
)
from ebidp.configuration import get_config
from ebidp import create_app


# phoenix生成建表sql语句
def generate_phoenix_table(table_uuid, columns_str):
    create_table_sql = "CREATE TABLE \"" + table_uuid + "\" ( "
    columns_list = columns_str.split("^")
    col_id = columns_list[0]
    create_table_sql += "\"" + col_id + "\" VARCHAR PRIMARY KEY, "
    columns_list.pop(0)
    for clu in columns_list:
        create_table_sql += "\"" + clu + "\" VARCHAR, "
    create_table_sql = create_table_sql[:-2]  # 去掉最后一个逗号
    create_table_sql += ")"

    return create_table_sql


# phoenix建表
def create_phoenix_table(create_sql):
    phoenix_app = create_app(get_config('develop'))
    phoenix_app.app_context()
    database_url = phoenix_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)

    with conn.cursor() as cursor:
        cursor.execute(create_sql)

    conn.close()


# phoenix插入数据
def insert_phoenix(table_name, columns_str, data_list):
    phoenix_app = create_app(get_config('develop'))
    phoenix_app.app_context()
    database_url = phoenix_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)

    with conn.cursor() as cursor:
        columns_list = columns_str.split("^")
        insert_sql = "UPSERT INTO \"" + table_name + "\" VALUES (?"
        for i in range(len(columns_list) - 1):
            insert_sql += ", ?"
        insert_sql += ")"

        for clu in data_list:
            try:
                clu = list(clu)
                clu.insert(0, uuid1().hex)
                cursor.execute(insert_sql, clu)
            except ValueError as e:
                print(e)

    conn.close()


# phoenix记录元数据
def insert_metadata(table_uuid, create_table_sql, columns,
                    original_table_sql, original_columns):
    phoenix_app = create_app(get_config('develop'))
    phoenix_app.app_context()
    database_url = phoenix_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)

    with conn.cursor() as cursor:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(insert_meta_sql, (table_uuid,
                                         create_table_sql, columns,
                                         original_table_sql, original_columns,
                                         now_time, now_time))

    conn.close()


# phoenix查询元数据
def query_metadata(value):
    phoenix_app = create_app(get_config('develop'))
    phoenix_app.app_context()
    database_url = phoenix_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)

    with conn.cursor() as cursor:
        query_sql = query_meta_sql % value
        cursor.execute(query_sql)
        fetchone = cursor.fetchone()
    conn.close()

    return fetchone


# phoenix删除元数据
def delete_meta_table(table_name):
    phoenix_app = create_app(get_config('develop'))
    phoenix_app.app_context()
    database_url = phoenix_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)

    with conn.cursor(cursor_factory=phoenixdb.cursor.DictCursor) as cursor:
        drop_sql = "delete from \"meta_table\" where \"id\" = '" \
                   + table_name + "'"
        cursor.execute(drop_sql)
    conn.close()


# phoenix查询数据
def query_dp_data(query_sql):
    phoenix_app = create_app(get_config('develop'))
    phoenix_app.app_context()
    database_url = phoenix_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)
    with conn.cursor() as cursor:
        cursor.execute(query_sql)
        fetchall = cursor.fetchall()
    conn.close()

    return fetchall


# phoenix删除表
def drop_table(table_name):
    phoenix_app = create_app(get_config('develop'))
    phoenix_app.app_context()
    database_url = phoenix_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)

    with conn.cursor(cursor_factory=phoenixdb.cursor.DictCursor) as cursor:
        drop_sql = "drop table \"" + table_name + "\""
        cursor.execute(drop_sql)
    conn.close()
