# 代码生成时间: 2025-09-16 07:46:12
import sqlite3
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """ create a table from the create_table_sql statement """
    create_table_sql = ""CREATE TABLE IF NOT EXISTS users(""id"" INTEGER PRIMARY KEY, ""username"" TEXT NOT NULL, ""email"" TEXT NOT NULL);"""
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def add_user(conn, username, email):
    """ Add a new user into the users table """
    sql = ""INSERT INTO users(username, email) VALUES(?, ?);"""
    try:
        c = conn.cursor()
        c.execute(sql, (username, email))
        conn.commit()
        return c.lastrowid
    except sqlite3.Error as e:
        print(e)
        return None

def select_all_users(conn):
    """ Query all rows in the users table """
    sql = ""SELECT * FROM users;"""
    try:
        c = conn.cursor()
        c.execute(sql)
        rows = c.fetchall()
        return rows
    except sqlite3.Error as e:
        print(e)
        return None

def main():
    database = r""database.db""
    # create a database connection
c    conn = create_connection(database)
    """ create tables """
    if conn is not None:
        create_table(conn)
        # add user
d        user_id = add_user(conn, 'example_username', 'example_email@example.com')
        print(f""User ID: {user_id}"")
        # select all users
d        all_users = select_all_users(conn)
        for row in all_users:
            print(row)
    else:
        print(""Error! cannot create the database connection."")

def __name__ == '__main__':
    main()