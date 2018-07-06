join_query_sql = "SELECT * FROM \"%s\" o %s \"%s\" t ON o.\"%s\" = t.\"%s\""
insert_meta_sql = "UPSERT INTO \"meta_table\" VALUES (?, ?, ?, ?, ?, ?, ?)"
query_meta_sql = "SELECT * FROM \"meta_table\" WHERE \"id\" = '%s'"
insert_sqoop_meta_sql = "UPSERT INTO \"meta_sqoop\" VALUES (?, ?, ?)"
query_sqoop_meta_sql = "SELECT * FROM \"meta_sqoop\" WHERE \"id\" = '%s'"
query_mysql_columns_sql = "select column_name from information_schema.columns "\
                          "where table_schema='%s' and table_name='%s'"
