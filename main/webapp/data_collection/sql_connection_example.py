import os
import mysql.connector

conn = mysql.connector.connect(
    host = os.environ['sql_host'],
    port = 3306,
    user = os.environ['sql_username'],
    password = os.environ['sql_password'],
    database = os.environ['sql_db_name'],
)
print(conn.is_connected())

cur = conn.cursor()
table_name='table_example'
cur.execute("DROP TABLE IF EXISTS {}".format(table_name))
cur.execute("CREATE TABLE {} ("
             "id int(5),"
             "latitude float(8),"
             "longitude float(8)"
             ")".format(table_name))
add_busstopdata =("INSERT INTO {} "
               "(id, latitude, longitude) "
                  "VALUES (%s, %s, %s)"
               ).format(table_name)

busstopdata1 = (1, 38.000, 138.000)
cur.execute(add_busstopdata, busstopdata1)
busstopdata2 = (2, 39.000, 136.000)
cur.execute(add_busstopdata, busstopdata2)
conn.commit()

cur.execute("SELECT * FROM {}".format(table_name))
for (id, latitude, longitude) in cur:
    print("id:{}, latitude:{}, longitude:{}".format(id, latitude, longitude))

#cur = conn.cursor(dictionary=True)
#print(cur.fetchall())

