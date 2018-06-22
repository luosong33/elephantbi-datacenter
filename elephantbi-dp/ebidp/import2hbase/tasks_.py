# from __future__ import absolute_import, unicode_literals
# from import_api import celery
# from import2hbase.hdf5_util import readH5
# from import2hbase import createHbaseTable
# from import2hbase import insertHbase
#
#
# # @app.task
# # def mysql2hbase_():
#     # mysql2hbase()
#
# @celery.task()
# def file2hbase_task(filePath, table_name, uuid_):
#
#     #  创建hbase表
#     families = {
#         "c": dict()
#     }
#     createHbaseTable(str(uuid_), families)
#
#     #  读取封装数据
#     columns = readH5(filePath, table_name)
#
#     #  数据导入hbase
#     insertHbase(uuid_, columns)
#
