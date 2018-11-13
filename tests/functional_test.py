# This Python file uses the following encoding: utf-8
import pytest
import app


@pytest.fixture
def my_app():
    my_app = app.hello_world()
    return my_app == "Hello World!"


def test_hello_world(my_app):
    # res = my_app.get("/")
    # assert res.status_code == 200
    assert my_app


# Fetch all parcel delivery orders
def test_parcels_api_endpoint():
    parcels_api_endpoint = app.ParcelsList()
    get_res = parcels_api_endpoint.get()
    post_res = parcels_api_endpoint.get()
    assert 200 in get_res and 200 in post_res


# Fetch a specific parcel delivery order
def test_parcel_api_endpoint():
    parcel_api_endpoint = app.Parcel()
    res = parcel_api_endpoint.get(order_id='test')
    assert 200 in res or 404 in res


# Cancel a specific parcel delivery order
def test_cancel_order_endpoint():
    cancel_order_endpoint = app.CancelOrder()
    res = cancel_order_endpoint.patch(order_id='test')
    assert 200 in res or 404 in res


# Change order destination
def test_change_destination_endpoint():
    change_destination_endpoint = app.ChangeDestination()
    res = change_destination_endpoint.patch(order_id='test')
    assert 200 in res or 404 in res


# Change order status
def test_change_status_endpoint():
    change_status_endpoint = app.ChangeDestination()
    res = change_status_endpoint.patch(order_id='test')
    assert 200 in res or 404 in res


# Change location
def test_change_location_endpoint():
    change_location_endpoint = app.ChangeDestination()
    res = change_location_endpoint.patch(order_id='test')
    assert 200 in res or 404 in res
