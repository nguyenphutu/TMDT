from functools import wraps
from flask_login import current_user
from flask import abort

def admin_required(func):
    @wraps(func)
    def decorate_funcs(*args, **kwargs):
        if current_user.role != '2':
            abort(404)
        return func(*args, **kwargs)
    return decorate_funcs

def manage_required(func):
    @wraps(func)
    def decorate_funcs(*args, **kwargs):
        if current_user.role not in ['1', '2']:
            abort(404)
        return func(*args, **kwargs)
    return decorate_funcs