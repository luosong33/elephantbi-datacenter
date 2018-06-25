#!/usr/bin/python
import os


def sqoop2hbase(uuid, host, port, user, pass_, db_name, table_name, rowkey):
    sqoopcom = "sqoop-import --connect jdbc:mysql://"+host+":"+port+"/"+db_name+" --username "+user+" --password "+pass_+" --table "+table_name+\
               " --hbase-table "+uuid+" --column-family c --hbase-row-key "+rowkey+" --hbase-create-table -m 1"
    print(sqoopcom)
    os.system(sqoopcom)

if __name__ == "__main__":
    sqoop2hbase("qweqweqwe","120.55.50.196","3306", "root", "rootROOT.1", "test", "test", "id")