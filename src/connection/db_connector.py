import sqlite3
from sqlite3 import Error
from singleton_decorator import singleton
import pandas as pd
from constants.paths import (PROD_DB_PATH, DEV_DB_PATH)
from crawlers.url_crawlers import get_our_world_in_data_attributes

@singleton
class DBConnection:
    def __init__(self):
        # * This creates a new DB file if it doesn't exist
        try:
            # TODO: Check prod/dev env
            # TODO: Need to check thread safety (Add serialized mode?)
            self.connection = sqlite3.connect(DEV_DB_PATH, check_same_thread=False)

            # table meta data
            column_meta_data = ""
            for key, value in get_our_world_in_data_attributes.items():
                column_meta_data += f"{key} {value}, "

            # * Create tables
            column_meta_data = column_meta_data.rstrip(', ')
            self.connection.execute(f'''
                CREATE TABLE IF NOT EXISTS covid (
                    {column_meta_data}
                )
            ''')
        except Error as e:
            print(e)

    def get_connection(self):
        return self.connection

    def close_connection(self):
        self.connection.close()

    def get_cursor(self):
        return self.connection.cursor()

    def populate_with_data_frame(self, table_name, df):
        df.to_sql(table_name, self.connection, if_exists='append', index = False)

    """
    The columns is a string of comma and space separated column names,
    e.g. "iso_code, date, new_cases"
    """
    def get_df(self, columns, table_name, where_clause=None):
        if where_clause:
            sql_query = pd.read_sql_query (f"SELECT {columns} FROM {table_name} WHERE {where_clause}", self.connection)
        else:
            sql_query = pd.read_sql_query (f"SELECT {columns} from {table_name}", self.connection)

        df = pd.DataFrame(sql_query, columns = columns.split(', '))
        return df