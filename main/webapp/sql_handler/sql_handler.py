import mysql.connector
import os

class sql_handler:
    def __init__(self):
        self.host_name = ""
        self.port_num = 0
        self.user_name = ""
        self.password = ""
        self.db_name = ""
    def check_env_setting(self):
        if os.environ.get("env_defined") == "True":
            return True
        else:
            return False

    def set_sql_param(self, param_dict):
        if "host_name" in param_dict:
            self.host_name = param_dict["host_name"]
        if "port_num" in param_dict:
            self.port_num = param_dict["port_num"]
        if "user_name" in param_dict:
            self.user_name = param_dict["user_name"]
        if "password" in param_dict:
            self.password = param_dict["password"]
        if "db_name" in param_dict:
            self.db_name = param_dict["db_name"]
    def set_host_name(self, host_name):
        self.host_name = host_name
    def set_sql_port_num(self, port_num):
        self.port_num = port_num
    def set_user_name(self, user_name):
        self.user_name = user_name
    def set_password(self, password):
        self.password = password
    def set_db_name(self, db_name):
        self.db_name = db_name
    def connect_sql(self):
        self.conn = mysql.connector.connect(
            host = self.host_name,
            port = self.port_num,
            user = self.user_name,
            password = self.password,
            database = self.db_name
        )
        self.cur = self.conn.cursor()
        return self.conn.is_connected()
    def initialize_table(self, table_name):
        self.cur.execute("DROP TABLE IF EXISTS {}".format(table_name))
    def create_table(self, table_name, columns_dict):
        query = "CREATE TABLE {} (".format(table_name)
        for key, value in columns_dict.items():
            query += "{} {},".format(key, value) 
        query = query[:-1] + ")"  ## delete last comma & add ")"
        self.cur.execute(query)
    def set_data(self, table_name, data_dict):
        query = "INSERT INTO {} (".format(table_name)
        for key in data_dict.keys():
            query += "{},".format(key)
        query = query[:-1] + ") VALUES ("
        for value in data_dict.values():
            query += "{},".format(value)
        query = query[:-1] + ")"  ## delete last comma & add ")"            
        self.cur.execute(query)
    def commit_data(self):
        self.conn.commit()
    def show_table(self, table_name):
        self.cur.execute("show columns from {}".format(table_name))
        print(self.cur.fetchall())
        self.cur.execute("SELECT * FROM {}".format(table_name))
        print(self.cur.fetchall())

        
