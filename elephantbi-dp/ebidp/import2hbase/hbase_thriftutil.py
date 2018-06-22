#!/usr/bin/python
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from hbase import Hbase
from hbase.ttypes import ColumnDescriptor, Mutation


class HbaseClient(object):
    def __init__(self, host='localhost', port=9090):
        transport = TTransport.TBufferedTransport(TSocket.TSocket(host, port))
        protocol = TBinaryProtocol.TBinaryProtocol(transport)
        self.client = Hbase.Client(protocol)
        transport.open()

    def get_tables(self):
        """
        获取所有表
        """
        return self.client.getTableNames()

    def create_table(self, table, *columns):
        """
        创建表
        """
        self.client.createTable(table, map(lambda column: ColumnDescriptor(column), columns))

    def put(self, table, row, columns, attributes=None):
        """
        添加记录
        @:param columns {"k:1":"11"}
        """
        # self.client.mutateRow(table, row, map(lambda (k,v): Mutation(column=k, value=v), columns.items()), attributes)

    def scan(self, table, start_row="", columns=None, attributes=None):
        """
        获取记录
        """

        scanner = self.client.scannerOpen(table, start_row, columns, attributes)
        while True:
            r = self.client.scannerGet(scanner)
            if not r:
                break
            # yield dict(map(lambda (k, v): (k, v.value),r[0].columns.items()))

if __name__ == "__main__":
    client = HbaseClient("192.168.19.74", 9090)
    client.create_table("student", "name", "coruse")
    print(client.get_tables())
    client.put("student", "1", {"name:":"zhangsan", "coruse:art": "88", "coruse:math": "12"})
    client.put("student", "2", {"name:":"lisi", "coruse:art": "90", "coruse:math": "100"})
    client.put("student", "3", {"name:":"lisi2"})
    for v in client.scan("student", columns=["name"]):
        print(v)
    for v in client.scan("student"):
        print(v)
