from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import psycopg2
import json

from db import connection, cursor
from tables import create_parcels_table


class ParcelsList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('placedBy',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('weight',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('weightmetric',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('sentOn',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('deliveredOn',
                        type=str,
                        # required=True,
                        # help="This field cannot be left blank!"
                        )
    parser.add_argument('status',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('source',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('destination',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('currentlocation',
                        type=str,
                        # required=True,
                        # help="This field cannot be left blank!"
                        )

    # Fetch all parcel delivery orders
    # @jwt_required()
    def get(self):
        get_parcels_query = "SELECT * FROM parcels"
        cursor.execute(get_parcels_query)
        all_parcels = cursor.fetchall()

        return {
                   'status': 200,
                   'data': json.dumps(all_parcels, default=str, separators=(',', ': '))
               }, 200

    # Post an order
    # @jwt_required()
    def post(self):
        data = ParcelsList.parser.parse_args()

        create_parcels_table()
        insert_query = """INSERT INTO parcels (placedBy, weight, weightmetric, 
                            sentOn, deliveredOn, status, source, destination, currentlocation) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;"""
        record_to_insert = list(data.values())

        cursor.execute(insert_query, record_to_insert)
        cursor.execute('SELECT LASTVAL()')
        row_id = cursor.fetchone()['lastval']
        connection.commit()

        return {
                   'status': 201,
                   'data': [{
                       'id': row_id,
                       'message': 'order created'
                   }]
               }, 201


# Fetch a specific parcel delivery order
class Parcel(Resource):
    # @jwt_required()
    def get(self, order_id):
        get_query = """SELECT *
                                FROM parcels
                                WHERE id = %s"""
        cursor.execute(get_query, (order_id,))
        one_parcel = cursor.fetchone()

        if one_parcel is not None:
            return {
                       'status': 200,
                       'data': json.dumps(one_parcel, default=str, separators=(',', ': '))
                   }, 200
        else:
            return {'message': "Parcel with id '{}' does not exist.".format(order_id)}, 404


# Cancel specific order
class CancelOrder(Resource):
    # @jwt_required()
    def patch(self, order_id):
        update_query = """UPDATE parcels
                            SET status = %s
                            WHERE id = %s"""
        cursor.execute(update_query, ('cancelled', order_id))
        connection.commit()
        count = cursor.rowcount

        if count is not 0:
            return {
                       'status': 200,
                       'data': [{
                           'id': order_id,
                           'message': 'order cancelled'
                       }]
                   }, 200
        else:
            return {'message': "Parcel with id '{}' does not exist.".format(order_id)}, 404


# Change status -- only admin
class ChangeStatus(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('status',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    # @jwt_required()
    def patch(self, order_id):
        data = ChangeStatus.parser.parse_args()

        update_query = """UPDATE parcels
                            SET status = %s
                            WHERE id = %s"""
        cursor.execute(update_query, (data['status'], order_id))
        connection.commit()
        count = cursor.rowcount

        if count is not 0:
            return {
                       'status': 200,
                       'data': [{
                           'id': order_id,
                           'message': 'status updated'
                       }]
                   }, 200
        else:
            return {'message': "Parcel with id '{}' does not exist.".format(order_id)}, 404


# Change current location -- only admin
class ChangeLocation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('currentlocation',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    # @jwt_required()
    def patch(self, order_id):
        data = ChangeLocation.parser.parse_args()

        update_query = """UPDATE parcels
                            SET currentlocation = %s
                            WHERE id = %s"""
        cursor.execute(update_query, (data['currentlocation'], order_id))
        connection.commit()
        count = cursor.rowcount

        if count is not 0:
            return {
                       'status': 200,
                       'data': [{
                           'id': order_id,
                           'message': 'current location updated'
                       }]
                   }, 200
        else:
            return {'message': "Parcel with id '{}' does not exist.".format(order_id)}, 404


# Change destination -- only admin
class ChangeDestination(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('destination',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    # @jwt_required()
    def patch(self, order_id):
        data = ChangeDestination.parser.parse_args()

        update_query = """UPDATE parcels
                                    SET destination = %s
                                    WHERE id = %s"""
        cursor.execute(update_query, (data['destination'], order_id))
        connection.commit()
        count = cursor.rowcount

        if count is not 0:
            return {
                       'status': 200,
                       'data': [{
                           'id': order_id,
                           'message': 'destination updated'
                       }]
                   }, 200
        else:
            return {'message': "Parcel with id '{}' does not exist.".format(order_id)}, 404
