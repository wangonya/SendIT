from flask_restful import Resource, reqparse
from db import connection, cursor
from tables import create_users_table

from flask_jwt_extended import (create_access_token, jwt_refresh_token_required, get_jwt_identity)

import json
import psycopg2
from passlib.hash import pbkdf2_sha256 as sha256

# TODO: ADD FEATURE -- LOGOUT


class User(Resource):
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        try:
            select_query = """SELECT id, username, pwd
                                            FROM users
                                            WHERE username = %s"""

            cursor.execute(select_query, username)
            row = cursor.fetchone()

            if row:
                return cls(row['id'], row['username'], row['pwd'])
        except (Exception, psycopg2.Error) as error:
            connection.rollback()
            return {
                        'status': 500,
                        'message': json.dumps(error, default=str)
                    }, 500

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


# signup
class UserRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('pwd',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('firstname',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('lastname',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('othernames',
                        type=str
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('registered',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('isAdmin',
                        type=bool
                        )

    def post(self):
        data = UserRegistration.parser.parse_args()
        data['pwd'] = User.generate_hash(data['pwd'])
        create_users_table()
        insert_query = """INSERT INTO users (username, pwd, firstname, 
                                    lastname, othernames, email, registered, isAdmin) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        record_to_insert = list(data.values())

        try:
            cursor.execute(insert_query, record_to_insert)
            connection.commit()
            access_token = create_access_token(identity=data['username'])
            return {
                       'status': 201,
                       'data': [{
                           'token': access_token,
                           'user': data['username']
                       }]
                   }, 201
        # TODO: HANDLE ERROR BETTER -- 409 IF CONFLICT, 500 IF OTHER
        except (Exception, psycopg2.Error) as error:
            connection.rollback()
            return {
                       'status': 500,
                       'message': json.dumps(error, default=str)
                   }, 500


# login
class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('pwd',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserLogin.parser.parse_args()
        user = User.find_by_username(username=[data['username']])

        if user is None:
            return {'message': "User '{}' does not exist".format(data['username'])}, 401
        else:
            pwd_verify_hash = User.verify_hash(data['pwd'], user.password)

            if pwd_verify_hash:
                access_token = create_access_token(identity=data['username'])
                return {
                           'status': 200,
                           'data': [{
                               'token': access_token,
                               'user': data['username']
                           }]
                       }, 200
            else:
                return {'message': "Wrong password"}, 401


# refresh token when it expires
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}
