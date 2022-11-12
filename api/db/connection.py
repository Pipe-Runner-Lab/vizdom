import sqlite3
from sqlite3 import Error
from singleton_decorator import singleton
from constants.paths import PROD_DB_PATH


@singleton
class DBConnection:
    def __init__(self):
        # * This creates a new DB file if it doesn't exist
        try:
            self.connection = sqlite3.connect(PROD_DB_PATH)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def get_connection(self):
        return self.connection

    def close_connection(self):
        self.connection.close()

    def get_cursor(self):
        return self.connection.cursor()
