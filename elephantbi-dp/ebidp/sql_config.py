join_query_sql = "select * from \"%s\" o %s \"%s\" t on o.\"%s\" = t.\"%s\""
join_query_prefix = "select \"%s\", "
join_query_suffix = " %s from \"%s\" o %s \"%s\" t on o.\"%s\" = t.\"%s\""
insert_meta_sql = "UPSERT INTO \"meta_table\" VALUES (?, ?, ?, ?, ?, ?, ?)"
query_meta_sql = "select * from \"meta_table\" where \"id\" = '%s'"
create_phoenix_prefix = 'CREATE TABLE "%s" ( '
create_phoenix_key = '%s"%s" VARCHAR PRIMARY KEY, '
create_phoenix_column = '%s"%s" VARCHAR, '
create_phoenix_suffix = '%s)'
insert_phoenix_prefix = 'UPSERT INTO "%s" VALUES (?'
insert_phoenix_column = '%s, ?'
insert_phoenix_suffix = '%s)'
data_phoenix_prefix = 'UPSERT INTO "%s" VALUES (?'
data_phoenix_column = '%s, ?'
data_phoenix_suffix = '%s)'
