#!/usr/bin/python
import os


def sqoop2hbase(uuid, host, port, user, pass_, db_name, table_name, key):
    sqoopcom = 'sqoop-import ' \
               '--connect jdbc:mysql://{0}:{1}/{2}' \
               ' --username {3} --password {4}' \
               ' --table {5} --hbase-table {6}' \
               ' --column-family c --hbase-row-key {7}' \
               ' --hbase-create-table -m 1'.\
        format(host, port, db_name, user, pass_, table_name, uuid, key)
    os.system(sqoopcom)
