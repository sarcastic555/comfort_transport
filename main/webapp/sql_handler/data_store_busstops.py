
import sys
import os
import sql_handler
import pandas as pd

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

## read the bus_stop data
directory_name = ""
df = pd.read_csv(directory_name + "stops.txt")
df_stops = df[df["location_type"] == 1][["stop_id", "stop_name", "stop_lat", "stop_lon"]]

## create table
table_name = "table_example"
table_column_dict = {"id":"int(8)", "name":"char(50)", "latitude":"float(10)", "longitude":"float(10)"}
sql_handler.initialize_table(table_name)
sql_handler.create_table(table_name, table_column_dict)

## insert data into table
for n_busstops in range(len(df_stops)):
    dict_busstop = df_stops.iloc[n].to_dict()
    sql_handler.set_data(table_name, dict_busstop)

sql_handler.commit_data()

## show table
print("===== output table content ==========")
sql_handler.show_table(table_name)
