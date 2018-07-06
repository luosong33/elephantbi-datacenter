import os
import phoenixdb
import phoenixdb.cursor
import datetime
import pexpect
from ebidp.configuration import get_config
from ebidp import create_app
from ebidp.sql_config import (
    insert_sqoop_meta_sql, query_sqoop_meta_sql
)


def sqoop_to_hbase(uuid, host, port, user, password, db_name, table_name, key):
    sqoop_con = 'sqoop-import ' \
                '--connect jdbc:mysql://{0}:{1}/{2}' \
                ' --username {3} --password {4}' \
                ' --table {5} --hbase-table {6}' \
                ' --column-family c --hbase-row-key {7}' \
                ' --hbase-create-table -m 1'.\
                format(host, port, db_name, user,
                       password, table_name, uuid, key)
    os.system(sqoop_con)


# 创建sqoop任务
def sqoop_create_job_to_hbase(job_name, table_uuid, host, port, user, password,
                              db_name, table_name, key, gmt_modified):
    sqoop_con = 'sqoop-job --create {0}' \
                ' -- import --connect jdbc:mysql://{1}:{2}/{3}' \
                ' --username {4} --password {5}' \
                ' --table {6} --hbase-table {7}' \
                ' --column-family c --hbase-row-key {8}' \
                ' --hbase-create-table -m 1'\
                ' --incremental lastmodified'\
                ' --check-column {9}' \
                ' --last-value \'2000-01-01 00:00:00\''.\
                format(job_name, host, port, db_name, user,
                       password, table_name, table_uuid, key, gmt_modified)
    os.system(sqoop_con)


# 执行sqoop任务
def sqoop_exec_job_to_hbase(job_name, password):
    # sqoop_con = 'sqoop-job --exec {0}'.format(job_name)
    # os.system(sqoop_con)
    child = pexpect.spawn('sqoop-job --exec {0}'.format(job_name))
    child.expect('password:')  # Enter password:
    child.sendline(password)
    return job_name


# sqoop任务记录元数据
def insert_sqoop_meta(job_id):
    phoenix_app = create_app(get_config('develop'))
    phoenix_app.app_context()
    database_url = phoenix_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)

    with conn.cursor() as cursor:
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(insert_sqoop_meta_sql, (job_id,
                                               now_time, now_time))

    conn.close()


# sqoop查询元数据
def query_sqoop_meta(job_id):
    phoenix_app = create_app(get_config('develop'))
    phoenix_app.app_context()
    database_url = phoenix_app.config['DATABASE_URL']
    conn = phoenixdb.connect(database_url, autocommit=True)

    with conn.cursor() as cursor:
        cursor.execute(query_sqoop_meta_sql, job_id)
        fetchone = cursor.fetchone()
    conn.close()

    return fetchone
