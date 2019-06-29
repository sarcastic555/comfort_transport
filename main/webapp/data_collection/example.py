import sys
import os
import data_collector

data_collector = data_collector.data_collector()

## set parameters
sql_param_dict = {
    "host_name": os.environ['sql_host'],
    "port_num": "3306",
    "user_name": os.environ['sql_username'],
    "password": os.environ['sql_password'],
    "db_name": os.environ['sql_db_name']
}
data_collector.set_sql_param(sql_param_dict)

## connect to SQL server
if not data_collector.connect_sql():
    print ("Error. SQL connection falied.")
    sys.exit()

## create table
table_name = "table_example"
table_column_dict = {"id":"int(5)", "latitude":"float(8)", "longitude":"float(8)"}
data_collector.initialize_table(table_name)
data_collector.create_table(table_name, table_column_dict)

## insert data into table
data1 = {"id":"1", "latitude":"35.000", "longitude":"135.000"}
data_collector.set_data(table_name, data1)
data2 = {"id":"2", "latitude":"38.000", "longitude":"130.000"}
data_collector.set_data(table_name, data2)
data_collector.commit_data()

## show table
print("===== output table content ==========")
data_collector.show_table(table_name)
