#!/usr/bin/python
import happybase

def createHbaseTable(name):
    connection = happybase.Connection(host="localhost", port=9090, timeout=None, autoconnect=True, table_prefix=None, #table_prefix_separator=b'_',
                                      compat='0.98', transport='buffered', protocol='binary')
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



if __name__ == "__main__":
    connection = happybase.Connection(host="localhost", port=9090, timeout=None, autoconnect=True, table_prefix=None,
                                      compat='0.98', transport='buffered', protocol='binary')
    connection.open()
    table = connection.table(str("f77ba62c-738e-11e8-ae56-30b49e461e49"))
    table.put('1333333', {"c:addr": '拉斯凯的军阀孙'})
    connection.close()

