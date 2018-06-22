#!/usr/bin/python
import pandas as pd


def readH5(filePath, table_name):
    table_ = pd.read_hdf(filePath, table_name)
    columns = []
    #  封装数据
    for index_ in table_.index:
        line_ = table_.loc[index_]  #每一行
        line_dict_ = line_.to_dict()  #每行转化为map（dict）
        colu = {}                   #创建一个dict，以rowkey为key
        colu.setdefault(index_, line_dict_)
        columns.append(colu)        #封装到总list中

    return columns



if __name__ == "__main__":
    readH5("/home/luosong/Downlod/out.h5", "订单", "15a2d0f8-6f75-11e8-840a-30b49e461e49")
