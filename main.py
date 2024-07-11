from flask import Flask, render_template, jsonify, request, redirect, session, make_response
import os
from modules.xss import xss_bp
from modules.path_travers import path_travers_bp
from modules.ssti import ssti_bp
from modules.upload import upload_bp
from modules.command_injection import command_injection_bp
from modules.csrf import csrf_bp
from modules.ssrf import ssrf_bp
import psycopg2 as psql
import base64
from modules.require_authentication import require_authentication
from flask_cors import CORS


DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = ""
DB_PASS = ""


FVA = Flask(__name__)
FVA.secret_key = 'some_secret_key'
app = Flask(__name__)
cors = CORS(FVA, resources={
    r"/*": {
        "origins": "http://localhost:80", # разрешает доступ для нашего сайта 
        "methods": ["GET", "POST"],
        "headers": ["Content-Type", "Authorization"],
        "credentials": False
    }
})



FVA.register_blueprint(xss_bp)
FVA.register_blueprint(path_travers_bp)
FVA.register_blueprint(ssti_bp)
FVA.register_blueprint(upload_bp)
FVA.register_blueprint(command_injection_bp)
FVA.register_blueprint(csrf_bp)
FVA.register_blueprint(ssrf_bp)

@FVA.route('/', methods=['GET', 'POST'])
def index():
    if request.cookies.get('user_id'):
        return redirect("/dashboard")
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Connect to the PostgreSQL database
        conn = psql.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cursor = conn.cursor()

        # Raw SQL query to check the credentials
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        result = cursor.fetchone()
        print(result)

        if result:
            # Add a cookie after successful authentication cookie == username
            resp = make_response(redirect("/dashboard"))
            # Кодируем куку в base64 и добавляем в сессию пользователя после аутентификации
            encoded_user_id = base64.b64encode(str(result[1]).encode()).decode()
            resp.set_cookie('user_id', encoded_user_id)
            return resp
        else:
            conn.close()
            return "Invalid username or password"

    return render_template('login.html')


@FVA.route('/dashboard')
@require_authentication
def dashboard():
    return render_template('home.html')


@FVA.route('/logout')
def logout():
    # Удаляем куку из сессии и перенаправляем на главную страницу
    resp = make_response(redirect("/"))
    resp.delete_cookie('user_id')
    return resp

@FVA.route('/api/data', methods=['POST'])
def handle_data():
    '''Функция используется для загрузки файлов в директорию /static'''
    file = request.files['file']
    if file:
        filename = file.filename
        file.save(os.path.join(FVA.static_folder, filename))
        return redirect("/upload")
    else:
        return jsonify({'error': 'Invalid file'})
    
@FVA.route('/api/users', methods=['GET'])
def get_users():
    return 'user password is qwerty'


if __name__ == "__main__":
    # Debug mode True, no TLS => Security misconfiguration
    FVA.run(host="localhost", port=8888, debug=True)