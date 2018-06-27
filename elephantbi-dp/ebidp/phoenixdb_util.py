#!/usr/bin/python
import phoenixdb
import phoenixdb.cursor
import datetime
from flask import current_app
from ebidp.sql_config import insert_meta_sql, query_meta_sql


# phoenix建表
def create_phoenix_table(_uuid, columns_str):
    database_url = current_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)
    cursor = conn.cursor()

    create_table_sql='CREATE TABLE "{0}" ( '.format(str(_uuid))
    columns_list = columns_str.split("^")
    id = columns_list[0]
    create_table_sql = '{0}"{1}" VARCHAR PRIMARY KEY, '\
        .format(create_table_sql, id)
    del columns_list[0]
    for clu in columns_list:
        create_table_sql = '{0}"{1}" VARCHAR, '.format(create_table_sql, clu)
    create_table_sql = create_table_sql[:-2]  # 去掉最后一个逗号
    create_table_sql = '{0})'.format(create_table_sql)

    cursor.execute(create_table_sql)
    conn.close()
    return create_table_sql


# phoenix插入数据
def insert_phoenix(table_name, columns_str, data_list):
    database_url = current_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)
    cursor = conn.cursor()

    clumns_list = columns_str.split("^")
    insert_sql = 'UPSERT INTO "{0}" VALUES (?'.format(table_name)
    for i in range(len(clumns_list) - 1):
        insert_sql = '{0}, ?'.format(insert_sql)
    insert_sql = '{0})'.format(insert_sql)

    for colu in data_list:
        try:
            cursor.execute(insert_sql,colu)
            raise ValueError("Something went wrong!")
        except ValueError as e:
            pass

    conn.close()


# phoenix记录元数据
def insert_metadata(uuid_, create_table_sql, columns):
    database_url = current_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)
    cursor = conn.cursor()

    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(insert_meta_sql, (str(uuid_), create_table_sql,
                                     columns, now_time, now_time))
    conn.close()


# phoenix查询元数据
def query_metadata(table_name, column, value):
    database_url = current_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)
    cursor = conn.cursor()

    query_sql = query_meta_sql % (table_name, column, value)
    cursor.execute(query_sql)
    fetchone = cursor.fetchone()
    conn.close()

    return fetchone


# phoenix查询数据
def query_dp_data(query_sql):
    database_url = current_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)
    cursor = conn.cursor()

    cursor.execute(query_sql)
    fetchall = cursor.fetchall()
    conn.close()

    return fetchall
