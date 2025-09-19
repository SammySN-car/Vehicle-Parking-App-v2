from flask_jwt_extended import get_jwt_identity,verify_jwt_in_request
from functools import wraps
from Backend.models.database import Users

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        verify_jwt_in_request()
        claims=get_jwt_identity()
        user=Users.query.get(claims)
        if user.role!='admin':
            return {'message':'admins only'},403
        return fn(*args,**kwargs)
    return wrapper

def user_required(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        verify_jwt_in_request()
        claims=get_jwt_identity()
        user=Users.query.get(claims)
        if user.role!='user':
            return {'message':'users only'},403
        return fn(*args,**kwargs)
    return wrapper