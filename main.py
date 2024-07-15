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

###### CSP headers #######
@FVA.after_request
def add_security_headers(resp):
    resp.headers['Content-Security-Policy'] = "default-src 'self';" \
                                               "style-src 'self';"
    return resp

###### CORS headers #######

cors = CORS(FVA, resources={
    r"/*": {
        "origins": "http://localhost:8000", # разрешает доступ для нашего сайта 
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
    '''
    The root route of the application.
    Parameters:
    If a user is already logged in, they are redirected to the dashboard.
    If the credentials are valid, a cookie is added to the response and the user is redirected to the dashboard.
    If the credentials are invalid, an error message is returned.
    '''
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
    '''
    Function used to render the 'home.html' template after successful authentication.
    '''
    return render_template('home.html')


@FVA.route('/logout')
def logout():
    """
    Function used to remove the user session cookie and redirect the user to the home page.
    Returns:
    - Response: A response object that redirects the user to the home page and removes the 'user_id' cookie.
    """
    resp = make_response(redirect("/"))
    resp.delete_cookie('user_id')
    return resp

@FVA.route('/api/data', methods=['POST'])
def handle_data():
    '''
    Function used to upload files to the static directory.
    Parameters:
    - file (FileStorage): The file to be uploaded.
    Returns:
    - Response: Redirects to the '/upload' route if the file is successfully uploaded.
    - json: Returns a JSON object with an 'error' key and the value 'Invalid file' if the file is invalid.
    '''
    file = request.files['file']
    if file:
        filename = file.filename
        file.save(os.path.join(FVA.static_folder, filename))
        return redirect("/upload")
    else:
        return jsonify({'error': 'Invalid file'})
    
@FVA.route('/api/users', methods=['GET'])
def get_users():
    '''handles a GET request to the '/api/users' endpoint. exposes sensitive information
    without authorization'''
    return 'user password is qwerty'


if __name__ == "__main__":
    # Debug mode True, no TLS => Security misconfiguration
    FVA.run(host="localhost", port=8888, debug=True)
