from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from parcels import ParcelsList, Parcel, CancelOrder, ChangeStatus, ChangeLocation, ChangeDestination, GetUserOrder
from user import UserRegistration, UserLogin
app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'kinyanjui-wangonya'
app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on app

jwt = JWTManager(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


# Flask Restful Routes
api.add_resource(ParcelsList, '/parcels')
api.add_resource(Parcel, '/parcels/<int:order_id>')
api.add_resource(CancelOrder, '/parcels/<int:order_id>/cancel')
api.add_resource(ChangeDestination, '/parcels/<int:order_id>/destination')
api.add_resource(ChangeStatus, '/parcels/<int:order_id>/status')
api.add_resource(ChangeLocation, '/parcels/<int:order_id>/currentlocation')
api.add_resource(GetUserOrder, '/users/<int:_id>/parcels')

# auth
api.add_resource(UserRegistration, '/auth/signup')
api.add_resource(UserLogin, '/auth/login')


if __name__ == '__main__':
    app.run(debug=True)
