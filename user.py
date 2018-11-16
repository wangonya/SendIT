from flask_restful import Resource, reqparse
from db import connection, cursor
from tables import create_users_table

import json
import psycopg2


class User(Resource):
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password


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
        create_users_table()
        insert_query = """INSERT INTO users (username, pwd, firstname, 
                                    lastname, othernames, email, registered, isAdmin) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        record_to_insert = list(data.values())

        try:
            cursor.execute(insert_query, record_to_insert)
            connection.commit()
            return {
                       'status': 201,
                       'data': [{
                           'token': 'tokenhere',
                           'user': data['username']
                       }]
                   }, 201
        except (Exception, psycopg2.Error) as error:
            connection.rollback()
            return {
                       'status': 400,
                       'message': json.dumps(error, default=str)
                   }, 400


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

        select_query = """SELECT username, pwd
                                FROM users
                                WHERE username = %s AND pwd = %s"""
        values = list(data.values())

        cursor.execute(select_query, values)
        row = cursor.fetchone()

        if row is not None:
            return {
                       'status': 200,
                       'data': [{
                           'token': 'tokenhere',
                           'user': data['username']
                       }]
                   }, 200
        else:
            return {'message': "Wrong password / User '{}' does not exist".format(data['username'])}, 404
