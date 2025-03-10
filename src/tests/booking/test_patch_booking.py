import pytest

from src.models.requests.booking import BookingModel, BookingDates
from src.models.services.booking_service import BookingService


@pytest.fixture
def booking_service():
    service = BookingService()
    service.authenticate()
    return service


@pytest.fixture
def original_booking(booking_service):
    booking = BookingModel(
        firstname="John",
        lastname="Snow",
        totalprice=1000,
        depositpaid=True,
        bookingdates=BookingDates(checkin="2024-01-01", checkout="2024-02-01"),
        additionalneeds="Breakfast",
    )
    response = booking_service.add_booking(booking)
    return response.data


def test_patch_booking_successfully(booking_service, original_booking):
    patched_booking = BookingModel(firstname="Jim")

    response = booking_service.partial_update_booking(
        original_booking.bookingid, patched_booking
    )
    assert response.status == 200

    assert response.data.firstname == patched_booking.firstname
    assert response.data.lastname == original_booking.booking.lastname
    assert response.data.totalprice == original_booking.booking.totalprice
    assert response.data.depositpaid is True
    assert (
        response.data.bookingdates.checkin
        == original_booking.booking.bookingdates.checkin
    )
    assert (
        response.data.bookingdates.checkout
        == original_booking.booking.bookingdates.checkout
    )
    assert response.data.additionalneeds == original_booking.booking.additionalneeds


def test_patch_booking_successfully_response_time(booking_service, original_booking):
    patched_booking = BookingModel(firstname="Jim")

    response = booking_service.partial_update_booking(
        original_booking.bookingid, patched_booking
    )
    assert response.response_time > 0


def test_unauthorized_patch_booking(original_booking):
    unauthorized_booking_service = BookingService()
    patched_booking = BookingModel(
        firstname="John",
        lastname="Winter",
        totalprice=500,
        depositpaid=True,
        bookingdates=BookingDates(checkin="2024-01-01", checkout="2024-02-01"),
        additionalneeds="Lunch",
    )
    response = unauthorized_booking_service.partial_update_booking(
        original_booking.bookingid, patched_booking
    )
    assert response.status == 403


@pytest.mark.skip(
    reason="BUG: https://github.com/damianpereira86/api-framework-python-pytest/issues/5"
)
def test_patch_non_existent_booking(booking_service):
    booking_id = 999999999
    patched_booking = BookingModel(
        firstname="John",
        lastname="Winter",
        totalprice=500,
        depositpaid=True,
        bookingdates=BookingDates(checkin="2024-01-01", checkout="2024-02-01"),
        additionalneeds="Lunch",
    )
    response = booking_service.partial_update_booking(booking_id, patched_booking)
    assert response.status == 404
