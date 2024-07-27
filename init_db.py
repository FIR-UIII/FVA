import psycopg2 as psql
import time

DB_HOST = "db"
DB_NAME = "postgres"
DB_USER = "test"
DB_PASS = "test"

def create_conn():
    conn = None
    while not conn:
        try:
            conn = psql.connect(
                dbname="postgres",
                user="test",
                password="test",
                host="db"
            )
            print("Database connection successful")
        except Exception as e:
            print(f"Failed to connect: {e}")
            time.sleep(5)
    return conn

def initiate_database():
    create_conn()
    '''Добавляет таблицу users sи наполняет ее пользователями'''
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


initiate_database()