#!/usr/bin/python
import phoenixdb
import phoenixdb.cursor
import datetime


# phoenix建表
def create_phoenix_table(uuid_, clumns_str):
    database_url = 'http://localhost:8765/'
    conn = phoenixdb.connect(database_url, autocommit=True)
    cursor = conn.cursor()

    create_table_sql='{0}{1}{2}'.format("CREATE TABLE \"", str(uuid_), "\" ( ")
    clumns_list = clumns_str.split("^")
    id = clumns_list[0]
    create_table_sql = '{0}{1}{2}{3}'.format(create_table_sql, "\"", id, "\" VARCHAR PRIMARY KEY, ")
    del clumns_list[0]
    for clu in clumns_list:
        create_table_sql = '{0}{1}{2}{3}'.format(create_table_sql, "\"", clu, "\" VARCHAR, ")
    create_table_sql = create_table_sql[:-2] # 去掉最后一个逗号
    create_table_sql = '{0}{1}'.format(create_table_sql, ")")

    cursor.execute(create_table_sql)
    conn.close()
    return create_table_sql


# phoenix插入数据
def insert_phoenix(tableName, clumns_str, datas):
    database_url = 'http://localhost:8765/'
    conn = phoenixdb.connect(database_url, autocommit=True)
    cursor = conn.cursor()

    clumns_list = clumns_str.split("^")
    insert_sql = '{0}{1}{2}'.format("UPSERT INTO \"", tableName, "\" VALUES (?")
    for i in range(len(clumns_list) - 1):
        insert_sql = '{0}{1}'.format(insert_sql, ", ?")
    insert_sql += ")"
    insert_sql = '{0}{1}'.format(insert_sql, ")")

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

    sql = '{0}{1}{2}{3}{4}{5}{6}'.format("SELECT * FROM \"", table_name, "\" where \"", clumn, "\" = '", value, "'")
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
