from functools import wraps
from flask_restful import abort
from flask import request, jsonify, make_response
from marshmallow import Schema, fields, ValidationError
from datetime import datetime, timedelta
import jwt
from app import app


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


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Check for token in the headers
        if 'Authorization' in request.headers:
            if 'Bearer' in request.headers['Authorization']:
                token = request.headers['Authorization'].split(" ")[1]
            else:
                abort(401, message='Bearer prefix is required')

        if not token:
            abort(401, message="Token is missing")

        try:
            # Decode the token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[app.config['JWT_ALGORITHM']])
        except jwt.ExpiredSignatureError:
            abort(401, message="Token has expired")
        except jwt.InvalidTokenError:
            abort(401, message="Invalid token")

        # Add the decoded token data (email in this case) to the request context
        request.user = data['email']
        return f(*args, **kwargs)

    return decorated


def generate_token(data):
    """
    Generate a JWT token
    :param data: Providing data as Email
    :return: return token
    """
    payload = {
        "email": data,
        "exp": datetime.utcnow() + timedelta(minutes=30)
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
