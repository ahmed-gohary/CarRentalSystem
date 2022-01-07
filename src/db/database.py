import os
import threading

import mysql.connector as ms_connector

lock = threading.Lock()


def locked(func):
    def wrapper(*args, **kwargs):
        try:
            lock.acquire(True)
            return func(*args, **kwargs)
        finally:
            lock.release()

    return wrapper


class DBConfig:

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password


class Database:
    __instance = None
    __DATABASE_NAME = "BookingDB"
    __DEFAULT_DB_CONFIG = DBConfig(
        host="localhost",
        user="gohary",
        password="12345678"
    )

    @staticmethod
    def get_instance():
        if Database.__instance is None:
            Database(Database.__DEFAULT_DB_CONFIG)
        return Database.__instance

    def __init__(self, db_config: DBConfig):
        if Database.__instance is not None:
            raise Exception("ONLY 1 INSTANCE CAN BE CREATED FROM [Database]")
        else:
            self.conn = self.__initialize_db(
                db_config=db_config
            )
            Database.__instance = self

    def __initialize_db(
        self,
        db_config: DBConfig
    ):
        print("Reading init script")
        init_script_content = self.__load_init_script()
        stored_procs_script_content = self.__load_stored_proc_script()
        print("Init script ready")

        print()
        print("Connecting to {}".format(Database.__DATABASE_NAME))
        conn = ms_connector.connect(
            host=db_config.host,
            user=db_config.user,
            password=db_config.password
        )
        print("Connected to {}".format(Database.__DATABASE_NAME))

        print()
        print("Loading init script...")
        conn_cursor = conn.cursor()
        conn_cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(Database.__DATABASE_NAME))
        conn_cursor.execute("USE {}".format(Database.__DATABASE_NAME))
        conn_cursor.execute(init_script_content)
        conn_cursor.close()
        conn.close()
        print("Tables Loaded")

        conn.reconnect()
        conn_cursor = conn.cursor()
        conn_cursor.execute("USE {}".format(Database.__DATABASE_NAME))
        conn_cursor.execute(stored_procs_script_content)
        print("Stored Procedures Loaded")

        return conn

    @staticmethod
    def __load_init_script():
        current_file_dir: str = os.path.dirname(__file__)
        with open(current_file_dir + "/scripts/booking_db.sql", 'r', encoding="utf-8") as init_file:
            return init_file.read()

    @staticmethod
    def __load_stored_proc_script():
        current_file_dir: str = os.path.dirname(__file__)
        with open(current_file_dir + "/scripts/procedures.sql", 'r', encoding="utf-8") as init_file:
            return init_file.read()

    def show_all_databases(self):
        conn_cursor = self.get_conn_cursor()
        conn_cursor.execute("""
                SHOW DATABASES;
            """)
        for database in conn_cursor:
            print(database)
        conn_cursor.close()

    def show_all_tables(self):
        conn_cursor = self.get_conn_cursor()
        conn_cursor.execute("""
            USE {};
            SHOW TABLES;
        """.format(Database.__DATABASE_NAME))
        for table in conn_cursor:
            print(table)
        conn_cursor.close()

    def drop_table(self, table_name: str):
        conn_cursor = self.get_conn_cursor()
        conn_cursor.execute("""
            USE {};
            DROP TABLE {};
        """.format(
            Database.__DATABASE_NAME,
            table_name
        ))
        conn_cursor.close()

    def does_table_exist(self, table_name: str):
        conn_cursor = self.get_conn_cursor()
        conn_cursor.execute("""
            SELECT TABLE_NAME FROM information_schema.tables WHERE table_name='{}';
        """.format(
            table_name
        ))
        data = conn_cursor.fetchone()
        conn_cursor.close()
        if data is not None and data[0] == table_name:
            return True
        return False

    def get_conn_cursor(self):
        try:
            self.conn.reconnect()
            cursor = self.conn.cursor()
            cursor.execute("USE {};".format(Database.__DATABASE_NAME))
            return cursor
        except Exception as e:
            print("Failed to connect to MySQL Server: " + str(e))
            return None

    def close_connection(self):
        print("Closing Connection")
        self.conn.close()

