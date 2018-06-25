#!/usr/bin/python
import phoenixdb
import phoenixdb.cursor
import datetime
import json


# phoenix建表
def create_phoenix_table(uuid_, clumns_str):
    database_url = 'http://localhost:8765/'
    conn = phoenixdb.connect(database_url, autocommit=True)
    cursor = conn.cursor()

    create_table_sql="CREATE TABLE \""+str(uuid_)+"\" ( "
    clumns_list = clumns_str.split("^")
    id = clumns_list[0]
    create_table_sql += "\""+id+"\" VARCHAR PRIMARY KEY, "
    del clumns_list[0]
    for clu in clumns_list:
        create_table_sql += "\""+clu+"\" VARCHAR, " # \"c\".
    create_table_sql = create_table_sql[:-2] # 去掉最后一个逗号
    create_table_sql += ")"

    cursor.execute(create_table_sql)
    conn.close()
    return create_table_sql


# phoenix插入数据
def insert_phoenix(tableName, clumns_str, datas):
    database_url = 'http://localhost:8765/'
    conn = phoenixdb.connect(database_url, autocommit=True)
    cursor = conn.cursor()

    clumns_list = clumns_str.split("^")
    insert_sql = "UPSERT INTO \""+tableName+"\" VALUES (?"
    for i in range(len(clumns_list) - 1):
        insert_sql += ", ?"
    insert_sql += ")"

    for colu in datas:
        try:
            cursor.execute(insert_sql,colu)
            raise ValueError("Something went wrong!")
        except ValueError as e:
            pass
        else:
            b.send()

    conn.close()


# phoenix记录元数据
def insert_metadata(uuid_, create_table_sql, clumns):
    database_url = 'http://localhost:8765/'
    conn = phoenixdb.connect(database_url, autocommit=True)
    cursor = conn.cursor()

    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("UPSERT INTO \"meta_table\" VALUES (?, ?, ?, ?, ?)", (str(uuid_), create_table_sql, clumns, nowTime, nowTime))
    conn.close()


# phoenix查询元数据
def query_metadata(table_name, clumn, value):
    database_url = 'http://localhost:8765/'
    conn = phoenixdb.connect(database_url, autocommit=True)
    cursor = conn.cursor()

    sql = "SELECT * FROM \""+table_name+"\" where \""+clumn+"\" = '"+value+"'"
    cursor.execute(sql)
    fetchone = cursor.fetchone()
    conn.close()

    return fetchone

# phoenix查询数据
def query_dpdata(query_sql):
    database_url = 'http://localhost:8765/'
    conn = phoenixdb.connect(database_url, autocommit=True)
    cursor = conn.cursor()

    cursor.execute(query_sql)
    fetchall = cursor.fetchall()
    conn.close()

    return fetchall


def query_test():
    database_url = 'http://localhost:8765/'
    conn = phoenixdb.connect(database_url, autocommit=True)

    cursor = conn.cursor()
    # cursor.execute("CREATE TABLE \"users\" (\"id\" INTEGER PRIMARY KEY, \"username\" VARCHAR)")
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # cursor.execute("UPSERT INTO \"meta_table\" (\"id\", \"table_describe\", \"column_describe\", \"gmt_create\", \"gmt_modified\") VALUES (NEXT VALUE FOR meta_table_sequence, '东北', '老罗', "+nowTime+", "+nowTime+");")
    # cursor.execute("UPSERT INTO \"meta_table\" VALUES (?,?,?,?,?)", ('users', 'CREATE TABLE \"users\" (\"id\" VARCHAR PRIMARY KEY, \"username\" VARCHAR, \"addr\" VARCHAR);', 'id^username^addr', nowTime, nowTime))
    # cursor.execute("UPSERT INTO \"manager\" VALUES (?, ?)",  ('2', '北上广深'))
    # cursor.execute("UPSERT INTO \"users\" VALUES (?, ?, ?)",  ('4', '东北', '老罗'))
    # cursor.execute("SELECT * FROM \"meta_table\"") #*
    sql = "UPSERT INTO \"17117368-7533-11e8-8102-30b49e461e49\" VALUES (?, ?, ?, ?, ?, ?, ?)"
    datas = [['1', 'zhangsan', 'dalian', '1', 'dalian', '1', 'dalian'], [None, None, None, None, None, '2', '沈阳'], [None, None, None, None, None, '3', '哈尔滨']]
    data = [1, 'zhangsan', 'dalian']
    for colu in datas:
        cursor.execute(sql,colu)

    print("end:::")
    return



if __name__ == '__main__':
    query_test()

    # clumns = "行 ID^订单 ID^订单日期^发货日期^邮寄方式^客户 ID^客户名称^细分^城市^省/自治区^国家^地区^产品 ID^类别^子类别^产品名称^销售额^数量^折扣^利润"
    # create_table("123123123123asdfasdf", clumns)

    # sql = "CREATE TABLE \"test\" (\"id\" VARCHAR PRIMARY KEY, \"addr\" VARCHAR);"
    # clumns = "id^addr"
    # insert_metadata("test", sql, clumns)

    # metadata = query_metadata("meta_table", "id", "test")
    # print(metadata)

    print("__name__")

