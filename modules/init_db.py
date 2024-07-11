import psycopg2 as psql

DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = ""
DB_PASS = ""

def create_database():
    '''Добавляет таблицу users sи наполняет ее пользователями'''
    sql_db = psql.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    sql_command = sql_db.cursor()
    sql_command.execute('''CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, username VARCHAR ( 50 ) NOT NULL, password VARCHAR ( 255 ) NOT NULL)''')
    sql_command.execute('''INSERT INTO users (username, password) VALUES ('FVA', 'FVA')''')
    sql_command.execute('''INSERT INTO users (username, password) VALUES ('admin', 'admin123')''')
    sql_command.execute('''INSERT INTO users (username, password) VALUES ('user', 'qwerty')''')
    sql_db.commit()
    sql_command.close()
    sql_db.close()


def delete_all_table():
    '''Удаляет всех пользователей из users'''
    sql_db = psql.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    sql_command = sql_db.cursor()
    sql_command.execute("DELETE FROM users")
    sql_db.commit()
    sql_command.close()
    sql_db.close()


create_database()