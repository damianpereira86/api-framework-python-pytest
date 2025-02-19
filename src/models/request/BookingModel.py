from pydantic import BaseModel


class BookingModel(BaseModel):
    id: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    totalprice: int | None = None
    depositpaid: bool | None = None
    bookingdates: dict | None = None
    additionalneeds: str | None = None
