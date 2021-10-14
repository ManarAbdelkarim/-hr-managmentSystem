from flask import request , abort
from functools import wraps

def admin_required(f):
    ''' Execute the function if the user is admin else abort '''
    @wraps(f)
    def check_authorization(*args, **kwargs):
        return f(*args, **kwargs) if request.headers.get("X-ADMIN") == "1" else abort(403)
    return check_authorization


