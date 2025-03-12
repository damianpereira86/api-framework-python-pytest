import pytest

from src.models.requests.booking.booking_model import BookingModel, BookingDates
from src.models.services.booking_service import BookingService


@pytest.fixture
def booking_service():
    service = BookingService()
    service.authenticate()
    return service


@pytest.fixture
def booking_id(booking_service):
    booking = BookingModel(
        firstname="John",
        lastname="Snow",
        totalprice=1000,
        depositpaid=True,
        bookingdates=BookingDates(checkin="2024-01-01", checkout="2024-02-01"),
        additionalneeds="Breakfast",
    )
    response = booking_service.add_booking(booking)
    return response.data.bookingid


def test_update_booking_successfully(booking_service, booking_id):
    booking = BookingModel(
        firstname="Jim",
        lastname="Brown",
        totalprice=111,
        depositpaid=False,
        bookingdates=BookingDates(checkin="2020-01-01", checkout="2021-01-01"),
        additionalneeds="Lunch",
    )

    response = booking_service.update_booking(booking_id, booking)
    assert response.status == 200
    assert response.data.firstname == booking.firstname
    assert response.data.lastname == booking.lastname
    assert response.data.totalprice == booking.totalprice
    assert response.data.depositpaid is False
    assert response.data.bookingdates.checkin == booking.bookingdates.checkin
    assert response.data.bookingdates.checkout == booking.bookingdates.checkout
    assert response.data.additionalneeds == booking.additionalneeds


def test_update_booking_successfully_response_time(booking_service, booking_id):
    booking = BookingModel(
        firstname="Jim",
        lastname="Brown",
        totalprice=111,
        depositpaid=False,
        bookingdates=BookingDates(checkin="2020-01-01", checkout="2021-01-01"),
        additionalneeds="Lunch",
    )

    response = booking_service.update_booking(booking_id, booking)
    assert response.response_time < 2000


def test_unauthorized_update_booking(booking_id):
    unauthorized_booking_service = BookingService()
    booking = BookingModel(
        firstname="John",
        lastname="Winter",
        totalprice=500,
        depositpaid=True,
        bookingdates=BookingDates(checkin="2024-01-01", checkout="2024-02-01"),
        additionalneeds="Lunch",
    )
    response = unauthorized_booking_service.update_booking(booking_id, booking)
    assert response.status == 403


@pytest.mark.skip(
    reason="BUG: https://github.com/damianpereira86/api-framework-python-pytest/issues/6"
)
def test_update_non_existent_booking(booking_service):
    booking_id = 999999999
    booking = BookingModel(
        firstname="John",
        lastname="Winter",
        totalprice=500,
        depositpaid=True,
        bookingdates=BookingDates(checkin="2024-01-01", checkout="2024-02-01"),
        additionalneeds="Lunch",
    )
    response = booking_service.update_booking(booking_id, booking)
    assert response.status == 404
