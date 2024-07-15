from flask import Blueprint, render_template, request
from modules.require_authentication import require_authentication


xss_bp = Blueprint("XSS", __name__)

@xss_bp.route('/xss', methods=['POST', 'GET'])
@require_authentication
def xss():
    if request.method == 'GET':
        user_input = request.args.get('param') #<-- точка ввода через query параметры xss reflected + SSTI    
        return render_template('xss.html', user_input=user_input) #<-- небезопасный вывод пользователю данных без санитизации
    if request.method == 'POST':
        data = request.form['user_input'] #<-- точка пользовательского ввода без валидации xss stored
        return render_template('xss.html', user_input=data)
    else:
        return render_template('xss.html')

