from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from auth import authenticate, identity
from parcels import ParcelsList, Parcel, CancelOrder, ChangeStatus, ChangeLocation, ChangeDestination
from user import UserRegistration, UserLogin
app = Flask(__name__)
api = Api(app)
app.secret_key = 'kinyanjui-wangonya'
app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on app

jwt = JWT(app, authenticate, identity)


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

# auth
api.add_resource(UserRegistration, '/auth/signup')
api.add_resource(UserLogin, '/auth/login')


if __name__ == '__main__':
    app.run(debug=True)
