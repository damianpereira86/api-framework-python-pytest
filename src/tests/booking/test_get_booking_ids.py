import pytest
from src.models.services.BookingService import BookingService
from src.models.responses.BookingResponse import (
    BookingDetails,
    BookingDates,
)


@pytest.fixture
def booking_service():
    return BookingService()


def test_get_all_booking_ids(booking_service):
    response = booking_service.get_booking_ids()
    assert response.status == 200
    assert isinstance(response.data, list)
    assert len(response.data) > 1


def test_get_all_booking_ids_response_time(booking_service):
    response = booking_service.get_booking_ids()
    assert response.status == 200
    assert response.response_time < 2000


def test_get_booking_ids_with_query_parameters_firstname(booking_service):
    random_firstname = "Damian" + str(hash("Damian"))
    booking = BookingDetails(
        firstname=random_firstname,
        lastname="Pereira",
        totalprice=1000,
        depositpaid=True,
        bookingdates=BookingDates(checkin="2024-01-01", checkout="2024-02-01"),
        additionalneeds="Breakfast",
    )
    response = booking_service.add_booking(booking)
    booking_id = response.data.bookingid

    params = {"firstname": random_firstname}
    response = booking_service.get_booking_ids(params)
    assert response.status == 200
    assert len(response.data) == 1
    assert response.data[0].bookingid == booking_id
