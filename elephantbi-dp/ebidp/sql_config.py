join_query_sql = "select * from \"%s\" o %s \"%s\" t on o.\"%s\" = t.\"%s\""
insert_meta_sql = "UPSERT INTO \"meta_table\" VALUES (?, ?, ?, ?, ?, ?, ?)"
query_meta_sql = "select * from \"meta_table\" where \"id\" = '%s'"
