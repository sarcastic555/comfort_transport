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

## table name definition
table_name = "table_example"

## show table
print("===== output table content ==========")
sql_handler.show_table(table_name)

## read each data column by column
print("===== read table content ==========")
column_list=sql_handler.get_column_list(table_name)
for (id, latitude, longitude) in column_list:
    print("id:{}, latitude:{}, longitude:{}".format(id, latitude, longitude))
