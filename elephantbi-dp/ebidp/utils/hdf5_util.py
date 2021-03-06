#!/usr/bin/python
import pandas as pd


# 获得hdf5文件表数据 返回hbase所需格式： list<dict<dict>>
def read_h5_data_list(file_path, table_name):
    table = pd.read_hdf(file_path, table_name)

    data_list = []
    # 封装数据
    for index_name in table.index:
        line_ = table.loc[index_name]  # 每一行
        line_dict_ = line_.to_dict()  # 每行转化为map（dict）
        clu = {}  # 创建一个dict，以index_的rowkey为key
        clu.setdefault(index_name, line_dict_)
        data_list.append(clu)  # 封装到总list中

    return data_list


# 获得hdf5文件表数据  返回phoenix所需格式： list<list>
def read_h5_phoenix_data_list(file_path, table_name):
    table = pd.read_hdf(file_path, table_name)

    data_list = []
    for line in list(table.values):
        line_list = map(str, line)
        data_list.append(line_list)  # 封装到总list中

    return data_list


# 获得hdf5文件表字段
def read_h5_columns(file_path, table_name):
    table = pd.read_hdf(file_path, table_name)
    columns_list = table.columns.values.tolist()
    columns_str = "^".join(columns_list)
    return columns_str


# hdf5写文件
def write_h5(file_path, table_name, data):
    try:
        data.to_hdf(file_path, table_name)
    except ValueError as e:
        print(e)
