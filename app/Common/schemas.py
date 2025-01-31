from functools import wraps
from flask import request, jsonify, make_response
from marshmallow import Schema, fields, ValidationError
from datetime import datetime, timedelta
import jwt




class UserSignupSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


def validate_api_schema(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                return {'error': 'Request must be JSON'}, 400
            data = request.get_json()
            try:
                validated_data = schema().load(data)
            except ValidationError as err:
                return {'error': 'Invalid request', 'details': err.messages}, 400
            kwargs['validated_data'] = validated_data
            return func(*args, **kwargs)
        return wrapper
    return decorator


def generate_token(data):
    """
    Generate a JWT token
    :param data: Providing data as Email
    :return: return token
    """
    payload = {
        "email": data,
        "exp": datetime.utcnow() + timedelta(minutes=3)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm=app.config['JWT_ALGORITHM'])
    return token



def checking_password(password):
    if len(password) < 8:
        abort(400, message="Password must be at least 8 characters long")
    elif not any(char.isdigit() for char in password):
        abort(400, message="Password must contain at least one number")
    elif not any(char.isupper() for char in password):
        abort(400, message="Password must contain at least one uppercase letter")
    elif not any(char.islower() for char in password):
        abort(400, message="Password must contain at least one lowercase letter")
    elif not any(char in '!@#$%^&*()_+-=' for char in password):
        abort(400, message="Password must contain at least one special character")

