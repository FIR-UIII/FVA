from flask import render_template, Blueprint, request, jsonify
from modules.require_authentication import require_authentication

csrf_bp = Blueprint('csrf_bp', __name__)

passwords = [
    {
        "id": 1,
        "username": "admin",
        "password": "admin123",
    },
    {
        "id": 2,
        "username": "user",
        "password": "qwerty",
    },
]

def password_changer(id, new_password):
    '''Function that changes the password for a user based on the provided ID'''
    if id == 1:  # Assuming the admin password is the first one in the list
        passwords[0]['password'] = new_password
        return f"Password for user '{passwords[id-1]['username']}' has been successfully changed to '{new_password}'. + {passwords}"
    elif id == 2:  # Assuming the user password is the second one in the list
        passwords[1]['password'] = new_password
        return f"Password for user '{passwords[id-1]['username']}' has been successfully changed to '{new_password}'. + {passwords}"
    return jsonify({"error": "Invalid user ID."})

@csrf_bp.route('/csrf')
@require_authentication
def csrf():
    return render_template('csrf.html')


@csrf_bp.route('/change_password', methods=['POST', 'GET']) #<-- critical actions mist be exucuted via POST request
# TODO: добавить защиту https://testdriven.io/blog/csrf-flask/
# TODO: ошибки при загрузке статики /static/scripting.png и /static/bootstrap.min.css
@require_authentication
def change_password():
    if request.method == 'POST':
        id = int(request.form.get('id'))
        new_password = str(request.form.get('new_password')) #<-- no info from fronend that this is user actions
        print(passwords)
        return password_changer(id, new_password)
    
    if request.method == 'GET': #<-- critical actions mist be exucuted via POST request
        id = int(request.args.get('id'))
        new_password = str(request.args.get('new_password')) #<-- no info from fronend that this is user actions
        return password_changer(id, new_password)
