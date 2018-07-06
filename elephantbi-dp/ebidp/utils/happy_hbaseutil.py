#!/usr/bin/python
import happybase
from ebidp.configuration import get_config
from ebidp import create_app


def create_hbase_table(name):
    phoenix_app = create_app(get_config('develop'))
    phoenix_app.app_context()
    hbase_host = phoenix_app.config['HBASE_HOST']
    hbase_port = phoenix_app.config['HBASE_PORT']
    timeout = phoenix_app.config['TIMEOUT']
    autoconnect = phoenix_app.config['AUTOCONNECT']
    table_prefix = phoenix_app.config['TABLE_PREFIX']
    compat = phoenix_app.config['COMPAT']
    transport = phoenix_app.config['TRANSPORT']
    protocol = phoenix_app.config['PROTOCOL']
    connection = happybase.Connection(host=hbase_host,
                                      port=hbase_port,
                                      timeout=timeout,
                                      autoconnect=autoconnect,
                                      table_prefix=table_prefix,
                                      compat=compat,
                                      transport=transport,
                                      protocol=protocol)
    connection.open()
    try:
        families = {
            "c": dict()
        }
        connection.create_table(name, families)
    except ValueError as e:
        print(e)
    connection.close()


def insert_hbase(table_name, data_list):
    phoenix_app = create_app(get_config('develop'))
    phoenix_app.app_context()
    hbase_host = phoenix_app.config['HBASE_HOST']
    hbase_port = phoenix_app.config['HBASE_PORT']
    timeout = phoenix_app.config['TIMEOUT']
    autoconnect = phoenix_app.config['AUTOCONNECT']
    table_prefix = phoenix_app.config['TABLE_PREFIX']
    compat = phoenix_app.config['COMPAT']
    transport = phoenix_app.config['TRANSPORT']
    protocol = phoenix_app.config['PROTOCOL']
    connection = happybase.Connection(host=hbase_host,
                                      port=hbase_port,
                                      timeout=timeout,
                                      autoconnect=autoconnect,
                                      table_prefix=table_prefix,
                                      compat=compat,
                                      transport=transport,
                                      protocol=protocol)
    connection.open()
    try:
        table = connection.table(str(table_name))
        for line_dict in data_list:
            for key, _dict in line_dict.items():
                data_clu = {}
                for k, v in _dict.items():
                    data_clu.setdefault('c:{0}{1}'.format(str(k), str(v)))

                try:
                    table.put(str(key), data_clu)
                    raise ValueError("Something went wrong!")
                except ValueError as e:
                    print(e)
    except ValueError as e:
        print(e)
    connection.close()
