# modules/require_authentication.py
import functools
from flask import request

def require_authentication(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        cookie = request.cookies.get('user_id') #<--значение cookie не проверяется
        if cookie:
            return f(*args, **kwargs)
        else:
            return "Please authenticate"
    return decorated