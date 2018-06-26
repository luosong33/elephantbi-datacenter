#!/usr/bin/python
import os


def sqoop2hbase(uuid, host, port, user, pass_, db_name, table_name, rowkey):
    sqoopcom = '{0}{1}{2}{3}{4}' \
               '{5}{6}{7}{8}{9}' \
               '{10}{11}{12}{13}' \
               '{14}{15}' \
               '{16}'.\
        format("sqoop-import --connect jdbc:mysql://", host, ":", port, "/",
               db_name, " --username ", user, " --password ", pass_,
               " --table ", table_name, " --hbase-table ", uuid,
               " --column-family c --hbase-row-key ", rowkey,
               " --hbase-create-table -m 1")
    os.system(sqoopcom)
