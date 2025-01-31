from flask_restful import Resource, abort
from app.Common.schemas import validate_api_schema, UserSignupSchema, UserLoginSchema, generate_token, checking_password
from datetime import datetime
from app.Models.database import DataBaseManager
from app import api, app

__all__ =['UserSignUp', 'UserLogin']


@api.route('/users/register', endpoint='UserSignUp')
class UserSignUp(Resource):
    @validate_api_schema(UserSignupSchema)
    def post(self, **kwargs):
        data = kwargs["validated_data"]
        existing_user = DataBaseManager().check_existing_user(data['email'])
        if existing_user:
            abort(400, message="User already exists")
        else:
            checking_password(data['password'])
            created_at = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            DataBaseManager().register_user(*data.values(), created_at)
            result = DataBaseManager().check_existing_user(data['email'])
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


@api.route('/users/login', endpoint="UserLogin")
class UserLogin(Resource):
    @validate_api_schema(UserLoginSchema)
    def post(self, **kwargs):
        data = kwargs["validated_data"]
        existing_user = DataBaseManager().check_existing_user(data['email'])
        existing_user = existing_user[0]
        if existing_user:
            if existing_user['password'] == data['password']:
                token = generate_token(data['email'])
                return {'message': 'Login successful', 'token': token}, 200
            else:
                abort(400, message="Incorrect password")
        else:
            abort(400, message="User does not exist")
