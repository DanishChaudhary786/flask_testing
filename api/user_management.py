from flask import Flask, json
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort, marshal
from main import api, app
from datetime import datetime

__all__ =['UserSignUp', 'UserLogin']

from Models.database import DataBaseManager




user_agent = reqparse.RequestParser()
user_agent.add_argument('name', type=str, required=True, location='json', help='name is required')
user_agent.add_argument('email', type=str, required=True, location='json', help='email is required')
user_agent.add_argument('password', type=str, required=True, location='json', help='password is required')
userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'password': fields.String,
    'created_at': fields.String
}
class UserSignUp(Resource):
    def post(self):
        args = user_agent.parse_args()
        existing_user = DataBaseManager().check_existing_user(args['email'])
        if existing_user:
            abort(400, message="User already exists")
        else:
            checking_password(args['password'])
            created_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            DataBaseManager().register_user(*args.values(), created_at)
            result = DataBaseManager().check_existing_user(args['email'])
            if result:
                result = result[0]
                if isinstance(result['created_at'], datetime):
                    created_at_str = result['created_at'].strftime('%Y-%m-%d %H:%M:%S')
                else:
                    created_at_str = result['created_at']
                result['created_at'] = created_at_str
                return result, 201
            else:
                abort(500, message="User registration failed")

api.add_resource(UserSignUp, '/api/users/register')


user_agent.add_argument('email', type=str, required=True, location='json', help='email is required')
user_agent.add_argument('password', type=str, required=True, location='json', help='password is required')
class UserLogin(Resource):
    def post(self):
        args = user_agent.parse_args()
        existing_user = DataBaseManager().check_existing_user(args['email'])
        if existing_user:
            pass
        else:
            abort(400, message="User does not exist")

api.add_resource(UserLogin, '/api/users/login')

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

if __name__ == '__main__':
    app.run(debug=True)