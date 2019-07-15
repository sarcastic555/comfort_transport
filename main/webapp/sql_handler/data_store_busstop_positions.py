import sys
import os
import requests
import sql_handler
import numpy as np

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
table_column_dict = {"id":"char(43)", "latitude":"float(15)", "longitude":"float(15)"}
sql_handler.initialize_table(table_name)
sql_handler.create_table(table_name, table_column_dict)

## requestsでデータを取ってきて、jsonに保存
## jsonデータからidと緯度経度を抜き出してSQLに入れる
HTTPS = "https://api-tokyochallenge.odpt.org/api/v4/odpt:BusstopPole?odpt:operator=odpt.Operator:"
KEY = "&acl:consumerKey=2deef49e96744c2566cca5bb289318cd28490a662d82b8e62a071d32afe3fc3c"
requests_result = requests.get(HTTPS + "SeibuBus" + KEY)
BusStops = requests_result.json()

f = lambda x: True if x is None else False
for busstop in BusStops:
    ## 西武バスの場合重要そうなのは下７桁だけ
#    data_tmp = {"id":busstop["@id"].encode()[-7:], "latitude":busstop["geo:lat"], "longitude":busstop["geo:long"]}
    latitude  = busstop["geo:lat"]
    longitude = busstop["geo:long"]
    if( f(latitude) ):
        latitude = 999
    if( f(longitude) ):
        longitude = 999
    data_tmp = {"latitude":latitude, "longitude":longitude}
    sql_handler.set_data(table_name, data_tmp)
sql_handler.commit_data()

## show table
print("===== output table content ==========")
sql_handler.show_table(table_name)
