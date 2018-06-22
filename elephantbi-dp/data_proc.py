#!/usr/bin/python
import uuid
import phoenixdb.cursor

from phoenixdb_util import query_metadata, create_phoenix_table, insert_metadata


def data_join_clu(table0, table1, join_clumn0, join_clumn1, join_type, uuid_):

    tmp_uuid = ""
    if uuid_ == None:
        tmp_uuid = uuid.uuid1()
    else:
        tmp_uuid = uuid_
    database_url = 'http://localhost:8765/'
    conn = phoenixdb.connect(database_url, autocommit=True)

    # 封装join后表结构并建表
    table0_metadata = query_metadata("meta_table", "id", table0)
    table0_clumns = table0_metadata[2]
    table1_metadata = query_metadata("meta_table", "id", table1)
    table1_clumns = table1_metadata[2]
    clumns_str = table0_clumns+"^"+table1_clumns
    # 处理重名字段
    same_name = "" # 是否重名标识 0不重 1重名
    clumns_list = clumns_str.split("^")
    for clu in set(clumns_list):
        count = clumns_list.count(clu)
        if count >= 2:
            same_name = "1"
            index = clumns_list.index(clu)
            first_pos = 0
            for i in range(count):
                new_list = clumns_list[first_pos:]
                next_pos = new_list.index(clu) + 1
                clumns_list[first_pos + new_list.index(clu)] = clu + "_" + str(i)
                first_pos += next_pos
        else:
            same_name = "0"
    clumns_str = "^".join(clumns_list)
    clumns_str_meta = "ROW^"+clumns_str

    create_table_sql = create_phoenix_table(str(tmp_uuid), clumns_str_meta)
    insert_metadata(str(tmp_uuid), create_table_sql, clumns_str)

    # 查询join数据并插入
    cursor = conn.cursor()
    join_str = ""
    if join_type == "left":
        join_str = "left join"
    elif join_type == "right":
        join_str = "right join"
    elif join_type == "inner":
        join_str = "inner join"
    elif join_type == "full":
        join_str = "full join"
    query_sql = "select * from \""+table0+"\" o "+join_str+" \""+table1+"\" t on o.\""+join_clumn0+"\" = t.\""+join_clumn1+"\""
    cursor.execute(query_sql)
    fetchall = cursor.fetchall()

    # 插入
    sql = "UPSERT INTO \"" + str(tmp_uuid) + "\" VALUES (?"
    # for clu in fetchone:
    size = len(clumns_str_meta.split("^"))
    for i in range(size - 1):
        sql += ", ?"
    sql += ")"
    for fetchone in fetchall:
        fetchone.insert(0, str(uuid.uuid1()))
        cursor.execute(sql, fetchone)

    return str(tmp_uuid)+"^"+same_name


def data_join_row():
    return


if __name__ == "__main__":

    #left right inner full
    # uuid_ = uuid.uuid1()
    # left_uuid = data_join_clu("users", "manager", "addr", "dizhi", "full", uuid_)
    # print(uuid_)

    name  = ['hello', 'world', 'a', 'b', 'c', 1, 2, 3, 'qqq', 'www', 'eee', 'rrrr', 'ttt', 4, 2, 5]
    # first_pos = 0
    # for i in range(name.count(2)):
    #     new_list = name[first_pos:] #从first_pos角标开始向后截取
    #     next_pos = new_list.index(2) + 1
    #     print(first_pos + new_list.index(2))
    #     first_pos += next_pos