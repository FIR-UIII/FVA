from flask import Blueprint, request, render_template_string
from modules.require_authentication import require_authentication

ssti_bp = Blueprint("SSTI", __name__)


@ssti_bp.route('/ssti', methods=['GET'])
@require_authentication
def ssti():
    print(request.args.get)
    user_input = request.args.get('param', 'Введите данные в query "?param="') #<-- точка ввода через query параметры xss reflected + SSTI
    template = '''<!DOCTYPE html>
<html>
<head>
    <title>SSTI</title>
    <link rel="stylesheet" href="static/bootstrap.min.css">
    <link rel="icon" href="static/scripting.png" type="image/x-icon">
</head>
<body>
    <div class="container mt-5">
            <pre class="alert alert-info"><b>Пользовательский ввод: </b>'''+user_input+'''</pre>
        <a href="/dashboard" class="btn btn-secondary">Назад</a></p>
    </div>
</body>
</html>'''

    return render_template_string(template) #<-- небезопасный вывод пользователю данных без санитизации