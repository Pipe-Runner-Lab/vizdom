import sqlite3
from sqlite3 import Error
from singleton_decorator import singleton
from constants.paths import (PROD_DB_PATH, DEV_DB_PATH)


@singleton
class DBConnection:
    def __init__(self):
        # * This creates a new DB file if it doesn't exist
        try:
            # TODO: Check prod/dev env
            self.connection = sqlite3.connect(DEV_DB_PATH)
            self.connection.execute("CREATE TABLE covid (iso_code TEXT, date TEXT, new_cases REAL)")
        except Error as e:
            print(e)

    def populate_with_data_frame(self, table_name, df):
        df.to_sql(table_name, self.connection, if_exists='append', index = False)

    def get_connection(self):
        return self.connection

    def close_connection(self):
        self.connection.close()

    def get_cursor(self):
        return self.connection.cursor()
