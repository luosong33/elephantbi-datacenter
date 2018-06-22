import happybase
import uuid

# class HappyHbaseUtil:
def createHbaseTable(name):
    connection = happybase.Connection(host="localhost", port=9090, timeout=None, autoconnect=True, table_prefix=None, #table_prefix_separator=b'_',
                                      compat='0.98', transport='buffered', protocol='binary')
    connection.open()
    families = {
        "c": dict()
    }
    connection.create_table(name, families)
    connection.close()


def insertHbase(tableName, columns):
    connection = happybase.Connection(host="localhost", port=9090, timeout=None, autoconnect=True, table_prefix=None,
                                      table_prefix_separator=b'_', compat='0.98', transport='buffered',
                                      protocol='binary')
    connection.open()
    table = connection.table(str(tableName))
    for colu in columns:
        for rowkey_, data_ in colu.items():
            data_clu = {}
            for k,v in data_.items():
                data_clu.setdefault("c:"+str(k), str(v))

            try:
                table.put(str(rowkey_), data_clu)
                raise ValueError("Something went wrong!")
            except ValueError as e:
                pass
            else:
                b.send()

    connection.close()



if __name__ == "__main__":
    # uuid_ = uuid.uuid1()
    # families = {
    #     "c": dict()
    # }
    # createHbaseTable(str(uuid_), families)

    connection = happybase.Connection(host="localhost", port=9090, timeout=None, autoconnect=True, table_prefix=None, #table_prefix_separator=b'_',
                                      compat='0.98', transport='buffered', protocol='binary')
    connection.open()
    table = connection.table(str("qweqweqwe"))
    # b = table.batch()
    # b.put(b'1333333', {b'c:addr': b'拉斯凯的军阀孙', b'c:phoen': b'13111115555'})
    table.put('1333333', {"c:addr": '拉斯凯的军阀孙'})
    connection.close()

