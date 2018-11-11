import pytest
import app


@pytest.fixture
def my_app():
    my_app = app.hello_world()
    return my_app


def test_hello_world(my_app):
    # res = my_app.get("/")
    # assert res.status_code == 200
    assert b"Hello World"


# api endpoints tests
def test_api_endpoints(my_app):
    # Fetch all parcel delivery orders
    res = my_app.get("/parcels")
    assert res.status_code == 200

    # Fetch a specific delivery order
    res = my_app.get("/parcels/<parcelId>")
    assert res.status_code == 200

    # Fetch all parcel delivery order by a specific user
    res = my_app.get("/users/<userId>/parcels")
    assert res.status_code == 200

    # Cancel a specific parcel delivery order
    res = my_app.get("/parcels/<parcelId>/cancel")
    assert res.status_code == 200

    # Create a parcel delivery order
    res = my_app.post("/parcels")
    assert res.status_code == 200

    # Create a user account
    res = my_app.post("/auth/signup")
    assert res.status_code == 200

    # Login a user
    res = my_app.post("/auth/login")
    assert res.status_code == 200

    '''Change the destination of a specific parcel delivery order. 
    Only the user who created the parcel should be able to change the destination of the parcel. 
    A parcel’s destination can only be changed if it is yet to be delivered'''
    res = my_app.patch("/parcels/<parcelId>/destination")
    assert res.status_code == 200

    '''Change the status of a specific parcel delivery order. 
    Only the Admin is allowed to access this endpoint'''
    res = my_app.patch("/parcels/<parcelId>/status")
    assert res.status_code == 200

    '''Change the present location of a specific parcel delivery order. 
    Only the Admin is allowed to access this endpoint'''
    res = my_app.patch("/parcels/<parcelId>/currentlocation")
    assert res.status_code == 200
