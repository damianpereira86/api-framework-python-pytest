from pydantic import BaseModel
from typing import Optional


class BookingDates(BaseModel):
    checkin: Optional[str] = None
    checkout: Optional[str] = None


class BookingModel(BaseModel):
    id: Optional[int] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    totalprice: Optional[int] = None
    depositpaid: Optional[bool] = None
    bookingdates: Optional[BookingDates] = None
    additionalneeds: Optional[str] = None
