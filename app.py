from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

app.testing = True

parcels = []


@app.route('/')
def hello_world():
    return 'Hello World!'


class ParcelsList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('id',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    # Fetch all parcel delivery orders
    def get(self):
        return {
                   'status': 200,
                   'data': [{'parcels': parcels}]
               }, 200

    # Post an order
    def post(self):
        data = ParcelsList.parser.parse_args()

        if next(filter(lambda x: x['id'] == data['id'], parcels), None) is not None:
            return {'message': "An item with id '{}' already exists.".format(data['id'])}, 409

        parcel = {'id': data['id'], 'name': data['name']}
        parcels.append(parcel)
        return parcel, 200


class Parcel(Resource):
    # Fetch a specific parcel delivery order
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
    parser.add_argument('message',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def patch(self, order_id):
        parcel = next(filter(lambda x: x['id'] == order_id, parcels), None)

        if parcel is not None:
            parcel.update(data)
            return parcel, 200
        else:
            return {'message': "Parcel with id '{}' does not exist.".format(order_id)}, 404


# Change status -- only admin
class ChangeStatus(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('status',
                        type=bool,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('message',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def patch(self, order_id):
        parcel = next(filter(lambda x: x['id'] == order_id, parcels), None)

        if parcel is not None:
            parcel.update(data)
            return parcel, 200
        else:
            return {'message': "Parcel with id '{}' does not exist.".format(order_id)}, 404


# Change current location -- only admin
class ChangeLocation(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('currentLocation',
                        type=bool,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('message',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def patch(self, order_id):
        parcel = next(filter(lambda x: x['id'] == order_id, parcels), None)

        if parcel is not None:
            parcel.update(data)
            return parcel, 200
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
    parser.add_argument('message',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def patch(self, order_id):
        parcel = next(filter(lambda x: x['id'] == order_id, parcels), None)

        if parcel is not None:
            parcel.update(data)
            return parcel, 200
        else:
            return {'message': "Parcel with id '{}' does not exist.".format(order_id)}, 404


# Flask Restful Routes
api.add_resource(ParcelsList, '/parcels')
api.add_resource(Parcel, '/parcels/<string:order_id>')
api.add_resource(CancelOrder, '/parcels/<string:order_id>/cancel')
api.add_resource(ChangeDestination, '/parcels/<string:order_id>/destination')
api.add_resource(ChangeStatus, '/parcels/<string:order_id>/status')
api.add_resource(ChangeLocation, '/parcels/<string:order_id>/currentlocation')


if __name__ == '__main__':
    app.run(debug=True)
