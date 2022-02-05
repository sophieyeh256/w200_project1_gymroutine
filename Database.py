"""
Creates a single database containing all the users in the program.
https://www.sqlitetutorial.net/sqlite-python/update/
Still need to test update_plan
"""
import sqlite3
from sqlite3 import Error
import os

from Library import Library

class Database:
    def __init__(self):
        self.library = Library()

        self.database = r"C:\sqlite\db\pythonsqlite.db"

        sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                            id integer PRIMARY KEY,
                                            numDays integer NOT NULL
                                        ); """

        sql_create_plans_table = """CREATE TABLE IF NOT EXISTS plans (
                                        id integer PRIMARY KEY,
                                        user_id integer NOT NULL,
                                        date text NOT NULL,
                                        task text NOT NULL,
                                        FOREIGN KEY (user_id) REFERENCES users (id)
                                    );"""

        # create a database connection
        self.conn = self.create_connection()

        # create tables
        if self.conn is not None:

            # create users table
            self.create_table(sql_create_users_table)

            # create plans table
            self.create_table(sql_create_plans_table)

        else:
            print("Error! cannot create the database connection.")

    def create_connection(self):
        """ create a database connection to a SQLite database """
        self.conn = None
        try:
            self.conn = sqlite3.connect(self.database)
            return self.conn
        except Error as e:
            print(e)

        return self.conn

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def get_users(self):
        sql = """ SELECT id
                  FROM users
              """
        cur = self.conn.cursor()
        cur.execute(sql)
        ans = cur.fetchall()
        ans = [str(item[0]) for item in  ans]
        return ans
        #return id #['1', '6', '8) ...]


if __name__ == '__main__':
    db = Database()
