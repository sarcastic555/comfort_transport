import sys
import os
import sql_handler

sql_handler = sql_handler.sql_handler()

## check environmental variable setting
if not sql_handler.check_env_setting():
    print("Env setting Error. Please create env.sh and source the script")
    print("See SQL connection section of AWS_connection_guide google doc")
    sys.exit()

## set parameters
sql_param_dict = {
    "host_name": os.environ['sql_host'],
    "port_num": "3306",
    "user_name": os.environ['sql_username'],
    "password": os.environ['sql_password'],
    "db_name": os.environ['sql_db_name']
}
sql_handler.set_sql_param(sql_param_dict)

## connect to SQL server
if not sql_handler.connect_sql():
    print ("Error. SQL connection falied.")
    sys.exit()

## create table
table_name = "table_example"
table_column_dict = {"id":"int(5)", "latitude":"float(8)", "longitude":"float(8)"}
sql_handler.initialize_table(table_name)
sql_handler.create_table(table_name, table_column_dict)

## insert data into table
data1 = {"id":"1", "latitude":"35.000", "longitude":"135.000"}
sql_handler.set_data(table_name, data1)
data2 = {"id":"2", "latitude":"38.000", "longitude":"130.000"}
sql_handler.set_data(table_name, data2)
sql_handler.commit_data()

## show table
print("===== output table content ==========")
sql_handler.show_table(table_name)
