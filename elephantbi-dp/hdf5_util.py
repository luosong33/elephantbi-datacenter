#!/usr/bin/python
import pandas as pd


# 获得hdf5文件表数据  返回hbase所需格式： list<dict<dict>>
def readH5_datas(filePath, table_name):
    table_ = pd.read_hdf(filePath, table_name)
    datas = []
    #  封装数据
    for index_ in table_.index:
        line_ = table_.loc[index_]    #每一行
        line_dict_ = line_.to_dict()  #每行转化为map（dict）
        colu = {}                     #创建一个dict，以index_的rowkey为key
        colu.setdefault(index_, line_dict_)
        datas.append(colu)            #封装到总list中

    return datas

# 获得hdf5文件表数据  返回phoenix所需格式： list<list>
def readH5_phoenix_datas(filePath, table_name):
    table_ = pd.read_hdf(filePath, table_name)
    datas = []
    #  封装数据
    for index_ in table_.index:
        line_ = table_.loc[index_] # 每一行
        line_list = list(line_)    # 每行转成list
        line_list = map(str, line_list)
        datas.append(line_list)    # 封装到总list中

    return datas

# 获得hdf5文件表字段
def redaH5_clumns(filePath, table_name):
    table_ = pd.read_hdf(filePath, table_name)
    clumns_list = table_.columns.values.tolist()
    clumns_str = "^".join(clumns_list)
    return clumns_str

# hdf5写文件
def write_h5(filePath, table_name, data):
    data.to_hdf(filePath, table_name)


if __name__ == "__main__":
    csv = pd.read_csv("/home/luosong/桌面/table2.csv")
    write_h5("/home/luosong/桌面/table2.h5","table2",csv)

    datas = readH5_datas("/home/luosong/桌面/table2.h5", "table2")
    print(datas)
