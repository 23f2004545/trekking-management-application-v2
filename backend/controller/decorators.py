from flask import jsonify, make_response
from flask_jwt_extended import get_jwt_identity
from controller.models import User
from functools import wraps

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
            
        if not user.role or user.role.name != 'admin':
            return make_response(jsonify({"message": "Unauthorized Access."}), 403)
            
        return f(*args, **kwargs)
    return decorated_function


def staff_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return make_response(jsonify({"message": "Account deleted."}), 403)
            
        if not user.role or user.role.name != 'trek_staff':
            return make_response(jsonify({"message": "Unauthorized Access."}), 403)
            
        return f(*args, **kwargs)
    return decorated_function


def trekker_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return make_response(jsonify({"message": "Account deleted."}), 403)
            
        if not user.role or user.role.name != 'trekker':
            return make_response(jsonify({"message": "Unauthorized Access."}), 403)
            
        return f(*args, **kwargs)
    return decorated_function