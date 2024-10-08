from flask import Blueprint, render_template, request
import psycopg2 as psql
import os
from flask import jsonify
bola_bp = Blueprint("bola", __name__)


DB_HOST = os.getenv("DB_HOST") # db - docker; localhost - manual init
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


# TODO: убрать функцию в модель инициирования всей БД initDB
def initiate_database4BOLA():
            '''Добавляет таблицу users sи наполняет ее пользователями'''
            sql_db = psql.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
            sql_command = sql_db.cursor()
            sql_command.execute('''CREATE TABLE IF NOT EXISTS bola1 (id serial PRIMARY KEY, username VARCHAR ( 50 ) NOT NULL, password VARCHAR ( 255 ) NOT NULL)''')
            sql_command.execute('''DELETE FROM bola1''')
            sql_command.execute('''INSERT INTO bola1 (username, password) VALUES ('client-1', 'man')''')
            sql_command.execute('''INSERT INTO bola1 (username, password) VALUES ('admin', 'Just_admin')''')
            sql_command.execute('''INSERT INTO bola1 (username, password) VALUES ('user', 'how?')''')

            sql_command.execute('''CREATE TABLE IF NOT EXISTS bola2 (id serial PRIMARY KEY, username VARCHAR ( 50 ) NOT NULL, password VARCHAR ( 255 ) NOT NULL)''')
            sql_command.execute('''DELETE FROM bola2''')
            sql_command.execute('''INSERT INTO bola2 (username, password) VALUES ('VIPVIPVIP', 'President')''')
            sql_command.execute('''INSERT INTO bola2 (username, password) VALUES ('MAster', '******')''')
            sql_command.execute('''INSERT INTO bola2 (username, password) VALUES ('boss', 'BOSS')''')
            sql_db.commit()
            sql_command.close()
            sql_db.close()
   
def database_worker(callDBName):
    '''Добавляет таблицу users и наполняет ее пользователями'''
    sql_db = psql.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    sql_command = sql_db.cursor()
    sql_command.execute("SELECT * FROM " + str(callDBName))
    sql_db.commit()
    Result = sql_command.fetchall()   
    sql_command.close()
    sql_db.close()
    return(Result)


@bola_bp.route('/idor/bola', methods=['GET', 'POST'])
def render_page():
    initiate_database4BOLA()
    if request.method == 'POST':
        # Expecting JSON data with a 'param' field
        data = request.get_json()
        parameter_received = data.get('param', None)
        resultParam = str(database_worker(parameter_received[0]))
        if parameter_received[0] == "bola2":
            successMassage = "congratulations! U find 2 vulnerabilities. IDOR: bola1/bola2 - names if DB. You have to change this variable for new GUID. BOLA: user 1 cannt see bola2. This show incorrect authorization" 
            resultParam = (str(database_worker((parameter_received[0]))) + successMassage)
        else:
            resultParam = str(database_worker(parameter_received[0]))
        # Process the received parameter as needed
        # For demonstration, logging it and returning a success message
        return jsonify({'status': 'success', 'message': resultParam})
    
    # For GET requests or if the POST request doesn't contain expected data
    return render_template('bola.html')






