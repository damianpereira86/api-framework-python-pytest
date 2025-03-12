from pydantic import BaseModel
from typing import Optional


class BookingDates(BaseModel):
    checkin: str
    checkout: str


class BookingDetails(BaseModel):
    id: Optional[int] = None
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: str


class BookingResponse(BaseModel):
    bookingid: int
    booking: BookingDetails


class BookingIdResponse(BaseModel):
    bookingid: int
