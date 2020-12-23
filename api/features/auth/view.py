from sqlalchemy.exc import IntegrityError
from psycopg2 import errors
from flask import request
from settings import endpoint
from .schema import UserSchema, LoginSchema
from .model import User
from ...utils.messages.errors import ALREADY_EXISTS, NOT_FOUND
from ...utils.token_helpers import create_token


@endpoint('/register', methods=['POST'])
def register_user():
    schema = UserSchema()
    user_data = schema.load(request.get_json())
    user = User(**user_data)

    try:
        user.save()
    except IntegrityError as e:
        if isinstance(e.orig, errors.UniqueViolation):
            return {
                'message': ALREADY_EXISTS.format('username or email'),
            }, 409
        else:
            return {
                'message': 'Error while inserting data',
            }, 400

    return schema.dump(user), 201


@endpoint('/login', methods=['POST'])
def login_user():
    schema = LoginSchema()
    login_details = schema.load(request.get_json())
    user = User.query.filter_by(email=login_details['email']).first()
    if not user or not user.verify_password(login_details['password']):
        return {
            'message': NOT_FOUND.format('Credentials'),
        }, 404

    schema = UserSchema()
    user_data = schema.dump(user)
    token = create_token(user_data)
    user_data['token'] = token
    return user_data, 200

