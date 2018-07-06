import pymysql


from ebidp.sql_config import query_mysql_columns_sql


# 查询mysql表字段
def query_table_columns(host, port, user, password, db_name, table_name):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=password,
                           db=db_name, charset='utf8')

    with conn.cursor() as cursor:
        query_sql = query_mysql_columns_sql % (db_name, table_name)
        cursor.execute(query_sql)
        fetchall = cursor.fetchall()
        data_all = []
        for data in fetchall:
            data_all.append(data[0])
    conn.close()
    column_str = "^".join(data_all)

    return column_str
