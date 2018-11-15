from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from auth import authenticate, identity, userid_mapping, users

app = Flask(__name__)
api = Api(app)
app.secret_key = 'kinyanjui-wangonya'
app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on app

parcels = []

jwt = JWT(app, authenticate, identity)


@app.route('/')
def hello_world():
    return 'Hello World!'


# TODO: CHECK USER API
class ParcelsList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!"
                        )
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
    parser.add_argument('from',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('to',
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
    @jwt_required()
    def get(self):
        return {
                   'status': 200,
                   'data': parcels
               }, 200

    # Post an order
    @jwt_required()
    def post(self):
        data = ParcelsList.parser.parse_args()

        if next(filter(lambda x: x['id'] == data['id'], parcels), None) is not None:
            return {'message': "An item with id '{}' already exists.".format(data['id'])}, 409

        parcels.append(data)
        return {
                   'status': 201,
                   'data': [{
                       'id': data['id'],
                       'message': 'order created'
                   }]
               }, 201


class Parcel(Resource):
    # Fetch a specific parcel delivery order
    @jwt_required()
    def get(self, order_id):
        parcel = next(filter(lambda x: x['id'] == order_id, parcels), None)
        if parcel is not None:
            return {'data': [{'parcels': parcel}]}, 200
        else:
            return {'message': "Parcel with id '{}' does not exist.".format(order_id)}, 404


# Fetch all parcel delivery order by a specific user
class CancelOrder(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('cancelled',
                        type=bool,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def patch(self, order_id):
        parcel = next(filter(lambda x: x['id'] == order_id, parcels), None)

        if parcel is not None:
            parcel.update(CancelOrder.parser.parse_args())
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

    @jwt_required()
    def patch(self, order_id):
        parcel = next(filter(lambda x: x['id'] == order_id, parcels), None)

        if parcel is not None:
            parcel.update(ChangeStatus.parser.parse_args())
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

    @jwt_required()
    def patch(self, order_id):
        parcel = next(filter(lambda x: x['id'] == order_id, parcels), None)

        if parcel is not None:
            parcel.update(ChangeLocation.parser.parse_args())
            return {
                       'status': 200,
                       'data': [{
                           'id': order_id,
                           'currentlocation': ChangeLocation.parser.parse_args().currentlocation,
                           'message': 'parcel location updated'
                       }]
                   }, 200
        else:
            return {'message': "Parcel with id '{}' does not exist.".format(order_id)}, 404


# Change destination -- only admin
class ChangeDestination(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('to',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def patch(self, order_id):
        parcel = next(filter(lambda x: x['id'] == order_id, parcels), None)

        if parcel is not None:
            parcel.update(ChangeDestination.parser.parse_args())
            return {
                       'status': 200,
                       'data': [{
                           'id': order_id,
                           'to': ChangeDestination.parser.parse_args().to,
                           'message': 'parcel destination updated'
                       }]
                   }, 200
        else:
            return {'message': "Parcel with id '{}' does not exist.".format(order_id)}, 404


# Flask Restful Routes
api.add_resource(ParcelsList, '/parcels')
api.add_resource(Parcel, '/parcels/<int:order_id>')
api.add_resource(CancelOrder, '/parcels/<int:order_id>/cancel')
api.add_resource(ChangeDestination, '/parcels/<int:order_id>/destination')
api.add_resource(ChangeStatus, '/parcels/<int:order_id>/status')
api.add_resource(ChangeLocation, '/parcels/<int:order_id>/currentlocation')


if __name__ == '__main__':
    app.run(debug=True)
