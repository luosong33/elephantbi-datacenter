join_query_sql = "SELECT * FROM \"%s\" o %s \"%s\" t ON o.\"%s\" = t.\"%s\""
insert_meta_sql = "UPSERT INTO \"meta_table\" VALUES (?, ?, ?, ?, ?, ?, ?)"
query_meta_sql = "SELECT * FROM \"meta_table\" WHERE \"id\" = '%s'"
