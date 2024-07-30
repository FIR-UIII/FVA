import psycopg2 as psql
import os


DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

def check_conn():
    conn = None
    while conn is not None:
        try:
            conn = psql.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            print("Database connection successful")
        except psql.errors.Error as e:
            print(f"Failed to connect: {e}")
            break
    return conn

def initiate_database():
    '''Добавляет таблицу users sи наполняет ее пользователями'''
    check_conn()
    if DB_HOST is not None:
        sql_db = psql.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        sql_command = sql_db.cursor()
        sql_command.execute('''CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, username VARCHAR ( 50 ) NOT NULL, password VARCHAR ( 255 ) NOT NULL)''')
        sql_command.execute('''DELETE FROM users''')
        sql_command.execute('''INSERT INTO users (username, password) VALUES ('FVA', 'FVA')''')
        sql_command.execute('''INSERT INTO users (username, password) VALUES ('admin', 'admin123')''')
        sql_command.execute('''INSERT INTO users (username, password) VALUES ('user', 'qwerty')''')
        sql_db.commit()
        sql_command.close()
        sql_db.close()