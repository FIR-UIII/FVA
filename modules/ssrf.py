from flask import Blueprint, request
import requests
from modules.require_authentication import require_authentication

ssrf_bp = Blueprint("SSRF", __name__)


@ssrf_bp.route('/ssrf', methods=['GET', 'POST'])
@require_authentication
def ssrf():
    if request.method == 'GET':
        url = request.args.get('url')
    elif request.method == 'POST':
        url = request.form.get('url')

    if not url:
        return 'В запросе нет URL'

    try:
        response = requests.get(url)
        return response.text
    except:
        return 'Что-то пошло не так'
