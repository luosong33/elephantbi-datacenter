#!/usr/bin/python
import happybase

from flask import current_app
# from import_api import app as current_app

def createHbaseTable(name):
    HBASE_HOST = current_app.config['HBASE_HOST']
    HBASE_PORT = current_app.config['HBASE_PORT']
    TIMEOUT = current_app.config['TIMEOUT']
    AUTOCONNECT = current_app.config['AUTOCONNECT']
    TABLE_PREFIX = current_app.config['TABLE_PREFIX']
    COMPAT = current_app.config['COMPAT']
    TRANSPORT = current_app.config['TRANSPORT']
    PROTOCOL = current_app.config['PROTOCOL']
    # connection = happybase.Connection(host="localhost", port=9090, timeout=None, autoconnect=True, table_prefix=None,
    #                                   compat='0.98', transport='buffered', protocol='binary')
    connection = happybase.Connection(host=HBASE_HOST,
                                      port=HBASE_PORT,
                                      timeout=TIMEOUT,
                                      autoconnect=AUTOCONNECT,
                                      table_prefix=TABLE_PREFIX,
                                      compat=COMPAT,
                                      transport=TRANSPORT,
                                      protocol=PROTOCOL)
    connection.open()
    families = {
        "c": dict()
    }
    connection.create_table(name, families)
    connection.close()


def insertHbase(tableName, datas):
    connection = happybase.Connection(host="localhost", port=9090, timeout=None, autoconnect=True, table_prefix=None,
                                      table_prefix_separator=b'_', compat='0.98', transport='buffered',
                                      protocol='binary')
    connection.open()
    table = connection.table(str(tableName))
    for colu in datas:
        for rowkey_, data_ in colu.items():
            data_clu = {}
            for k,v in data_.items():
                data_clu.setdefault('{0}{1}'.format("c:", str(k)), str(v))

            try:
                table.put(str(rowkey_), data_clu)
                raise ValueError("Something went wrong!")
            except ValueError as e:
                pass
            else:
                b.send()

    connection.close()

if __name__ == '__main__':
    createHbaseTable("test_config")
