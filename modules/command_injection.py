from flask import Blueprint, request, render_template
from os import system as system
import subprocess
from modules.require_authentication import require_authentication


command_injection_bp = Blueprint("command_injection", __name__)
@require_authentication
@command_injection_bp.route('/execute', methods=['GET', 'POST'])
def execute():
    cookie = request.cookies.get('user_id')
    print(cookie)
    if request.method == 'POST':
        command = request.form.get('command')
        try:
            if cookie == 'YWRtaW4=': # => уязвимость в использовании статичных секретов в коде
                result = subprocess.check_output(command, shell=True, text=True)
                # проверяем что результат не является пустым значением
                if result:
                    return render_template('command_injection.html', result=result)
                else:
                    return render_template('command_injection.html', error="Нет результата, проверьте правильность команды")
            else:
                return render_template('command_injection.html', error="У Вас нет прав на выполнение этой операции")
        # обработка ошибок
        except subprocess.SubprocessError:
            return render_template('command_injection.html', error="Данная команда не найдена")

    else:
        return render_template('command_injection.html')