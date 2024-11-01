from flask import Blueprint, render_template, request
from modules.require_authentication import require_authentication


xss_bp = Blueprint("XSS", __name__)


@xss_bp.route('/xss', methods=['GET'])
@require_authentication
def xss():
    return render_template('xss.html')

@xss_bp.route('/xss/reflected', methods=['POST', 'GET'])
@require_authentication
def xss_reflected():
    if request.method == 'GET':
        user_input = request.args.get('param') #<-- точка ввода через query параметры xss reflected + SSTI    
        return render_template('/xss_labs/xss_reflected.html', user_input=user_input) #<-- небезопасный вывод пользователю данных без санитизации
    if request.method == 'POST':
        data = request.form['user_input'] #<-- точка пользовательского ввода без валидации xss stored
        return render_template('/xss_labs/xss_reflected.html', user_input=data)
    else:
        return render_template('/xss_labs/xss_reflected.html')

@xss_bp.route('/xss/dom1', methods=['GET', 'POST'])
@require_authentication
def xss_dom():
    return render_template("/xss_labs/dom1.html",)

@xss_bp.route('/xss/dom2', methods=['GET', 'POST'])
@require_authentication
def xss_dom2():
    return render_template("/xss_labs/dom2.html",)

@xss_bp.route('/xss/dom3', methods=['GET', 'POST'])
# @require_authentication
def xss_dom3():
    return render_template("/xss_labs/dom3.html",)